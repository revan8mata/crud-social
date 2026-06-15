"""add date

Revision ID: 7bcc2f7e5d89
Revises: 9bec31e606b0
Create Date: 2026-06-15 09:11:03.032914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bcc2f7e5d89'
down_revision: Union[str, Sequence[str], None] = '9bec31e606b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text(
            'NOW()')) )

def downgrade() -> None:
    op.drop_column('posts', 'created_at')

