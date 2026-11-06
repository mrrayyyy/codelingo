"""Relational models; JSON columns retain provider-independent contracts."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config as AlembicConfig
from alembic.migration import MigrationContext
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, MetaData, String, Text, UniqueConstraint, create_engine, event, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.pool import NullPool

from .config import settings

# Stable constraint names so SQLite and PostgreSQL migrations stay identical (Alembic docs, "naming conventions").
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


def now() -> datetime:
    return datetime.now(timezone.utc)


def uid() -> str:
    return str(uuid4())


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    native_language: Mapped[str] = mapped_column(String(8), default="vi")
    target_level: Mapped[str] = mapped_column(String(8), default="B1")
    daily_goal: Mapped[int] = mapped_column(Integer, default=10)
    tts_voice: Mapped[str] = mapped_column(String(100), default="en_US")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Repo(Base):
    __tablename__ = "repos"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(150))
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="queued")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ImportJob(Base):
    __tablename__ = "import_jobs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    repo_id: Mapped[str] = mapped_column(ForeignKey("repos.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(20), default="queued")
    progress: Mapped[int] = mapped_column(Integer, default=0)
    message: Mapped[str] = mapped_column(String(200), default="Waiting to extract vocabulary")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class VocabItem(Base):
    __tablename__ = "vocab_items"
    __table_args__ = (UniqueConstraint("user_id", "lemma", "part_of_speech"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    lemma: Mapped[str] = mapped_column(String(100))
    part_of_speech: Mapped[str] = mapped_column(String(20))
    cefr: Mapped[str] = mapped_column(String(8))
    cefr_estimated: Mapped[bool] = mapped_column(Boolean, default=True)
    ipa: Mapped[str | None] = mapped_column(String(150), nullable=True)
    definition: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list] = mapped_column(JSON, default=list)


class RepoVocab(Base):
    __tablename__ = "repo_vocab"
    __table_args__ = (UniqueConstraint("repo_id", "vocab_id"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    repo_id: Mapped[str] = mapped_column(ForeignKey("repos.id", ondelete="CASCADE"))
    vocab_id: Mapped[str] = mapped_column(ForeignKey("vocab_items.id", ondelete="CASCADE"))
    frequency: Mapped[int] = mapped_column(Integer)
    rank: Mapped[float] = mapped_column(Float)


class ContextSentence(Base):
    __tablename__ = "context_sentences"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    repo_vocab_id: Mapped[str] = mapped_column(ForeignKey("repo_vocab.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(Text)
    file_path: Mapped[str] = mapped_column(Text)
    line_number: Mapped[int] = mapped_column(Integer)
    kind: Mapped[str] = mapped_column(String(30))


class Plugin(Base):
    __tablename__ = "plugins"
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    version: Mapped[str] = mapped_column(String(20))
    skills: Mapped[list] = mapped_column(JSON)
    services: Mapped[list] = mapped_column(JSON)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class ExerciseRow(Base):
    __tablename__ = "exercises"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    vocab_id: Mapped[str] = mapped_column(ForeignKey("vocab_items.id", ondelete="CASCADE"))
    plugin_id: Mapped[str] = mapped_column(ForeignKey("plugins.id"))
    payload: Mapped[dict] = mapped_column(JSON)
    answer_key: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Attempt(Base):
    __tablename__ = "attempts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    exercise_id: Mapped[str | None] = mapped_column(ForeignKey("exercises.id", ondelete="CASCADE"), nullable=True)
    vocab_id: Mapped[str] = mapped_column(ForeignKey("vocab_items.id", ondelete="CASCADE"))
    submission_id: Mapped[str] = mapped_column(String(36), unique=True)
    answer: Mapped[dict] = mapped_column(JSON)
    score: Mapped[float] = mapped_column(Float)
    feedback: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ReviewSchedule(Base):
    __tablename__ = "review_schedule"
    __table_args__ = (UniqueConstraint("user_id", "vocab_id"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    vocab_id: Mapped[str] = mapped_column(ForeignKey("vocab_items.id", ondelete="CASCADE"))
    card: Mapped[dict] = mapped_column(JSON)
    due: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, index=True)
    reviews: Mapped[int] = mapped_column(Integer, default=0)
    lapses: Mapped[int] = mapped_column(Integer, default=0)
    version: Mapped[int] = mapped_column(Integer, default=0)


if settings.database_url.startswith("sqlite"):
    Path(".data").mkdir(exist_ok=True)
engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {})
if settings.database_url.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def sqlite_setup(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA busy_timeout=10000")

SessionLocal = sessionmaker(engine, expire_on_commit=False)


MIGRATIONS = Path(__file__).parent / "migrations"


def alembic_config(connection=None) -> AlembicConfig:
    """Alembic config that works from any cwd and inside both Docker images."""
    config = AlembicConfig()
    config.set_main_option("script_location", str(MIGRATIONS))
    config.set_main_option("sqlalchemy.url", settings.database_url.replace("%", "%%"))
    if connection is not None:
        config.attributes["connection"] = connection
    return config


def _sqlite_unique_index_exists(connection, diff) -> bool:
    """SQLite reflection misses unnamed column-level UNIQUE constraints, though their unique index exists."""
    if connection.dialect.name != "sqlite" or diff[0] != "add_constraint" or not isinstance(diff[1], UniqueConstraint):
        return False
    table, columns = diff[1].table.name, [column.name for column in diff[1].columns]
    # Table and index names come from our own metadata and sqlite_master, never from user input.
    for _, name, unique, *_ in connection.exec_driver_sql(f'PRAGMA index_list("{table}")'):
        if unique and [row[2] for row in connection.exec_driver_sql(f'PRAGMA index_info("{name}")')] == columns:
            return True
    return False


def schema_differences(connection) -> list:
    """Differences between the live database and the models (empty when in sync)."""
    context = MigrationContext.configure(connection, opts={"compare_type": True})
    return [diff for diff in compare_metadata(context, Base.metadata) if not _sqlite_unique_index_exists(connection, diff)]


def migrate(connection) -> None:
    tables = set(inspect(connection).get_table_names())
    if tables and "alembic_version" not in tables:
        # Database created by the pre-Alembic create_all(): adopt it only if it matches revision 0001.
        differences = schema_differences(connection)
        if differences:
            raise RuntimeError(
                "Existing database was created before Alembic and does not match the initial schema "
                f"({len(differences)} difference(s)). Back it up, then remove it or migrate it manually; "
                "data was not modified.")
        command.stamp(alembic_config(connection), "0001_initial")
    command.upgrade(alembic_config(connection), "head")


def migration_engine():
    """Neon advises a direct (non-pooled) connection for schema migrations; the app keeps the pooled URL."""
    if not settings.migration_database_url:
        return engine
    return create_engine(settings.migration_database_url, pool_pre_ping=True, poolclass=NullPool)


def init_db() -> None:
    target = migration_engine()
    try:
        with target.begin() as connection:
            migrate(connection)
    finally:
        if target is not engine:
            target.dispose()
    with SessionLocal.begin() as db:
        if not db.get(User, "local-user"):
            db.add(User(id="local-user"))


def get_db():
    with SessionLocal() as db:
        yield db
