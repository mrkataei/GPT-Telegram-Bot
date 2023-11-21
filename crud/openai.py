from crud.base import CRUDBase
from models.openai import OpenAI, StatusEnum
from schema.openai import OpenAICreate, OpenAIUpdate
from sqlalchemy.orm import Session


class CRUDOpenAI(CRUDBase[OpenAI, OpenAIUpdate, OpenAICreate]):
    def create(self, db: Session, *, obj_in: OpenAICreate) -> OpenAI:
        db_obj = self.model(api=obj_in.api, email=obj_in.email,
                            chat_id=obj_in.chat_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
    def update_status(self, db: Session, db_obj: OpenAI, status: StatusEnum) -> OpenAI:
        db_obj.status = status
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, api: str) -> OpenAI:
        return db.query(self.model).filter(self.model.api == api).first()
    
    def get_first_active(self, db: Session) -> OpenAI:   
        apis = super().get_multi(db=db)
        for api in apis:
            if api.status == StatusEnum.ACTIVE:
                return api
            
    def remove(self, db: Session, email: str)-> OpenAI:
        obj = db.query(self.model).filter(self.model.email == email).first()
        db.delete(obj)
        db.commit()
        return obj


API = CRUDOpenAI(OpenAI)
