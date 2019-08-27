from typing import Optional
from functools import wraps

from flask import g
from sqlalchemy.orm import Session

from api.services.auth import Auth
from api.utilities.jwk import load_jwk, create_jwks, generate_jwk, has_jwk, store_jwk
from config import Config


def singleton(f: callable) -> callable:
    instance = None
    initialized = False

    @wraps(f)
    def wrapper(*args, **kwargs):
        nonlocal instance, initialized
        if not initialized:
            instance = f(*args, **kwargs)
            initialized = True
        return instance

    return wrapper


def app_context(f: callable) -> callable:
    @wraps(f)
    def wrapper(*args, **kwargs):
        if f.__name__ not in g:
            g[f.__name__] = f(*args, **kwargs)
        return g[f.__name__]

    return wrapper


@singleton
def auth_jwk() -> dict:
    if Config.LOCAL_JWK:
        if not has_jwk():
            jwk = generate_jwk()
            store_jwk(jwk)
            return jwk
        return load_jwk()

    raise Exception("Can't get 'jwk' when 'LOCAL_JWK' is False")


@singleton
def auth_jwks() -> dict:
    if Config.LOCAL_JWK:
        jwk = auth_jwk()
        return create_jwks(jwk)

    return Auth.get_jwks(Config.AUTH0_DOMAIN)


@singleton
def auth() -> Auth:
    return Auth(
        Config.AUTH0_ALGORITHMS,
        Config.AUTH0_AUDIENCE,
        Config.AUTH0_DOMAIN,
        auth_jwks())


@singleton
def db_session() -> Session:
    from api.models.meta import session
    return session
