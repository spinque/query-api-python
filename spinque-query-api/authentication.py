import os.path
import time
import requests

from typing import Union, Tuple
from operator import xor

CONFIG_DIR = os.path.expanduser('~/.config/')
CACHE_DIR = os.path.expanduser('~/.cache/')
SPINQUE_CONFIG_FILE = "spinque.config"


class Authentication:

    def __init__(self,
                 name: str,
                 client_id: str = None,
                 client_secret: str = None,
                 base_url: str = None,
                 auth_server: str = 'https://login.spinque.com'
                 ):
        self.name = name
        self.auth_server = auth_server
        self.client_secret = client_secret
        self.client_id = client_id
        self.base_url = base_url
        if not name:
            raise ValueError('App name needs to be provided')
        if bool(client_id) ^ bool(client_secret):
            raise ValueError('Either client_id and client_secret must be provided, or neither (and read from file)')
        self.access_token: Union[str, None] = None
        self.expires: Union[int, None] = 0

    def try_load_credentials(self) -> None:
        if os.path.isfile("spinque.config"):
            filename = "spinque.config"
        elif os.path.isfile(os.path.join(CONFIG_DIR, SPINQUE_CONFIG_FILE)):
            filename = os.path.join(CONFIG_DIR, SPINQUE_CONFIG_FILE)
        elif os.path.isfile(os.path.join(os.path.expanduser('~'), SPINQUE_CONFIG_FILE)):
            filename = os.path.join(os.path.expanduser('~'), SPINQUE_CONFIG_FILE)
        elif os.path.isfile(f"/etc/{SPINQUE_CONFIG_FILE}"):
            filename = f"/etc/{SPINQUE_CONFIG_FILE}"
        else:
            raise RuntimeError("Spinque config file not found")
        with open(filename) as f:
            for line in f.readlines():
                param, value = line.strip().split('=')
                if param == 'clientid':
                    self.client_id = value
                elif param == 'clientsecret':
                    self.client_secret = value
                else:
                    raise ValueError("Unrecognized parameter", param)

    def try_load_token(self) -> None:
        token_file = os.path.join(CACHE_DIR, f"spinqueToken.{self.name}")
        if os.path.isfile(token_file):
            with open(token_file, 'r') as f:
                for line in f:
                    param, value = line.strip().split('=')
                    if param == 'token':
                        self.access_token = value.strip('"')
                    elif param == 'expires':
                        self.expires = int(value)
                    else:
                        raise ValueError("Unrecognized parameter", param)

    def get_access_token(self) -> Tuple[str, int]:
        if not self.client_id:
            self.try_load_credentials()
        if not self.access_token:
            self.try_load_token()
        if self.access_token and self.expires > time.time() - 10_000:
            return self.access_token, self.expires
        else:
            self.generate_token()
            return self.access_token, self.expires

    def write_token(self) -> None:
        with open(os.path.join(CACHE_DIR, f"spinqueToken.{self.name}"), 'w') as f:
            f.write(f'token="{self.access_token}"\n')
            f.write(f"expires={self.expires}")

    def generate_token(self) -> None:
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'audience': self.base_url
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post(f'{self.auth_server}/oauth/token', headers=headers, data=body)
        if r.status_code == 200:
            self.access_token = r.json()['access_token']
            self.expires = time.time() + r.json()['expires_in']
            self.write_token()
        else:
            raise ValueError(f"Could not generate access token: {r.text}")
