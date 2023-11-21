from pydantic import BaseModel

# Shared properties


class PaymentBase(BaseModel):
    chat_id: str
    amount: float
    authority: str

# Properties to receive via API on creation


class PaymentCreate(PaymentBase):
    pass

# Properties to receive via API on update


class PaymentUpdate(PaymentBase):
    pass
