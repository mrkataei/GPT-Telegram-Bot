from crud.base import CRUDBase
from models.used_offer import UsedOffer
from schema.used_offer import UsedOfferCreate, UsedOfferUpdate
from sqlalchemy.orm import Session


class CRUDUsedOffer(CRUDBase[UsedOffer, UsedOfferUpdate, UsedOfferCreate]):
    def create(self, db: Session, *, obj_in: UsedOfferCreate) -> UsedOffer:
        db_obj = self.model(
            chat_id=obj_in.chat_id,
            code=obj_in.code
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, *, chat_id: str, code: str) -> UsedOffer:
        return db.query(self.model).filter(self.model.chat_id == chat_id , self.model.code == code).all()


Used = CRUDUsedOffer(UsedOffer)
