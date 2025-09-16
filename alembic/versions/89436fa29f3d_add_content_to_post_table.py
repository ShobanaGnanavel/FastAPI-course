"""add content to Post table

Revision ID: 89436fa29f3d
Revises: 72e0cc8c584c
Create Date: 2025-09-16 15:41:04.194226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89436fa29f3d'
down_revision: Union[str, Sequence[str], None] = '72e0cc8c584c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("postTable",sa.Column('content',sa.String(255),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("postTable",'content')
    pass
