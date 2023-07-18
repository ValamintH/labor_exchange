"""Modified tables

Revision ID: 6e88e5d5abf3
Revises: e6b667630d8a
Create Date: 2023-07-12 10:14:31.130508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e88e5d5abf3'
down_revision = 'e6b667630d8a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('title', sa.String(), nullable=True, comment='Название вакансии'))
    op.add_column('jobs', sa.Column('description', sa.String(), nullable=True, comment='Описание вакансии'))
    op.add_column('jobs', sa.Column('salary_from', sa.Numeric(), nullable=True, comment='Зарплата от'))
    op.add_column('jobs', sa.Column('salary_to', sa.Numeric(), nullable=True, comment='Зарплата до'))
    op.add_column('jobs', sa.Column('is_active', sa.Boolean(), nullable=True, comment='Активна ли вакансия'))
    op.add_column('jobs', sa.Column('created_at', sa.DateTime(), nullable=True, comment='Дата создания записи'))
    op.alter_column('users', 'id',
               existing_type=sa.INTEGER(),
               comment='Идентификатор пользователя',
               existing_comment='Идентификатор задачи',
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('users_id_seq'::regclass)"))
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('users', 'id',
               existing_type=sa.INTEGER(),
               comment='Идентификатор задачи',
               existing_comment='Идентификатор пользователя',
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('users_id_seq'::regclass)"))
    op.drop_column('jobs', 'created_at')
    op.drop_column('jobs', 'is_active')
    op.drop_column('jobs', 'salary_to')
    op.drop_column('jobs', 'salary_from')
    op.drop_column('jobs', 'description')
    op.drop_column('jobs', 'title')
    # ### end Alembic commands ###