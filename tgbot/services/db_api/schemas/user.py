from sqlalchemy import Integer, Column, BigInteger, String, sql, BOOLEAN
from asyncpg import UniqueViolationError

from tgbot.services.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, unique=True)
    username = Column(String(100))
    is_premium = Column(BOOLEAN())
    language_code = Column(String(5))
    full_name = Column(String(150))
    prime = Column(BOOLEAN())
    referal = Column(String(50))
    chat_id = Column(BigInteger)
    count_query = Column(Integer)
    query: sql.Select

    @staticmethod
    async def add_user(tg_id: int, username: str, is_premium: bool, language_code: str, full_name: str, prime: bool,
                       referal: str, chat_id: int, count_query: int):
        try:
            user = User(tg_id=tg_id, username=username, is_premium=is_premium, language_code=language_code,
                        full_name=full_name, prime=prime, referal=referal, chat_id=chat_id, count_query=count_query)
            await user.create()

        except UniqueViolationError:
            pass

    @staticmethod
    async def add_count_one(tg_id: int):
        await User.update.values(count_query=User.count_query + 1).where(User.tg_id == tg_id).gino.status()

    @staticmethod
    async def get_last_change(tg_id: int):
        user = await User.query.where(User.tg_id == tg_id).gino.first()
        return user.updated_at

    @staticmethod
    async def clear_counter(tg_id: int):
        await User.update.values(count_query=0).where(User.tg_id == tg_id).gino.status()

    @staticmethod
    async def set_language(tg_id: int, language: str):
        await User.update.values(language_code=language).where(User.tg_id == tg_id).gino.status()



    @staticmethod
    async def select_all_users():
        users = await User.query.gino.all()
        return users

    @staticmethod
    async def select_user(tg_id: int):
        user = await User.query.where(User.tg_id == tg_id).gino.first()
        return user

    @staticmethod
    async def select_user_referal(referal: str):
        user = await User.query.where(User.referal == referal).gino.all()
        return len(user)

    @staticmethod
    async def delete_user(chat_id: str):
        await User.delete.where((User.chat_id == chat_id)).gino.scalar()



    # @staticmethod
    # async def count_users():
    #     total = await db.func.count(User.id).gino.scalar()
    #     return total
    @staticmethod
    async def update_prime(tg_id, prime):
        user = await User.get(tg_id)
        await user.update(prime=prime).apply()








class UserAllForStat(TimedBaseModel):
    __tablename__ = 'users_stat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, unique=True)
    username = Column(String(100))
    is_premium = Column(BOOLEAN())
    language_code = Column(String(5))
    full_name = Column(String(150))
    prime = Column(BOOLEAN())
    referal = Column(String(50))
    chat_id = Column(BigInteger)
    count_query = Column(BigInteger)
    query: sql.Select

    @staticmethod
    async def add_user(tg_id: int, username: str, is_premium: bool, language_code: str, full_name: str, prime: bool,
                       referal: str, chat_id: int, count_query: int):
        try:
            user = UserAllForStat(tg_id=tg_id, username=username, is_premium=is_premium, language_code=language_code,
                        full_name=full_name, prime=prime, referal=referal, chat_id=chat_id, count_query=count_query)
            await user.create()

        except UniqueViolationError:
            pass

    @staticmethod
    async def add_count_one(tg_id: int):
        await UserAllForStat.update.values(count_query=UserAllForStat.count_query + 1).where(UserAllForStat.tg_id == tg_id).gino.status()

    @staticmethod
    async def get_last_change(tg_id: int):
        user = await UserAllForStat.query.where(UserAllForStat.tg_id == tg_id).gino.first()
        return user.updated_at

    @staticmethod
    async def clear_counter(tg_id: int):
        await UserAllForStat.update.values(count_query=0).where(UserAllForStat.tg_id == tg_id).gino.status()



    @staticmethod
    async def select_all_users():
        users = await UserAllForStat.query.gino.all()
        return users

    @staticmethod
    async def select_user(tg_id: int):
        user = await UserAllForStat.query.where(UserAllForStat.tg_id == tg_id).gino.first()
        return user

    @staticmethod
    async def select_user_referal(referal: str):
        user = await UserAllForStat.query.where(UserAllForStat.referal == referal).gino.all()
        return len(user)

    @staticmethod
    async def delete_user(chat_id: str):
        await UserAllForStat.delete.where((UserAllForStat.chat_id == chat_id)).gino.scalar()



    @staticmethod
    async def update_prime(tg_id, prime):
        user = await UserAllForStat.get(tg_id)
        await user.update(prime=prime).apply()
