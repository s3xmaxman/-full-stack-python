from datetime import datetime
import reflex as rx
from sqlmodel import Field, Relationship
import sqlalchemy
from .. import utils
from reflex_local_auth.user import LocalUser


class UserInfo(rx.Model, table=True):
    email: str
    user_id: int = Field(foreign_key="localuser.id")
    user: LocalUser | None = Relationship()
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_datetime,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_datetime,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False,
    )
