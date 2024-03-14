# Secrets Wrapper

This is a library for wrapping up different ways of accessing secrets and configuration.

## Dotenv files

Gets values from .env files. Good for development purposes.

```python
from secret_lib import EnvFileSecret

my_secrets = EnvFileSecret(file_path="/my/path/.env")
secret_one = my_secrets.get("secret_one")
```

## Environ values

Gets values from system variables. Gets all the variables prefixed with the specified string.

```python
from secret_lib import EnvironSecret

my_secrets = EnvironSecret(prefix="MY_APP_")
secret_one = my_secrets.get("secret_one")
```

## HaShiCorp Vault

Uses HSC Vault with the hsc-vault python library. Needs a fully configured and authenticated `hvac.Client`.

```python
import hvac
from secret_lib.hsc_vault import HscVaultSecret

# Create a client instance
client = hvac.Client(url='https://vault.trustnet.app:8200')
client.auth.userpass.login(
    username='username',
    password='password'
)

secret = HscVaultSecret(client=client, paths=['secret/data/l0', 'secret/data/l1'])

first_secret = secret.get('first_secret')
```