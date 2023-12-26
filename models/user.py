from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from appconfig.config import Base
from models.role import Role


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    teleg_id: Mapped[str]=mapped_column(default="",unique=True,nullable=False)
    username:Mapped[str]=mapped_column(default="",unique=True,nullable=False)
    mail: Mapped[str]=mapped_column(default="",unique=True,nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"),default=None)
    role: Mapped[List[Role]] = relationship()

    def serialize(self):
        result = list()
        result.append(self.id)
        result.append(self.teleg_id)
        result.append(self.username)
        result.append(self.mail)
        result.append(self.role_id)
        return result

    def deserialize(self, serialized: dict):
        #self.id = serialized["id"]
        self.teleg_id = serialized["teleg_id"]
        self.username=serialized["username"]
        self.mail = serialized["mail"]
        self.role_id = serialized["role_id"]
