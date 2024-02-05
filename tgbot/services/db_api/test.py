# -*- coding: utf-8 -*-


import asyncio
import datetime
import time

from tgbot.services.db_api.db_gino import db
from tgbot.services.db_api.schemas.MessageEdit import MessageEdit
from tgbot.services.db_api.schemas.data import Token, Proxy
from tgbot.services.db_api.schemas.user import User


async def test():
    await db.set_bind('postgresql://postgres:24651asd@127.0.0.1/gemini_bot')
    await db.gino.drop_all()
    await db.gino.create_all()

    await User.add_user(tg_id=778981429, username='dfgdfg', is_premium=True, language_code='gf', full_name='dfgdfg', prime=False, referal='xxx', chat_id=778981429, count_query=0)
    await User.add_user(tg_id=37452, username='dfgdfg', is_premium=True, language_code='gf', full_name='dfgdfg', prime=False, referal='xxx1', chat_id=778981429, count_query=0)
    await User.add_user(tg_id=34751, username='dfgdfg', is_premium=True, language_code='gf', full_name='dfgdfg', prime=False, referal='xxx', chat_id=778981429, count_query=0)
    await User.add_user(tg_id=5543, username='dfgdfg', is_premium=True, language_code='gf', full_name='dfgdfg', prime=False, referal='xxx', chat_id=778981429, count_query=0)

    await User.add_count_one(778981429)
    await User.add_count_one(778981429)
    await User.add_count_one(778981429)
    await User.clear_counter(778981429)

    print(await User.get_last_change(778981429))
    user: User = await User.select_user(778981429)
    time.sleep(20)
    time_difference = datetime.datetime.now() - user.updated_at
    print(time_difference.seconds)
    if time_difference.days >= 1:
        print("----------------------------------------")
    else:
        print("Прошло менее суток с последнего обновления.")

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
import re

# Ваш исходный текст
