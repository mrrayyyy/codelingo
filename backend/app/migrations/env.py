"""Alembic environment: runs from app.db.init_db() at startup or from the alembic CLI."""
from alembic import context
from sqlalchemy import create_engine

from app.db import Base, NAMING_CONVENTION  # noqa: F401  (naming convention lives on Base.metadata)

config = context.config
target_metadata = Base.metadata


def configure(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        # SQLite cannot ALTER most constraints; batch mode copies the table instead.
        render_as_batch=connection.dialect.name == "sqlite",
    )
    with context.begin_transaction():
        context.run_migrations()


def run_offline() -> None:
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata,
                      literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


def run_online() -> None:
    connection = config.attributes.get("connection")
    if connection is not None:
        # Reuse the caller's connection (init_db and tests) so SQLite pragmas and transactions apply.
        configure(connection)
        return
    from app.config import settings
    engine = create_engine(config.get_main_option("sqlalchemy.url") or settings.database_url)
    with engine.connect() as connection:
        configure(connection)
        connection.commit()


if context.is_offline_mode():
    run_offline()
else:
    run_online()
