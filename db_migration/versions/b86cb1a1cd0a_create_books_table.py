"""create: books table

Revision ID: b86cb1a1cd0a
Revises: 024ee833dce7
Create Date: 2026-06-23 10:50:15.978579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlmodel import SQLModel


# revision identifiers, used by Alembic.
revision: str = 'b86cb1a1cd0a'
down_revision: Union[str, Sequence[str], None] = '024ee833dce7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
