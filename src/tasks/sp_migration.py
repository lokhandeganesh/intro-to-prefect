# tasks/sp_migration.py
import polars as pl
from prefect import task
from sqlalchemy import insert, select

from db.database import get_db_connection, get_db_session
from models.sales import ProcessedSummary, RawTransaction


@task
def extract_transactions() -> pl.DataFrame:
    """Uses SQLAlchemy ORM select statement, loaded directly into Polars."""
    stmt = select(
        RawTransaction.customer_id,
        RawTransaction.amount,
        RawTransaction.status
    ).where(RawTransaction.status == "completed")

    with get_db_connection() as conn:
        # Polars reads directly using the active SQLAlchemy connection
        df = pl.read_database(query=stmt, connection=conn)

    return df

@task
def transform_metrics(df: pl.DataFrame) -> pl.DataFrame:
    """Replaces SP grouping, aggregates, and CASE statements."""
    if df.is_empty():
        return df

    summary = (
        df.group_by("customer_id")
        .agg([
            pl.col("amount").sum().alias("total_spend"),
            pl.len().alias("transaction_count")
        ])
        .with_columns(
            pl.when(pl.col("total_spend") > 5000)
            .then(pl.lit("Gold"))
            .otherwise(pl.lit("Standard"))
            .alias("customer_tier")
        )
    )
    return summary

@task
def load_summaries(df: pl.DataFrame):
    """Bulk loads data using SQLAlchemy ORM with explicit manual commit."""
    if df.is_empty():
        return

    records = df.to_dicts()

    with get_db_session() as session:
        # SQLAlchemy 2.0 Bulk Insert mapped directly to the ORM model
        session.execute(
            insert(ProcessedSummary),
            records
        )
        # Manual session commit
        session.commit()
