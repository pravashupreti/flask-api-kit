# pylint: disable=redefined-outer-name,unused-variable
import logging
from time import time

from flask import Flask, g, request, Response
from logzero import logger, loglevel, logfile, formatter

from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from api.commands import register_commands
from api.models.meta import db
from api.services import StorageService, NotificationService
from api.resources.api import api
from api.utilities.json_encoder import JsonEncoder
from api.utilities.units import define_units
from api.utilities.mode import has_mode, MODE_MAINTENANCE
from api.exceptions.error_handlers import init_error_handlers
from sampleserve.app import init_v1_app
from admin.app import init_admin_app


def _init_services():
    StorageService(Config.MINIO_HOST, Config.MINIO_ACCESS_KEY, Config.MINIO_SECRET_KEY)
    NotificationService(Config.FCM_URL, Config.FCM_AUTHORIZATION_KEY)
    define_units()


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
    _init_services()

    app.config['RESTPLUS_JSON']['cls'] = app.json_encoder = JsonEncoder

    api.init_app(app)
    db.init_app(app)
    app.jinja_env.add_extension('jinja2.ext.do')

    _init_logging()
    _register_before_request(app)
    _register_after_request(app)
    _register_maintenance_mode(app)
    register_commands(app)

    init_v1_app(app)
    init_admin_app(app)

    app.after_request(apply_version_header)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host=application.config.get("HOST"), port=application.config.get("PORT"))
