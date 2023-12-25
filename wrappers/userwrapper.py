from abc import ABC

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from models.user import User
from wrappers.abstract_wrapper import AbstractWrapper


class UserWrapper(AbstractWrapper, ABC):

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def select(self, **kwargs):
        results = None
        lresult = list()
        if kwargs != {}:
            if kwargs.keys().__contains__("id"):
                async with self.session() as _session:
                    async with _session.begin():
                        stmt = select(User).filter(User.id == (kwargs["id"]))
                        results = await _session.execute(stmt)
            elif kwargs.keys().__contains__("name"):
                async  with self.session() as _session:
                    async  with _session.begin():
                        stmt = select(User).filter(User.teleg_id == (kwargs["name"]))
                        results = await _session.execute(stmt)
            elif kwargs.keys().__contains__("username"):
                async  with self.session() as _session:
                    async  with _session.begin():
                        stmt = select(User).filter(User.teleg_id == (kwargs["username"]))
                        results = await _session.execute(stmt)
        else:
            async with self.session() as _session:
                async  with _session.begin():
                    stmt = select(User)
                    results = await _session.execute(stmt)
        if results is not None:
            for result in results.scalars():
                lresult.append(result.serialize())
        return lresult

    async def update(self, **kwargs):
        async  with self.session() as _session:
            async with _session.begin():
                result = await _session.execute(select(User).filter(User.id == kwargs["id"]))
                updatable: User = result.scalars().one()
                if kwargs.keys().__contains__("name"):
                    updatable.teleg_id = kwargs["teleg_id"]
                if kwargs.keys().__contains__("mail"):
                    updatable.mail = kwargs["mail"]
                if kwargs.keys().__contains__("role_id"):
                    updatable.role_id = kwargs["role_id"]
                if kwargs.keys().__conains__("username"):
                    updatable.username = kwargs["username"]
                await _session.commit()

    async def insert(self, users: list):
        async with self.session() as _session:
            async with _session.begin():
                for item in users:
                    writable_user = User()
                    writable_user.deserialize(item)
                    writable_user.id = None
                    _session.add(writable_user)
                await _session.commit()

    async def delete(self, row_id):
        async with self.session() as _session:
            async with _session.begin():
                await _session.execute(delete(User).filter(User.id == row_id))
                await _session.commit()
