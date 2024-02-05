# -*- coding: utf-8 -*-
from tgbot.services.lang_translate import _

import logging

from aiogram import Dispatcher
from aiogram.types import Update



async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """
    from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                          CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                          MessageTextIsEmpty, RetryAfter,
                                          CantParseEntities, MessageCantBeDeleted, BadRequest, MessageIsTooLong)

    if isinstance(exception, CantDemoteChatCreator):
        await Update.get_current().message.answer(_('Произошла внутренняя ошибка, попробуйте позже! '))

        logging.exception(f'CantDemoteChatCreator: {exception} \nUpdate: {update}')
        return True


    if isinstance(exception, MessageIsTooLong):
        await Update.get_current().message.answer(_('Длина ответа превышает лимиты Telegram, попробуйте другой запрос'))

        logging.exception(f'MessageIsTooLong: {exception} \nUpdate: {update}')



    if isinstance(exception, MessageNotModified):
        await Update.get_current().message.answer(_('Произошла ошибка, попробуйте позже! '))

        logging.exception(f'MessageNotModified: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        await Update.get_current().message.answer(_('Произошла ошибка, попробуйте позже!'))

        logging.exception(f'MessageCantBeDeleted: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        await Update.get_current().message.answer(_('Произошла ошибка, попробуйте позже! '))

        logging.exception(f'MessageToDeleteNotFound: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        await Update.get_current().message.answer(_('Произошла ошибка, попробуйте позже! '))

        logging.exception(f'MessageTextIsEmpty: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, Unauthorized):
        await Update.get_current().message.answer(_('Произошла ошибка, попробуйте позже! '))

        logging.exception(f'Unauthorized: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, InvalidQueryID):
        await Update.get_current().message.answer(_('Произошла ошибка, попробуйте позже! '))

        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')

        await Update.get_current().message.answer(_('Произошла ошибка c форматированием ответа, попробуйте другой запрос!'))
        return True

    if isinstance(exception, RetryAfter):
        await Update.get_current().message.answer(_('Произошла ошибка на стороне Telegram, попробуйте позже! '))

        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, BadRequest):
        await Update.get_current().message.answer(_('Произошла ошибка на стороне Telegram, попробуйте позже!'))

        logging.exception(f'BadRequest: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, TelegramAPIError):
        await Update.get_current().message.answer(_('Произошла ошибка с TelegramAPI, попробуйте позже!'))

        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    logging.exception(f'Update: {update} \n{exception}')


def register_error_bot(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)
