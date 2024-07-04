from .. import navigation
from ..ui.base import base_page
import reflex as rx
from ..models import ContactEntryModel
from . import form, state


def contact_entry_list_item(contact: ContactEntryModel) -> rx.Component:
    return rx.box(
        rx.heading(contact.first_name),
        rx.text("Message:", contact.message),
        padding="1em",
    )


def contact_entries_list_page() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Contact Entries", size="5"),
            spacing="5",
            align="center",
            min_height="85vh",
        )
    )


def contact_page() -> rx.Component:
    my_child = rx.vstack(
        rx.heading("Contact", size="9"),
        rx.cond(state.ContactState.did_submit, state.ContactState.thank_you, ""),
        rx.mobile_only(rx.box(form.contact_form(), width="95vw")),
        rx.tablet_only(rx.box(form.contact_form(), width="75vw")),
        rx.desktop_only(rx.box(form.contact_form(), width="50vw")),
        spacing="5",
        justify="center",
        min_height="85vh",
        align="center",
        id="my-child",
    )

    return base_page(my_child)
