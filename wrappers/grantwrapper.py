import logging
from abc import ABC

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from models.grant import Grant
from models.role import Role
from wrappers.abstract_wrapper import AbstractWrapper


class GrantWrapper(AbstractWrapper, ABC):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def select(self, **kwargs):
        results = None
        lresult = list()
        if kwargs != {}:
            if kwargs.keys().__contains__("id"):
                async with self.session() as _session:
                    async with _session.begin():
                        stmt = select(Grant).filter(Grant.id == kwargs["id"])
                        results = await _session.execute(stmt)
            elif kwargs.keys().__contains__("task_id"):
                async  with self.session() as _session:
                    async  with _session.begin():
                        stmt = select(Grant).filter(Grant.task_id == kwargs["task_id"])
                        results = await _session.execute(stmt)
            elif kwargs.keys().__contains__("user_id"):
                async  with self.session() as _session:
                    async  with _session.begin():
                        stmt = select(Grant).filter(Grant.user_id == kwargs["user_id"])
                        results = await _session.execute(stmt)

        else:
            async with self.session() as _session:
                async  with _session.begin():
                    stmt = select(Grant)
                    results = await _session.execute(stmt)
        if results is not None:
            for result in results.scalars():
                lresult.append(result.serialize())
        return lresult
        pass

    async def update(self, **kwargs):
        pass

    async def insert(self, grants):
        def create_writable(item) -> Grant:
            grant: Grant = Grant()
            grant.deserialize(item)
            return grant

        async with self.session() as _session:
            async with _session.begin():
                _session.add_all(map(create_writable, grants))
            await _session.commit()
#            try:
#                await _session.commit()
#            except Exception as ex:
#                logging.log("Unique constraint error.Rollback")
#                await _session.rollback()


    async def delete(self, row_id):
        async with self.session() as _session:
            async with _session.begin():
                await _session.execute(delete(Grant).filter(Grant.id == row_id))
                await _session.commit()

    async def delete_ext(self, task_id=None, user_id=None):
        async with self.session() as _session:
            async with _session.begin():
                if task_id is not None and user_id is not None:
                    await _session.execute(
                        delete(Grant).filter((Grant.task_id == task_id and Grant.user_id == user_id)))
                elif task_id is None and user_id is not None:
                    await _session.execute(
                        delete(Grant).filter(Grant.user_id == user_id))
                elif task_id is not None and user_id is None:
                    await _session.execute(
                        delete(Grant).filter(Grant.task_id == task_id))
                await _session.commit()
