"""create review_tasks table

Revision ID: 05dbf9bbf3ab
Revises: 
Create Date: 2025-07-23 20:35:48.724383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05dbf9bbf3ab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'review_tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('repo_url', sa.String, nullable=False),
        sa.Column('pr_number', sa.Integer, nullable=False),
        sa.Column('auth_token', sa.String, nullable=True),
        sa.Column('status', sa.String, nullable=False),
        sa.Column('results', sa.Text, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('review_tasks')
