import reflex as rx
from ..ui.base import base_page


import reflex as rx
from ..ui.base import base_page


class ContactState(rx.State):
    from_data: dict = {}

    def handle_submit(self, from_data: dict):
        print(from_data)
        self.from_data = from_data


def contact_page() -> rx.Component:
    my_form = (
        rx.form(
            rx.vstack(
                rx.hstack(
                    rx.input(
                        placeholder="First Name",
                        name="first_name",
                        required=True,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Last Name",
                        name="last_name",
                        width="100%",
                    ),
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
        rx.mobile_and_tablet(rx.box(my_form, width="85vw")),
        rx.desktop_only(rx.box(my_form, width="50vw")),
        spacing="5",
        justify="center",
        min_height="85vh",
        align="center",
        id="my-child",
    )

    return base_page(my_child)
