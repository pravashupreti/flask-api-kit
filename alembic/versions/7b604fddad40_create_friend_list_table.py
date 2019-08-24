# pylint: disable=invalid-name,no-member
"""create friend_list table

Revision ID: 7b604fddad40
Revises: 49864a828842
Create Date: 2019-08-24 16:50:27.591557

"""
import sqlalchemy as sa
from alembic import op

import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = '7b604fddad40'
down_revision = '49864a828842'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'friend_list',
        sa.Column('id',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=False),        
        sa.Column('user_id',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=False),
        sa.Column('friend_id',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        )


def downgrade():
    op.drop_table('friend_list')
