# pylint: disable=invalid-name,no-member
"""create likes table

Revision ID: 2e405757e397
Revises: 7b604fddad40
Create Date: 2019-08-24 16:50:35.106470

"""
import sqlalchemy as sa
from alembic import op

import sqlalchemy_utils
import uuid


# revision identifiers, used by Alembic.
revision = '2e405757e397'
down_revision = '7b604fddad40'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'likes',
        sa.Column('id',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=False),
        sa.Column('user_id',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=False),
        sa.Column('friend_id',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=False),                  
        sa.PrimaryKeyConstraint('id')        
        )


def downgrade():
    op.drop_table('likes')
