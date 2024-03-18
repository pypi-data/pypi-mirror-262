from __future__ import annotations

import contextlib

import pytest
from asedb.initialization import make_sqlite_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def engine(tmp_path):
    fname = tmp_path / "foo.db"
    engine = make_sqlite_engine(fname, initialize=True)
    yield engine
    with contextlib.suppress(FileNotFoundError):
        fname.unlink()


@pytest.fixture
def session(engine):
    # expire_on_commit: Ensure no objects are cached after a commit
    Session = sessionmaker(bind=engine, expire_on_commit=True)
    yield Session()
