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


class DataDictionary(Enum):
    DD_USER = auto(),
    DD_ROLE = auto(),
    DD_GRANT = auto(),
    DD_APPTSK = auto()
