# -*- coding: utf-8 -*-


from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.db_api.schemas.user import User


async def new_user(message: Message):
    # await User.add_user(tg_id=message.from_user.id, username=message.from_user.username,
    #                     is_premium=message.from_user.is_premium,
    #                     language_code=message.from_user.language_code,
    #                     full_name=message.from_user.full_name, prime=False)
    print(message.from_user)
    print('-----------------------------------------------------------------------------------------------------------')

    await message.answer('Привет!\n'
                         'Мы рады что вы проявили интерес к боту Gemini AI, но он пока находится в разработке\n'
                         'Через 2-3 недели он будет стабильно и быстро работать, также он будет бесплатным\n'
                         'Ждем вас снова!')


def register_user(dp: Dispatcher):
    dp.register_message_handler(new_user, is_new=True)
