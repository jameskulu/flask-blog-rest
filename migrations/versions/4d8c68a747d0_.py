"""empty message

Revision ID: 4d8c68a747d0
Revises: 3a498a4518cb
Create Date: 2022-06-13 15:07:19.429881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d8c68a747d0'
down_revision = '3a498a4518cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('email_token', sa.String(length=500), nullable=True))
    op.add_column('users', sa.Column('email_token_expire_date', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('reset_token', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('reset_token_expire_date', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('created_on', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('updated_on', sa.DateTime(), nullable=True))
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'updated_on')
    op.drop_column('users', 'created_on')
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'reset_token_expire_date')
    op.drop_column('users', 'reset_token')
    op.drop_column('users', 'email_token_expire_date')
    op.drop_column('users', 'email_token')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###