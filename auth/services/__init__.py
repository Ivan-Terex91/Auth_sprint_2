from flask import current_app
from werkzeug.local import LocalProxy

from services.auth import TokenService
from services.history import UserHistoryService
from services.users import UserService

services = LocalProxy(lambda: current_app.extensions["services"])


class Services:
    def __init__(self, session, redis, secret_key):
        self.session = session
        self.redis = redis
        self.user = UserService(session)
        self.user_history = UserHistoryService(session)
        self.token_service = TokenService(session, redis, secret_key)
