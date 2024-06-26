"""Descripción de la migración

Revision ID: 12d6ef4c4144
Revises: c320c51caea7
Create Date: 2024-05-11 22:52:41.084611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12d6ef4c4144'
down_revision: Union[str, None] = 'c320c51caea7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_table('orden_compra')

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('productos', sa.Column('tipo', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('productos', 'tipo')
    # ### end Alembic commands ###
