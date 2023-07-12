import time
import requests

from typing import Union, Tuple


class Authentication:

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 base_url: str,
                 auth_server: str = 'https://login.spinque.com'
                 ):
        self.auth_server = auth_server
        self.client_secret = client_secret
        self.client_id = client_id
        self.base_url = base_url

        self.access_token: Union[str, None] = None
        self.expires: Union[int, None] = None

    def get_access_token(self) -> Tuple[str, int]:
        if self.access_token and self.expires > time.time():
            return self.access_token, self.expires
        else:
            self.generate_token()
            return self.access_token, self.expires

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
        else:
            raise ValueError(f"Could not generate access token: {r.text}")
