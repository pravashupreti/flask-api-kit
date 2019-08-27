import os
import json
from datetime import datetime, timedelta, timezone
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

from jose import jwt
from jose.jwk import construct

from config import Config


def has_jwk() -> bool:
    return os.path.isfile(Config.JWK_PATH)


def load_jwk() -> dict:
    with open(Config.JWK_PATH, "r") as f:
        return json.load(f)


def store_jwk(jwk: dict):
    with open(Config.JWK_PATH, "w+") as f:
        json.dump(jwk, f, indent=4)


def generate_private_key() -> str:
    """
    Not Secure! only use this for testing, NEVER production
    :return: An RSA Private key
    """
    key = rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=3,
        key_size=512
    )

    return key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )


def generate_jwk() -> dict:
    key = generate_private_key()
    jwk = construct(key, Config.AUTH0_ALGORITHMS[0])
    raw = jwk.to_dict()

    # some of the values are in bytes and don't convert well to json
    data = {k: v.decode("utf-8") if isinstance(v, bytes) else v for k, v in raw.items()}

    # Auth fails when "kid" is not set
    # TODO randomly generate this
    data["kid"] = "TEST"

    return data


def create_jwks(jwk: dict) -> dict:
    return {
        "keys": [
            {
                "alg": Config.AUTH0_ALGORITHMS[0],
                "kty": jwk["kty"],
                "use": "sig",
                "n": jwk["n"],
                "e": jwk["e"],
                "kid": jwk["kid"],
            }
        ]
    }


def create_rsa_key(jwk: dict) -> dict:
    return {
        "e": jwk["e"],
        "kid": jwk["kid"],
        "kty": jwk["kty"],
        "n": jwk["n"],
        "use": "sig"
    }


def create_header(kid: str, **kwargs) -> dict:
    header = {
        "typ": "JWT",
        "alg": Config.AUTH0_ALGORITHMS[0],
        "kid": kid,
    }

    return dict(header, **kwargs)


def create_claim(
        sub: str,
        iss: str = "https://{}/".format(Config.AUTH0_DOMAIN),
        aud: str = Config.AUTH0_AUDIENCE,
        iat: datetime = None,
        exp: datetime = None,
        **kwargs) -> dict:

    iat = iat or datetime.utcnow()
    exp = exp or iat + timedelta(hours=12)

    tz = timezone.utc

    return dict(
        kwargs,
        iss=iss,
        sub=sub,
        aud=aud,
        iat=iat.astimezone(tz).timestamp(),
        exp=exp.astimezone(tz).timestamp()
    )


def create_token(claim: dict, jwk: dict, header: dict = None) -> str:
    header = header or create_header(jwk["kid"])

    return jwt.encode(claim, jwk, Config.AUTH0_ALGORITHMS[0], header)
