import platform
from keyring.backend import KeyringBackend
import hashlib
import os

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
if platform.system() == "Windows":
    from keyring.backends.Windows import WinVaultKeyring
    os_keyring = WinVaultKeyring()
elif platform.system() == "Linux":
    from keyring.backends.SecretService import Keyring
    os_keyring = Keyring()
elif platform.system() == "Darwin":
    from keyring.backends.macOS import Keyring
    os_keyring = Keyring()
else:
    os_keyring = None

os_keyring : KeyringBackend

def compute_mod_hash(root_dir) -> str:
    # gather files and compute file hash
    compute = hashlib.sha256()
    for root, dirs, files in os.walk(root_dir):
        # gather all files that ends in .py
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'rb') as f:
                    compute.update(f.read())

    return compute.hexdigest()