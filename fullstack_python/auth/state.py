import reflex as rx
import reflex_local_auth

import sqlmodel

from .models import UserInfo


class SessionState(reflex_local_auth.LocalAuthState):

    @rx.cached_var
    def authenticated_user_info(self) -> UserInfo | None:
        if self.authenticated_user.id < 0:
            return
        with rx.session() as session:
            return session.exec(
                sqlmodel.select(UserInfo).where(
                    UserInfo.user_id == self.authenticated_user.id
                ),
            ).one_or_none()

    def on_load(self):
        if not self.authenticated:
            return reflex_local_auth.LoginState.redir


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
