# -*- coding: utf-8 -*-
from hashlib import sha1
from hmac import new as hmac_new
from time import time

from requests import get, post

from .config import BASE_URL, DEFAULT_HEADERS, REGISTRATION_SHARED_KEY
from .utils import check_username, temp_password


class Nonce:
    def __init__(self, payload: dict) -> None:
        self.nonce: str = payload.get('nonce')


class RegisterSuccess:
    def __init__(self, payload: dict) -> None:
        self.access_token: str = payload.get('access_token')
        self.user_id: str = payload.get('user_id')
        self.home_server: str = payload.get('home_server')
        self.device_id: str = payload.get('device_id')


def get_nonce() -> Nonce | None:
    res = get(
        url=f'{BASE_URL}/_synapse/admin/v1/register',
        headers=DEFAULT_HEADERS
    )
    if (code := res.status_code) != 200:
        print(f'Connection error: {code}')
        return None
    return Nonce(res.json())

def generate_mac(
        nonce: str,
        user: str,
        password: str,
        admin: str = False,
        user_type=None
    ) -> str:

    mac = hmac_new(
      key=REGISTRATION_SHARED_KEY.encode('utf-8'),
      digestmod=sha1,
    )

    mac.update(nonce.encode('utf8'))
    mac.update(b"\x00")
    mac.update(user.encode('utf8'))
    mac.update(b"\x00")
    mac.update(password.encode('utf8'))
    mac.update(b"\x00")
    mac.update(b"admin" if admin else b"notadmin")
    if user_type:
        mac.update(b"\x00")
        mac.update(user_type.encode('utf8'))

    return mac.hexdigest()

def register_user(
        username: str,
        display_name: str,
        admin: bool = False
    ) -> RegisterSuccess | None:
    if not check_username(username):
        print('Username has to be lowercase and contain only underscores')
        return None

    if not (nonce := get_nonce()):
        print('Unable to register user')
        return None

    password = temp_password()
    mac = generate_mac(
        nonce=nonce.nonce,
        user=username,
        password=password,
        admin=admin
    )
    json = {
        'nonce': nonce.nonce,
        'username': username,
        'displayname': display_name,
        'password': password,
        'admin': admin,
        'mac': mac
    }
    res = post(
        url=f'{BASE_URL}/_synapse/admin/v1/register',
        json=json,
        headers=DEFAULT_HEADERS
    )

    if (code := res.status_code) != 200:
        print(f'Connection error: {code}')
        print(res.text)
        return None

    return RegisterSuccess(res.json())
