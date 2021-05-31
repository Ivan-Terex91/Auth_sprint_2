from functools import wraps

from flask import g, request
from flask_restx import Resource as RestResource

from core.db import session
from core.exceptions import AuthError
from services import services


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        token = request.headers.get("TOKEN")
        if not token:
            raise AuthError("Access token required")

        g.access_token = services.token_service.decode_access_token(token)

        return func(*args, **kwargs)

    return decorated_view


class Resource(RestResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.services = self.api.services

    def dispatch_request(self, *args, **kwargs):
        try:
            resp = super().dispatch_request(*args, **kwargs)
            session.commit()
            return resp
        except Exception as exc:
            session.rollback()
            raise exc
        finally:
            session.remove()
