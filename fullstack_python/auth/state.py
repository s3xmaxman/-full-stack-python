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

    def handle_registration_email(self, from_data):
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
