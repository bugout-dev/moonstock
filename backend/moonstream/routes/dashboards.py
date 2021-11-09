import logging
from os import read
from typing import Any, List, Optional, Dict
from uuid import UUID

import boto3  # type: ignore
from bugout.data import BugoutResource, BugoutResources
from bugout.exceptions import BugoutResponseException
from fastapi import APIRouter, Request, Query

from .. import actions
from .. import data
from ..middleware import MoonstreamHTTPException
from ..reporter import reporter
from ..settings import (
    MOONSTREAM_APPLICATION_ID,
    bugout_client as bc,
    SMARTCONTRACTS_ABI_BUCKET,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    SMARTCONTRACTS_ABI_BUCKET,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/dashboards",
)

BUGOUT_RESOURCE_TYPE_DASHBOARD = "dashboards"

BUGOUT_RESOURCE_TYPE_SUBSCRIPTION = "subscription"


@router.post("/", tags=["dashboards"], response_model=data.SubscriptionResourceData)
async def add_dashboard_handler(
    request: Request,
    name: str,
    subscriptions: List[data.DashboardMeta],
) -> BugoutResource:
    """
    Add subscription to blockchain stream data for user.
    """

    token = request.state.token

    user = request.state.user

    dashboard_subscriptions = subscriptions

    # Get all user subscriptions
    params = {
        "type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
        "user_id": str(user.id),
    }
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}) with token ({request.state.token}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    # process existing subscriptions with supplied ids

    s3_client = boto3.client("s3")

    available_subscriptions = {
        resource.id: resource.resource_data for resource in resources.resources
    }

    for dashboard_subscription in dashboard_subscriptions:
        if dashboard_subscription.subscription_id in available_subscriptions:

            # TODO(Andrey): Add some dedublication for get object from s3 for repeated subscription_id

            bucket = available_subscriptions[dashboard_subscription.subscription_id][
                "bucket"
            ]
            abi_path = available_subscriptions[dashboard_subscription.subscription_id][
                "abi_path"
            ]

            if bucket is None or abi_path is None:
                logger.error(
                    f"Error on dashboard resource {dashboard_subscription.subscription_id} does not have an abi"
                )
                raise MoonstreamHTTPException(
                    status_code=404,
                    detail=f"Error on dashboard resource {dashboard_subscription.subscription_id} does not have an abi",
                )
            s3_path = f"s3://{bucket}/{abi_path}"

            try:

                response = s3_client.get_object(
                    Bucket=bucket,
                    Key=abi_path,
                )

            except s3_client.exceptions.NoSuchKey as e:
                logger.error(
                    f"Error getting Abi for subscription {dashboard_subscription.subscription_id} S3 {s3_path} does not exist : {str(e)}"
                )
                raise MoonstreamHTTPException(
                    status_code=500,
                    internal_error=e,
                    detail=f"We can't access the abi for subscription with id:{dashboard_subscription.subscription_id}.",
                )

            abi = data.DashboardMeta(**response["Body"].read().decode("utf-8"))

            actions.dashboards_abi_validation(
                dashboard_subscription, abi, s3_path=s3_path
            )

        else:
            logger.error(
                f"Error subscription_id: {dashboard_subscription.subscription_id} not exists."
            )
            raise MoonstreamHTTPException(status_code=404)

    dashboard_resource = data.DashboardResource(
        type=BUGOUT_RESOURCE_TYPE_DASHBOARD,
        user_id=user.id,
        name=name,
        dashboard_subscriptions=dashboard_subscriptions,
    )

    try:
        resource: BugoutResource = bc.create_resource(
            token=token,
            application_id=MOONSTREAM_APPLICATION_ID,
            resource_data=dashboard_resource.dict(),
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error creating subscription resource: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return resource


@router.delete(
    "/{dashboard_id}",
    tags=["subscriptions"],
    response_model=data.SubscriptionResourceData,
)
async def delete_subscription_handler(request: Request, dashboard_id: str):
    """
    Delete subscriptions.
    """
    token = request.state.token
    try:
        deleted_resource = bc.delete_resource(token=token, resource_id=dashboard_id)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error deleting subscription: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return deleted_resource


@router.get("/", tags=["dashboards"], response_model=BugoutResources)
async def get_dashboards_handler(
    request: Request,
    limit: int = Query(10),
    offset: int = Query(0),
) -> BugoutResources:
    """
    Get user's subscriptions.
    """
    token = request.state.token
    params = {
        "type": BUGOUT_RESOURCE_TYPE_DASHBOARD,
        "user_id": str(request.state.user.id),
    }
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}) with token ({request.state.token}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return resources


@router.get("/{dashboarsd_id}", tags=["dashboards"], response_model=BugoutResource)
async def get_dashboard_handler(
    request: Request, dashboarsd_id: UUID
) -> BugoutResource:
    """
    Get user's subscriptions.
    """
    token = request.state.token

    try:
        resource: BugoutResource = bc.get_resource(
            token=token,
            resource_id=dashboarsd_id,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}) with token ({request.state.token}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return resource


@router.put("/{dashboard_id}", tags=["dashboards"], response_model=BugoutResource)
async def update_dashboard_handler(
    request: Request,
    dashboard_id: str,
    name: Optional[str],
    subscriptions: List[data.DashboardMeta],
) -> BugoutResource:
    """
    Update dashboards mainly fully overwrite name and subscription metadata
    """

    token = request.state.token

    user = request.state.user

    dashboard_subscriptions = subscriptions

    params = {
        "type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
        "user_id": str(user.id),
    }
    try:
        resources: BugoutResources = bc.list_resources(token=token, params=params)
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}) with token ({request.state.token}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    s3_client = boto3.client("s3")

    available_subscriptions = {
        resource.id: resource.resource_data for resource in resources.resources
    }

    for dashboard_subscription in dashboard_subscriptions:
        if dashboard_subscription.subscription_id in available_subscriptions:

            # TODO(Andrey): Add some dedublication for get object from s3 for repeated subscription_id

            bucket = available_subscriptions[dashboard_subscription.subscription_id][
                "bucket"
            ]
            abi_path = available_subscriptions[dashboard_subscription.subscription_id][
                "abi_path"
            ]

            if bucket is None or abi_path is None:
                logger.error(
                    f"Error on dashboard resource {dashboard_subscription.subscription_id} does not have an abi"
                )
                raise MoonstreamHTTPException(
                    status_code=404,
                    detail=f"Error on dashboard resource {dashboard_subscription.subscription_id} does not have an abi",
                )
            s3_path = f"s3://{bucket}/{abi_path}"

            try:

                response = s3_client.get_object(
                    Bucket=bucket,
                    Key=abi_path,
                )

            except s3_client.exceptions.NoSuchKey as e:
                logger.error(
                    f"Error getting Abi for subscription {dashboard_subscription.subscription_id} S3 {s3_path} does not exist : {str(e)}"
                )
                raise MoonstreamHTTPException(
                    status_code=500,
                    internal_error=e,
                    detail=f"We can't access the abi for subscription with id:{dashboard_subscription.subscription_id}.",
                )

            abi = data.DashboardMeta(**response["Body"].read().decode("utf-8"))

            actions.dashboards_abi_validation(
                dashboard_subscription, abi, s3_path=s3_path
            )

        else:
            logger.error(
                f"Error subscription_id: {dashboard_subscription.subscription_id} not exists."
            )
            raise MoonstreamHTTPException(status_code=404)

    dashboard_resource: Dict[str, Any] = {}

    if subscriptions:

        dashboard_resource["subscriptions"] = subscriptions

    if name is not None:
        dashboard_resource["name"] = name

    try:
        resource: BugoutResource = bc.update_resource(
            token=token,
            resource_id=dashboard_id,
            resource_data=dashboard_resource,
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(f"Error creating subscription resource: {str(e)}")
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    return resource


@router.get(
    "/{dashboard_id}/data_links", tags=["dashboards"], response_model=BugoutResource
)
async def get_dashboard_data_links_handler(
    request: Request, dashboard_id: str
) -> Dict[str, Any]:
    """
    Update dashboards mainly fully overwrite name and subscription metadata
    """

    token = request.state.token

    user = request.state.user

    try:
        dashboard_resource: BugoutResource = bc.get_resource(
            token=token, resource_id=dashboard_id
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}) with token ({request.state.token}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)

    s3_client = boto3.client("s3")

    # get subscriptions

    params = {
        "type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
        "user_id": str(user.id),
    }
    try:
        subscription_resources: BugoutResources = bc.list_resources(
            token=token, params=params
        )
    except BugoutResponseException as e:
        raise MoonstreamHTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error(
            f"Error listing subscriptions for user ({request.user.id}) with token ({request.state.token}), error: {str(e)}"
        )
        reporter.error_report(e)
        raise MoonstreamHTTPException(status_code=500, internal_error=e)
    # filter out dasboards

    dashboard_subscriptions = [
        subscription
        for subscription in subscription_resources.resources
        if subscription.id
        in dashboard_resource.resource_data["dashboard_subscriptions"]
    ]

    # generate s3 links

    s3_client = boto3.client("s3")

    stats: Dict[str, Any] = {}

    for subscription in dashboard_subscriptions:

        available_timescales = [timescale.value for timescale in data.TimeScale]
        stats[subscription.id] = {}
        for timescale in available_timescales:
            try:
                result_key = f'contracts_data/{subscription.resource_data["address"]}/v1/{timescale}.json'
                stats_presigned_url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": SMARTCONTRACTS_ABI_BUCKET, "Key": result_key},
                    ExpiresIn=300,
                    HttpMethod="GET",
                )
                stats[subscription.id][timescale] = stats_presigned_url
            except Exception as err:
                logger.warning(
                    f"Can't generate S3 presigned url in stats endpoint for Bucket:{SMARTCONTRACTS_ABI_BUCKET}, Key:{result_key} get error:{err}"
                )

    return stats
