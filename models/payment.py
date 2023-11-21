from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Float
from sqlalchemy.sql import func

from db.base_class import Base


class Payment(Base):
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String(15), ForeignKey('user.chat_id'))
    amount = Column(Float)
    authority = Column(String(60), unique=True)

    transaction_date = Column(DateTime(timezone=True),
                              server_default=func.now())

    def __init__(self, chat_id: str, amount: float, authority: str) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.amount = amount
        self.authority = authority

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
