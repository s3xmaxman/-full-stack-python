"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import reflex_local_auth
from . import blog, contact, navigation, pages
from rxconfig import config

from .ui.base import base_page


class State(rx.State):
    """The app state."""

    label = "Welcome to Reflex!"

    def handle_title_input_change(self, val):
        self.label = val

    def did_click(self):
        print("did click")

    ...


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


app.add_page(
    route=reflex_local_auth.routes.LOGIN_ROUTE,
    title="Login",
)


app.add_page(
    route=reflex_local_auth.routes.REGISTER_ROUTE,
    title="Register",
)


app.add_page(
    pages.about_page,
    route=navigation.routes.ABOUT_US_ROUTE,
)

app.add_page(
    blog.blog_post_list_page,
    route=navigation.routes.BLOG_POSTS_ROUTE,
    on_load=blog.BlogPostState.load_posts,
)
app.add_page(
    blog.blog_post_add_page,
    route=navigation.routes.BLOG_POST_ADD_ROUTE,
    # on_load=blog.BlogPostState.add_post,
)
app.add_page(
    blog.blog_post_detail_page,
    route="/blog/[blog_id]",
    on_load=blog.BlogPostState.get_post_detail,
)


app.add_page(
    blog.blog_post_edit_page,
    route="/blog/[blog_id]/edit",
)

app.add_page(
    pages.pricing_page,
    route=navigation.routes.PRICING_ROUTE,
)

app.add_page(
    contact.contact_page,
    route=navigation.routes.CONTACT_US_ROUTE,
)
app.add_page(
    contact.contact_entries_list_page,
    route=navigation.routes.CONTACT_ENTRIES_ROUTE,
    on_load=contact.ContactState.list_entries,
)
