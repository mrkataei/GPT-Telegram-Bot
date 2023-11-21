from pydantic import BaseModel

# Shared properties


class SubscribeBase(BaseModel):
    channel_id: str

# Properties to receive via API on creation


class SubscribeCreate(SubscribeBase):
    channel_id: str

# Properties to receive via API on update


class SubscribeUpdate(SubscribeBase):
    pass
