from pathlib import Path

import pytest
from alembic import command
from sqlalchemy import MetaData, create_engine, inspect, text

from app.db import Base, alembic_config, migrate, schema_differences

TABLES = {table.name for table in Base.metadata.sorted_tables}


def sqlite_engine(tmp_path: Path, name: str = "migrate.db"):
    return create_engine(f"sqlite:///{tmp_path / name}")


def legacy_create_all(engine) -> None:
    """Recreate what create_all() produced before Alembic: same tables, no naming convention."""
    legacy = MetaData()
    for table in Base.metadata.sorted_tables:
        table.to_metadata(legacy)
    legacy.create_all(engine)


def head_revision(connection) -> str:
    return connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()


def test_empty_database_upgrades_to_models(tmp_path):
    with sqlite_engine(tmp_path).begin() as connection:
        migrate(connection)
        assert TABLES <= set(inspect(connection).get_table_names())
        assert head_revision(connection) == "0001_initial"
        assert schema_differences(connection) == []


def test_downgrade_and_upgrade_round_trip(tmp_path):
    with sqlite_engine(tmp_path).begin() as connection:
        migrate(connection)
        command.downgrade(alembic_config(connection), "base")
        assert not TABLES & set(inspect(connection).get_table_names())
        command.upgrade(alembic_config(connection), "head")
        assert schema_differences(connection) == []


def test_matching_pre_alembic_database_is_adopted(tmp_path):
    engine = sqlite_engine(tmp_path)
    legacy_create_all(engine)
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO users (id, native_language, target_level, daily_goal, tts_voice, created_at) "
                                "VALUES ('kept-user', 'vi', 'B1', 10, 'en_US', '2026-11-01 00:00:00')"))
    with engine.begin() as connection:
        migrate(connection)
        assert head_revision(connection) == "0001_initial"
        assert connection.execute(text("SELECT count(*) FROM users WHERE id = 'kept-user'")).scalar_one() == 1


def test_mismatched_pre_alembic_database_is_left_untouched(tmp_path):
    engine = sqlite_engine(tmp_path)
    legacy_create_all(engine)
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE users ADD COLUMN nickname TEXT"))
    with engine.begin() as connection:
        with pytest.raises(RuntimeError, match="does not match the initial schema"):
            migrate(connection)
    with engine.connect() as connection:
        tables = set(inspect(connection).get_table_names())
        assert "alembic_version" not in tables
        assert "nickname" in {column["name"] for column in inspect(connection).get_columns("users")}
