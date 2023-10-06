# -*- coding: utf-8 -*-
from datetime import datetime
from time import time

from requests import get, post

from .config import BASE_URL, DEFAULT_HEADERS


class RegistrationToken:
    def __init__(self, payload: dict) -> None:
        self.token: str = payload.get('token')
        self.uses_allowed: int = payload.get('uses_allowed')
        self.pending: int = payload.get('pending')
        self.completed: int = payload.get('completed')
        self.expiry_time: int = payload.get('expiry_time')

    @property
    def expiry_date(self) -> str:
        dt = datetime.fromtimestamp(self.expiry_time / 1000)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def __str__(self) -> str:
        return \
            'Token: {0.token}\n' \
            'Uses allowed: {0.uses_allowed}\n' \
            'Pending registrations: {0.pending}\n' \
            'Completed registrations: {0.completed}\n' \
            'Expiry time: {0.expiry_time} ({0.expiry_date})\n' \
            ''.format(self)

    def delete(self) -> bool:
        # TODO - Token deleting method
        pass


def generate_token(uses: int = 1, valid_for: int = 120) -> RegistrationToken | None:
    if valid_for > 600:
        print('Token should not be valid for more than 10 minutes')
        return None
    json = {
        'uses_allowed': uses,
        'expiry_time': (int(time()) + valid_for) * 1000
    }
    res = post(
        url=f'{BASE_URL}/_synapse/admin/v1/registration_tokens/new',
        json=json,
        headers=DEFAULT_HEADERS
    )
    if (code := res.status_code) != 200:
        print(f'Unable to generate token, error {code}')
        print(res.text)
        return None
    token = RegistrationToken(res.json())
    return token

def get_tokens(valid: bool = None) -> list[RegistrationToken] | None:
    url=f'{BASE_URL}/_synapse/admin/v1/registration_tokens'
    if valid is True:
        url += '?valid=true'
    elif valid is False:
        url += '?valid=false'
    res = get(
        url=url,
        headers=DEFAULT_HEADERS
    )
    if (code := res.status_code) != 200:
        print(f'Unable to get tokens, error {code}')
        print(res.text)
        return None
    tokens = list(map(
        lambda t: RegistrationToken(t),
        res.json().get('registration_tokens', {})
    ))
    return tokens
