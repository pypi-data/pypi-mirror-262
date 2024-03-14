from abc import ABC, abstractmethod
from secret_lib.exceptions import SecretException


class Secret(ABC):
    _secrets: dict | None = None

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """should populate the _secrets instance attribute"""

    def get(self, key):
        if not self._secrets:
            raise SecretException(f'Must populate _secrets attribute in init function')
        try:
            return self._secrets[key]
        except KeyError:
            raise SecretException(f'Secret {key} is missing')
