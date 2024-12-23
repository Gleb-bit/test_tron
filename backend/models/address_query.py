from pydantic import BaseModel


class QueryModel(BaseModel):
    id: int

    address: str
    trx_balance: float

    bandwidth: int
    energy: int
