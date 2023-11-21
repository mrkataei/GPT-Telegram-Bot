from sqlalchemy import Column, String, ForeignKey, Enum
from enum import Enum as PythonEnum

from db.base_class import Base

class StatusEnum(PythonEnum):
    PENDING = 'Pending'
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    
class OpenAI(Base):
    api = Column(String(60), unique=True)
    email = Column(String(60), primary_key=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.ACTIVE, nullable=False)
    chat_id = Column(String(15), ForeignKey('user.chat_id'))
    
    def __init__(self, chat_id: str, api: str, email: float, status: StatusEnum = StatusEnum.ACTIVE) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.api = api
        self.email = email
        self.status = status
        
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
