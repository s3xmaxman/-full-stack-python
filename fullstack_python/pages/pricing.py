import reflex as rx
from ..ui.base import base_page


class ContactState(rx.State):
    from_data: dict = {}

    def handle_submit(self, from_data: dict):
        print(from_data)
        self.from_data = from_data


def pricing_page() -> rx.Component:
    my_form = (
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="First Name",
                    name="first_name",
                    required=True,
                ),
                rx.input(
                    placeholder="Last Name",
                    name="last_name",
                ),
                rx.input(
                    placeholder="Your Email",
                    name="email",
                    type="email",
                ),
                rx.text_area(
                    placeholder="Your Message",
                    name="message",
                    required=True,
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=ContactState.handle_submit,
            reset_on_submit=True,
        ),
    )
    my_child = rx.vstack(
        rx.heading("Pricing", size="9"),
        my_form,
        spacing="5",
        justify="center",
        min_height="85vh",
        align="center",
        id="my-child",
    )

    return base_page(my_child)
