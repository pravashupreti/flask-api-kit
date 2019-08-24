# pylint: disable=invalid-name,no-member
"""create comments table

Revision ID: 49864a828842
Revises: 
Create Date: 2019-08-24 16:50:00.836557

"""
import sqlalchemy as sa
from alembic import op

import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = '49864a828842'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=False),
        sa.Column('comment',
                  sa.String(),
                  nullable=False),
        sa.Column('post_id',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=True),
        sa.Column('comment_id',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=True),
        sa.Column('commented_by',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=False),
        sa.PrimaryKeyConstraint('id'),        
        )


def downgrade():
    op.drop_table('comments')
