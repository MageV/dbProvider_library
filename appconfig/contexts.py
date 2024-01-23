import contextvars


_sqlite_str = "sqlite+aiosqlite:///bot.db"
_postgres_str = "postgresql://user:%1@localhost/%2"
_mysql_str = "mysql://user:%1@localhost/%2"
sec_user_ctx: contextvars.ContextVar[str] = contextvars.ContextVar('sec_user')
sec_preloaded: contextvars.ContextVar[list] = contextvars.ContextVar('sec_preloaded', default=[])
db_sql_debug: contextvars.ContextVar[bool] = contextvars.ContextVar('db_sql_debug', default=False)
db_sql_connection: contextvars.ContextVar[str] = contextvars.ContextVar('db_sql_connection',
                                                                        default=_sqlite_str)
