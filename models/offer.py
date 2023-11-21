from sqlalchemy import Column, String, DateTime, Float, Boolean
from datetime import datetime, timedelta
from db.base_class import Base
import string, random


class Offer(Base):
    code = Column(String(5), unique=True, primary_key=True)
    expire_date = Column(DateTime)
    discount = Column(Float)
    is_active = Column(Boolean(), default=True)
    
    @staticmethod
    def generate_offer_code() -> str:
        letters = string.ascii_uppercase
        return ''.join(random.choice(letters) for _ in range(5))
    
    @staticmethod
    def generate_expire_date(days: int) -> datetime:
        return datetime.now() + timedelta(days=days)

    def __init__(self,discount: float, days: int) -> None:
        super().__init__()
        self.code = self.generate_offer_code()
        self.expire_date = self.generate_expire_date(days)
        self.discount = discount
        
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
