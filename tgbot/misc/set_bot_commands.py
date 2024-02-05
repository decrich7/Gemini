# -*- coding: utf-8 -*-


from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота или перезагрузить"),
        types.BotCommand("chat", "Режим чата(бот будет запоминать сообщения)"),
        # types.BotCommand("settings", "Настройки безопасности"),
        types.BotCommand("mode", "Выбор Режима бота"),

    ])