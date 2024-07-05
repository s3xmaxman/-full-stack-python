from datetime import datetime
from typing import Optional, List
import reflex as rx

import sqlalchemy
from sqlmodel import select

from .. import navigation
from ..auth.state import SessionState
from ..models import BlogPostModel, UserInfo

BLOG_POSTS_ROUTE = navigation.routes.BLOG_POSTS_ROUTE
if BLOG_POSTS_ROUTE.endswith("/"):
    BLOG_POSTS_ROUTE = BLOG_POSTS_ROUTE[:-1]


class BlogPostState(SessionState):
    """
    ブログ投稿の状態を管理するためのクラス。

    Attributes:
        posts (List["BlogPostModel"]): ブログ投稿のリスト。
        post (Optional["BlogPostModel"]): 現在選択されているブログ投稿。
        post_content (str): 現在選択されているブログ投稿の内容。
        post_publish_active (bool): 現在選択されているブログ投稿が公開されているかどうか。
    """

    posts: List["BlogPostModel"] = []
    post: Optional["BlogPostModel"] = None
    post_content: str = ""
    post_publish_active: bool = False

    @rx.var
    def blog_post_id(self):
        """
        現在選択されているブログ投稿のIDを取得する。

        Returns:
            str: ブログ投稿のID。
        """
        return self.router.page.params.get("blog_id", "")

    @rx.var
    def blog_post_url(self):
        """
        現在選択されているブログ投稿のURLを取得する。

        Returns:
            str: ブログ投稿のURL。
        """
        if not self.post:
            return f"{BLOG_POSTS_ROUTE}"
        return f"{BLOG_POSTS_ROUTE}/{self.post.id}"

    @rx.var
    def blog_post_edit_url(self):
        """
        現在選択されているブログ投稿の編集ページのURLを取得する。

        Returns:
            str: ブログ投稿の編集ページのURL。
        """
        if not self.post:
            return f"{BLOG_POSTS_ROUTE}"
        return f"{BLOG_POSTS_ROUTE}/{self.post.id}/edit"

    def get_post_detail(self):
        """
        現在選択されているブログ投稿の詳細を取得する。
        """
        if self.my_userinfo_id is None:
            self.post = None
            self.post_content = ""
            self.post_publish_active = False
            return
        lookups = (BlogPostModel.userinfo_id == self.my_userinfo_id) & (
            BlogPostModel.id == self.blog_post_id
        )
        with rx.session() as session:
            if self.blog_post_id == "":
                self.post = None
                return
            # ブログ投稿を取得するSQLクエリを構築する。
            sql_statement = (
                select(BlogPostModel)
                .options(
                    sqlalchemy.orm.joinedload(BlogPostModel.userinfo).joinedload(
                        UserInfo.user
                    )
                )
                .where(lookups)
            )
            # SQLクエリを実行して、結果を取得する。
            result = session.exec(sql_statement).one_or_none()
            self.post = result
            if result is None:
                self.post_content = ""
                return
            self.post_content = self.post.content
            self.post_publish_active = self.post.publish_active
        # return

    def load_posts(self, *args, **kwargs):
        """
        現在のユーザーのすべてのブログ投稿を読み込む。
        """
        with rx.session() as session:
            # 現在のユーザーのすべてのブログ投稿を取得するSQLクエリを構築する。
            result = session.exec(
                select(BlogPostModel)
                .options(sqlalchemy.orm.joinedload(BlogPostModel.userinfo))
                .where(BlogPostModel.userinfo_id == self.my_userinfo_id)
            ).all()
            self.posts = result

    def add_post(self, form_data: dict):
        """
        新しいブログ投稿を追加する。

        Args:
            form_data (dict): 新しいブログ投稿のデータ。
        """
        with rx.session() as session:
            post = BlogPostModel(**form_data)

            session.add(post)
            session.commit()
            session.refresh(post)

            self.post = post

    def edit_post(self, post_id: int, updated_data: dict):
        """
        既存のブログ投稿を編集する。

        Args:
            post_id (int): 編集するブログ投稿のID。
            updated_data (dict): 更新されたブログ投稿のデータ。
        """
        with rx.session() as session:
            # 編集するブログ投稿を取得するSQLクエリを構築する。
            post = session.exec(
                select(BlogPostModel).where(BlogPostModel.id == post_id)
            ).one_or_none()
            if post is None:
                return
            for key, value in updated_data.items():
                setattr(post, key, value)
            session.add(post)
            session.commit()
            session.refresh(post)
            self.post = post

    def to_blog_post(self, edit_page=False):
        """
        現在選択されているブログ投稿のページ、またはブログ投稿のリストページにリダイレクトする。

        Args:
            edit_page (bool, optional): ブログ投稿の編集ページにリダイレクトする場合はTrue、そうでない場合はFalse。デフォルトはFalse。

        Returns:
            rx.redirect: リダイレクトオブジェクト。
        """
        if not self.post:
            return rx.redirect(BLOG_POSTS_ROUTE)
        if edit_page:
            return rx.redirect(f"{self.blog_post_edit_url}")
        return rx.redirect(f"{self.blog_post_url}")


class BlogAddPostFormState(BlogPostState):
    """
    ブログ投稿の追加フォームの状態を管理するためのクラス。

    Attributes:
        form_data (dict): フォームデータ。
    """

    form_data: dict = {}

    def handle_submit(self, form_data):
        """
        フォームが送信されたときに呼び出される。

        Args:
            form_data (dict): フォームデータ。
        """
        data = form_data.copy()
        if self.my_userinfo_id is not None:
            data["userinfo_id"] = self.my_userinfo_id
        self.form_data = data
        self.add_post(data)
        return self.to_blog_post(edit_page=True)


class BlogEditFormState(BlogPostState):
    """
    ブログ投稿の編集フォームの状態を管理するためのクラス。

    Attributes:
        form_data (dict): フォームデータ。
    """

    form_data: dict = {}

    @rx.var
    def publish_display_date(self) -> str:
        """
        公開日の表示用の文字列を取得する。
        """
        if not self.post:
            return datetime.now().strftime("%Y-%m-%d")
        if not self.post.publish_date:
            return datetime.now().strftime("%Y-%m-%d")
        return self.post.publish_date.strftime("%Y-%m-%d")

    @rx.var
    def publish_display_time(self) -> str:
        """
        公開時刻の表示用の文字列を取得する。
        """
        if not self.post:
            return datetime.now().strftime("%H:%M:%S")
        if not self.post.publish_date:
            return datetime.now().strftime("%H:%M:%S")
        return self.post.publish_date.strftime("%H:%M:%S")

    def handle_submit(self, form_data):
        """
        フォームが送信されたときに呼び出される。

        Args:
            form_data (dict): フォームデータ。
        """
        self.form_data = form_data
        post_id = form_data.pop("post_id")

        publish_date = None
        if "publish_date" in form_data:
            publish_date = form_data.pop("publish_date")

        publish_time = None
        if "publish_time" in form_data:
            publish_time = form_data.pop("publish_time")

        publish_input_string = f"{publish_date} {publish_time}"

        try:
            final_publish_date = datetime.strptime(
                publish_input_string, "%Y-%m-%d %H:%M:%S"
            )
        except:
            final_publish_date = None
        publish_active = False

        if "publish_active" in form_data:
            publish_active = form_data.pop("publish_active") == "on"

        updated_data = {**form_data}
        updated_data["publish_active"] = publish_active
        updated_data["publish_date"] = final_publish_date
        self.edit_post(post_id, updated_data)
        return self.to_blog_post()
