# -*- coding: utf-8 -*-



from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import ChatActions
import datetime
from tgbot.keyboards.chat_mode import finish_chat
from tgbot.keyboards.mode_keyboard import mode, finish_mode, offers_kb
from tgbot.misc.states import Mode
from tgbot.misc.throttling import rate_limit
from tgbot.services.db_api.schemas.ChatMode import Chat, ChatMessages
from tgbot.services.db_api.schemas.MessageEdit import MessageEdit
import logging
from tgbot.keyboards.inline_mode_msg import get_refactor_inline_keyboards
from tgbot.services.Gemini_TextInput import main_text_input
from tgbot.services.Gemini_ChatInput import main_chat_input
from tgbot.services.db_api.schemas.data import ModePrompt
from tgbot.services.db_api.schemas.user import User
from tgbot.services.lang_translate import _


# @rate_limit(3, key='chat')
# async def send_chat_model_chat(message: types.Message):
#     await message.answer('Чат уже начат, если вы хотите выйти из режима чата, то нажмите на кнопку завершить чат',
#                          reply_markup=finish_chat)


@rate_limit(3, key='mode')
async def start_model_mode(message: types.Message, state: FSMContext):
    await message.answer_chat_action(ChatActions.TYPING)

    user: User = await User.select_user(message.from_user.id)
    if user is None:
        await User.add_user(tg_id=message.from_user.id, username=message.from_user.username,
                            is_premium=message.from_user.is_premium,
                            language_code=message.from_user.language_code,
                            full_name=message.from_user.full_name, prime=False,
                            referal=None, chat_id=message.chat.id, count_query=0)
        user: User = await User.select_user(message.from_user.id)
    time_difference = datetime.datetime.now() - user.updated_at

    if user.count_query > 35 and time_difference.days <= 1:
        logging.info(f'Превысил лимит пользователь - {message.from_user.username}')
        await message.answer(_('🥺 Похоже вы достигли лимита запросов на сегодня, попробуйте через 24 часа😚\n'
                             '🥸Мы предоставляем самые большие <strong>БЕСПЛАТНЫЕ</strong> лимиты в телеграм\n'
                             'Но не можем их совсем убрать из за угрозы атаки злоумышленников😞'))
        return
    elif time_difference.days >= 1:
        await User.clear_counter(message.from_user.id)
        await User.add_count_one(message.from_user.id)

    else:
        await User.add_count_one(message.from_user.id)

    list_mode = await ModePrompt.select_all()
    await message.answer(_('🦾 Выберите режим в котором будет работать бот:'),
                         reply_markup=offers_kb(list_mode, 5))

    await Mode.mode.set()
    id = await Chat.add_chat(user_tg_id=message.from_user.id)
    await state.update_data(
        {"id_chat": id,
         'cur_list': 5}
    )


async def offers_process(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data1 = call.data.replace("_offers", "")
    if data1 == "forward":
        _cur_list = data.get("cur_list") + 5
    elif data1 == "back":
        _cur_list = data.get("cur_list") - 5

    else:
        await state.finish()
        await call.message.delete()
        return

    list_mode = await ModePrompt.select_all()

    await state.update_data(cur_list=_cur_list)  # вносим новый индекс
    await call.message.edit_reply_markup(offers_kb(list_mode,
                                                   _cur_list))  # и для плавности работы не переотправляем сообщение, а просто изменяем уже отправленное сообщение


async def start_prompt_model(call: CallbackQuery, state: FSMContext):
    await call.message.answer_chat_action(ChatActions.TYPING)




    # await call.message.edit_text(_('Подождите...'))
    list_mode = await ModePrompt.select_all()

    # await call.answer(cache_time=60)
    id_chat = await state.get_data()

    prompt = call.data.split(':')[-1]

    for subarray in list_mode:
        if subarray[0] == prompt:
            prompt = subarray[1]
            mode_name = subarray[-1]
            break

    await ChatMessages.add_msg(chat_id=id_chat.get('id_chat'), role='user', text=prompt)
    # start_prompt = [{'user': prompt}]
    # params = {
    #     'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
    #     'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
    #     'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
    #     'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
    #     'temperature': 0.5
    #
    # }



    # text_model = await main_chat_input(start_prompt, params=params)

    await ChatMessages.add_msg(chat_id=id_chat.get('id_chat'), role='model', text='ok')
    await call.message.edit_text(_('Режим: <strong>{mode_name}</strong> включен!').format(mode_name=mode_name),
                                 reply_markup=finish_mode)

    await Mode.change_mode.set()

    # await call.message.answer('Чат завершен')


@rate_limit(3, key='msg')
async def answer_model_mode(message: types.Message, state: FSMContext):
    await message.answer_chat_action(ChatActions.TYPING)

    user: User = await User.select_user(message.from_user.id)
    if user is None:
        await User.add_user(tg_id=message.from_user.id, username=message.from_user.username,
                            is_premium=message.from_user.is_premium,
                            language_code=message.from_user.language_code,
                            full_name=message.from_user.full_name, prime=False,
                            referal=None, chat_id=message.chat.id, count_query=0)
        user: User = await User.select_user(message.from_user.id)

    time_difference = datetime.datetime.now() - user.updated_at

    if user.count_query > 35 and time_difference.days <= 1:
        logging.info(f'Превысил лимит пользователь - {message.from_user.username}')
        await message.answer(_('🥺 Похоже вы достигли лимита запросов на сегодня, попробуйте через 24 часа😚\n'
                               '🥸Мы предоставляем самые большие <strong>БЕСПЛАТНЫЕ</strong> лимиты в телеграм\n'
                               'Но не можем их совсем убрать из за угрозы атаки злоумышленников😞'))
        await state.finish()
        return
    elif time_difference.days >= 1:
        await User.clear_counter(message.from_user.id)
        await User.add_count_one(message.from_user.id)

    else:
        await User.add_count_one(message.from_user.id)



    stiker = await message.answer_sticker('CAACAgIAAxkBAAEDLTlluSyxd49nDKFLl8umFD_0086lXQACkhYAAnU0OErf-3hMDWEWtDQE')

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
    await stiker.delete()
    await message.answer(text_model,
                            reply_markup=finish_chat)


async def finish_mode_callback(call: CallbackQuery, state: FSMContext):
    await call.message.answer(_('Вы вышли из режима'))

    await call.answer(cache_time=60)
    # await call.message.answer('Чат завершен')
    # print(call.data)
    id_chat = await state.get_data()

    await Chat.delete_chat(id_chat.get('id_chat'))
    await ChatMessages.delete_messages(id_chat.get('id_chat'))

    await state.finish()


def register_mode(dp: Dispatcher):
    # dp.register_message_handler(bot_echo_all, state="*", is_admin=True)
    dp.register_message_handler(start_model_mode, commands=['mode'])
    dp.register_callback_query_handler(start_prompt_model, state=Mode.mode, text_startswith="mode")
    dp.register_callback_query_handler(offers_process, state=Mode.mode, text_endswith="_offers")
    dp.register_message_handler(answer_model_mode, state=Mode.change_mode)

    dp.register_callback_query_handler(finish_mode_callback, state=Mode.change_mode)
