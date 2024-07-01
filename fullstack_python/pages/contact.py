from .. import navigation
from ..ui.base import base_page
import reflex as rx

from .. import contact

import reflex as rx


@rx.page(route=navigation.routes.CONTACT_US_ROUTE)
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
            on_submit=contact.ContactState.handle_submit,
            reset_on_submit=True,
        ),
    )
    my_child = rx.vstack(
        rx.heading("Contact", size="9"),
        rx.cond(contact.ContactState.did_submit, contact.ContactState.thank_you, ""),
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
