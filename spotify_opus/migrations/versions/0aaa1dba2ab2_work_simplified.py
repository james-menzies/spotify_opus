"""Work simplified

Revision ID: 0aaa1dba2ab2
Revises: dc89fcb3d42c
Create Date: 2020-12-22 09:46:46.265812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0aaa1dba2ab2'
down_revision = 'dc89fcb3d42c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('works', schema=None) as batch_op:
        batch_op.add_column(sa.Column('composer_id', sa.Integer(), nullable=False))
        batch_op.alter_column('date_written',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.create_foreign_key(None, 'composers', ['composer_id'], ['composer_id'])
        batch_op.drop_column('work_number')
        batch_op.drop_column('subtitle')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('works', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subtitle', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('work_number', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('date_written',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.drop_column('composer_id')

    # ### end Alembic commands ###
