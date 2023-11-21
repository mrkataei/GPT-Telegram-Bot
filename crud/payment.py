from crud.base import CRUDBase
from models.payment import Payment
from schema.payment import PaymentCreate, PaymentUpdate
from sqlalchemy.orm import Session


class CRUDPayment(CRUDBase[Payment, PaymentUpdate, PaymentCreate]):
    def create(self, db: Session, *, obj_in: PaymentCreate) -> Payment:
        db_obj = self.model(
            chat_id=obj_in.chat_id,
            amount=obj_in.amount,
            authority=obj_in.authority
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_chat_id_auth(self, db: Session, *, chat_id: str, authority: str) -> Payment:
        return db.query(self.model).filter(self.model.chat_id == chat_id , self.model.authority == authority).all()


payment = CRUDPayment(Payment)
