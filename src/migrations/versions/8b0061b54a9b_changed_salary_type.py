"""changed salary type

Revision ID: 8b0061b54a9b
Revises: cac5e85054bf
Create Date: 2023-07-20 11:31:50.483562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b0061b54a9b'
down_revision = 'cac5e85054bf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('jobs_user_id_fkey', 'jobs', type_='foreignkey')
    op.create_foreign_key(None, 'jobs', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('responses_job_id_fkey', 'responses', type_='foreignkey')
    op.create_foreign_key(None, 'responses', 'jobs', ['job_id'], ['id'], ondelete='CASCADE')
    op.alter_column('jobs', 'salary_from', type_=sa.DECIMAL)
    op.alter_column('jobs', 'salary_to', type_=sa.DECIMAL)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'responses', type_='foreignkey')
    op.create_foreign_key('responses_job_id_fkey', 'responses', 'jobs', ['job_id'], ['id'])
    op.drop_constraint(None, 'jobs', type_='foreignkey')
    op.create_foreign_key('jobs_user_id_fkey', 'jobs', 'users', ['user_id'], ['id'])
    op.alter_column('jobs', 'salary_from', type_=sa.Numeric)
    op.alter_column('jobs', 'salary_to', type_=sa.Numeric)
    # ### end Alembic commands ###
