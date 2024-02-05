from sqlalchemy import Integer, Column, BigInteger, String, sql, BOOLEAN
from asyncpg import UniqueViolationError
import random
from tgbot.services.db_api.db_gino import TimedBaseModel


class Proxy(TimedBaseModel):
    __tablename__ = 'proxy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    proxy = Column(String(100))
    login = Column(String(100))
    password = Column(String(100))

    query: sql.Select

    @staticmethod
    async def add_proxy(proxy: str, login: str, password: str):
        try:
            proxy = Proxy(proxy=proxy, login=login, password=password)
            await proxy.create()

        except UniqueViolationError:
            pass

    @staticmethod
    async def select_random_proxy():
        proxy = random.choice(await Proxy.query.gino.all())
        return {'proxy': proxy.proxy,
                'login': proxy.login,
                'password': proxy.password}

    @staticmethod
    async def select_proxy(id: int):
        user = await Proxy.query.where(Proxy.id == id).gino.first()
        return user

    @staticmethod
    async def delete_proxy(proxy: str):
        await Proxy.delete.where((Proxy.proxy == proxy)).gino.scalar()


class Token(TimedBaseModel):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(320))
    email = Column(String(100))

    query: sql.Select

    @staticmethod
    async def add_token(token: str, email: str):
        try:
            token = Token(token=token, email=email)
            await token.create()

        except UniqueViolationError:
            pass

    @staticmethod
    async def select_random_token():
        token = random.choice(await Token.query.gino.all())
        return token.token, token.email

    @staticmethod
    async def select_token(email: int):
        user = await Token.query.where(Token.email == email).gino.first()
        return user

    @staticmethod
    async def delete_token(email: str):
        await Token.delete.where((Token.email == email)).gino.scalar()




class ModePrompt(TimedBaseModel):
    __tablename__ = 'prompt'
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(50))
    name_mode = Column(String(100))
    prompt = Column(String(4096))

    query: sql.Select

    @staticmethod
    async def add_prompt(label: str, prompt: str, name_mode: str):
        try:
            prompt = ModePrompt(label=label, prompt=prompt, name_mode=name_mode)
            await prompt.create()

        except UniqueViolationError:
            pass


    @staticmethod
    async def select_all():
        prompts = [(i.label, i.prompt, i.name_mode) for i in await ModePrompt.query.gino.all()]
        return prompts

    @staticmethod
    async def delete_prompt(label: str):
        await ModePrompt.delete.where((ModePrompt.label == label)).gino.scalar()
