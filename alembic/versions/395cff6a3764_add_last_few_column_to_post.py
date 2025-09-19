"""add last few column to post

Revision ID: 395cff6a3764
Revises: 19e9ab25a835
Create Date: 2025-09-16 16:02:37.431602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '395cff6a3764'
down_revision: Union[str, Sequence[str], None] = '19e9ab25a835'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('postTable', sa.Column(
        'published', sa.Boolean(), nullable=False,  default=True, server_default="1"),)
    op.add_column('postTable', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('postTable', 'published')
    op.drop_column('postTable', 'created_at')
    pass
