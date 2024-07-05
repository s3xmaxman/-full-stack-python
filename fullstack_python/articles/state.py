"""
このスクリプトは、ブログ記事の状態管理を行うためのクラスを定義しています。
主な機能は、記事の詳細取得、記事のリストのロード、および記事へのリダイレクトです。

主な仕様:
- 記事の詳細を取得し、状態を更新する。
- 記事のリストをロードし、状態を更新する。
- 記事へのリダイレクトを行う。

制限事項:
- 記事の取得は公開されているものに限定される。
- 記事のリストのロードは指定された制限数までに限定される。
"""

from datetime import datetime
from typing import Optional, List
import reflex as rx

import sqlalchemy
from sqlmodel import select

from .. import navigation
from ..auth.state import SessionState
from ..models import BlogPostModel, UserInfo

ARTICLE_LIST_ROUTE = navigation.routes.ARTICLE_LIST_ROUTE
if ARTICLE_LIST_ROUTE.endswith("/"):
    ARTICLE_LIST_ROUTE = ARTICLE_LIST_ROUTE[:-1]


class ArticlePublicState(SessionState):
    """
    公開されている記事の状態を管理するクラス。

    属性:
    posts (List[BlogPostModel]): 記事のリスト。
    post (Optional[BlogPostModel]): 現在選択されている記事。
    post_content (str): 現在選択されている記事の内容。
    post_publish_active (bool): 記事が公開されているかどうか。
    limit (int): 記事のリストをロードする際の制限数。
    """

    posts: List["BlogPostModel"] = []
    post: Optional["BlogPostModel"] = None
    post_content: str = ""
    post_publish_active: bool = False
    limit: int = 20

    @rx.var
    def post_id(self) -> str:
        """
        現在のページのパラメータから記事IDを取得する。

        戻り値:
        str: 記事ID。存在しない場合は空文字列。
        """
        return self.router.page.params.get("post_id", "")

    @rx.var
    def post_url(self) -> str:
        """
        現在選択されている記事のURLを生成する。

        戻り値:
        str: 記事のURL。記事が選択されていない場合は記事リストのルートURL。
        """
        if not self.post:
            return f"{ARTICLE_LIST_ROUTE}"
        return f"{ARTICLE_LIST_ROUTE}/{self.post.id}"

    def get_post_detail(self):
        """
        記事の詳細を取得し、状態を更新する。

        例外:
        - 記事IDが空の場合、記事の詳細をクリアする。
        - 記事が存在しない場合、記事の内容をクリアする。
        """
        lookups = (
            (BlogPostModel.publish_active == True)
            & (BlogPostModel.publish_date < datetime.now())
            & (BlogPostModel.id == self.post_id)
        )
        with rx.session() as session:
            if self.post_id == "":
                self.post = None
                self.post_content = ""
                self.post_publish_active = False
                return
            sql_statement = (
                select(BlogPostModel)
                .options(
                    sqlalchemy.orm.joinedload(BlogPostModel.userinfo).joinedload(
                        UserInfo.user
                    )
                )
                .where(lookups)
            )
            result = session.exec(sql_statement).one_or_none()
            self.post = result
            if result is None:
                self.post_content = ""
                return
            self.post_content = self.post.content
            self.post_publish_active = self.post.publish_active

    def set_limit_and_reload(self, new_limit: int = 5):
        """
        記事のリストの制限数を設定し、記事のリストを再ロードする。

        引数:
        new_limit (int): 新しい制限数。
        """
        self.limit = new_limit
        self.load_posts()
        yield

    def load_posts(self, *args, **kwargs):
        """
        記事のリストをロードし、状態を更新する。
        """
        lookup_args = (BlogPostModel.publish_active == True) & (
            BlogPostModel.publish_date < datetime.now()
        )
        with rx.session() as session:
            result = session.exec(
                select(BlogPostModel)
                .options(sqlalchemy.orm.joinedload(BlogPostModel.userinfo))
                .where(lookup_args)
                .limit(self.limit)
            ).all()
            self.posts = result

    def to_post(self):
        """
        現在選択されている記事へリダイレクトする。

         戻り値:
        rx.redirect: 記事のURLへのリダイレクト。記事が選択されていない場合は記事リストのルートURLへのリダイレクト。
        """
        if not self.post:
            return rx.redirect(ARTICLE_LIST_ROUTE)
        return rx.redirect(f"{self.post_url}")
