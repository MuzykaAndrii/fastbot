"""empty message

Revision ID: 1ca7276a8283
Revises: 42c773427fde
Create Date: 2023-11-26 16:53:47.039509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ca7276a8283'
down_revision: Union[str, None] = '42c773427fde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vocabulary_sets', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vocabulary_sets', 'created_at')
    # ### end Alembic commands ###
