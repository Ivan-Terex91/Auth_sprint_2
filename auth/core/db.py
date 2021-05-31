import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from core.enums import Action, DeviceType

session = scoped_session(sessionmaker(autocommit=False, autoflush=False))

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User {self.first_name} - {self.last_name}>"


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    token = Column(String, index=True, nullable=False)
    access_token = Column(String, index=True, nullable=False)
    exp = Column(DateTime, nullable=False)


def create_partition(target, connection, **kw) -> None:

    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_at_pc" PARTITION OF "history" FOR VALUES IN ('pc')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_at_mobile" PARTITION OF "history" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_at_tablet" PARTITION OF "history" FOR VALUES IN ('tablet')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_at_undefined" PARTITION OF "history" FOR VALUES IN ('undefined')"""
    )


class History(Base):
    __tablename__ = "history"

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    action = Column(ENUM(Action), nullable=False)
    datetime = Column(DateTime, nullable=False)
    user_agent = Column(String, nullable=False)
    device_type = Column(ENUM(DeviceType), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(id, device_type),
        UniqueConstraint(id, device_type),
        {
            "postgresql_partition_by": "LIST (device_type)",
            "listeners": [("after_create", create_partition)],
        },
    )

    def __repr__(self):
        return f"{self.user_id} - {self.action} - {self.datetime} - {self.device_type}"


def init_session(dsn):
    engine = create_engine(dsn)
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
    return session
