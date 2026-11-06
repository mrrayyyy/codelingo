"""Initial schema: the tables created by the pre-Alembic create_all(), with named constraints.

Revision ID: 0001_initial
Revises: 
Create Date: 2026-11-06 10:56:35.715117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001_initial'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('plugins',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('version', sa.String(length=20), nullable=False),
    sa.Column('skills', sa.JSON(), nullable=False),
    sa.Column('services', sa.JSON(), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_plugins'))
    )
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('native_language', sa.String(length=8), nullable=False),
    sa.Column('target_level', sa.String(length=8), nullable=False),
    sa.Column('daily_goal', sa.Integer(), nullable=False),
    sa.Column('tts_voice', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_table('repos',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('source_url', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_repos_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_repos'))
    )
    op.create_table('vocab_items',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('lemma', sa.String(length=100), nullable=False),
    sa.Column('part_of_speech', sa.String(length=20), nullable=False),
    sa.Column('cefr', sa.String(length=8), nullable=False),
    sa.Column('cefr_estimated', sa.Boolean(), nullable=False),
    sa.Column('ipa', sa.String(length=150), nullable=True),
    sa.Column('definition', sa.Text(), nullable=True),
    sa.Column('tags', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_vocab_items_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_vocab_items')),
    sa.UniqueConstraint('user_id', 'lemma', 'part_of_speech', name=op.f('uq_vocab_items_user_id_lemma_part_of_speech'))
    )
    op.create_table('exercises',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('vocab_id', sa.String(length=36), nullable=False),
    sa.Column('plugin_id', sa.String(length=60), nullable=False),
    sa.Column('payload', sa.JSON(), nullable=False),
    sa.Column('answer_key', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['plugin_id'], ['plugins.id'], name=op.f('fk_exercises_plugin_id_plugins')),
    sa.ForeignKeyConstraint(['vocab_id'], ['vocab_items.id'], name=op.f('fk_exercises_vocab_id_vocab_items'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_exercises'))
    )
    op.create_table('import_jobs',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('repo_id', sa.String(length=36), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('progress', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=200), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['repo_id'], ['repos.id'], name=op.f('fk_import_jobs_repo_id_repos'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_import_jobs'))
    )
    op.create_table('repo_vocab',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('repo_id', sa.String(length=36), nullable=False),
    sa.Column('vocab_id', sa.String(length=36), nullable=False),
    sa.Column('frequency', sa.Integer(), nullable=False),
    sa.Column('rank', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['repo_id'], ['repos.id'], name=op.f('fk_repo_vocab_repo_id_repos'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vocab_id'], ['vocab_items.id'], name=op.f('fk_repo_vocab_vocab_id_vocab_items'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_repo_vocab')),
    sa.UniqueConstraint('repo_id', 'vocab_id', name=op.f('uq_repo_vocab_repo_id_vocab_id'))
    )
    op.create_table('review_schedule',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('vocab_id', sa.String(length=36), nullable=False),
    sa.Column('card', sa.JSON(), nullable=False),
    sa.Column('due', sa.DateTime(timezone=True), nullable=False),
    sa.Column('reviews', sa.Integer(), nullable=False),
    sa.Column('lapses', sa.Integer(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_review_schedule_user_id_users'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vocab_id'], ['vocab_items.id'], name=op.f('fk_review_schedule_vocab_id_vocab_items'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_review_schedule')),
    sa.UniqueConstraint('user_id', 'vocab_id', name=op.f('uq_review_schedule_user_id_vocab_id'))
    )
    op.create_index(op.f('ix_review_schedule_due'), 'review_schedule', ['due'], unique=False)
    op.create_table('attempts',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('exercise_id', sa.String(length=36), nullable=True),
    sa.Column('vocab_id', sa.String(length=36), nullable=False),
    sa.Column('submission_id', sa.String(length=36), nullable=False),
    sa.Column('answer', sa.JSON(), nullable=False),
    sa.Column('score', sa.Float(), nullable=False),
    sa.Column('feedback', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], name=op.f('fk_attempts_exercise_id_exercises'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_attempts_user_id_users'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vocab_id'], ['vocab_items.id'], name=op.f('fk_attempts_vocab_id_vocab_items'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_attempts')),
    sa.UniqueConstraint('submission_id', name=op.f('uq_attempts_submission_id'))
    )
    op.create_table('context_sentences',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('repo_vocab_id', sa.String(length=36), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('file_path', sa.Text(), nullable=False),
    sa.Column('line_number', sa.Integer(), nullable=False),
    sa.Column('kind', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['repo_vocab_id'], ['repo_vocab.id'], name=op.f('fk_context_sentences_repo_vocab_id_repo_vocab'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_context_sentences'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('context_sentences')
    op.drop_table('attempts')
    op.drop_index(op.f('ix_review_schedule_due'), table_name='review_schedule')
    op.drop_table('review_schedule')
    op.drop_table('repo_vocab')
    op.drop_table('import_jobs')
    op.drop_table('exercises')
    op.drop_table('vocab_items')
    op.drop_table('repos')
    op.drop_table('users')
    op.drop_table('plugins')
