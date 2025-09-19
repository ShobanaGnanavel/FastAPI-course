"""add foreignkey to posttable

Revision ID: 19e9ab25a835
Revises: b3fb64c39cd2
Create Date: 2025-09-16 15:56:15.105863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19e9ab25a835'
down_revision: Union[str, Sequence[str], None] = 'b3fb64c39cd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',source_table='posts',referent_table='usersTable',
                          local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_user_fk','posts')
    op.drop_column('posts','owner_id')
    pass
