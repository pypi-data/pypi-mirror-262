"""empty message

Revision ID: 29c08c6a8cb3
Revises: 27d3e55759fa
Create Date: 2024-02-14 11:39:19.765632

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "29c08c6a8cb3"
down_revision = "27d3e55759fa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("instances", schema=None) as batch_op:
        batch_op.drop_column("status_message")
        batch_op.drop_column("resource_spec_data")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("instances", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("resource_spec_data", sa.VARCHAR(length=4000), nullable=True)
        )
        batch_op.add_column(sa.Column("status_message", sa.VARCHAR(length=50), nullable=True))

    # ### end Alembic commands ###
