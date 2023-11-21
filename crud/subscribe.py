from crud.base import CRUDBase
from models.subscribe import Subscribe
from schema.subscribe import SubscribeCreate, SubscribeUpdate
from sqlalchemy.orm import Session
from typing import List


class CRUDSubscribe(CRUDBase[Subscribe, SubscribeCreate, SubscribeUpdate]):
    def create(self, db: Session, *, obj_in: SubscribeCreate) -> Subscribe:
        db_obj = self.model(
            channel_id=obj_in.channel_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_multi(self, db: Session, *, obj_in: List[SubscribeCreate]):
        blucks = []
        for obj in obj_in:
            blucks.append(self.model(channel_id=obj.channel_id))
        db.add_all(blucks)
        db.commit()

    def get_channels(self, db: Session) -> List[Subscribe]:
        return db.query(self.model).all()

    def get(self, db: Session, *, channel_id: str) -> Subscribe:
        return db.query(self.model).filter(self.model.channel_id == channel_id).first()


subscribe = CRUDSubscribe(Subscribe)
