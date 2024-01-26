# -*- coding: utf-8 -*-
from aiogram.dispatcher import FSMContext

from tgbot.misc.throttling import rate_limit
from tgbot.services.db_api.schemas.user import User
from aiogram import Dispatcher
from aiogram.types import Message



@rate_limit(2)
async def help_bot(message: Message, state: FSMContext):
    # await User.add_user(tg_id=message.from_user.id, username=message.from_user.username,
    #                     is_premium=message.from_user.is_premium,
    #                     language_code=message.from_user.language_code,
    #                     full_name=message.from_user.full_name, prime=False)

    # await state.finish()
    # print(message.message_id)
    # print(message)

    await message.answer('Помощь\n'
                         'Команды которые я поддерживаю\n'
                         '/mode - Выбор Режима бота\n'
                         '/chat - Режим чата(бот будет запоминать сообщения)\n'
                         '<strong>Если бот перестал отвечать, для перезагрузки нажмите</strong> - /start')


def register_help_bot(dp: Dispatcher):
    dp.register_message_handler(help_bot, commands=["help"], state='*')
