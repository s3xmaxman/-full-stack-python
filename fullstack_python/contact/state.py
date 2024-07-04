from typing import List
import asyncio
import reflex as rx

from sqlmodel import select

# SessionStateクラスをインポート
from ..auth.state import SessionState

# ContactEntryModelクラスをインポート
from .models import ContactEntryModel


# ContactStateクラスはSessionStateクラスを継承
class ContactState(SessionState):
    """
    ContactStateクラスは、コンタクトフォームの状態を管理します。
    """

    # フォームデータを保持する辞書
    form_data: dict = {}
    # ContactEntryModelのリストを保持
    entries: List["ContactEntryModel"] = []
    # フォームが送信されたかどうかを示すフラグ
    did_submit: bool = False

    # フォーム送信後の感謝メッセージを生成
    @rx.var
    def thank_you(self):
        """
        フォーム送信後の感謝メッセージを生成します。
        :return: 感謝メッセージの文字列
        """
        first_name = self.form_data.get("first_name") or ""
        return f"Thank you {first_name}".strip() + "!"

    # フォーム送信を処理する非同期関数
    async def handle_submit(self, form_data: dict):
        """
        フォーム送信を処理し、データベースにデータを保存します。
        :param form_data: フォームデータの辞書
        """
        self.form_data = form_data
        data = {}

        # フォームデータから空の値を除外
        for k, v in form_data.items():
            if v == "" or v is None:
                continue
            data[k] = v

        # ユーザーIDが存在する場合、データに追加
        if self.my_user_id is not None:
            data["user_id"] = self.my_user_id

        # ユーザー情報IDが存在する場合、データに追加
        if self.my_userinfo_id is not None:
            data["userinfo_id"] = self.my_userinfo_id

        # データベースセッションを開始
        with rx.session() as session:
            db_entry = ContactEntryModel(**data)
            session.add(db_entry)
            session.commit()
            self.did_submit = True
            yield
        # 2秒待機後、送信フラグをリセット
        await asyncio.sleep(2)
        self.did_submit = False
        yield

    # データベースからエントリをリストアップする関数
    def list_entries(self):
        """
        データベースからエントリをリストアップし、entriesに格納します。
        """
        with rx.session() as session:
            entries = session.exec(select(ContactEntryModel)).all()
            self.entries = entries
