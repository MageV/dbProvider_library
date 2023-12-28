from sqlalchemy import Table, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from appconfig.config import Base, views_sql, indexs_sql, sql_debug
from models.role import Role
from models.user import User
from wrappers.grantwrapper import GrantWrapper
from wrappers.rolewrapper import RoleWrapper
from wrappers.taskwrapper import AppTaskWrapper
from wrappers.userwrapper import UserWrapper


class DbProvider:
    _user_role_view: Table
    _user_task_view: Table

    # initialization class
    # parameter string  - connection string to DB
    # example in config.py
    def __init__(self, connstr):
        self._connstr = connstr
        self._async_session = None
        self._user_wrapper = None
        self._role_wrapper = None
        self._apptask_wrapper = None
        self._grant_wrapper = None
        self._engine = create_async_engine(self._connstr, echo=sql_debug)
        self._entities = None

    # must execute before using
    # no parameters
    # no returns
    async def create_engine(self) -> None:
        self._async_session = async_sessionmaker(self._engine, autocommit=False, expire_on_commit=False)
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await self._async_session().commit()

        async  with self._engine.begin() as conn:
            for row in views_sql:
                await self._ddl_create_views(row)
            for row in indexs_sql:
                await self._ddl_create_indexes(row)

        async with self._engine.begin() as conn:
            self._user_role_view = await conn.run_sync(
                lambda cnn: Table('user_over_role', Base.metadata, autoload_with=cnn))
            self._user_task_view = await conn.run_sync(
                lambda cnn: Table('users_over_tasks_view', Base.metadata, autoload_with=cnn))
        self._user_wrapper: UserWrapper = UserWrapper(self._async_session)
        self._role_wrapper: RoleWrapper = RoleWrapper(self._async_session)
        self._apptask_wrapper: AppTaskWrapper = AppTaskWrapper(self._async_session)
        self._grant_wrapper: GrantWrapper = GrantWrapper(self._async_session)

    # must execute before closing app
    # no parameters
    # no returns
    async def destroy_engine(self):
        async with self._async_session() as session:
            await session.close()
        await self._engine.dispose()

    async def _ddl_create_views(self, ddl_string: str):
        async with self._async_session() as session:
            await session.execute(text(ddl_string))
        await session.commit()

    async def _ddl_create_indexes(self, ddl_string: str):
        async with self._async_session() as session:
            await session.execute(text(ddl_string))
        await session.commit()

    # getters for table "users" wrapped on UsersWrapper & DB Views
    # return list of cortèges of rows (teleg_id,'username','user_role'
    # with_role optional default - True

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

    # return list of property "teleg_id" for role with name
    # role must exist in tables roles
    # otherwise returns []
    async def get_users_of_role(self, role: str):
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

    # return list of cortèges of rows (id,teleg_id,name,mail,role_id) selected by properties
    # valid properties id,teleg_id,username
    # property must have chosen only one,e.g id or id_teleg or username
    async def get_user_detail(self, **kwargs):
        return await self._user_wrapper.select(**kwargs)

    # return list of cortèges of rows (id,name,operations,active) from roles
    async def get_roles(self):
        return await self._role_wrapper.select()

    async def get_role_detail(self, **kwargs):
        return await self._role_wrapper.select(**kwargs)

    # roles for table tasks

    async def get_tasks(self):
        return await self._apptask_wrapper.select()

    async def get_task_detail(self, **kwargs):
        return await self._apptask_wrapper.select(**kwargs)

    async def get_tasks_of_user_id(self, teleg_id):
        lresult = list()
        results = None
        async with self._async_session() as session:
            async with session.begin():
                stmt = self._user_task_view.select().filter(self._user_task_view.c.teleg_id == teleg_id)
                results = await session.execute(stmt)
            if results is not None:
                for result in results:
                    lresult.append(result)
        return lresult

    async def get_tasks_of_username(self, username):
        lresult = list()
        results = None
        async with self._async_session() as session:
            async with session.begin():
                stmt = self._user_task_view.select().filter(self._user_task_view.c.username == username)
                results = await session.execute(stmt)
            if results is not None:
                for result in results:
                    lresult.append(result)
        return lresult

    async def get_users_of_task_id(self, task_id):
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

    async def get_users_of_taskname(self, taskname):
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

    # using
    # users_to_create_list = list(
    #    [{"teleg_id": "000015", "username": "Black Queen", "mail": "bq@nonedomain.com", "role": "gu_operator"},
    #     {"teleg_id": "000010", "username": "White Queen", "mail": "wq@nonedomain.com", "role": "administrator"}])
    # constraints:
    # unique for teleg_id+username
    # roles must exist
    async def create_users(self, users: list):
        users_to_append = list()
        for item in users:
            role_id = (await self.get_role_detail(name=item["role"]))
            item["role_id"] = role_id[0][0]
            users_to_append.append(item)
        await self._user_wrapper.insert(users=users_to_append)

    # using
    # roles_to_create_list = list([{"name": "econ_viewer", "active": 1, "operations": "N"},
    #                             {"name": "gu_consumer", "active": 0, "operations": "N"}])
    # await dbprovider.create_roles(roles_to_create_list)
    # constraints:
    # unique for name
    async def create_roles(self, roles: list):
        await self._role_wrapper.insert(roles=roles)

    async def create_tasks(self, tasks: list):
        await self._apptask_wrapper.insert(apptasks=tasks)

    async def create_grants(self, grants):
        grants_to_append = list()
        for item in grants:
            task_id = (await self.get_task_detail(name=item["task"]))
            item["task_id"] = task_id[0][0]
            user_id = -1
            if item.keys().__contains__("teleg_id"):
                user_id = (await self.get_user_detail(teleg_id=item["teleg_id"]))
            elif item.keys().__contains__("username"):
                user_id = (await self.get_user_detail(username=item["username"]))
            if user_id != -1 and user_id != []:
                item["user_id"] = user_id[0][0]
                grants_to_append.append(item)
        await self._grant_wrapper.insert(grants_to_append)
