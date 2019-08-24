# pylint: disable=invalid-name,no-member
"""create posts table

Revision ID: 730f2b899c60
Revises: 2e405757e397
Create Date: 2019-08-24 16:50:43.483817

"""
import sqlalchemy as sa
from alembic import op

import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = '730f2b899c60'
down_revision = '2e405757e397'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=False),
        sa.Column('post',
                  sa.String(),
                  nullable=False),        
        sa.Column('posted_by',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=False),
        sa.PrimaryKeyConstraint('id'),        
        )


def downgrade():
    op.drop_table('posts')
