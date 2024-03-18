from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema

from .abstract import Base


def make_sqlite_engine(filename: str, initialize: bool = False) -> sa.Engine:
    """Helper function to create a sqlite Engine,
    that disables the usage of the default schema."""
    engine = create_engine(
        f"sqlite:///{filename}",
        execution_options={"schema_translate_map": {"asedb": None}},
    )
    if initialize:
        initialize_engine(engine)
    return engine


def initialize_engine(engine: sa.Engine):
    dialect = engine.dialect.name
    if dialect != "sqlite":
        # sqlite doesn't support schemas
        create_schema(engine)
    Base.metadata.create_all(engine)


def create_schema(engine: sa.Engine):
    with engine.begin() as con:
        con.execute(CreateSchema("asedb", if_not_exists=True))
        con.commit()
