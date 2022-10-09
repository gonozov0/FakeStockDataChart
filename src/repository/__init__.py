from random import random

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from repository import models, schemas
from repository.db import SessionLocal


def generate_new_ticker_values(session: Session):
    def generate_movement():
        movement = -1 if random() < 0.5 else 1
        return movement

    last_ticker_values_subquery = session.query(
        func.max(models.TickerValue.id)
    ).group_by(models.TickerValue.ticker_id)
    last_ticker_values = session.query(models.TickerValue).filter(
        models.TickerValue.id.in_(last_ticker_values_subquery)
    )
    for last_ticker_value in last_ticker_values:
        new_ticker_value = models.TickerValue(
            ticker_id=last_ticker_value.ticker_id,
            value=last_ticker_value.value + generate_movement(),
        )
        session.add(new_ticker_value)
    session.commit()


def get_tickers(session: Session) -> list[schemas.Ticker]:
    tickers = session.query(models.Ticker).all()
    return [
        schemas.Ticker(
            id=ticker.id,
            name=ticker.name,
        )
        for ticker in tickers
    ]


def get_ticker_with_values(
    session: Session, ticker_id: int
) -> schemas.TickerWithValues:
    ticker = (
        session.query(models.Ticker)
        .options(joinedload(models.Ticker.values))
        .filter(models.Ticker.id == ticker_id)
        .first()
    )
    return schemas.TickerWithValues(
        id=ticker.id,
        name=ticker.name,
        values=[ticker_value.value for ticker_value in ticker.values],
    )
