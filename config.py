# pylint: disable=too-few-public-methods
import os
import json
from typing import Type

from dotenv import load_dotenv

load_dotenv(verbose=True)


def _is_truthy(key: str, default: bool) -> bool:
    if key not in os.environ:
        return default

    return os.environ.get(key).lower() in ["1", "true", "yes"]


def _not_falsy(key: str, default: bool) -> bool:
    if key not in os.environ:
        return default

    return os.environ.get(key).lower() not in ["0", "false", "no"]


DEVELOPMENT = "development"
PRODUCTION = "production"
TESTING = "testing"


class BaseConfig:
    ROOT = os.path.dirname(os.path.realpath(__file__))

    APP_NAME = "Flask API Kit"
    FLASK_ENV = os.environ.get("FLASK_ENV", DEVELOPMENT)
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5000))
    SERVER_URL = os.environ.get("SERVER_URL", "http://{}:{}".format(HOST, PORT))
    WEBAPP_URL = os.environ.get("WEBAPP_URL", "http://localhost")

    LOG_PATH = os.environ.get("LOG_PATH", "logs/flask_api_kit.log")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "ERROR").upper()

    DATABASE_URI = os.environ.get("DATABASE_URI")
    if not DATABASE_URI:
        raise Exception('"DATABASE_URI" not set')

    DATABASE_COMMIT_CONTEXT = True
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_ALGORITHMS = json.loads(os.environ.get("AUTH0_ALGORITHMS", '["RS256"]'))
    
    MINIO_HOST = os.environ.get("MINIO_HOST")
    if not MINIO_HOST:
        raise Exception("MINIO_HOST not set")

    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
    if not MINIO_ACCESS_KEY:
        raise Exception("MINIO_ACCESS_KEY not set")

    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
    if not MINIO_SECRET_KEY:
        raise Exception("MINIO_SECRET_KEY not set")

    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = _is_truthy("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    SEED_DATABASE = _is_truthy("SEED_DATABASE", False)

    AUTH_REQUIRED = _not_falsy("AUTH_REQUIRED", True)

    with open(ROOT + '/version.txt') as f:
        VERSION = f.read().strip()


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG").upper()
    JWK_PATH = "{}/jwk.json".format(BaseConfig.ROOT)


class TestConfig(DevelopmentConfig):
    TESTING = True
    LOG_PATH = None

    DATABASE_URI = os.environ.get("TEST_DATABASE_URI")
    if not DATABASE_URI:
        raise Exception('"TEST_DATABASE_URI" not set')

    DATABASE_COMMIT_CONTEXT = False

    SQLALCHEMY_DATABASE_URI = DATABASE_URI

    
class ProductionConfig(BaseConfig):
    DEBUG = False


def _config_class() -> Type[BaseConfig]:
    env = BaseConfig.FLASK_ENV

    if env == DEVELOPMENT:
        return DevelopmentConfig
    if env == TESTING:
        return TestConfig
    if env == PRODUCTION:
        return ProductionConfig

    raise Exception("unknown config type '%s'" % env)


Config = _config_class()
