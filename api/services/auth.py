import json
from typing import List
from functools import wraps

from jose import jwt
from six.moves.urllib.request import urlopen
from flask import request, g
from werkzeug.datastructures import Headers

from api.exceptions.auth_exception import (
    AuthException,
    AuthInvalidHeader,
    AuthHeaderMissing,
    AuthTokenExpired,
    AuthMissingScope,
    AuthInvalidClaim
)

from config import Config


# see https://auth0.com/docs/quickstart/backend/python/01-authorization
class Auth:
    def __init__(self, algorithms: List[str], identifier: str, domain: str, jwks: dict = None):
        self.domain = domain
        self.identifier = identifier
        self.algorithms = algorithms
        if not jwks:
            jwks = self.get_jwks(domain)
        self.jwks = jwks

    @property
    def claim(self) -> dict:
        return self._get_claim()

    def _get_claim(self) -> dict:
        if "claim" not in g:
            token = self.get_token_auth_header(request.headers)
            payload = self.get_payload(token)

            g.claim = payload
        return g.claim

    @property
    def scopes(self) -> List[str]:
        if "scopes" not in g:
            token = self.get_token_auth_header(request.headers)
            unverified_claims = jwt.get_unverified_claims(token)
            if unverified_claims.get("scope"):
                g.scopes = unverified_claims["scope"].split()
            else:
                g.scopes = []
        return g.scopes

    @classmethod
    def get_jwks(cls, domain: str) -> dict:
        json_url = urlopen('https://{}/.well-known/jwks.json'.format(domain))
        jwks = json.loads(json_url.read())
        return jwks

    @classmethod
    def get_unverified_header(cls, token: str) -> dict:
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise AuthInvalidHeader('Invalid header. ' 'Use an RS256 signed JWT Access Token')

        if unverified_header['alg'] == 'HS256':
            raise AuthInvalidHeader('Invalid header. ' 'Use an RS256 signed JWT Access Token')
        return unverified_header

    @classmethod
    def get_token_auth_header(cls, headers: Headers) -> str:
        """
        Obtains the access token from the Authorization Header
        """
        auth_header = headers.get("Authorization", None)
        if not auth_header:
            raise AuthHeaderMissing()

        parts = auth_header.split()

        if parts[0].lower() != "bearer":
            raise AuthInvalidHeader("Authorization header must start with Bearer")
        if len(parts) == 1:
            raise AuthInvalidHeader("Token not found")
        if len(parts) > 2:
            raise AuthInvalidHeader("Authorization header must be Bearer token")

        token = parts[1]
        return token

    def canonicalize_openid_url(self, sub: str) -> str:
        return "http://{domain}/{sub}".format(domain=self.domain, sub=sub)

    def get_rsa_key(self, unverified_header: dict) -> dict:
        for key in self.jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                return {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e'],
                }

        raise AuthInvalidHeader('Unable to find appropriate key')

    def get_payload(self, token: str) -> dict:
        rsa_key = self.get_rsa_key(self.get_unverified_header(token))
        
        try:
            return jwt.decode(
            token,
            rsa_key,
            algorithms=self.algorithms,
            audience=self.identifier,
            issuer='https://%s/' % self.domain,
        )            
        except jwt.ExpiredSignatureError:
            raise AuthTokenExpired
        except jwt.JWTClaimsError:
            raise AuthInvalidClaim
        except Exception:
            raise AuthException()

    def required(self, f: callable) -> callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            self._get_claim()
            return f(*args, **kwargs)

        return wrapper

    def scope(self, scope):
        def decorator(f: callable) -> callable:
            @wraps(f)
            def wrapper(*args, **kwargs):
                if scope not in self.scopes:
                    raise AuthMissingScope(scope)
                return f(*args, **kwargs)

            return wrapper

        return decorator
