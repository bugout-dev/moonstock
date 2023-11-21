"""
Leaderboard API.
"""
import logging
from typing import Any, Dict, List, Optional, Any, Union
from uuid import UUID

from bugout.exceptions import BugoutResponseException
from fastapi import Body, Depends, FastAPI, Header, Path, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from web3 import Web3

from .. import actions, data, db
from ..middleware import (
    BugoutCORSMiddleware,
    EngineHTTPException,
    ExtractBearerTokenMiddleware,
)
from ..settings import ALLOW_ORIGINS, DOCS_TARGET_PATH
from ..settings import bugout_client as bc
from ..version import VERSION

logger = logging.getLogger(__name__)


tags_metadata = [
    {
        "name": "Public Endpoints",
        "description": "Endpoints under this tag can be accessed without any authentication. They are open to all and do not require any specific headers or tokens to be passed. Suitable for general access and non-sensitive operations.",
    },
    {
        "name": "Authorized Endpoints",
        "description": """
Endpoints under this tag require authentication. To access these endpoints, a valid `moonstream token` must be included in the request header as:

```
Authorization: Bearer <moonstream token>
```

Failure to provide a valid token will result in unauthorized access errors. These endpoints are suitable for operations that involve sensitive data or actions that only authenticated users are allowed to perform.""",
    },
]

AuthHeader = Header(
    ..., description="The expected format is 'Bearer YOUR_MOONSTREAM_ACCESS_TOKEN'."
)


leaderboad_whitelist = {
    f"/leaderboard/{DOCS_TARGET_PATH}": "GET",
    "/leaderboard/openapi.json": "GET",
    "/leaderboard/info": "GET",
    "/leaderboard/scores/changes": "GET",
    "/leaderboard/quartiles": "GET",
    "/leaderboard/count/addresses": "GET",
    "/leaderboard/position": "GET",
    "/leaderboard": "GET",
    "/leaderboard/": "GET",
    "/leaderboard/rank": "GET",
    "/leaderboard/ranks": "GET",
    "/scores/changes": "GET",
    "/leaderboard/docs": "GET",
    "/leaderboard/openapi.json": "GET",
}

app = FastAPI(
    title=f"Moonstream Engine leaderboard API",
    description="Moonstream Engine leaderboard API endpoints.",
    version=VERSION,
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=f"/{DOCS_TARGET_PATH}",
)


app.add_middleware(ExtractBearerTokenMiddleware, whitelist=leaderboad_whitelist)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(ALLOW_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "",
    response_model=Union[
        List[data.LeaderboardPosition], List[data.LeaderboardUnformattedPosition]
    ],
    tags=["Public Endpoints"],
)
@app.get(
    "/",
    response_model=Union[
        List[data.LeaderboardPosition], List[data.LeaderboardUnformattedPosition]
    ],
    tags=["Public Endpoints"],
)
async def leaderboard(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    limit: int = Query(10),
    offset: int = Query(0),
    db_session: Session = Depends(db.yield_db_session),
) -> Any:
    """
    Returns the leaderboard positions.
    """

    ### Check if leaderboard exists
    try:
        leaderboard = actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    leaderboard_positions = actions.get_leaderboard_positions(
        db_session, leaderboard_id, limit, offset
    )
    if len(leaderboard.columns_names) > 0:
        result = [
            data.LeaderboardUnformattedPosition(
                column_1=position[1],
                column_2=position[2],
                column_3=position[4],
                column_4=position[3],
            )
            for position in leaderboard_positions
        ]

    else:
        result = [
            data.LeaderboardPosition(
                address=position.address,
                score=position.score,
                rank=position.rank,
                points_data=position.points_data,
            )
            for position in leaderboard_positions
        ]

    return result


@app.post(
    "", response_model=data.LeaderboardCreatedResponse, tags=["Authorized Endpoints"]
)
@app.post(
    "/", response_model=data.LeaderboardCreatedResponse, tags=["Authorized Endpoints"]
)
async def create_leaderboard(
    request: Request,
    leaderboard: data.LeaderboardCreateRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardCreatedResponse:
    """
    Create leaderboard.
    """

    token = request.state.token

    try:
        created_leaderboard = actions.create_leaderboard(
            db_session,
            title=leaderboard.title,
            description=leaderboard.description,
            token=token,
            wallet_connect=leaderboard.wallet_connect,
            blockchain_ids=leaderboard.blockchain_ids,
            columns_names=leaderboard.columns_names,
        )
    except actions.LeaderboardCreateError as e:
        logger.error(f"Error while creating leaderboard: {e}")
        raise EngineHTTPException(
            status_code=500,
            detail="Leaderboard creation failed. Please try again.",
        )

    except Exception as e:
        logger.error(f"Error while creating leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    # Add resource to the leaderboard

    return data.LeaderboardCreatedResponse(
        id=created_leaderboard.id,  # type: ignore
        title=created_leaderboard.title,  # type: ignore
        description=created_leaderboard.description,  # type: ignore
        resource_id=created_leaderboard.resource_id,  # type: ignore
        wallet_connect=created_leaderboard.wallet_connect,  # type: ignore
        blockchain_ids=created_leaderboard.blockchain_ids,  # type: ignore
        columns_names=created_leaderboard.columns_names,  # type: ignore
        created_at=created_leaderboard.created_at,  # type: ignore
        updated_at=created_leaderboard.updated_at,  # type: ignore
    )


@app.put(
    "/{leaderboard_id}",
    response_model=data.LeaderboardUpdatedResponse,
    tags=["Authorized Endpoints"],
)
async def update_leaderboard(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    leaderboard: data.LeaderboardUpdateRequest = Body(...),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardUpdatedResponse:
    """
    Update leaderboard.
    """

    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if access != True:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        updated_leaderboard = actions.update_leaderboard(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            title=leaderboard.title,
            description=leaderboard.description,
            wallet_connect=leaderboard.wallet_connect,
            blockchain_ids=leaderboard.blockchain_ids,
            columns_names=leaderboard.columns_names,
        )
    except actions.LeaderboardUpdateError as e:
        logger.error(f"Error while updating leaderboard: {e}")
        raise EngineHTTPException(
            status_code=500,
            detail="Leaderboard update failed. Please try again.",
        )

    except Exception as e:
        logger.error(f"Error while updating leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardUpdatedResponse(
        id=updated_leaderboard.id,  # type: ignore
        title=updated_leaderboard.title,  # type: ignore
        description=updated_leaderboard.description,  # type: ignore
        resource_id=updated_leaderboard.resource_id,  # type: ignore
        wallet_connect=updated_leaderboard.wallet_connect,  # type: ignore
        blockchain_ids=updated_leaderboard.blockchain_ids,  # type: ignore
        columns_names=updated_leaderboard.columns_names,  # type: ignore
        created_at=updated_leaderboard.created_at,  # type: ignore
        updated_at=updated_leaderboard.updated_at,  # type: ignore
    )


@app.delete(
    "/{leaderboard_id}",
    response_model=data.LeaderboardDeletedResponse,
    tags=["Authorized Endpoints"],
)
async def delete_leaderboard(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardDeletedResponse:
    """
    Delete leaderboard.
    """

    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if access != True:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        deleted_leaderboard = actions.delete_leaderboard(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except actions.LeaderboardDeleteError as e:
        logger.error(f"Error while deleting leaderboard: {e}")
        raise EngineHTTPException(
            status_code=500,
            detail="Leaderboard deletion failed. Please try again.",
        )

    except Exception as e:
        logger.error(f"Error while deleting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardDeletedResponse(
        id=deleted_leaderboard.id,  # type: ignore
        title=deleted_leaderboard.title,  # type: ignore
        description=deleted_leaderboard.description,  # type: ignore
        resource_id=deleted_leaderboard.resource_id,  # type: ignore
        wallet_connect=deleted_leaderboard.wallet_connect,  # type: ignore
        blockchain_ids=deleted_leaderboard.blockchain_ids,  # type: ignore
        columns_names=deleted_leaderboard.columns_names,  # type: ignore
        created_at=deleted_leaderboard.created_at,  # type: ignore
        updated_at=deleted_leaderboard.updated_at,  # type: ignore
    )


@app.get(
    "/leaderboards",
    response_model=List[data.Leaderboard],
    tags=["Authorized Endpoints"],
)
async def get_leaderboards(
    request: Request,
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> List[data.Leaderboard]:
    """
    Returns leaderboard list to which user has access.
    """

    token = request.state.token

    try:
        leaderboards = actions.get_leaderboards(db_session, token)
    except actions.LeaderboardsResourcesNotFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboards not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboards: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    results = [
        data.Leaderboard(
            id=leaderboard.id,  # type: ignore
            title=leaderboard.title,  # type: ignore
            description=leaderboard.description,  # type: ignore
            resource_id=leaderboard.resource_id,  # type: ignore
            wallet_connect=leaderboard.wallet_connect,  # type: ignore
            blockchain_ids=leaderboard.blockchain_ids,  # type: ignore
            columns_names=leaderboard.columns_names,  # type: ignore
            created_at=leaderboard.created_at,  # type: ignore
            updated_at=leaderboard.updated_at,  # type: ignore
        )
        for leaderboard in leaderboards
    ]

    return results


@app.get(
    "/count/addresses",
    response_model=data.CountAddressesResponse,
    tags=["Public Endpoints"],
)
async def count_addresses(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
) -> data.CountAddressesResponse:
    """
    Returns the number of addresses in the leaderboard.
    """

    ### Check if leaderboard exists
    try:
        actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    count = actions.get_leaderboard_total_count(db_session, leaderboard_id)

    return data.CountAddressesResponse(count=count)


@app.get(
    "/info", response_model=data.LeaderboardInfoResponse, tags=["Public Endpoints"]
)
async def leadeboard_info(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
) -> data.LeaderboardInfoResponse:
    """
    Returns leaderboard info.
    """
    try:
        leaderboard = actions.get_leaderboard_info(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardInfoResponse(
        id=leaderboard.id,
        title=leaderboard.title,
        description=leaderboard.description,
        users_count=leaderboard.users_count,
        last_updated_at=leaderboard.last_update,
    )


@app.get(
    "/scores/changes",
    response_model=List[data.LeaderboardScoresChangesResponse],
    tags=["Public Endpoints"],
)
async def get_scores_changes(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
) -> List[data.LeaderboardScoresChangesResponse]:
    """
    Returns the score history for the given address.
    """

    try:
        scores = actions.get_leaderboard_scores_changes(db_session, leaderboard_id)
    except actions.LeaderboardIsEmpty:
        raise EngineHTTPException(status_code=204, detail="Leaderboard is empty.")

    except Exception as e:
        logger.error(f"Error while getting scores: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return [
        data.LeaderboardScoresChangesResponse(
            players_count=score.players_count,
            date=score.date,
        )
        for score in scores
    ]


@app.get("/quartiles", response_model=data.QuartilesResponse, tags=["Public Endpoints"])
async def quartiles(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
) -> data.QuartilesResponse:
    """
    Returns the quartiles of the leaderboard.
    """
    ### Check if leaderboard exists
    try:
        leaderboard = actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    try:
        q1, q2, q3 = actions.get_qurtiles(db_session, leaderboard_id)
    except actions.LeaderboardIsEmpty:
        raise EngineHTTPException(status_code=204, detail="Leaderboard is empty.")
    except Exception as e:
        logger.error(f"Error while getting quartiles: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    if len(leaderboard.columns_names) > 0:
        result = data.QuartilesResponse(
            percentile_25={
                "column_1": q1.address,
                "column_2": q1.rank,
                "column_3": q1.score,
            },
            percentile_50={
                "column_1": q2.address,
                "column_2": q2.rank,
                "column_3": q2.score,
            },
            percentile_75={
                "column_1": q3.address,
                "column_2": q3.rank,
                "column_3": q3.score,
            },
        )
    else:
        result = data.QuartilesResponse(
            percentile_25={"address": q1.address, "rank": q1.rank, "score": q1.score},
            percentile_50={"address": q2.address, "rank": q2.rank, "score": q2.score},
            percentile_75={"address": q3.address, "rank": q3.rank, "score": q3.score},
        )

    return result


@app.get(
    "/position",
    response_model=Union[
        List[data.LeaderboardPosition], List[data.LeaderboardUnformattedPosition]
    ],
    tags=["Public Endpoints"],
)
async def position(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    address: str = Query(..., description="Address to get position for."),
    window_size: int = Query(1, description="Amount of positions up and down."),
    limit: int = Query(10),
    offset: int = Query(0),
    normalize_addresses: bool = Query(
        True, description="Normalize addresses to checksum."
    ),
    db_session: Session = Depends(db.yield_db_session),
) -> Union[List[data.LeaderboardPosition], List[data.LeaderboardUnformattedPosition]]:
    """
    Returns the leaderboard posotion for the given address.
    With given window size.
    """

    ### Check if leaderboard exists
    try:
        leaderboard = actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    if normalize_addresses:
        address = Web3.toChecksumAddress(address)

    positions = actions.get_position(
        db_session, leaderboard_id, address, window_size, limit, offset
    )

    if len(leaderboard.columns_names) > 0:
        results = [
            data.LeaderboardUnformattedPosition(
                column_1=position.address,
                column_2=position.rank,
                column_3=position.score,
                column_4=position.points_data,
            )
            for position in positions
        ]

    else:
        results = [
            data.LeaderboardPosition(
                address=position.address,
                score=position.score,
                rank=position.rank,
                points_data=position.points_data,
            )
            for position in positions
        ]

    return results


@app.get(
    "/rank",
    response_model=Union[
        List[data.LeaderboardPosition], List[data.LeaderboardUnformattedPosition]
    ],
    tags=["Public Endpoints"],
)
async def rank(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    rank: int = Query(1, description="Rank to get."),
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(None),
    db_session: Session = Depends(db.yield_db_session),
) -> Union[List[data.LeaderboardPosition], List[data.LeaderboardUnformattedPosition]]:
    """
    Returns the leaderboard scores for the given rank.
    """

    ### Check if leaderboard exists
    try:
        leaderboard = actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    leaderboard_rank = actions.get_rank(
        db_session, leaderboard_id, rank, limit=limit, offset=offset
    )

    if len(leaderboard.columns_names) > 0:
        results = [
            data.LeaderboardUnformattedPosition(
                column_1=position.address,
                column_2=position.rank,
                column_3=position.score,
                column_4=position.points_data,
            )
            for position in leaderboard_rank
        ]
    else:
        results = [
            data.LeaderboardPosition(
                address=position.address,
                score=position.score,
                rank=position.rank,
                points_data=position.points_data,
            )
            for position in leaderboard_rank
        ]
    return results


@app.get("/ranks", response_model=List[data.RanksResponse], tags=["Public Endpoints"])
async def ranks(
    leaderboard_id: UUID = Query(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
) -> List[data.RanksResponse]:
    """
    Returns the leaderboard rank buckets overview with score and size of bucket.
    """

    ### Check if leaderboard exists
    try:
        actions.get_leaderboard_by_id(db_session, leaderboard_id)
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    ranks = actions.get_ranks(db_session, leaderboard_id)
    results = [
        data.RanksResponse(
            score=rank.score,
            rank=rank.rank,
            size=rank.size,
        )
        for rank in ranks
    ]
    return results


@app.put(
    "/{leaderboard_id}/scores",
    response_model=List[data.LeaderboardScore],
    tags=["Authorized Endpoints"],
)
async def leaderboard_push_scores(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    scores: List[data.Score] = Body(
        ..., description="Scores to put to the leaderboard."
    ),
    overwrite: bool = Query(
        False,
        description="If enabled, this will delete all current scores and replace them with the new scores provided.",
    ),
    normalize_addresses: bool = Query(
        True, description="Normalize addresses to checksum."
    ),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> List[data.LeaderboardScore]:
    """
    Put the leaderboard to the database.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        leaderboard_points = actions.add_scores(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            scores=scores,
            overwrite=overwrite,
            normalize_addresses=normalize_addresses,
        )
    except actions.DuplicateLeaderboardAddressError as e:
        raise EngineHTTPException(
            status_code=409,
            detail=f"Duplicates in push to database is disallowed.\n List of duplicates:{e.duplicates}.\n Please handle duplicates manualy.",
        )
    except actions.LeaderboardDeleteScoresError as e:
        logger.error(f"Delete scores failed with error: {e}")
        raise EngineHTTPException(
            status_code=500,
            detail=f"Delete scores failed.",
        )
    except Exception as e:
        logger.error(f"Score update failed with error: {e}")
        raise EngineHTTPException(status_code=500, detail="Score update failed.")

    result = [
        data.LeaderboardScore(
            leaderboard_id=score["leaderboard_id"],
            address=score["address"],
            score=score["score"],
            points_data=score["points_data"],
        )
        for score in leaderboard_points
    ]

    return result


@app.get(
    "/{leaderboard_id}/config",
    response_model=data.LeaderboardConfig,
    tags=["Authorized Endpoints"],
)
async def leaderboard_config(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardConfig:
    """
    Get leaderboard config.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        leaderboard_config = actions.get_leaderboard_config(
            leaderboard_id=leaderboard_id,
        )
    except BugoutResponseException as e:
        raise EngineHTTPException(status_code=e.status_code, detail=e.detail)
    except actions.LeaderboardConfigNotFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard config not found.",
        )
    except Exception as e:
        logger.error(f"Error while getting leaderboard config: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardConfig(**leaderboard_config)


@app.put(
    "/{leaderboard_id}/config",
    response_model=data.LeaderboardConfig,
    tags=["Authorized Endpoints"],
)
async def leaderboard_config_update(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    config: data.LeaderboardConfigUpdate = Body(..., description="Leaderboard config."),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> data.LeaderboardConfig:
    """
    Update leaderboard config.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        leaderboard_config = actions.update_leaderboard_config(
            leaderboard_id=leaderboard_id,
            config=config,
        )
    except BugoutResponseException as e:
        raise EngineHTTPException(status_code=e.status_code, detail=e.detail)
    except actions.LeaderboardConfigNotFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard config not found.",
        )
    except Exception as e:
        logger.error(f"Error while updating leaderboard config: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return data.LeaderboardConfig(**leaderboard_config)


@app.post(
    "/{leaderboard_id}/config/activate",
    response_model=bool,
    tags=["Authorized Endpoints"],
)
async def leaderboard_config_activate(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> bool:
    """
    Activate leaderboard config.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        actions.activate_leaderboard_config(
            leaderboard_id=leaderboard_id,
        )
    except BugoutResponseException as e:
        raise EngineHTTPException(status_code=e.status_code, detail=e.detail)
    except actions.LeaderboardConfigNotFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard config not found.",
        )
    except actions.LeaderboardConfigAlreadyActive as e:
        raise EngineHTTPException(
            status_code=409,
            detail="Leaderboard config is already active.",
        )
    except Exception as e:
        logger.error(f"Error while activating leaderboard config: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return True


@app.post(
    "/{leaderboard_id}/config/deactivate",
    response_model=bool,
    tags=["Authorized Endpoints"],
)
async def leaderboard_config_deactivate(
    request: Request,
    leaderboard_id: UUID = Path(..., description="Leaderboard ID"),
    db_session: Session = Depends(db.yield_db_session),
    Authorization: str = AuthHeader,
) -> bool:
    """
    Deactivate leaderboard config.
    """
    token = request.state.token
    try:
        access = actions.check_leaderboard_resource_permissions(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            token=token,
        )
    except NoResultFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard not found.",
        )

    if not access:
        raise EngineHTTPException(
            status_code=403, detail="You don't have access to this leaderboard."
        )

    try:
        actions.deactivate_leaderboard_config(
            leaderboard_id=leaderboard_id,
        )
    except BugoutResponseException as e:
        raise EngineHTTPException(status_code=e.status_code, detail=e.detail)
    except actions.LeaderboardConfigNotFound as e:
        raise EngineHTTPException(
            status_code=404,
            detail="Leaderboard config not found.",
        )
    except actions.LeaderboardConfigAlreadyInactive as e:
        raise EngineHTTPException(
            status_code=409,
            detail="Leaderboard config is already inactive.",
        )
    except Exception as e:
        logger.error(f"Error while deactivating leaderboard config: {e}")
        raise EngineHTTPException(status_code=500, detail="Internal server error")

    return True
