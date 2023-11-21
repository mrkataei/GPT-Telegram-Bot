from pydantic import BaseModel

# Shared properties
class OpenAIBase(BaseModel):
    api: str
    email: str
    chat_id: str
# Properties to receive via API on creation
class OpenAICreate(OpenAIBase):
    pass
# Properties to receive via API on update
class OpenAIUpdate(OpenAIBase):
    status : str
