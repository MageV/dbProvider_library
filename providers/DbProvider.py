from sqlalchemy import Table
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from appconfig.config import Base
from wrappers.grantwrapper import GrantWrapper
from wrappers.rolewrapper import RoleWrapper
from wrappers.taskwrapper import AppTaskWrapper
from wrappers.userwrapper import UserWrapper


class DbProvider:
    _user_role_view: Table
    _user_task_view: Table

    def __init__(self, connstr):
        self._connstr = connstr
        self._async_session = None
        self._user_wrapper = None
        self._role_wrapper = None
        self._apptask_wrapper = None
        self._grant_wrapper = None
        self._engine = create_async_engine(self._connstr, echo=True)
        self._entities = None

    async def create_engine(self) -> None:
        self._async_session = async_sessionmaker(self._engine, expire_on_commit=False)
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            self._user_role_view = await conn.run_sync(
                lambda cnn: Table('user_over_role', Base.metadata, autoload_with=cnn))
            self._user_task_view = await conn.run_sync(
                lambda cnn: Table('users_over_tasks_view', Base.metadata, autoload_with=cnn))
        self._user_wrapper: UserWrapper = UserWrapper(self._async_session)
        self._role_wrapper: RoleWrapper = RoleWrapper(self._async_session)
        self._apptask_wrapper: AppTaskWrapper = AppTaskWrapper(self._async_session)
        self._grant_wrapper: GrantWrapper = GrantWrapper(self._async_session)

    async def destroy_engine(self):
        async with self._async_session() as session:
            await session.close()

    # getters for table "users" wrapped on UsersWrapper & DB Views
    async def get_users(self, with_role=True):
        lresult = list()
        results = None
        async with self._async_session() as session:
            async with session.begin():
                stmt = self._user_role_view.select()
                results = await session.execute(stmt)
        if results is not None:
            if with_role:
                for result in results:
                    lresult.append(result)
            else:
                for result in results.scalars():
                    lresult.append(result)
        return lresult

    async def get_users_with_role(self, role: str):
        lresult = list()
        results = None
        async with self._async_session() as session:
            async with session.begin():
                stmt = self._user_role_view.select().filter(self._user_role_view.c.rolename == role)
                results = await session.execute(stmt)
        if results is not None:
            for result in results.scalars():
                lresult.append(result)
        return lresult

    async def get_user_detail(self, **kwargs):
        return await self._user_wrapper.select(**kwargs)

    # getters for table "roles"

    async def get_roles(self):
        return await self._role_wrapper.select()

    async def get_role_detail(self, **kwargs):
        return await self._role_wrapper.select(**kwargs)

    #roles for table tasks

    async def get_tasks(self):
        return await self._apptask_wrapper.select()

    async def get_task_detail(self, **kwargs):
        return await self._apptask_wrapper.select(**kwargs)

    async def get_tasks_of_user_id(self,teleg_id):
        lresult=list()
        results=None
        async with self._async_session() as session:
            async with session.begin():
                stmt=self._user_task_view.select().filter(self._user_task_view.c.teleg_id==teleg_id)
                results=await session.execute(stmt)
            if results is not None:
                for result in results:
                    lresult.append(result)
        return lresult

    async def get_tasks_of_username(self,username):
        lresult=list()
        results=None
        async with self._async_session() as session:
            async with session.begin():
                stmt = self._user_task_view.select().filter(self._user_task_view.c.username == username)
                results = await session.execute(stmt)
            if results is not None:
                for result in results:
                    lresult.append(result)
        return lresult

    async def get_users_of_task_id(self,task_id):
        lresult = list()
        results = None
        async with self._async_session() as session:
            async with session.begin():
                stmt = self._user_task_view.select().filter(self._user_task_view.c.task_id == task_id)
                results = await session.execute(stmt)
            if results is not None:
                for result in results:
                    lresult.append(result)
        return lresult

    async def get_users_of_taskname(self,taskname):
        lresult = list()
        results = None
        async with self._async_session() as session:
            async with session.begin():
                stmt = self._user_task_view.select().filter(self._user_task_view.c.taskname == taskname)
                results = await session.execute(stmt)
            if results is not None:
                for result in results:
                    lresult.append(result)
        return lresult

