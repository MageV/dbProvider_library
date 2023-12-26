from sqlalchemy.orm import Mapped, mapped_column

from appconfig.config import Base


class AppTask(Base):
    __tablename__ = "apptasks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]=mapped_column(default="")
    active: Mapped[int] = mapped_column(default=0)

    def serialize(self):
        result = list()
        result.append(self.id)
        result.append(self.name)
        result.append(self.active)
        return result

    def deserialize(self, serialized: dict):
        #self.id = serialized["id"]
        self.name = serialized["name"]
        self.active = serialized["active"]
