import reflex as rx
from .nav import navbar


def base_page(child: rx.Component, hide_navbar=False, *args, **kwargs) -> rx.Component:
    if not isinstance(child, rx.Component):
        child = rx.heading("this is not invalid child")
    if hide_navbar:
        return rx.container(
            child,
            rx.logo(),
            rx.color_mode.button(position="bottom-left"),
        )

    return rx.fragment(
        navbar(),
        rx.box(
            child,
            # bg=rx.color("accent", 3),
            padding="1em",
            width="100%",
            id="my-content-area-el",
        ),
        rx.logo(),
        rx.color_mode.button(position="bottom-left"),
        # padding='10em',
        # id="my-base-container"
    )
