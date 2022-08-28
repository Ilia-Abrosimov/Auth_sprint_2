import abc
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Optional

import redis as redis
from loguru import logger
from settings import RedisConfig


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class RedisStorage(BaseStorage):
    def __init__(self, redis_dsn: RedisConfig, key: str):
        self._key = key
        self._redis = redis.Redis(**redis_dsn.dict())

    def save_state(self, state: dict) -> None:
        self._redis.set(self._key, json.dumps(state))

    def retrieve_state(self) -> Optional[dict]:
        ret = self._redis.get(self._key)
        return json.loads(ret) if ret else {}


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path: Path = Path(file_path)

    def save_state(self, state: dict) -> None:
        try:
            with open(self.file_path, 'w') as f:
                json.dump(state, f)
        except Exception as e:
            logger.error(e)
            return

    def retrieve_state(self) -> dict:
        if not self.file_path.exists():
            return {}
        try:
            with self.file_path.open('r') as json_file:
                return json.load(json_file)
        except JSONDecodeError as error:
            logger.error(error)
            return {}


class State:
    def __init__(self, storage: BaseStorage):
        self.storage: BaseStorage = storage
        self.data: dict = self.storage.retrieve_state()

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.data[key] = value
        self.storage.save_state(self.data)

    def get_state(self, key: str, default: Any = None) -> Any:
        """Получить состояние по определённому ключу"""
        return self.data.get(key, default)
