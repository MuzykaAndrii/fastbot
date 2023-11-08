from pydantic import BaseModel, Field

class MessageEntity(BaseModel):
    offset: int
    length: int
    type: str

class MessageFrom(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str = ''
    username: str
    language_code: str

class MessageChat(BaseModel):
    id: int
    first_name: str
    username: str
    type: str

class Message(BaseModel):
    message_id: int
    from_user: MessageFrom = Field(alias="from")
    chat: MessageChat
    date: int
    text: str
    entities: list[MessageEntity]

class TgBotResponse(BaseModel):
    update_id: int
    message: Message