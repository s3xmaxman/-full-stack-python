import reflex as rx
from ..ui.base import base_page
import asyncio


class ContactEntryModel(rx.Model, table=True):
    first_name: str
    last_name: str
    email: str
    message: str


class ContactState(rx.State):
    from_data: dict = {}
    did_submit: bool = False

    @rx.var
    def thank_you(self):
        first_name = self.from_data.get("first_name") or ""
        return f"Thank you {first_name}".strip() + "!"

    async def handle_submit(self, from_data: dict):
        print(from_data)
        self.from_data = from_data
        self.did_submit = True
        yield
        await asyncio.sleep(2)
        self.did_submit = False
        yield


def contact_page() -> rx.Component:
    my_form = (
        rx.form(
            rx.vstack(
                rx.hstack(
                    rx.input(
                        placeholder="First Name",
                        name="first_name",
                        required=True,
                        type="text",
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Last Name",
                        name="last_name",
                        required=True,
                        type="text",
                        width="100%",
                    ),
                    width="100%",
                ),
                rx.input(
                    placeholder="Your Email",
                    name="email",
                    type="email",
                    width="100%",
                ),
                rx.text_area(
                    placeholder="Your Message",
                    name="message",
                    required=True,
                    width="100%",
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=ContactState.handle_submit,
            reset_on_submit=True,
        ),
    )
    my_child = rx.vstack(
        rx.heading("Contact", size="9"),
        rx.cond(ContactState.did_submit, ContactState.thank_you, ""),
        rx.mobile_only(rx.box(my_form, width="95vw")),
        rx.tablet_only(rx.box(my_form, width="75vw")),
        rx.desktop_only(rx.box(my_form, width="50vw")),
        spacing="5",
        justify="center",
        min_height="85vh",
        align="center",
        id="my-child",
    )

    return base_page(my_child)
