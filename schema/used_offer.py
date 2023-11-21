from pydantic import BaseModel

# Shared properties


class UsedOfferBase(BaseModel):
    chat_id: str
    code: str

# Properties to receive via API on creation


class UsedOfferCreate(UsedOfferBase):
    pass
# Properties to receive via API on update


class UsedOfferUpdate(UsedOfferBase):
    pass
