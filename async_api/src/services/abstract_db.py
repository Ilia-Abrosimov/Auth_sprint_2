from abc import ABC, abstractmethod


class AsyncStorage(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        pass

    @abstractmethod
    async def search(self, *args, **kwargs):
        pass
