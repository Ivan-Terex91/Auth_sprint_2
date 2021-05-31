from flask import Flask
from pydantic import BaseSettings, PostgresDsn, RedisDsn
from redis import Redis

from api import api
from api.staff.v1.auth import ns as staff_auth_ns
from api.v1.auth import ns as auth_ns
from api.v1.users import ns as profile_ns
from core.db import init_session
from services import Services


class Settings(BaseSettings):
    redis_dsn: RedisDsn
    postgres_dsn: PostgresDsn
    secret_key: str


def create_app():
    settings = Settings()

    app = Flask(__name__)
    app.config["ERROR_404_HELP"] = False

    session = init_session(f"{str(settings.postgres_dsn)}/auth")
    redis = Redis(host=settings.redis_dsn.host, port=settings.redis_dsn.port, db=1)

    api.init_app(app)
    api.add_namespace(profile_ns, "/api/v1/profile")
    api.add_namespace(auth_ns, "/api/v1/auth")
    api.add_namespace(staff_auth_ns, "/staff/api/v1/auth")

    services = Services(session, redis, settings.secret_key)
    app.extensions["services"] = services
    api.services = services

    return app


app = create_app()
