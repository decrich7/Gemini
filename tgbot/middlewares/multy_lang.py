from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types

from tgbot.services.db_api.schemas.user import User


async def get_lang(user_id):
    # Делаем запрос к базе, узнаем установленный язык
    user = await User.select_user(user_id)
    if user:
        # Если пользователь найден - возвращаем его
        return user.language_code


class ACLMiddleware(I18nMiddleware):
    # Каждый раз, когда нужно узнать язык пользователя - выполняется эта функция
    async def get_user_locale(self, action, args):
        user = types.User.get_current()
        lang_for_db = await get_lang(user.id)
        loc = user.locale
        if user.locale != 'ru' and user.locale != 'en':
            loc = 'en'

        if lang_for_db != 'ru' and lang_for_db != 'en':
            lang_for_db = 'en'
        # Возвращаем язык из базы ИЛИ (если не найден) - язык из Телеграма
        return lang_for_db or loc


