from typing import List

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from appconfig.config import Base
from models.apptask import AppTask
from models.user import User


class Grant(Base):
    __tablename__ = "grants"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=None)
    task_id: Mapped[int] = mapped_column(ForeignKey("apptasks.id"), default=None)
    user: Mapped[List[User]] = relationship()
    task: Mapped[List[AppTask]] = relationship()

    def serialize(self):
        result = dict()
        result["id"] = self.id
        result["user_id"] = self.user_id
        result["task_id"] = self.task_id
        return result

    def deserialize(self, serialized: dict):
        self.id = serialized["dict"]
        self.user_id = serialized["user_id"]
        self.task_id = serialized["task_id"]
