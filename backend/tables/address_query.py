from sqlalchemy import Column, Integer, String, Float, DateTime

from config.database_conf import Base


class AddressQuery(Base):
    __tablename__ = "address_queries"

    id = Column(Integer, primary_key=True, index=True)

    address = Column(String, index=True)
    trx_balance = Column(Float)

    bandwidth = Column(Integer)
    energy = Column(Integer)
