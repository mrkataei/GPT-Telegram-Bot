from sqlalchemy import Boolean, Column, String, DateTime, Integer
from sqlalchemy.sql import func

from db.base_class import Base


class User(Base):
    chat_id = Column(String(15), index=True, unique=True, primary_key=True)
    is_superuser = Column(Boolean(), default=False)
    signup_date = Column(DateTime(timezone=True), server_default=func.now())
    requests = Column(Integer, default=0)
    token = Column(Integer, default=20)
    score = Column(Integer, default=0)
    username = Column(String(70), default=None)
    first_name = Column(String(70), default=None)
    referral_code = Column(String, unique=True, default=None)
    invite_link = Column(String, unique=True, default=None)

    def __init__(self, chat_id: str, username: str, first_name: str, referral_code: str, invite_link: str) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.username = username
        self.first_name = first_name
        self.referral_code = referral_code
        self.invite_link = invite_link

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
