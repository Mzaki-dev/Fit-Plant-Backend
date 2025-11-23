"""update_empty_full_names

Revision ID: c7f09bcaa0fc
Revises: 5d479b975ae8
Create Date: 2025-11-23 20:29:23.285862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7f09bcaa0fc'
down_revision: Union[str, Sequence[str], None] = '5d479b975ae8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Update empty or null full_names to 'Unknown'
    op.execute("UPDATE users SET full_name = 'Unknown' WHERE full_name IS NULL OR full_name = ''")


def downgrade() -> None:
    """Downgrade schema."""
    # Optionally, set them back to empty, but since we're fixing data, maybe no downgrade
    pass
