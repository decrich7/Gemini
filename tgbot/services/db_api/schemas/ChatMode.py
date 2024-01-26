from sqlalchemy import select, update, delete, ForeignKey

from sqlalchemy import Integer, Column, BigInteger, String, sql, BOOLEAN
from asyncpg import UniqueViolationError
from sqlalchemy.orm import relationship

from tgbot.services.db_api.db_gino import TimedBaseModel
from tgbot.services.db_api.schemas.user import User


class Chat(TimedBaseModel):
    __tablename__ = 'chats'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_tg_id = Column(BigInteger)
    messages = relationship('ChatMessages', backref='chat', cascade='all, delete')
    query: sql.Select

    async def add_chat(user_tg_id: int):
        try:
            chat = await Chat.create(user_tg_id=user_tg_id)
            return chat.id

        except UniqueViolationError:
            pass

    async def select_chat(id: int):
        chat = await Chat.query.where((Chat.id == id)).gino.first()
        return chat

    async def select_chats_user(user_tg_id: int):
        chat = await Chat.query.where((Chat.user_tg_id == user_tg_id)).gino.first()
        return chat

    async def delete_chat(id: int):
        await Chat.delete.where((Chat.id == id)).gino.scalar()


class ChatMessages(TimedBaseModel):
    __tablename__ = 'chat_messages'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    role = Column(String(7))
    text = Column(String(4096))

    query: sql.Select

    @staticmethod
    async def add_msg(chat_id: int, role: str, text: str):
        try:
            chat = await ChatMessages.create(role=role, text=text, chat_id=chat_id)
            return chat.id

        except UniqueViolationError:
            pass

    @staticmethod
    async def select_msg_chat(chat_id: int):
        msgs = await ChatMessages.query.where((ChatMessages.chat_id == chat_id)).gino.all()
        return msgs

    @staticmethod
    async def delete_messages(chat_id: int):
        await ChatMessages.delete.where((ChatMessages.chat_id == chat_id)).gino.scalar()
