import reflex as rx
import reflex_local_auth

import sqlmodel

from .models import UserInfo


class SessionState(reflex_local_auth.LocalAuthState):
    """
    ユーザー認証に関連する状態を管理するクラス。
    """

    @rx.cached_var
    def my_user_id(self) -> str | None:
        """
        認証済みユーザーのIDを返す。IDが負の場合はNoneを返す。

        Returns:
            str | None: 認証済みユーザーのIDまたはNone。
        """
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.id

    @rx.cached_var
    def authenticated_username(self) -> str | None:
        """
        認証済みユーザーのユーザー名を返す。IDが負の場合はNoneを返す。

        Returns:
            str | None: 認証済みユーザーのユーザー名またはNone。
        """
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.username

    @rx.cached_var
    def authenticated_user_info(self) -> UserInfo | None:
        """
        認証済みユーザーの詳細情報をデータベースから取得して返す。IDが負の場合はNoneを返す。

        Returns:
            UserInfo | None: 認証済みユーザーの詳細情報またはNone。
        """
        if self.authenticated_user.id < 0:
            return None
        with rx.session() as session:
            result = session.exec(
                sqlmodel.select(UserInfo).where(
                    UserInfo.user_id == self.authenticated_user.id
                ),
            ).one_or_none()
            if result is None:
                return None

            return result

    def on_load(self):
        """
        ページロード時の処理。認証されていない場合はログインページにリダイレクトする。

        Returns:
            LoginState: ログイン状態。
        """
        if not self.authenticated:
            return reflex_local_auth.LoginState.redir

    def perform_logout(self):
        """
        ログアウト処理を実行し、トップページにリダイレクトする。

        Returns:
            rx.redirect: トップページへのリダイレクト。
        """
        self.do_logout()
        return rx.redirect("/")


class MyRegisterState(reflex_local_auth.RegistrationState):
    """
    ユーザー登録処理を行うクラス。
    """

    def handle_registration_email(self, from_data):
        """
        ユーザー登録処理を実行し、登録結果を返す。

        Args:
            from_data (dict): 登録フォームから送信されたデータ。

        Returns:
            RegistrationResult: 登録結果。
        """
        registration_result = super().handle_registration_email(from_data)

        if self.new_user_id >= 0:
            with rx.session() as session:
                session.add(
                    UserInfo(
                        email=from_data["email"],
                        user_id=self.new_user_id,
                    )
                )
                session.commit()
        return registration_result

    def handle_registration_email(self, form_data):
        """
        ユーザー登録処理を実行し、登録結果を返す。

        Args:
            form_data (dict): 登録フォームから送信されたデータ。

        Returns:
            RegistrationResult: 登録結果。
        """
        new_user_id = self.handle_registration(form_data)
        if new_user_id >= 0:
            with rx.session() as session:
                session.add(
                    UserInfo(
                        email=form_data["email"],
                        user_id=self.new_user_id,
                    )
                )
                session.commit()
        return type(self).successful_registration
