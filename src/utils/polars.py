import polars as pl
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

# 1. Setup the SQLAlchemy connection
DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL)

# --- Option A: Query using a raw text string ---
query_string = "SELECT id, name, created_at FROM users WHERE active = 1"
df_from_text = pl.read_database(query=query_string, connection=engine)

# --- Option B: Query using a SQLAlchemy Selectable expression ---
Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    active: Mapped[bool]

# Build a programmatic query expression
stmt = select(User).where(User.active == True)

# Polars processes the Selectable object natively
df_from_orm = pl.read_database(query=stmt, connection=engine)
