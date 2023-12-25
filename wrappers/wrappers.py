from abc import ABC

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from models.apptask import AppTask
from models.grant import Grant
from models.role import Role
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

    async def insert(self, users: dict):
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

    async def insert(self, roles):
        async with self.session() as _session:
            async with _session.begin():
                _session.add_all(roles)
                await _session.commit()

    async def delete(self, row_id):
        async with self.session() as _session:
            async with _session.begin():
                result = await _session.execute(select(Role).filter(Role.id == row_id))
                updatable: Role = result.scalars().one()
                updatable.active = 0
                await _session.commit()


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

    async def insert(self, apptasks):
        async with self.session() as _session:
            async with _session.begin():
                _session.add_all(apptasks)
                await _session.commit()

    async def delete(self, row_id):
        async with self.session() as _session:
            async with _session.begin():
                result = await _session.execute(select(AppTask).filter(AppTask.id == row_id))
                updatable: AppTask = result.scalars().one()
                updatable.active = 0
                await _session.commit()


class GrantWrapper(AbstractWrapper, ABC):
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def select(self, **kwargs):
        results = None
        lresult = list()
        if kwargs !={}:
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
                    stmt = select(Grant).filter(Role.active == 1)
                    results = await _session.execute(stmt)
        if results is not None:
            for result in results.scalars():
                lresult.append(result.serialize())
        return lresult
        pass

    async def update(self, **kwargs):
        pass

    async def insert(self, grants):
        async with self.session() as _session:
            async with _session.begin():
                _session.add_all(grants)
                await _session.commit()

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
