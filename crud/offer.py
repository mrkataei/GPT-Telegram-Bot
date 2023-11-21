from crud.base import CRUDBase
from models.offer import Offer
from schema.offer import OfferCreate, OfferUpdate
from sqlalchemy.orm import Session
from datetime import datetime


class CRUDOffer(CRUDBase[Offer, OfferUpdate, OfferCreate]):
    def create(self, db: Session, *, obj_in: OfferCreate) -> Offer:
        db_obj = self.model(discount=obj_in.discount,
                            days=obj_in.days)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
    def update_active(self, db: Session, db_obj: Offer, is_active: bool) -> Offer:
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, code: str) -> Offer:
        obj = db.query(self.model).filter(self.model.code == code).first()
        if obj and obj.expire_date >= datetime.now() and obj.is_active:
            return obj
        else:
            return None
            
    


OFF = CRUDOffer(Offer)
