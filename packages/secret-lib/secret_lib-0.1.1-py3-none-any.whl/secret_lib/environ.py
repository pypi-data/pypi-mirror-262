import os

from secret_lib.secret_interface import Secret


class EnvironSecret(Secret):

    def __init__(self, *args, prefix: str, **kwargs):
        super().__init__(*args, **kwargs)
        prefix_len = len(prefix)
        self._secrets = {key[prefix_len:]: value for key, value in os.environ.items() if key.startswith(prefix)}
