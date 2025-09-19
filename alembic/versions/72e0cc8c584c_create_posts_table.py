"""create posts table

Revision ID: 72e0cc8c584c
Revises: 
Create Date: 2025-09-16 14:23:54.341751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72e0cc8c584c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('postTable',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(255),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('postTable')
    pass
