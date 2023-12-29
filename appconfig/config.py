import logging
from enum import Enum

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

sqlite_str = "sqlite+aiosqlite:///bot.db"
postgres_str = "postgresql://user:%1@localhost/%2"
mysql_str = "mysql://user:%1@localhost/%2"
sql_debug = False

class Base(AsyncAttrs, DeclarativeBase):
    pass



indexs_sql: list = ["CREATE UNIQUE INDEX IF NOT EXISTS 'apt_uix' ON apptasks(name)",
                    "CREATE UNIQUE INDEX IF NOT EXISTS 'grants_uix' on grants(user_id,task_id)",
                    "CREATE UNIQUE INDEX IF NOT EXISTS 'rls_uix' on roles(name)",
                    "CREATE UNIQUE INDEX IF NOT EXISTS 'usr_uix' on users(teleg_id,username)"]
views_sql: list = ["CREATE VIEW IF NOT EXISTS user_over_role as select users.teleg_id,users.username,roles.name as "
                   "'rolename' from users "
                   "inner join roles on users.role_id=roles.id where roles.active=1",
                   "CREATE VIEW IF NOT EXISTS  sys_userid_tasks_view as select grants.user_id,apptasks.name as "
                   "'taskname' from apptasks "
                   "inner join grants on grants.task_id=apptasks.id where apptasks.active=1",
                   "CREATE VIEW IF NOT EXISTS  users_over_tasks_view as select users.teleg_id,"
                   "sys_userid_tasks_view.taskname from "
                   "users inner join sys_userid_tasks_view on users.id=sys_userid_tasks_view.user_id",
                   "CREATE VIEW IF NOT EXISTS sys_roles as select users.teleg_id,users.username,roles.operations from"
                   " users inner join roles on users.role_id=roles.id"]

#logging.basicConfig(level=logging.INFO, filename="db_log.log", filemode="w")


class SEC_DB_OPERATION(Enum):
    SDO_READ = 'R'
    SDO_UPDATE = 'U'
    SDO_DELETE = 'D'
    SDO_CREATE = 'C'


