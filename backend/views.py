from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database_conf import get_session
from core.sqlalchemy.crud import Crud
from models.address_query import QueryModel
from services.tron import get_tron_info
from tables.address_query import AddressQuery

query_router = APIRouter()
query_crud = Crud(AddressQuery)


@query_router.post("/", response_model=QueryModel)
async def create_query_address(
    address: str,
    session: AsyncSession = Depends(get_session),
):
    trx_balance, bandwidth, energy = get_tron_info(address)

    return await query_crud.create(
        {
            "address": address,
            "trx_balance": trx_balance,
            "bandwidth": bandwidth,
            "energy": energy
        },
        session,
    )


@query_router.get("/", response_model=List[QueryModel])
async def get_queries(
    offset: int = None,
    limit: int = None,
    session: AsyncSession = Depends(get_session),
):
    return await query_crud.list(session, offset=offset, limit=limit)
