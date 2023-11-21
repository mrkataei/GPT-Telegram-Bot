from crud.base import CRUDBase
from models.message import Message
from schema.message import MessageCreate, MessageUpdate
from sqlalchemy.orm import Session
from typing import List


class CRUDMessage(CRUDBase[Message, MessageUpdate, MessageUpdate]):
    def create(self, db: Session, *, obj_in: MessageCreate) -> Message:
        db_obj = self.model(
            chat_id=obj_in.chat_id,
            message_id=obj_in.message_id,
            text=obj_in.text,
            role=obj_in.role
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_multi(self, db: Session, *, obj_in: List[MessageCreate]):
        blucks = []
        for obj in obj_in:
            blucks.append(
                self.model(
                    chat_id=obj.chat_id,
                    message_id=obj.message_id,
                    text=obj.text,
                    role=obj.role
                )
            )
        db.add_all(blucks)
        db.commit()

    def get_by_message_id(self, db: Session, *, message_id: str, chat_id: str) -> List[Message]:
        return db.query(self.model).filter(self.model.message_id == message_id , self.model.chat_id == chat_id).all()


message = CRUDMessage(Message)
