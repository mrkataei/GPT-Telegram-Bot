from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func

from db.base_class import Base


class UsedOffer(Base):
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String(15), ForeignKey('user.chat_id'))
    code = Column(String(5), ForeignKey('offer.code'))
    date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, chat_id: str, code: str) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.code = code

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
