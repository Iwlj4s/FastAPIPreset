"""empty message

Revision ID: 6af544a3a854
Revises: 59f7fa011628
Create Date: 2025-03-10 15:34:59.210590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6af544a3a854'
down_revision: Union[str, None] = '59f7fa011628'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем внешний ключ в таблицу something
    with op.batch_alter_table('something') as batch_op:
        batch_op.create_foreign_key(
            'fk_something_user_id',  # Имя ограничения внешнего ключа
            'users',                 # Таблица, на которую ссылается внешний ключ
            ['user_id'],             # Столбец в таблице something
            ['id']                   # Столбец в таблице users
        )


def downgrade() -> None:
    # Удаляем внешний ключ из таблицы something
    with op.batch_alter_table('something') as batch_op:
        batch_op.drop_constraint('fk_something_user_id', type_='foreignkey')