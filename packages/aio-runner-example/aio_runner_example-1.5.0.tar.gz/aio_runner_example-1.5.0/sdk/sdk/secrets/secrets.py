from abc import ABC, abstractmethod
from dataclasses import dataclass

from vyper import v

from sdk.secrets.exceptions import NotFoundError


@dataclass
class SecretsABC(ABC):
    @staticmethod
    @abstractmethod
    def get_secret() -> str:
        pass


@dataclass
class Secrets(SecretsABC):
    @staticmethod
    def get_secret(key: str) -> str:
        real_key = f"{key.upper()}"
        result = v.get_string(real_key)
        if result == "":
            raise NotFoundError(key)
        return result
