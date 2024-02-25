# -*- coding: utf-8 -*-
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.lang import languages_markup
from tgbot.misc.throttling import rate_limit
from tgbot.services.db_api.schemas.user import User, UserAllForStat
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import decode_payload
from tgbot.services.lang_translate import _


@rate_limit(2, key='start')
async def start_bot(message: Message, state: FSMContext):
    args = message.text.split(' ')
    if len(args) == 2:
        await User.add_user(tg_id=message.from_user.id, username=message.from_user.username,
                            is_premium=message.from_user.is_premium,
                            language_code=message.from_user.language_code,
                            full_name=message.from_user.full_name, prime=False,
                            referal=args[-1], chat_id=message.chat.id, count_query=0)

        # await UserAllForStat.add_user(tg_id=message.from_user.id, username=message.from_user.username,
        #                     is_premium=message.from_user.is_premium,
        #                     language_code=message.from_user.language_code,
        #                     full_name=message.from_user.full_name, prime=False,
        #                     referal=args[-1], chat_id=message.chat.id, count_query=0)
    else:
        await User.add_user(tg_id=message.from_user.id, username=message.from_user.username,
                            is_premium=message.from_user.is_premium,
                            language_code=message.from_user.language_code,
                            full_name=message.from_user.full_name, prime=False,
                            referal=None, chat_id=message.chat.id, count_query=0)

        # await UserAllForStat.add_user(tg_id=message.from_user.id, username=message.from_user.username,
        #                     is_premium=message.from_user.is_premium,
        #                     language_code=message.from_user.language_code,
        #                     full_name=message.from_user.full_name, prime=False,
        #                     referal=None, chat_id=message.chat.id, count_query=0)
    await state.finish()
    # print(message.message_id)
    # print(message)

    await message.answer(_('🚀 Приветствую тебя!\n\n<strong>🤖 Я ПОЛНОСТЬЮ БЕСПЛАТНЫЙ ассистент, основанный на новейшем искусственном интеллекте Gemini от компании Google.</strong>\n\n<strong>Что я умею:\n</strong>    1. 📄 <i>Написание сочинений, эссэ, докладов на различные темы и в разных стиля</i>\n\n    2. 🌙 <i>Толкование снов</i>\n\n    3. 🔮 <i>Индивидуальный астрологический прогноз и составление нотальной карты</i>\n\n   4. 🤵‍♂ <i>Генерирование идей для стартапа</i>\n\n    5. 🎥 <i>Написание сценариев к Reels, TikTok, Shorts</i>\n    <strong>И многое другое!</strong>\n\n🌌 Встречай будущее прямо здесь и сейчас! 🌌\n\n🤓Чтобы узнать все возможности нажми - /help'))
    await message.answer(_('🤔 Выберите язык'), reply_markup=languages_markup)
    await message.answer(_('🤠<strong>Нажмите</strong> - /mode для выбора роли(<i>Астролог, Сценарист и т.д</i>)'))



# Альтернативно можно использовать фильтр text_contains, он улавливает то, что указано в call.data
async def change_language(call: CallbackQuery):
    await call.message.edit_reply_markup()
    # Достаем последние 2 символа (например ru)
    lang = call.data[-2:]

    await User.set_language(call.from_user.id, lang)

    # После того, как мы поменяли язык, в этой функции все еще указан старый, поэтому передаем locale=lang
    await call.message.answer(_("Ваш язык был изменен", locale=lang))


def register_start_bot(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start'], state='*')
    dp.register_callback_query_handler(change_language, text_contains="lang")
