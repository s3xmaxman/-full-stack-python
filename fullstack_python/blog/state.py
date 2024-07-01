import reflex as rx
from typing import List, Optional
from sqlmodel import select
from .model import BlogPostModel


class BlogPostState(rx.State):
    posts: List["BlogPostModel"] = []
    post: Optional["BlogPostModel"] = None

    @rx.var
    def blog_post_id(self):
        return self.router.page.params.get("blog_id", "")

    def get_post_detail(self):
        with rx.session() as session:

            if self.blog_post_id == "":
                self.post = None
                return

            result = session.exec(
                select(BlogPostModel).where(BlogPostModel.id == self.blog_post_id)
            ).one_or_none()

            self.post = result

    def add_post(self, form_data: dict):
        with rx.session() as session:
            post = BlogPostModel(**form_data)
            session.add(post)
            session.commit()
            session.refresh(post)
            self.post = post

    def load_posts(self):
        pass


class BlogAddPostFormState(BlogPostState):
    form_data: dict = {}

    def handle_submit(self, from_data):
        self.form_data = from_data
        self.add_post(from_data)
