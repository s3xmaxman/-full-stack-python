import reflex as rx

from ..articles.list import article_public_list_component


def dashboard_component() -> rx.Component:
    return rx.box(
        rx.heading("Welcome back", size="2"),
        rx.divider(margin_top="1rem", margin_bottom="1rem"),
        article_public_list_component(columns=3, limit=20),
        min_height="85vh",
    )
