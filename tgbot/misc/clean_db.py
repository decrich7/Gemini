from datetime import datetime, timedelta

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.sql import delete, select
from aiogram.dispatcher import FSMContext

from tgbot.services.db_api.schemas.ChatMode import ChatMessages, Chat
from tgbot.services.db_api.schemas.MessageEdit import MessageEdit
from tgbot.services.db_api.schemas.user import User


async def clean_message_edit():
    one_day_ago = datetime.now() - timedelta(days=2)

    await MessageEdit.delete.where(MessageEdit.created_at < one_day_ago).gino.scalar()
    # delete_query = delete(MessageEdit).where(MessageEdit.created_at < one_day_ago)


async def clean_chats_and_msg_chats(storage):
    one_day_ago = datetime.now() - timedelta(days=2)

    # await ChatMessages.delete.where(ChatMessages.created_at < one_day_ago).gino.scalar()
    # await Chat.delete.where(Chat.created_at < one_day_ago).gino.scalar()
    all = await User.select_all_users()
    for i in all:
        state = FSMContext(storage, chat=i.tg_id, user=i.chat_id)
        await state.finish()
    await ChatMessages.delete.where(ChatMessages.created_at < one_day_ago).gino.scalar()
    await Chat.delete.where(Chat.created_at < one_day_ago).gino.scalar()


async def clean_count_query_users():
    await User.update.values(count_query=0).gino.status()
