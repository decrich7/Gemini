from sqlalchemy import select, update, delete

from sqlalchemy import Integer, Column, BigInteger, String, sql, BOOLEAN
from asyncpg import UniqueViolationError

from tgbot.services.db_api.db_gino import TimedBaseModel


class MessageEdit(TimedBaseModel):
    __tablename__ = 'message_edit'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger)
    msg_id = Column(BigInteger)
    user_promt = Column(String(4096))
    work = Column(BOOLEAN())
    query: sql.Select

    @staticmethod
    async def add_msg(tg_id: int, user_promt: str, work: bool, msg_id: int):
        try:
            msg = MessageEdit(tg_id=tg_id, user_promt=user_promt,
                               msg_id=msg_id, work=work)
            await msg.create()

        except UniqueViolationError:
            pass

    @staticmethod
    async def select_msg(tg_id: int, msg_id:int):
        msg = await MessageEdit.query.where((MessageEdit.tg_id == tg_id) | (MessageEdit.msg_id == msg_id)).gino.first()
        return msg

    @staticmethod
    async def delete_all():
        await MessageEdit.delete.gino.scalar()


    # async def count_users():
    #     total = await db.func.count(User.id).gino.scalar()
    #     return total
    @staticmethod
    async def delete_msg(tg_id: int, msg_id: int):
        await MessageEdit.delete.where((MessageEdit.tg_id == tg_id) | (MessageEdit.msg_id == msg_id)).gino.scalar()
