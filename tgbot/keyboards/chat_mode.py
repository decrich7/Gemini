# -*- coding: utf-8 -*-

from aiogram.utils.callback_data import CallbackData
from tgbot.services.lang_translate import _

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




finish_chat = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=_("❎Завершить чат❎"), callback_data='finish_chat')
    ]
])


def get_refactor_inline_keyboards(db_msg_id):
    refactor_msg = InlineKeyboardMarkup(row_width=2)

    short = InlineKeyboardButton(text="c",
                                 callback_data=f'edit:{db_msg_id}:short')
    refactor_msg.insert(short)

    long = InlineKeyboardButton(text="⬅️Длиннее➡️",
                                callback_data=f'edit:{db_msg_id}:long')
    refactor_msg.insert(long)

    prof = InlineKeyboardButton(text="🥸Профессиональнее🥸",
                                callback_data=f'edit:{db_msg_id}:prof')
    refactor_msg.insert(prof)

    simple = InlineKeyboardButton(text="🤷‍♂️Проще🤷‍♂️",
                                  callback_data=f'edit:{db_msg_id}:simple')

    refactor_msg.insert(simple)

    return refactor_msg