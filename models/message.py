from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.sql import func

from db.base_class import Base


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String(15), ForeignKey('user.chat_id'))
    message_id = Column(String(15))
    role = Column(String(15))
    text = Column(Text())
    create_on = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, chat_id: str, message_id: str, text: str, role: str) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.message_id = message_id
        self.text = text
        self.role = role

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
