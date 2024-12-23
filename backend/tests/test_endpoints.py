import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from tests.config import engine, Base, async_session


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_create_query(async_client):
    response = await async_client.post(
        "/queries/", params={"address": "TRjE1H8dxypKM1NZRdysbs9wo7huR4bdNz"}
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json.get("address") == "TRjE1H8dxypKM1NZRdysbs9wo7huR4bdNz"
    assert response_json.get("trx_balance") == 104.837
    assert response_json.get("bandwidth") == 0
    assert response_json.get("energy") == 0
    assert response_json.get("id") is not None


@pytest.mark.asyncio
async def test_get_queries(async_client):
    response = await async_client.get("/queries/")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json
