# -*- coding: utf-8 -*-
import logging

from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
import datetime
from tgbot.misc.throttling import rate_limit
from tgbot.services.db_api.schemas.MessageEdit import MessageEdit
from sulguk import SULGUK_PARSE_MODE
from aiogram.types import ChatActions

from tgbot.keyboards.inline_mode_msg import get_refactor_inline_keyboards
from tgbot.services.Gemini_TextInput import main_text_input
from tgbot.services.Gemini_ChatInput import main_chat_input
from tgbot.services.db_api.schemas.user import User


@rate_limit(3, key='msg')
async def answer_model_base(message: types.Message):
    await message.answer_chat_action(ChatActions.TYPING)

    user: User = await User.select_user(message.from_user.id)
    time_difference = datetime.datetime.now() - user.updated_at

    if user.count_query > 7 and time_difference.seconds <= 200:
        logging.info(f'Превысил лимит пользователь - {message.from_user.username}')
        await message.answer('🥺 Похоже вы достигли лимита запросов на сегодня, попробуйте через 24 часа😚\n'
                             '🥸Мы предоставляем самые большие <strong>БЕСПЛАТНЫЕ</strong> лимиты в телеграм\n'
                             'Но не можем их совсем убрать из за угрозы атаки злоумышленников😞')
        return
    elif time_difference.seconds >= 200:
        await User.clear_counter(message.from_user.id)
        await User.add_count_one(message.from_user.id)

    else:
        await User.add_count_one(message.from_user.id)



    print(message.text, message.from_user.username)
    params = {
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
        'temperature': 0.3

    }
    text = await main_text_input(message.text, params=params)
    await MessageEdit.add_msg(tg_id=message.from_user.id, user_promt=message.text, work=False,
                              msg_id=message.message_id)

    # text = '234'

    await message.answer(text,
                         reply_markup=get_refactor_inline_keyboards(db_msg_id=message.message_id))


@rate_limit(3)
async def buying_apples(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_text('Подождите...')

    type_refactor, id_msg = call.data.split(':')[2], int(call.data.split(':')[1])
    a = await MessageEdit.select_msg(call.message.from_user.id, id_msg)
    if a is None:
        await call.message.edit_text(
            '🤔 Похоже вы взаимодействуете со старым сообщением\nПопробуйте задать этот вопрос снова😊')
        return

    dict_value = {
        'short': 'Сделай ответ короче',
        'long': 'Сделай ответ длиннее',
        'prof': 'Сделай ответ более проффесиональным',
        'simple': 'Сделай ответ проще',

    }
    dict_chat_edit = [
        {'user': a.user_promt},
        {'model': call.message.text},
        {'user': dict_value[type_refactor]}
    ]
    resp = await main_chat_input(dict_chat_edit)
    await MessageEdit.delete_msg(call.message.from_user.id, id_msg)
    # print(type_refactor)

    # quantity = callback_data.get("quantity") parse_mode=SULGUK_PARSE_MODE
    await call.message.edit_text(resp)
    print(2222)


def register_base_mode(dp: Dispatcher):
    # dp.register_message_handler(bot_echo_all, state="*", is_admin=True)
    dp.register_callback_query_handler(buying_apples, text_contains="edit")
    dp.register_message_handler(answer_model_base)
