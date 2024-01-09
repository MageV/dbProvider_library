from abc import ABC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from models.role import Role
from abstract.wrapper import AbstractWrapper


class RoleWrapper(AbstractWrapper, ABC):

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def select(self, **kwargs):
        results = None
        lresult = list()
        if kwargs != {}:
            if kwargs.keys().__contains__("id"):
                async with self.session() as _session:
                    async with _session.begin():
                        stmt = select(Role).filter(Role.id == kwargs["id"])
                        results = await _session.execute(stmt)
            elif kwargs.keys().__contains__("name"):
                async  with self.session() as _session:
                    async  with _session.begin():
                        stmt = select(Role).filter(Role.name == kwargs["name"])
                        results = await _session.execute(stmt)
        else:
            async with self.session() as _session:
                async  with _session.begin():
                    stmt = select(Role).filter(Role.active == 1)
                    results = await _session.execute(stmt)
        if results is not None:
            for result in results.scalars():
                lresult.append(result.serialize())
        return lresult

    async def update(self, **kwargs):
        async  with self.session() as _session:
            async with _session.begin():
                result = await _session.execute(select(Role).filter(Role.id == kwargs["id"]))
                updatable: Role = result.scalars().one()
                if kwargs.keys().__contains__("name"):
                    updatable.name = kwargs["name"]
                if kwargs.keys().__contains__("operations"):
                    updatable.operations = kwargs["operations"]
                if kwargs.keys().__contains__("active"):
                    updatable.active = kwargs["active"]
                await _session.commit()

    async def insert(self, roles: list):
        def create_writeable(item) -> Role:
            role: Role = Role()
            role.deserialize(item)
            return role

        async with self.session() as _session:
            async with _session.begin():
                _session.add_all(map(create_writeable, roles))
                await _session.commit()

    async def delete(self, row_id):
        async with self.session() as _session:
            async with _session.begin():
                result = await _session.execute(select(Role).filter(Role.id == row_id))
                updatable: Role = result.scalars().one()
                updatable.active = 0
                await _session.commit()
