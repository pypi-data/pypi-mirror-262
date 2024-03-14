import hvac
from secret_lib.secret_interface import Secret
from secret_lib.exceptions import SecretException


class HscVaultSecret(Secret):

    def __init__(
            self,
            client: hvac.Client,
            paths: [str]
    ):
        # populates _secrets with merging all secrets from the vaults paths
        # be careful to use different names even if there's different paths
        self._secrets = dict()
        for secret_path in paths:
            secret = client.read(secret_path)
            if secret and 'data' in secret:
                secret_data = secret['data']['data']
                for key, value in secret_data.items():
                    if key in self._secrets:
                        raise SecretException(f"Key {key} exists in multiple provided paths. Please use different name to differentiate.")
                    self._secrets[key] = value
