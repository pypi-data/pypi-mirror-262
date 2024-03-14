import os
from collections import namedtuple

from dotenv import load_dotenv

Credentials = namedtuple('Credentials', ['username', 'password'])


load_dotenv()
PROVIDER = os.getenv('PROVIDER')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
CREDENTIALS = Credentials(USERNAME, PASSWORD)
