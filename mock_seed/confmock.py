import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from alembic.config import Config

script_path = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_path, "../.env")
alembic_directory = os.path.join(script_path, "../alembic")
ini_path = os.path.join(script_path, "../alembic.ini")
alembic_cfg = Config(ini_path)
alembic_cfg.set_main_option("script_location", alembic_directory)

load_dotenv(verbose=True, dotenv_path=env_path)
database_uri = os.environ.get("DATABASE_URI")
if not database_uri:
    raise Exception('"DATABASE_URI" not set')

minio_host = os.environ.get("MINIO_HOST")
minio_access_key = os.environ.get("MINIO_ACCESS_KEY")
minion_secret_key = os.environ.get("MINIO_SECRET_KEY")

if not minio_host or not minio_access_key or not minion_secret_key:
    raise Exception('Minio configuration not set')

engine = create_engine(database_uri)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

seed_file_order = [
    "users.xml"
]
