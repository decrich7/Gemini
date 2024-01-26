# -*- coding: utf-8 -*-
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from sulguk import transform_html



import asyncio
import logging
from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config

from tgbot.filters.admin import AdminFilter, NewFilter
from tgbot.handlers.admin import register_admin
# from tgbot.handlers.echo import register_echo
from tgbot.handlers.base_mode import register_base_mode
from tgbot.handlers.chat_mode import register_chat_mode
from tgbot.handlers.error import register_error_bot
from tgbot.handlers.help import register_help_bot
from tgbot.handlers.mode import register_mode
from tgbot.handlers.new_users import register_user
from tgbot.handlers.start import register_start_bot
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.misc.clean_db import clean_message_edit,clean_chats_and_msg_chats
from tgbot.misc.set_bot_commands import set_default_commands
from tgbot.services.db_api import db, db_gino
from tgbot.services.db_api.schemas.data import Proxy, Token, ModePrompt
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.services.db_api.schemas.user import User

scheduler = AsyncIOScheduler()

logger = logging.getLogger(__name__)


def shedule_jobs():
    scheduler.add_job(clean_message_edit, "interval", hours=24)
    scheduler.add_job(clean_chats_and_msg_chats, "interval", hours=24)



def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(ThrottlingMiddleware())
    # dp.setup_middleware(LoggingMiddleware())

    # dp.setup_middleware(AiogramSulgukMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(NewFilter)

    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_error_bot(dp)
    register_help_bot(dp)
    # register_user(dp)
    # register_admin(dp)
    register_mode(dp)
    register_start_bot(dp)
    register_chat_mode(dp)

    register_base_mode(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        # filename="py_log.log"
    )
    # logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)

    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)

    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    await db_gino.on_startup(dp, config=config)
    print("Готово")

    print("Чистим базу")
    await db.gino.drop_all()



    print("Создаем таблицы")
    await db.gino.create_all()


    print("Потом удалить")

    await Proxy.add_proxy("http://45.4.197.124:8000", "8K58YN", '6km5bA')
    await Token.add_token('AIzaSyAMpQKMwsGXW_u03oPijFoaPQeIv4K_uKE', "pavel.boy4enko900@gmai.com")
    await ModePrompt.add_prompt("mode_astrolog", "Я хочу, чтобы вы выступили в роли астролога. Вы знаете все о знаках зодиака и их значении, понимаете положение планет и то, как они влияют на жизнь человека, сможете точно интерпретировать гороскопы и поделиться своими знаниями с теми, кто ищет совета или совета.", '🔮 Астролог 🔮')
    await ModePrompt.add_prompt("mode_sleep", "Я хочу, чтобы вы выступили в роли толкователя снов. Я опишу вам свои сны, а вы дадите толкования, основанные на символах и темах, присутствующих во сне. Не высказывайте личного мнения или предположений о сновидце. Предоставляйте только фактические интерпретации, основанные на предоставленной информации.", '🌌 Толкователь снов 🌌')
    await ModePrompt.add_prompt("mode_psychologist", "Я хочу, чтобы ты выступил психологом. я изложу вам свои мысли. Я хочу, чтобы вы дали мне научные рекомендации, которые помогут мне чувствовать себя лучше.", '👩‍🏫 Психолог 👩‍🏫')
    await ModePrompt.add_prompt("mode_contact", "Я хочу, чтобы вы выступили в роли тренера по отношениям. Я предоставлю некоторые подробности о двух людях, участвующих в конфликте, а ваша задача — высказать предложения о том, как они могут справиться с проблемами, которые их разделяют. Это может включать в себя советы по методам общения или различным стратегиям для улучшения понимания точек зрения друг друга.", '❤️ Коуч по отношениям ❤️')
    # await ModePrompt.add_prompt("mode_astrolog", "xc", '🔮 Програмист 🔮')
    await ModePrompt.add_prompt("mode_sum_text", "Я хочу, чтобы вы выступили в роли суммаризатора текста. Я напишу вам текст, а вы подведете его итог, используюя самые важные предложения, присутствующие в тексте.", '🧾 Суммаризатор текста 🧾')
    await ModePrompt.add_prompt("mode_startup", "Создавайте цифровые идеи для стартапов на основе пожеланий людей. Например, когда я говорю: «Хотел бы я, чтобы в моем маленьком городе был большой торговый центр», вы создаете бизнес-план для цифрового стартапа с названием идеи, краткой аннотацией, целевым персонажем пользователя, проблемами пользователя, которые нужно решить, основными ценностные предложения, каналы продаж и маркетинга, источники потока доходов, структуры затрат, основные виды деятельности, ключевые ресурсы, ключевые партнеры, этапы проверки идеи, расчетная стоимость эксплуатации в первый год и потенциальные бизнес-задачи, на которые следует обратить внимание. Запишите результат в таблицу уценки.", '🤵‍♂️ Генератор идей для стартапов 🤵‍♂️')
    await ModePrompt.add_prompt("mode_marketing", "Я хочу, чтобы вы выступили в роли специалиста по маркетингу. Предоставьте мне список потенциальных идей и стратегий маркетинговых кампаний, которые можно использовать для увеличения продаж и вовлечения клиентов. Ваши предложения должны быть конкретными, действенными и адаптированными для разных целевых аудиторий. Не предоставляйте подробных планов реализации, сосредоточьтесь на общей концепции и ключевых преимуществах.", '🧠 Идеи для Маркетинга 🧠')
    await ModePrompt.add_prompt("mode_etimolog", "Я хочу, чтобы вы выступили в роли этимолога. Я дам вам слово, и вы будете исследовать происхождение этого слова, прослеживая его до древних корней. Вы также должны предоставить информацию о том, как значение слова изменилось с течением времени, если применимо.", '👨‍🏫 Этимолог 👨‍🏫')
    # await ModePrompt.add_prompt("mode_astrolog", "xc", '🔮 Эксперт по написанию эссэ 🔮')
    await User.add_user(tg_id=778981429, username='dfgdfg', is_premium=True, language_code='gf', full_name='dfgdfg', prime=False, referal='xxx', chat_id=778981429, count_query=0)
    await User.add_user(tg_id=37452, username='dfgdfg',is_premium=True,language_code='gf',full_name='dfgdfg', prime=False, referal='xxx1', chat_id=778981429, count_query=0)
    await User.add_user(tg_id=34751, username='dfgdfg',is_premium=True,language_code='gf',full_name='dfgdfg', prime=False, referal='xxx', chat_id=778981429, count_query=0)
    await User.add_user(tg_id=5543, username='dfgdfg',is_premium=True,language_code='gf',full_name='dfgdfg', prime=False, referal='xxx', chat_id=778981429, count_query=0)





    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    shedule_jobs()
    scheduler.start()


    await set_default_commands(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
