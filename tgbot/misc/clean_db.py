from datetime import datetime, timedelta
from sqlalchemy.sql import delete, select

from tgbot.services.db_api.schemas.ChatMode import ChatMessages, Chat
from tgbot.services.db_api.schemas.MessageEdit import MessageEdit


async def clean_message_edit():
    one_day_ago = datetime.now() - timedelta(days=2)

    await MessageEdit.delete.where(MessageEdit.created_at < one_day_ago).gino.scalar()
    # delete_query = delete(MessageEdit).where(MessageEdit.created_at < one_day_ago)


async def clean_chats_and_msg_chats():
    one_day_ago = datetime.now() - timedelta(days=2)
    # await Chat.delete_chat(id_chat.get('id_chat'))
    # await ChatMessages.delete_messages(id_chat.get('id_chat'))
    await ChatMessages.delete.where(ChatMessages.created_at < one_day_ago).gino.scalar()
    await Chat.delete.where(Chat.created_at < one_day_ago).gino.scalar()






