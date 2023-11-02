from alembic import op
import sqlalchemy as sa


revision = 'd833be7e077b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=300), nullable=True))


def downgrade():
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_column('description')
