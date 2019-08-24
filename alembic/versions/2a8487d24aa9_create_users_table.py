# pylint: disable=invalid-name,no-member
"""create users table

Revision ID: 2a8487d24aa9
Revises: 730f2b899c60
Create Date: 2019-08-24 16:50:50.682959

"""
import sqlalchemy as sa
from alembic import op

import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = '2a8487d24aa9'
down_revision = '730f2b899c60'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id',
                  sqlalchemy_utils.types.uuid.UUIDType(),
                  default=uuid.uuid4, nullable=False),
        sa.Column('email',
                  sqlalchemy_utils.types.email.EmailType(length=255),
                  nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='users_email_key')
        )


def downgrade():
    op.drop_table('users')
