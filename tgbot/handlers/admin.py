# -*- coding: utf-8 -*-
import asyncio
from aiogram.utils.exceptions import RetryAfter, BotBlocked
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from tgbot.misc.states import AdminState
from tgbot.services.db_api.schemas.data import Token, Proxy, ModePrompt
from tgbot.services.db_api.schemas.user import User


async def admin_start(message: Message):
    await message.reply('''Здарова админ\n
    Команды:\n
    1. Добавить Токен - /add_token\n\n
    2. Удалить Токен - /del_token\n\n
    3. Добавить Прокси - /add_proxy\n\n
    4. Удалить Прокси - /del_proxy\n\n
    5. Добавить Промпт - /add_prompt\n\n
    6. Удалить Промпт - /del_prompt\n\n
    7. Посчитать кол-во пользователей c рефералки - /count_referal\n\n
    8. Рассылка сообщения - /mass_post\n\n
    9. Файл с подписчиками - /get_file_tg\n\n
    10. Начать рассылку с определенного id - /mass_post_id\n\n
    11. Кол-во всех пользователей - /count_all

    ''')


async def admin_add_token(message: Message, state: FSMContext):
    await AdminState.token_add.set()

    await message.reply('''скинь токен в формате \n
    токен|Почта''')


async def admin_add_token2(message: Message, state: FSMContext):
    token, email = message.text.split('|')
    try:
        await Token.add_token(token, email)
        await message.answer('''Токен добавлен''')

    except Exception as e:
        await message.answer(f'Ошибка добавления токена: {e}')

    await state.finish()


async def admin_del_token(message: Message, state: FSMContext):
    await AdminState.token_del.set()

    await message.reply('''скинь email токена в формате ''')


async def admin_del_token2(message: Message, state: FSMContext):
    email = message.text
    try:
        await Token.delete_token(email)
        await message.answer('''Токен удален''')

    except Exception as e:
        await message.answer(f'Ошибка удаления токена: {e}')

    await state.finish()


async def admin_add_proxy(message: Message, state: FSMContext):
    await AdminState.proxy_add.set()

    await message.reply('''скинь proxy в формате \n
    proxy|login|password''')


async def admin_add_proxy2(message: Message, state: FSMContext):
    proxy, login, password = message.text.split('|')
    try:
        await Proxy.add_proxy(proxy, login, password)
        await message.answer('''Proxy добавлен''')

    except Exception as e:
        await message.answer(f'Ошибка добавления proxy: {e}')

    await state.finish()


async def admin_del_proxy(message: Message, state: FSMContext):
    await AdminState.proxy_del.set()

    await message.reply('''скинь proxy чтобы удалить''')


async def admin_del_proxy2(message: Message, state: FSMContext):
    proxy = message.text
    try:
        await Proxy.delete_proxy(proxy)
        await message.answer('''Proxy удален''')

    except Exception as e:
        await message.answer(f'Ошибка удаления Proxy: {e}')

    await state.finish()


async def admin_add_prompt(message: Message, state: FSMContext):
    await AdminState.prompt_add.set()

    await message.reply('''скинь prompt в формате \n
    label|prompt|name_mode''')


async def admin_add_prompt2(message: Message, state: FSMContext):
    label, prompt, name_mode = message.text.split('|')
    try:
        await ModePrompt.add_prompt(label, prompt, name_mode)
        await message.answer('''Prompt добавлен''')

    except Exception as e:
        await message.answer(f'Ошибка добавления prompt: {e}')

    await state.finish()


async def admin_del_prompt(message: Message, state: FSMContext):
    await AdminState.prompt_del.set()

    await message.reply('''скинь label чтобы удалить''')


async def admin_del_prompt2(message: Message, state: FSMContext):
    label = message.text
    try:
        await ModePrompt.delete_prompt(label)
        await message.answer('''Prompt удален''')

    except Exception as e:
        await message.answer(f'Ошибка удаления Prompt: {e}')

    await state.finish()


async def admin_count_referal(message: Message, state: FSMContext):
    await AdminState.count_referal.set()

    await message.reply('''скинь referal''')


async def admin_count_all_users(message: Message, state: FSMContext):
    all_user = await User.select_all_users()

    await message.reply(len(all_user))


async def admin_count_referal2(message: Message, state: FSMContext):
    referal = message.text
    try:
        count_user = await User.select_user_referal(referal)
        await message.answer(count_user)

    except Exception as e:
        await message.answer(f'Ошибка подсчета referal: {e}')

    await state.finish()


async def admin_mass_post(message: Message, state: FSMContext):
    args = message.text.split(' ')
    if len(args) == 2:
        await state.update_data(id=int(args[-1]))
    await AdminState.mass_post.set()

    is_button = InlineKeyboardMarkup(row_width=2)

    short = InlineKeyboardButton(text="Да",
                                 callback_data=f'button_yes')
    is_button.insert(short)

    long = InlineKeyboardButton(text="Нет",
                                callback_data=f'button_no')
    is_button.insert(long)

    long = InlineKeyboardButton(text="Отмена",
                                callback_data=f'button_cancel')
    is_button.insert(long)

    await message.reply('''Выбери наличие клавиатуры в сообщении''', reply_markup=is_button)


async def admin_mass_post_button(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    text = call.data.split('_')[-1]
    if text == 'no':
        await call.message.answer('Перешлите сообщение(клавиатуры нет)')
    elif text == 'cancel':
        await call.message.answer('Выход')
        await state.finish()
    else:
        await call.message.answer(
            'Напиши клавиатуру в формате -\nКнопка 1-https://test.com|Кнопка 2-https://test.com')
        await AdminState.mass_post_button.set()


async def admin_mass_post_create_button(message: Message, state: FSMContext):
    # inline_keyboard_markup = InlineKeyboardMarkup(row_width=1)
    #
    # buttons_info = message.text.split("|")
    # for button_info in buttons_info:
    #     button_text, button_link = button_info.split("-")
    #     inline_keyboard_markup.add(InlineKeyboardButton(text=button_text, url=button_link))
    await AdminState.mass_post.set()
    await state.update_data(button=message.text)
    await message.reply('''Перешли сообщение''')


async def send_message(message: Message, from_chat_id, message_id, chat_id, keyboard=None):
    try:
        await message.bot.copy_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id,
                                       reply_markup=keyboard)

    except RetryAfter as e:
        await asyncio.sleep(e.timeout)
        return await message.bot.copy_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id,
                                              reply_markup=keyboard)
    except BotBlocked as e:
        await User.delete_user(chat_id)
    except Exception as e:
        await message.bot.send_message(from_chat_id, f'Ошибка отправки сообщения - {e}')

    else:
        return True

    return False


async def admin_mass_post2(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("button") is None:
        inline_keyboard_markup = None
    else:
        inline_keyboard_markup = InlineKeyboardMarkup(row_width=1)

        buttons_info = data.get("button").split("|")
        for button_info in buttons_info:
            button_text, button_link = button_info.split("-")
            inline_keyboard_markup.add(InlineKeyboardButton(text=button_text, url=button_link))

    await message.bot.copy_message(from_chat_id=message.chat.id, chat_id=message.chat.id,
                                   message_id=message.message_id)

    count_send = 0
    id_last = 0
    if data.get("id") is not None:
        pass
    all_user = await User.select_all_users()
    # print(all_user)
    try:
        for user_id in all_user:
            id_last = user_id.tg_id
            if await send_message(message, from_chat_id=message.chat.id, message_id=message.message_id,
                                  chat_id=user_id.chat_id, keyboard=inline_keyboard_markup):
                count_send += 1
            await asyncio.sleep(0.07)

    finally:
        await message.answer(f'Всего пользователей в базе - {len(all_user)}\n'
                             f'Отправленно - {count_send}\n'
                             f'Последний id в базе - {all_user[-1].tg_id}\n'
                             f'Рассылка закончилась на - {id_last}\n')

    await state.finish()




async def admin_get_file_user_id(message: Message, state: FSMContext):
    all_user = await User.select_all_users()
    all_user = [str(i.tg_id) for i in all_user]
    with open('user_id.txt', 'w') as f:
        f.write('\n'.join(all_user))

    await message.answer_document(open("user_id.txt", "rb"))






def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["admin"], state="*", is_admin=True)

    dp.register_message_handler(admin_add_token, commands=["add_token"], state="*", is_admin=True)
    dp.register_message_handler(admin_add_token2, state=AdminState.token_add, is_admin=True)
    dp.register_message_handler(admin_del_token, commands=["del_token"], state="*", is_admin=True)
    dp.register_message_handler(admin_del_token2, state=AdminState.token_del, is_admin=True)

    dp.register_message_handler(admin_add_proxy, commands=["add_proxy"], state="*", is_admin=True)
    dp.register_message_handler(admin_add_proxy2, state=AdminState.proxy_add, is_admin=True)
    dp.register_message_handler(admin_del_proxy, commands=["del_proxy"], state="*", is_admin=True)
    dp.register_message_handler(admin_del_proxy2, state=AdminState.proxy_del, is_admin=True)

    dp.register_message_handler(admin_add_prompt, commands=["add_prompt"], state="*", is_admin=True)
    dp.register_message_handler(admin_add_prompt2, state=AdminState.prompt_add, is_admin=True)
    dp.register_message_handler(admin_del_prompt, commands=["del_prompt"], state="*", is_admin=True)
    dp.register_message_handler(admin_del_prompt2, state=AdminState.prompt_del, is_admin=True)

    dp.register_message_handler(admin_count_referal, commands=["count_referal"], state="*", is_admin=True)
    dp.register_message_handler(admin_count_referal2, state=AdminState.count_referal, is_admin=True)

    dp.register_message_handler(admin_mass_post, commands=["mass_post"], state="*", is_admin=True)
    dp.register_callback_query_handler(admin_mass_post_button, state=AdminState.mass_post, text_startswith="button")
    dp.register_message_handler(admin_mass_post_create_button, state=AdminState.mass_post_button, is_admin=True)
    dp.register_message_handler(admin_get_file_user_id, commands=["get_file_tg"], state='*', is_admin=True)

    dp.register_message_handler(admin_mass_post2, state=AdminState.mass_post, is_admin=True,
                                content_types=ContentType.ANY)

    dp.register_message_handler(admin_count_all_users, commands=["count_all"], state="*", is_admin=True)

