from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from repository.db import Base


class Ticker(Base):
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    values = relationship("TickerValue", back_populates="ticker")


class TickerValue(Base):
    __tablename__ = "ticker_values"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer)
    ticker_id = Column(Integer, ForeignKey("tickers.id"))

    ticker = relationship("Ticker", back_populates="values")
