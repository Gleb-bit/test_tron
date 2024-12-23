import asyncio
from typing import Generator

import pytest
import pytest_asyncio

from tests.config import engine, Base, async_session


@pytest_asyncio.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_insert_query(db_session):
    from tables.address_query import AddressQuery

    query_data = {
        "address": "TRjE1H8dxypKM1NZRdysbs9wo7huR4bdNz",
        "trx_balance": 104.837,
        "bandwidth": 0,
        "energy": 0,
    }
    query = AddressQuery(**query_data)

    db_session.add(query)
    await db_session.commit()

    saved_query = await db_session.get(AddressQuery, query.id)

    assert saved_query is not None
    assert saved_query.address == query_data["address"]
    assert saved_query.trx_balance == query_data["trx_balance"]
    assert saved_query.bandwidth == query_data["bandwidth"]
    assert saved_query.energy == query_data["energy"]
