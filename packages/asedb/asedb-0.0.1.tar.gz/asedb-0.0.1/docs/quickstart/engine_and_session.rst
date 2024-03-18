Engine & Session
-----------------

First, you need to set up an engine & session as with any SQLAlchemy project. A helper function for creating a
SQLite engine has been provided:

.. code-block:: python

    from asedb import make_sqlite_engine, initialize_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    engine = make_sqlite_engine("foo.db")  # Helper function to create a SQL Alchemy engine for sqlite
    initialize_engine(engine)  # Create necessary schema/tables

    Session = sessionmaker(bind=engine)
    session = Session()


Here, we used the `make_sqlite_engine` helper function to create the SQL Alchemy engine
object for a sqlite database. You can also create your own engine, e.g. for postgres:


.. code-block:: python

    import urllib.parse
    from sqlalchemy import create_engine

    def make_engine():
        database = os.environ["PG_DATABASE"]
        user = os.environ["PG_USER"]
        password = urllib.parse.quote_plus(os.environ["PG_PASSWORD"])
        host = os.environ["PG_HOST"]
        port = os.environ["PG_PORT"]
        connection_string = (
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )
        return create_engine(connection_string)

    engine = make_engine()
