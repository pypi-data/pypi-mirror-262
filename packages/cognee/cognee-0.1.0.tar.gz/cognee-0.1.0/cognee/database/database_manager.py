"""This module provides functionalities for creating and managing databases."""

import os
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from cognee.config import Config
from cognee.database.relationaldb.database import Base, get_sqlalchemy_database_url

globalConfig = Config()

class DatabaseManager:
    """Manages database creation, deletion, and table initialization."""
    def __init__(self):
        """Initialize the Database Url with a given configuration."""
        self.engine = create_async_engine(get_sqlalchemy_database_url(globalConfig.db_type), echo = True)
        self.db_type = globalConfig.db_type

    @asynccontextmanager
    async def get_connection(self):
        """Initialize the DatabaseManager with a given configuration."""
        if self.db_type in ["sqlite", "duckdb"]:
            # For SQLite and DuckDB, the engine itself manages connections
            yield self.engine
        else:
            async with self.engine.connect() as connection:
                yield connection

    async def database_exists(self, db_name):
        """Check if a database exists."""
        if self.db_type in ["sqlite", "duckdb"]:
            # For SQLite and DuckDB, check if the database file exists
            return os.path.exists(db_name)
        else:
            query = text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
            async with self.get_connection() as connection:
                result = await connection.execute(query)
                return  result.fetchone() is not None

    async def create_database(self, db_name):
        """Create a new database."""
        if self.db_type not in ["sqlite", "duckdb"]:
            # For databases like PostgreSQL, create the database explicitly
            async with self.get_connection() as connection:
                await connection.execute(text(f"CREATE DATABASE {db_name}"))

    async def drop_database(self, db_name):
        """Drop an existing database."""
        if self.db_type in ["sqlite", "duckdb"]:
            # For SQLite and DuckDB, simply remove the database file
            os.remove(db_name)
        else:
            async with self.get_connection() as connection:
                await connection.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))

    async def create_tables(self):
        """Create tables based on the SQLAlchemy Base metadata."""
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            print(e)
            raise e
