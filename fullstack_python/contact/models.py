from datetime import datetime, timezone
import reflex as rx

from sqlmodel import Field
import sqlalchemy


def get_utc_datetime() -> datetime:
    return datetime.now(timezone.utc)


class ContactEntryModel(rx.Model, table=True):
    first_name: str
    last_name: str | None = None
    email: str | None = None
    message: str
    created_at: datetime = Field(
        default_factory=get_utc_datetime,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )
