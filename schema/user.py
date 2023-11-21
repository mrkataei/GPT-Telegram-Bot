from pydantic import BaseModel

# Shared properties


class UserBase(BaseModel):
    chat_id: str
    is_superuser: bool = False
    toekn: int = 20
    referral_code: str
    invite_link: str
    score: int = 0

# Properties to receive via API on creation


class UserCreate(UserBase):
    username: str
    first_name: str
# Properties to receive via API on update


class UserUpdate(UserBase):
    requests: int
