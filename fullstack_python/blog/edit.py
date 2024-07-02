from ..ui.base import base_page
import reflex as rx

from . import forms

from .state import (
    BlogAddPostFormState,
    # BlogEditFormState
)


class BlogEditFormState(rx.State):

    def handle_submit(self, from_data):
        print(from_data)


def blog_post_add_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.hstack(
                rx.input(
                    name="title",
                    placeholder="Title",
                    required=True,
                    type="text",
                    width="100%",
                ),
                width="100%",
            ),
            rx.text_area(
                name="content",
                placeholder="Your message",
                required=True,
                height="50vh",
                width="100%",
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=BlogAddPostFormState.handle_submit,
    )


def blog_post_edit_page() -> rx.Component:
    my_form = forms.blog_post_add_form()
    my_child = rx.vstack(
        rx.heading("Edit Blog Post", size="9"),
        rx.desktop_only(rx.box(my_form, width="50vw")),
        rx.tablet_only(rx.box(my_form, width="75vw")),
        rx.mobile_only(rx.box(my_form, width="95vw")),
        spacing="5",
        align="center",
        min_height="95vh",
    )
    return base_page(my_child)
