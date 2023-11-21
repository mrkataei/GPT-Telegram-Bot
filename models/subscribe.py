from sqlalchemy import Column, String, Integer

from db.base_class import Base


class Subscribe(Base):
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String(15), index=True, unique=True)

    def __init__(self, channel_id: str) -> None:
        super().__init__()
        self.channel_id = channel_id
