# pylint: disable=redefined-outer-name,unused-variable
import logging
from time import time

from flask import Flask, g, request, Response
from logzero import logger, loglevel, logfile, formatter

from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from api.models.meta import db
from api.services import StorageService
from api.resources.api import api
from api.utilities.mode import has_mode, MODE_MAINTENANCE
from api.exceptions.error_handlers import init_error_handlers


def _init_services():
    StorageService(Config.MINIO_HOST, Config.MINIO_ACCESS_KEY, Config.MINIO_SECRET_KEY)


def _init_logging():
    log = logging.getLogger("werkzeug")
    log.disabled = True
    loglevel(Config.LOG_LEVEL)
    formatter(logging.Formatter("[%(asctime)s] - %(levelname)s: %(message)s"))

    if Config.LOG_PATH:
        logfile(
            Config.LOG_PATH,
            maxBytes=1000000,
            backupCount=3,
            loglevel=Config.LOG_LEVEL,
        )


def _register_before_request(app: Flask):
    def before_request():
        """
            A function to run before each request.
        """

        logger.debug("Request [%s] : %s", request.method, request.base_url)
        g.start_time = time()

    app.before_request(before_request)


def _register_after_request(app: Flask):
    def after_request(response):
        """
            A function to run after each request.
        """

        execution_time = time() - g.start_time
        logger.debug("Request completion time: %s", execution_time)

        return response

    app.after_request(after_request)


def _register_maintenance_mode(app: Flask):
    def check_for_maintenance():
        if has_mode(MODE_MAINTENANCE):
            # TODO json maintenance response
            return "Down for maintenance", 503

    app.before_request(check_for_maintenance)


def simple_app() -> Flask:
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(Config)
    init_error_handlers(app)

    return app


def apply_version_header(response: Response):
    response.headers['X-API-Version'] = Config.VERSION
    return response


def create_app() -> Flask:
    app = simple_app()
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    api.init_app(app)
    db.init_app(app)
    
    _init_logging()
    _register_before_request(app)
    _register_after_request(app)
    _register_maintenance_mode(app)
    
    app.after_request(apply_version_header)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host=application.config.get("HOST"), port=application.config.get("PORT"))
