# -*- coding: utf-8 -*-

from aiogram.utils.callback_data import CallbackData

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.services.lang_translate import _





def get_refactor_inline_keyboards(db_msg_id):
    refactor_msg = InlineKeyboardMarkup(row_width=2)

    short = InlineKeyboardButton(text=_("➡️Короче⬅️"),
                                 callback_data=f'edit:{db_msg_id}:short')
    refactor_msg.insert(short)

    long = InlineKeyboardButton(text=_("⬅️Длиннее➡️"),
                                callback_data=f'edit:{db_msg_id}:long')
    refactor_msg.insert(long)

    prof = InlineKeyboardButton(text=_("🤓Профессиональнее🤓"),
                                callback_data=f'edit:{db_msg_id}:prof')
    refactor_msg.insert(prof)

    simple = InlineKeyboardButton(text=_("🤷‍♂️Проще🤷‍♂️"),
                                  callback_data=f'edit:{db_msg_id}:simple')

    refactor_msg.insert(simple)

    return refactor_msg
