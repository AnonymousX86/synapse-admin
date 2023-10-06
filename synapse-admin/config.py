# -*- coding: utf-8 -*-
from os import getenv

from dotenv import load_dotenv


load_dotenv()

ACCESS_TOKEN = getenv('ACCESS_TOKEN')
BASE_URL = getenv('BASE_URL', 'http://127.0.0.1:8008')
REGISTRATION_SHARED_KEY = getenv('REGISTRATION_SHARED_KEY')

DEFAULT_HEADERS = { 'Authorization': f'Bearer {ACCESS_TOKEN}' }
