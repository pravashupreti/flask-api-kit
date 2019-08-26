import os

from dotenv import load_dotenv
from alembic.config import Config

test_path = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(test_path, "../.env")
alembic_directory = os.path.join(test_path, "../alembic")
ini_path = os.path.join(test_path, "seed/alembic.ini")
alembic_cfg = Config(ini_path)
alembic_cfg.set_main_option("script_location", alembic_directory)

load_dotenv(verbose=True, dotenv_path=env_path)
database_uri = os.environ.get("TEST_DATABASE_URI")
if not database_uri:
    raise Exception('"TEST_DATABASE_URI" not set')

os.environ["FLASK_ENV"] = "testing"
os.environ["DATABASE_URI"] = database_uri

seed_file_order = [
    "users.xml",
    "posts.xml",
    "friend_list.xml",
    "comments.xml",
    "likes.xml"
]
