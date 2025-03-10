"""empty message

Revision ID: 59f7fa011628
Revises: 
Create Date: 2025-03-10 15:12:28.986803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, Integer, ForeignKey, inspect

# revision identifiers, used by Alembic.
revision: str = '59f7fa011628'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем столбец в таблицу users
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('new_column', sa.String, nullable=True))

    # Добавляем внешний ключ в таблицу something (если нужно)
    with op.batch_alter_table('something') as batch_op:
        batch_op.create_foreign_key(
            'fk_something_user_id',
            'users',
            ['user_id'],
            ['id']
        )


def downgrade() -> None:
    # Удаляем внешний ключ из таблицы something
    with op.batch_alter_table('something') as batch_op:
        batch_op.drop_constraint('fk_something_user_id', type_='foreignkey')

    # Удаляем столбец из таблицы users
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('new_column')