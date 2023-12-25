from abc import ABC, abstractmethod


class AbstractWrapper(ABC):
    @abstractmethod
    async def select(self, **kwargs):
        pass

    @abstractmethod
    async def update(self, **kwargs):
        pass

    @abstractmethod
    async def insert(self, **kwargs):
        pass

    @abstractmethod
    async def delete(self, row_id):
        pass
