from pydantic import BaseModel

# Shared properties
class OfferBase(BaseModel):
    days: int
    discount: int
# Properties to receive via API on creation
class OfferCreate(OfferBase):
    pass
# Properties to receive via API on update
class OfferUpdate(OfferBase):
    is_active: bool
