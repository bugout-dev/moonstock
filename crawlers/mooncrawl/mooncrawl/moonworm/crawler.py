from datetime import datetime
from enum import Enum
import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, cast
from bugout.data import BugoutSearchResult

from eth_typing.evm import ChecksumAddress
from moonstreamdb.models import Base
from sqlalchemy.orm.session import Session
from web3.main import Web3

from mooncrawl.data import AvailableBlockchainType

from ..blockchain import connect
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_MOONWORM_TASKS_JOURNAL,
    bugout_client,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SubscriptionTypes(Enum):
    POLYGON_BLOCKCHAIN = "polygon_blockchain"
    ETHEREUM_BLOCKCHAIN = "ethereum_blockchain"


def blockchain_type_to_subscription_type(
    blockchain_type: AvailableBlockchainType,
) -> SubscriptionTypes:
    if blockchain_type == AvailableBlockchainType.ETHEREUM:
        return SubscriptionTypes.ETHEREUM_BLOCKCHAIN
    elif blockchain_type == AvailableBlockchainType.POLYGON:
        return SubscriptionTypes.POLYGON_BLOCKCHAIN
    else:
        raise ValueError(f"Unknown blockchain type: {blockchain_type}")


@dataclass
class EventCrawlJob:
    event_abi_hash: str
    event_abi: Dict[str, Any]
    contracts: List[ChecksumAddress]
    created_at: int


def _retry_connect_web3(
    blockchain_type: AvailableBlockchainType,
    retry_count: int = 10,
    sleep_time: float = 5,
) -> Web3:
    """
    Retry connecting to the blockchain.
    """
    while retry_count > 0:
        retry_count -= 1
        try:
            web3 = connect(blockchain_type)
            web3.eth.block_number
            logger.info(f"Connected to {blockchain_type}")
            return web3
        except Exception as e:
            if retry_count == 0:
                error = e
                break
            logger.error(f"Failed to connect to {blockchain_type} blockchain: {e}")
            logger.info(f"Retrying in {sleep_time} seconds")
            time.sleep(sleep_time)
    raise Exception(
        f"Failed to connect to {blockchain_type} blockchain after {retry_count} retries: {error}"
    )


def get_crawl_job_entries(
    subscription_type: SubscriptionTypes,
    crawler_type: str,
    journal_id: str = MOONSTREAM_MOONWORM_TASKS_JOURNAL,
    created_at_filter: int = None,
    limit: int = 200,
) -> List[BugoutSearchResult]:
    """
    Get all event ABIs from bugout journal
    where tags are:
    - #crawler_type:crawler_type (either event or function)
    - #status:active
    - #subscription_type:subscription_type (either polygon_blockchain or ethereum_blockchain)

    """
    query = f"#status:active #type:{crawler_type} #subscription_type:{subscription_type.value}"

    if created_at_filter is not None:
        # Filtering by created_at
        # Filtering not by strictly greater than
        # because theoretically we can miss some jobs
        #       (in the last query bugout didn't return all of by last created_at)
        # On the other hand, we may have multiple same jobs that will be filtered out
        #
        query += f" #created_at:>={created_at_filter}"

    current_offset = 0
    entries = []
    while True:
        search_result = bugout_client.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=journal_id,
            query=query,
            offset=current_offset,
            limit=limit,
        )
        entries.extend(search_result.results)

        # if len(entries) >= search_result.total_results:
        if len(search_result.results) == 0:
            break
        current_offset += limit
    return entries


def make_event_crawl_jobs(entries: List[BugoutSearchResult]) -> List[EventCrawlJob]:
    """
    Create EventCrawlJob objects from bugout entries.
    """

    def _get_tag(entry: BugoutSearchResult, tag: str) -> str:
        for entry_tag in entry.tags:
            if entry_tag.startswith(tag):
                return entry_tag.split(":")[1]
        raise ValueError(f"Tag {tag} not found in {entry}")

    crawl_job_by_hash: Dict[str, EventCrawlJob] = {}

    for entry in entries:
        # TODO in entries there is misspelling of 'abi_method_hash'
        abi_hash = _get_tag(entry, "abi_metod_hash")
        contract_address = Web3().toChecksumAddress(_get_tag(entry, "address"))

        existing_crawl_job = crawl_job_by_hash.get(abi_hash)
        if existing_crawl_job is not None:
            if contract_address not in existing_crawl_job.contracts:
                existing_crawl_job.contracts.append(contract_address)
        else:
            abi = cast(str, entry.content)
            new_crawl_job = EventCrawlJob(
                event_abi_hash=abi_hash,
                event_abi=json.loads(abi),
                contracts=[contract_address],
                created_at=int(datetime.fromisoformat(entry.created_at).timestamp()),
            )
            crawl_job_by_hash[abi_hash] = new_crawl_job

    return [crawl_job for crawl_job in crawl_job_by_hash.values()]


def merge_event_crawl_jobs(
    old_crawl_jobs: List[EventCrawlJob], new_event_crawl_jobs: List[EventCrawlJob]
) -> List[EventCrawlJob]:
    """
    Merge new event crawl jobs with old ones.
    If there is a new event crawl job with the same event_abi_hash
    then we will merge the contracts to one job.
    Othervise new job will be created

    Important:
        old_crawl_jobs will be modified
    Returns:
        Merged list of event crawl jobs
    """
    for new_crawl_job in new_event_crawl_jobs:
        for old_crawl_job in old_crawl_jobs:
            if new_crawl_job.event_abi_hash == old_crawl_job.event_abi_hash:
                old_crawl_job.contracts.extend(new_crawl_job.contracts)
                break
        else:
            old_crawl_jobs.append(new_crawl_job)
    return old_crawl_jobs


def _get_heartbeat_entry_id(
    crawler_type: str, blockchain_type: AvailableBlockchainType
) -> str:
    entries = bugout_client.search(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        query=f"#{crawler_type} #heartbeat #{blockchain_type.value}",
        limit=1,
    )
    if entries.results:
        return entries.results[0].entry_url.split("/")[-1]
    else:
        logger.info(f"No {crawler_type} heartbeat entry found, creating one")
        entry = bugout_client.create_entry(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
            title=f"{crawler_type} Heartbeat - {blockchain_type.value}",
            tags=[crawler_type, "heartbeat", blockchain_type.value],
            content="",
        )
        return str(entry.id)


def heartbeat(
    crawler_type: str,
    blockchain_type: AvailableBlockchainType,
    crawler_status: Dict[str, Any],
) -> None:
    """
    Periodically crawler will update the status in bugout entry:
    - Started at timestamp
    - Started at block number
    - Status: Running/Dead
    - Last crawled block number
    - Number of current jobs
    - Time taken to crawl last crawl_step and speed per block

    and other information later will be added.
    """
    heartbeat_entry_id = _get_heartbeat_entry_id(crawler_type, blockchain_type)
    bugout_client.update_entry_content(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        entry_id=heartbeat_entry_id,
        title=f"{crawler_type} Heartbeat - {blockchain_type.value}",
        content=f"{json.dumps(crawler_status, indent=2)}",
    )


def save_labels(db_session: Session, labels: List[Base]) -> None:
    """
    Save labels in the database.
    """
    try:
        db_session.add_all(labels)
        db_session.commit()
    except Exception as e:
        logger.error(f"Failed to save labels: {e}")
        db_session.rollback()
        raise e