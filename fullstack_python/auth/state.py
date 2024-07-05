import reflex as rx
import reflex_local_auth

import sqlmodel

from ..models import UserInfo


class SessionState(reflex_local_auth.LocalAuthState):
    """セッション状態を管理するクラス。 reflex_local_auth.LocalAuthState を継承。

    Attributes:
        my_userinfo_id (str | None): ログイン中のユーザー情報ID。
        my_user_id (str | None): ログイン中のユーザーID。
        authenticated_username (str | None): ログイン中のユーザー名。
        authenticated_user_info (UserInfo | None): ログイン中のユーザー情報。
    """

    @rx.cached_var
    def my_userinfo_id(self) -> str | None:
        """ログイン中のユーザー情報IDを取得する。

        Returns:
            str | None: ユーザー情報ID。ログインしていない場合は None。
        """
        if self.authenticated_user_info is None:
            return None
        return self.authenticated_user_info.id

    @rx.cached_var
    def my_user_id(self) -> str | None:
        """ログイン中のユーザーIDを取得する。

        Returns:
            str | None: ユーザーID。ログインしていない場合は None。
        """
        # authenticated_user.id が 0未満の場合、ログインしていないと判断する
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.id

    @rx.cached_var
    def authenticated_username(self) -> str | None:
        """ログイン中のユーザー名を取得する。

        Returns:
            str | None: ユーザー名。ログインしていない場合は None。
        """
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.username

    @rx.cached_var
    def authenticated_user_info(self) -> UserInfo | None:
        """ログイン中のユーザー情報を取得する。

        Returns:
            UserInfo | None: ユーザー情報。ログインしていない場合は None。
        """
        if self.authenticated_user.id < 0:
            return None
        with rx.session() as session:
            # ユーザーIDを条件に、UserInfoテーブルからデータを取得する
            result = session.exec(
                sqlmodel.select(UserInfo).where(
                    UserInfo.user_id == self.authenticated_user.id
                ),
            ).one_or_none()
            if result is None:
                return None
            return result

    def on_load(self):
        """ページ読み込み時に実行される処理。

        ログインしていない場合は、ログインページにリダイレクトする。
        """
        if not self.is_authenticated:
            return reflex_local_auth.LoginState.redir
        print(self.is_authenticated)
        print(self.authenticated_user_info)

    def perform_logout(self):
        """ログアウト処理を実行する。

        Returns:
            rx.redirect: ルートページへのリダイレクト。
        """
        self.do_logout()
        return rx.redirect("/")


class MyRegisterState(reflex_local_auth.RegistrationState):
    """ユーザー登録処理を行うクラス。 reflex_local_auth.RegistrationState を継承。"""

    def handle_registration(
        self, form_data
    ) -> rx.event.EventSpec | list[rx.event.EventSpec]:
        """ユーザー登録処理を実行する。

        Args:
            form_data: フォームデータ。

        Returns:
            rx.event.EventSpec | list[rx.event.EventSpec]: イベント情報。
        """
        username = form_data["username"]
        password = form_data["password"]
        # 入力値のバリデーションチェックを行う
        validation_errors = self._validate_fields(
            username, password, form_data["confirm_password"]
        )
        if validation_errors:
            # バリデーションエラーがある場合は、エラーメッセージを返す
            self.new_user_id = -1
            return validation_errors
        # ユーザー登録処理を実行する
        self._register_user(username, password)
        return self.new_user_id

    def handle_registration_email(self, form_data):
        """ユーザー登録処理(メールアドレスを含む)を実行する。

        Args:
            form_data: フォームデータ。

        Returns:
            rx.event.EventSpec | list[rx.event.EventSpec]: イベント情報。
        """
        # ユーザー登録処理を実行する
        new_user_id = self.handle_registration(form_data)
        if new_user_id >= 0:
            # ユーザー登録が成功した場合、ユーザー情報をUserInfoテーブルに登録する
            with rx.session() as session:
                session.add(
                    UserInfo(
                        email=form_data["email"],
                        user_id=self.new_user_id,
                    )
                )
                session.commit()
        return type(self).successful_registration
