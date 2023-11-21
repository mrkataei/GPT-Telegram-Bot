from pydantic import BaseModel

# Shared properties


class MessageBase(BaseModel):
    chat_id: str
    message_id: str
    text: str
    role: str

# Properties to receive via API on creation


class MessageCreate(MessageBase):
    pass
# Properties to receive via API on update


class MessageUpdate(MessageBase):
    pass
