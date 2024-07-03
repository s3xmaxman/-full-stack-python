import reflex as rx
from typing import List, Optional
from sqlmodel import select
from .model import BlogPostModel
from .. import navigation

BLOG_POSTS_ROUTE = navigation.routes.BLOG_POSTS_ROUTE
if BLOG_POSTS_ROUTE.endswith("/"):
    BLOG_POSTS_ROUTE = BLOG_POSTS_ROUTE[:-1]


class BlogPostState(rx.State):
    posts: List["BlogPostModel"] = []
    post: Optional["BlogPostModel"] = None
    post_content: str = ""
    post_publish_active: bool = False

    @rx.var
    def blog_post_id(self):
        return self.router.page.params.get("blog_id", "")

    @rx.var
    def blog_post_url(self):
        if not self.post:
            return f"{BLOG_POSTS_ROUTE}"
        return f"{BLOG_POSTS_ROUTE}/{self.post.id}"

    @rx.var
    def blog_post_edit_url(self):
        if not self.post:
            return f"{BLOG_POSTS_ROUTE}"
        return f"{BLOG_POSTS_ROUTE}/{self.post.id}/edit"

    def get_post_detail(self):
        with rx.session() as session:

            if self.blog_post_id == "":
                self.post = None
                return

            result = session.exec(
                select(BlogPostModel).where(BlogPostModel.id == self.blog_post_id)
            ).one_or_none()

            self.post = result

            if result is None:
                self.post_content = ""
                return

            self.post_content = result.content
            self.post_publish_active = result.publish_active

    def add_post(self, form_data: dict):
        with rx.session() as session:
            post = BlogPostModel(**form_data)
            session.add(post)
            session.commit()
            session.refresh(post)
            self.post = post

    def edit_post(self, post_id: int, updated_data: dict):
        with rx.session() as session:
            post = session.exec(
                select(BlogPostModel).where(BlogPostModel.id == self.blog_post_id)
            ).one_or_none()
            post = BlogPostModel(**updated_data)

            if post is None:
                return

            for key, value in updated_data.items():
                setattr(post, key, value)

            session.add(post)
            session.commit()
            session.refresh(post)
            self.post = post

    def to_blog_post(self, edit_page=False):
        if not self.post:
            return rx.redirect(BLOG_POSTS_ROUTE)
        if edit_page:
            return rx.redirect(f"{self.blog_post_edit_url}")
        return rx.redirect(f"{self.blog_post_url}")

    def load_posts(self):
        pass


class BlogAddPostFormState(BlogPostState):
    form_data: dict = {}

    def handle_submit(self, from_data):
        self.form_data = from_data
        self.add_post(from_data)
        return self.to_blog_post(edit_page=True)


class BlogEditFormState(BlogPostState):
    form_data: dict = {}
    content: str = ""

    def handle_submit(self, form_data):
        self.form_data = form_data
        post_id = form_data.pop("post_id")

        publish_date = None
        if "publish_date" in form_data:
            publish_date = form_data.pop("publish_date")

        publish_time = None
        if "publish_time" in form_data:
            publish_time = form_data.pop("publish_time")
        publish_input_string = f"{publish_date} {publish_time}"

        publish_active = False
        if "publish_active" in form_data:
            publish_active = form_data.pop("publish_active") == "on"

        updated_data = {**form_data, "publish_date": publish_input_string}
        updated_data["publish_active"] = publish_active
        self.edit_post(post_id, updated_data)
        return self.to_blog_post()
