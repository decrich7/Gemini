# -*- coding: utf-8 -*-


from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import ChatActions
import logging
from tgbot.keyboards.chat_mode import finish_chat
from tgbot.misc.states import ChatMode
from tgbot.misc.throttling import rate_limit
from tgbot.services.db_api.schemas.ChatMode import Chat, ChatMessages
from tgbot.services.db_api.schemas.MessageEdit import MessageEdit
import datetime
from tgbot.keyboards.inline_mode_msg import get_refactor_inline_keyboards
from tgbot.services.Gemini_TextInput import main_text_input
from tgbot.services.Gemini_ChatInput import main_chat_input
from tgbot.services.db_api.schemas.user import User


@rate_limit(3, key='chat')
async def send_chat_model_chat(message: types.Message):
    await message.answer('Чат уже начат, если вы хотите выйти из режима чата, то нажмите на кнопку завершить чат',
                         reply_markup=finish_chat)


@rate_limit(3, key='chat')
async def start_model_chat(message: types.Message, state: FSMContext):
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

    await message.answer('Теперь вы можете отправлять боту сообщения и он будет их запоминать🤓\n'
                         'И вести с вами диалог🙃',
                         reply_markup=finish_chat)

    await ChatMode.chat.set()
    id = await Chat.add_chat(user_tg_id=message.from_user.id)
    await state.update_data(
        {"id_chat": id}
    )


@rate_limit(3, key='msg')
async def answer_model_chat(message: types.Message, state: FSMContext):
    await message.answer_chat_action(ChatActions.TYPING)

    # user = await User.select_user(message.from_user.id)
    id_chat = await state.get_data()
    # chat = await Chat.select_chat(id_chat.get('id_chat'))
    await ChatMessages.add_msg(chat_id=id_chat.get('id_chat'), role='user', text=message.text)
    msgs = await ChatMessages.select_msg_chat(id_chat.get('id_chat'))
    list_answers = [{i.role: i.text} for i in msgs]
    params = {
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
        'temperature': 0.3

    }

    text_model = await main_chat_input(list_answers, params=params)

    await ChatMessages.add_msg(chat_id=id_chat.get('id_chat'), role='model', text=text_model)

    await message.answer(text_model,
                         reply_markup=finish_chat)


async def finish_chat_callback(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer('Чат завершен')
    id_chat = await state.get_data()

    await Chat.delete_chat(id_chat.get('id_chat'))
    await ChatMessages.delete_messages(id_chat.get('id_chat'))

    await state.finish()


def register_chat_mode(dp: Dispatcher):
    # dp.register_message_handler(bot_echo_all, state="*", is_admin=True)
    dp.register_message_handler(start_model_chat, commands=['chat'])
    dp.register_message_handler(send_chat_model_chat, commands=['chat'], state="*")

    dp.register_message_handler(answer_model_chat, state=ChatMode.chat)

    dp.register_callback_query_handler(finish_chat_callback, state=ChatMode.chat)
