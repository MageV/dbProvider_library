from abc import ABC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from models.apptask import AppTask
from abstract.wrapper import AbstractWrapper


class AppTaskWrapper(AbstractWrapper, ABC):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def select(self, **kwargs):
        results = None
        lresult = list()
        if kwargs!={}:
            if kwargs.keys().__contains__("id"):
                async with self.session() as _session:
                    async with _session.begin():
                        stmt = select(AppTask).filter(AppTask.id == kwargs["id"])
                        results = await _session.execute(stmt)
            elif kwargs.keys().__contains__("name"):
                async  with self.session() as _session:
                    async  with _session.begin():
                        stmt = select(AppTask).filter(AppTask.name == kwargs["name"])
                        results = await _session.execute(stmt)
        else:
            async with self.session() as _session:
                async  with _session.begin():
                    stmt = select(AppTask).filter(AppTask.active == 1)
                    results = await _session.execute(stmt)
        if results is not None:
            for result in results.scalars():
                lresult.append(result.serialize())
        return lresult

    async def update(self, **kwargs):
        async  with self.session() as _session:
            async with _session.begin():
                result = await _session.execute(select(AppTask).filter(AppTask.id == kwargs["id"]))
                updatable: AppTask = result.scalars().one()
                if kwargs.keys().__contains__("name"):
                    updatable.name = kwargs["name"]
                if kwargs.keys().__contains__("active"):
                    updatable.active = kwargs["active"]
            await _session.commit()

    async def insert(self, apptasks):
        async with self.session() as _session:
            async with _session.begin():
                for item in apptasks:
                    writable_task=AppTask()
                    writable_task.deserialize(item)
                    #writable_task.id=None
                    _session.add(writable_task)
                await _session.commit()

    async def delete(self, row_id):
        async with self.session() as _session:
            async with _session.begin():
                result = await _session.execute(select(AppTask).filter(AppTask.id == row_id))
                updatable: AppTask = result.scalars().one()
                updatable.active = 0
                await _session.commit()

