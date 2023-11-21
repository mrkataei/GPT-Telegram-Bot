from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.user import User
from schema.user import UserCreate, UserUpdate
import os 

EXCHANGE_SCORE = int(os.getenv("EXCHANGE_SCORE"))
TOKEN_REWARD = int(os.getenv("TOKEN_REWARD"))

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_chat_id(self, db: Session, *, chat_id: str) -> User:
        return db.query(self.model).filter(self.model.chat_id == chat_id).first()

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = self.model(
            chat_id=obj_in.chat_id,
            username=obj_in.username,
            first_name=obj_in.first_name,
            invite_link=obj_in.invite_link,
            referral_code=obj_in.referral_code
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def use_token(self, db: Session, *, chat_id: str, value: int, score: int = 0) -> User:
        user = db.query(self.model).filter(
            self.model.chat_id == chat_id).first()
        user.token -= value
        user.requests += value
        if score > 0 :
            user.score += score
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def update_score(self, db: Session, *, chat_id: str, score: int) -> User:
        user = db.query(self.model).filter(self.model.chat_id == chat_id).first()
        user.score += score
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def exchange_score(self, db: Session, *, chat_id: str, score: int) -> User:
        user = db.query(self.model).filter(self.model.chat_id == chat_id).first()
        if score > user.score:
            return None
        token = int(score // EXCHANGE_SCORE) * TOKEN_REWARD
        if token < 1:
            return None
        
        user.score -= int(score // EXCHANGE_SCORE) * EXCHANGE_SCORE
        user.token += token
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def charge_token(self, db: Session, *, chat_id: str, value: int) -> User:
        user = db.query(self.model).filter(
            self.model.chat_id == chat_id).first()
        user.token += value
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_link(self, db: Session, *, chat_id: str, referral_code: str, invite_link: str) -> User:
        user = db.query(self.model).filter(
            self.model.chat_id == chat_id).first()
        if user:
            user.referral_code = referral_code
            user.invite_link = invite_link
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    def get_by_referral(self, db: Session, *, referral_code: str) -> User:
        return db.query(self.model).filter(self.model.referral_code == referral_code).first()

    def has_token(self, *, db_oj: User, token: int = 0) -> bool:
        if token == 0: # it is free command
            return True
        return False if db_oj.token - token < 0  else True

    def is_admin(self, db: Session, *, chat_id: str) -> bool:
        user = db.query(self.model).filter(
            self.model.chat_id == chat_id).first()
        return True if user and user.is_superuser else False


user = CRUDUser(User)
