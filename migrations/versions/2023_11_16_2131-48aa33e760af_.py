"""empty message

Revision ID: 48aa33e760af
Revises: fa05e3a728b4
Create Date: 2023-11-16 21:31:32.040714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48aa33e760af'
down_revision: Union[str, None] = 'fa05e3a728b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vocabulary_sets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('language_pairs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vocabulary_id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=100), nullable=False),
    sa.Column('translation', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['vocabulary_id'], ['vocabulary_sets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('language_pairs')
    op.drop_table('vocabulary_sets')
    # ### end Alembic commands ###