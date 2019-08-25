# pylint: disable=no-member,wrong-import-position
import sys
import os
sys.path.insert(0, os.getcwd())

from logging.config import fileConfig
import sqlalchemy_utils
from alembic import context

from app import simple_app
from api.models.meta import db, Base
from config import Config


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.attributes.get('configure_logger', True):
    fileConfig(config.config_file_name)

# this needs to be able to use the Base for migration generation
# engine = create_engine(DATABASE_URI)
app = simple_app()
app.app_context().push()
db.init_app(app)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    url = Config.DATABASE_URI
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


# Fixes issue with UUID migrations having length attribute
# https://github.com/kvesteri/sqlalchemy-utils/issues/129#issuecomment-322734082
def render_item(type_, obj, autogen_context):
    """Apply custom rendering for selected items."""

    if type_ == 'type' and isinstance(obj, sqlalchemy_utils.types.uuid.UUIDType):
        # add import for this type
        autogen_context.imports.add("import sqlalchemy_utils")
        autogen_context.imports.add("import uuid")
        return "sqlalchemy_utils.types.uuid.UUIDType(), default=uuid.uuid4"

    # default rendering for other objects
    return False


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = db.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
