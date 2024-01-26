# -*- coding: utf-8 -*-

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
        await Update.get_current().message.answer(f'Произошла ошибка, попробуйте позже! CantDemoteChatCreator: {exception.args}')

        logging.debug("Can't demote chat creator")
        return True


    if isinstance(exception, MessageIsTooLong):
        await Update.get_current().message.answer(f'Длинна ответа превышает лимиты Telegram, попробуйте другой запрос')

        logging.debug('Message is not modified')



    if isinstance(exception, MessageNotModified):
        await Update.get_current().message.answer(f'Произошла ошибка, попробуйте позже! MessageNotModified: {exception.args}')

        logging.debug('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        await Update.get_current().message.answer(f'Произошла ошибка, попробуйте позже! MessageCantBeDeleted: {exception.args}')

        logging.info('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        await Update.get_current().message.answer(f'Произошла ошибка, попробуйте позже! MessageToDeleteNotFound: {exception.args}')

        logging.info('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        await Update.get_current().message.answer(f'Произошла ошибка, попробуйте позже! MessageTextIsEmpty: {exception.args}')

        logging.debug('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        await Update.get_current().message.answer(f'Произошла ошибка, попробуйте позже! Unauthorized: {exception.args}')

        logging.info(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        await Update.get_current().message.answer(f'Произошла ошибка, попробуйте позже! InvalidQueryID: {exception.args}')

        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')

        await Update.get_current().message.answer(f'Произошла ошибка, попробуйте позже! CantParseEntities: {exception.args}')
        return True

    if isinstance(exception, RetryAfter):
        await Update.get_current().message.answer(f'Произошла ошибка, попробуйте позже! RetryAfter: {exception.args}')

        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, BadRequest):
        await Update.get_current().message.answer(f'Произошла ошибка, попробуйте позже! BadRequest: {exception.args}')

        logging.exception(f'BadRequest: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, TelegramAPIError):
        await Update.get_current().message.answer(f'Произошла ошибка, попробуйте позже! TelegramAPIError: {exception.args}')

        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    logging.exception(f'Update: {update} \n{exception}')


def register_error_bot(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)
