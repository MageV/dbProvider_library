import logging
from enum import Enum, auto

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

sqlite_str = "sqlite+aiosqlite:///bot.db"
postgres_str = "postgresql://user:%1@localhost/%2"
mysql_str = "mysql://user:%1@localhost/%2"


class Base(AsyncAttrs, DeclarativeBase):
    pass


drops_sql: list = ["drop view if exists main.user_over_role",
                   "drop view if exists main.users_over_tasks_view",
                   "drop view if exists main.sys_userid_tasks_view"]
views_sql: list = ["CREATE VIEW user_over_role as select users.teleg_id,users.username,roles.name as "
                   "'rolename' from users"
                   "inner join roles on users.role_id=roles.id where roles.active=1",
                   "CREATE VIEW sys_userid_tasks_view as select grants.user_id,apptasks.name as 'taskname' "
                   "from apptasks"
                   "inner join grants on grants.task_id=apptasks.id where apptasks.active=1",
                   "create view users_over_tasks_view as select users.teleg_id,sys_userid_tasks_view.taskname from "
                   "users inner join sys_userid_tasks_view on users.id=sys_userid_tasks_view.user_id"]

logging.basicConfig(level=logging.INFO, filename="db_log.log", filemode="w")


class DataDictionary(Enum):
    DD_USER = auto(),
    DD_ROLE = auto(),
    DD_GRANT = auto(),
    DD_APPTSK = auto()
