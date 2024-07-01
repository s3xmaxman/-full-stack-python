from typing import List
import asyncio
import reflex as rx

from .models import ContactEntryModel

from sqlmodel import select


class ContactState(rx.State):
    from_data: dict = {}
    entries: List["ContactEntryModel"] = []
    did_submit: bool = False

    @rx.var
    def thank_you(self):
        first_name = self.from_data.get("first_name") or ""
        return f"Thank you {first_name}".strip() + "!"

    async def handle_submit(self, from_data: dict):
        print(from_data)
        self.from_data = from_data
        data = {}
        for k, v in from_data.items():
            if v == "" or v is None:
                continue
            data[k] = v

        with rx.session() as session:
            db_entry = ContactEntryModel(**from_data)
            session.add(db_entry)
            session.commit()

        self.did_submit = True
        yield
        await asyncio.sleep(2)
        self.did_submit = False
        yield

    def list_entries(self):
        with rx.session() as session:
            entries = session.exec(select(ContactEntryModel)).all()
            self.entries = entries
