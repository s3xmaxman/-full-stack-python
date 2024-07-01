"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    label = "Welcome to Reflex!"

    def handle_title_input_change(self, val):
        self.label = val

    def did_click(self):
        print("did click")

    ...


def navbar() -> rx.Component:
    return rx.heading("SaaS", size="9")


def base_page(
    children: rx.Component, hide_navbar=False, *args, **kwargs
) -> rx.Component:
    if not isinstance(children, rx.Component):
        children = rx.heading("this is not invalid child")
    if hide_navbar:
        return rx.container(
            navbar(),
            children,
            rx.logo(),
            rx.color_mode.button(position="bottom-left"),
        )


def index() -> rx.Component:
    # Welcome Page (Index)
    return base_page(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.input(
                default_value=State.label,
                on_change=State.handle_title_input_change,
                on_click=State.did_click,
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)
