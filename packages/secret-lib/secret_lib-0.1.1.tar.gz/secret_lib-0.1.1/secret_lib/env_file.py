from dotenv import dotenv_values
from secret_lib.secret_interface import Secret


class EnvFileSecret(Secret):

    def __init__(self, *args, file_path: str, **kwargs):
        super().__init__(*args, **kwargs)
        self._secrets = dotenv_values(file_path)
