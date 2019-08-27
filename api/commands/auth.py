import json

from flask.cli import AppGroup

from api.utilities.jwk import generate_jwk, store_jwk, create_claim, create_token, create_header
from api import di

auth_cli = AppGroup("auth")


@auth_cli.command("generate_jwk")
def cli_generate_jwk():
    jwk = generate_jwk()

    store_jwk(jwk)

    print('"jwk.json" created')


@auth_cli.command("generate_token")
def cli_generate_token():
    jwk = di.auth_jwk()

    header = create_header(jwk["kid"], scope="openid email")

    claim = create_claim("example|1234567890", email="guy@example.com", email_verified=True)

    token = create_token(claim, jwk, header)

    print("Bearer {}".format(token))


@auth_cli.command("get_jwk")
def cli_get_jwk():
    jwk = di.auth_jwk()

    print(json.dumps(jwk, indent=4))
