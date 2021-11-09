#!/usr/bin/env bash

# Deployment script - intended to run on Moonstream crawlers server

# Colors
C_RESET='\033[0m'
C_RED='\033[1;31m'
C_GREEN='\033[1;32m'
C_YELLOW='\033[1;33m'

# Logs
PREFIX_INFO="${C_GREEN}[INFO]${C_RESET} [$(date +%d-%m\ %T)]"
PREFIX_WARN="${C_YELLOW}[WARN]${C_RESET} [$(date +%d-%m\ %T)]"
PREFIX_CRIT="${C_RED}[CRIT]${C_RESET} [$(date +%d-%m\ %T)]"

# Main
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
APP_DIR="${APP_DIR:-/home/ubuntu/moonstream}"
APP_CRAWLERS_DIR="${APP_DIR}/crawlers"
PYTHON_ENV_DIR="${PYTHON_ENV_DIR:-/home/ubuntu/moonstream-env}"
PYTHON="${PYTHON_ENV_DIR}/bin/python"
PIP="${PYTHON_ENV_DIR}/bin/pip"
SECRETS_DIR="${SECRETS_DIR:-/home/ubuntu/moonstream-secrets}"
PARAMETERS_ENV_PATH="${SECRETS_DIR}/app.env"
AWS_SSM_PARAMETER_PATH="${AWS_SSM_PARAMETER_PATH:-/moonstream/prod}"
SCRIPT_DIR="$(realpath $(dirname $0))"
PARAMETERS_SCRIPT="${SCRIPT_DIR}/parameters.py"
CHECKENV_REPO_URL="https://raw.githubusercontent.com/bugout-dev/checkenv/main/scripts"
CHECKENV_PARAMETERS_SCRIPT_URL="${CHECKENV_REPO_URL}/parameters.bash"
CHECKENV_NODES_CONNECTIONS_SCRIPT_URL="${CHECKENV_REPO_URL}/nodes-connections.bash"

# Ethereum service files
ETHEREUM_SYNCHRONIZE_SERVICE="ethereum-synchronize.service"
ETHEREUM_TRENDING_SERVICE_FILE="ethereum-trending.service"
ETHEREUM_TRENDING_TIMER_FILE="ethereum-trending.service"
ETHEREUM_TXPOOL_SERVICE_FILE="ethereum-txpool.service"

# Polygon service file
POLYGON_SYNCHRONIZE_SERVICE="polygon-synchronize.service"

CRAWLERS_SERVICE_FILE="moonstreamcrawlers.service"



set -eu

echo
echo
echo -e "${PREFIX_INFO} Building executable Ethereum transaction pool crawler script with Go"
EXEC_DIR=$(pwd)
cd "${APP_CRAWLERS_DIR}/ethtxpool"
HOME=/root /usr/local/go/bin/go build -o "${APP_CRAWLERS_DIR}/ethtxpool/ethtxpool" "${APP_CRAWLERS_DIR}/ethtxpool/main.go"
cd "${EXEC_DIR}"

echo
echo
echo -e "${PREFIX_INFO} Building executable server of moonstreamcrawlers with Go"
EXEC_DIR=$(pwd)
cd "${APP_CRAWLERS_DIR}/server"
HOME=/root /usr/local/go/bin/go build -o "${APP_CRAWLERS_DIR}/server/moonstreamcrawlers" "${APP_CRAWLERS_DIR}/server/main.go"
cd "${EXEC_DIR}"

echo
echo
echo -e "${PREFIX_INFO} Updating Python dependencies"
"${PIP}" install --upgrade pip
"${PIP}" install -r "${APP_CRAWLERS_DIR}/mooncrawl/requirements.txt"

echo
echo
echo -e "${PREFIX_INFO} Retrieving deployment parameters"
mkdir -p "${SECRETS_DIR}"
AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" "${PYTHON}" "${PARAMETERS_SCRIPT}" extract -p "${AWS_SSM_PARAMETER_PATH}" -o "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Retrieving addition deployment parameters"
curl -s "${CHECKENV_PARAMETERS_SCRIPT_URL}" | bash /dev/stdin -v -p "moonstream" -o "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Updating nodes connection parameters"
curl -s "${CHECKENV_NODES_CONNECTIONS_SCRIPT_URL}" | bash /dev/stdin -v -f "${PARAMETERS_ENV_PATH}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum block with transactions syncronizer service definition with ${ETHEREUM_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${ETHEREUM_SYNCHRONIZE_SERVICE}" "/etc/systemd/system/${ETHEREUM_SYNCHRONIZE_SERVICE}"
systemctl daemon-reload
systemctl restart "${ETHEREUM_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum trending service and timer with: ${ETHEREUM_TRENDING_SERVICE_FILE}, ${ETHEREUM_TRENDING_TIMER_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_TRENDING_SERVICE_FILE}" "${SCRIPT_DIR}/${ETHEREUM_TRENDING_TIMER_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_TRENDING_SERVICE_FILE}" "/etc/systemd/system/${ETHEREUM_TRENDING_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_TRENDING_TIMER_FILE}" "/etc/systemd/system/${ETHEREUM_TRENDING_TIMER_FILE}"
systemctl daemon-reload
systemctl restart "${ETHEREUM_TRENDING_TIMER_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Ethereum transaction pool crawler service definition with ${ETHEREUM_TXPOOL_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${ETHEREUM_TXPOOL_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${ETHEREUM_TXPOOL_SERVICE_FILE}" "/etc/systemd/system/${ETHEREUM_TXPOOL_SERVICE_FILE}"
systemctl daemon-reload
systemctl restart "${ETHEREUM_TXPOOL_SERVICE_FILE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing Polygon block with transactions syncronizer service definition with ${POLYGON_SYNCHRONIZE_SERVICE}"
chmod 644 "${SCRIPT_DIR}/${POLYGON_SYNCHRONIZE_SERVICE}"
cp "${SCRIPT_DIR}/${POLYGON_SYNCHRONIZE_SERVICE}" "/etc/systemd/system/${POLYGON_SYNCHRONIZE_SERVICE}"
systemctl daemon-reload
systemctl restart "${POLYGON_SYNCHRONIZE_SERVICE}"

echo
echo
echo -e "${PREFIX_INFO} Replacing existing moonstreamcrawlers service definition with ${CRAWLERS_SERVICE_FILE}"
chmod 644 "${SCRIPT_DIR}/${CRAWLERS_SERVICE_FILE}"
cp "${SCRIPT_DIR}/${CRAWLERS_SERVICE_FILE}" "/etc/systemd/system/${CRAWLERS_SERVICE_FILE}"
systemctl daemon-reload
systemctl restart "${CRAWLERS_SERVICE_FILE}"
systemctl status "${CRAWLERS_SERVICE_FILE}"

