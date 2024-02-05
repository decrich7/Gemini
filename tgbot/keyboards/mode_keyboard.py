# -*- coding: utf-8 -*-

from aiogram.utils.callback_data import CallbackData

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.services.lang_translate import _


def offers_kb(posts, n):
    offers_kb = InlineKeyboardMarkup()
    for i in range(n - 5, len(posts)):
        if i >= n or i > len(posts):
            break
        else:
            cur = InlineKeyboardButton(posts[i][-1], callback_data=posts[i][0])
            offers_kb.add(cur)
    if n <= 5 and n >= len(posts):
        cancel = InlineKeyboardButton(_("❎Cancel❎"), callback_data="cancel_offers")
        offers_kb.row(cancel)
    elif n == 5:
        forward = InlineKeyboardButton(_("⏩Вперед⏩"), callback_data="forward_offers")
        cancel = InlineKeyboardButton(_("❎Cancel❎"), callback_data="cancel_offers")
        offers_kb.row(forward)
        offers_kb.row(cancel)
    elif n >= len(posts):
        back = InlineKeyboardButton(_("⏪Назад⏪"), callback_data="back_offers")
        cancel = InlineKeyboardButton(_("❎Cancel❎"), callback_data="cancel_offers")
        offers_kb.row(back)
        offers_kb.row(cancel)
    else:
        forward = InlineKeyboardButton(_("⏩Вперед⏩"), callback_data="forward_offers")
        back = InlineKeyboardButton(_("⏪Назад⏪"), callback_data="back_offers")
        cancel = InlineKeyboardButton(_("❎Cancel❎"), callback_data="cancel_offers")
        offers_kb.row(back, forward)
        offers_kb.row(cancel)
    return offers_kb


#
# # Команда /start для инициализации интерфейса меню
# @dp.message_handler(Command('start'))
# async def start_menu(message: types.Message):
#     await message.answer('Выберите категорию блюд:', reply_markup=create_keyboard())
#
#
# # Обработка нажатий на кнопки
# @dp.callback_query_handler(lambda c: c.data == 'prev_page' or c.data == 'next_page')
# async def paginate_callback_handler(query: types.CallbackQuery):
#     global current_page
#
#     # Обработчик кнопки "Назад"
#     if query.data == 'prev_page':
#         current_page -= 1
#     # Обработчик кнопки "Вперед"
#     elif query.data == 'next_page':
#         current_page += 1
#
#     # Обновляем сообщение с новой клавиатурой
#     await query.message.edit_reply_markup(reply_markup=create_keyboard())


finish_mode = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❎Выйти из режима❎", callback_data='finish_mode')
    ]
])

mode = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Суммаризатор текста", callback_data="mode_text"),
        InlineKeyboardButton(text="Толкователь снов", callback_data="mode:sleep"),
        InlineKeyboardButton(text="Диетолог", callback_data="mode_dietolog"),
        InlineKeyboardButton(text="Программист", callback_data="mode_developer"),
        InlineKeyboardButton(text="Астролог", callback_data="mode:astrolog")
    ]
])
