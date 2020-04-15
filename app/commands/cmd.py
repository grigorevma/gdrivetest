from urllib.parse import urlparse
from hashlib import pbkdf2_hmac
from os import remove
from asyncio import sleep


def get_id(url):
    t = urlparse(url)
    query_id = t.query[3:]
    return query_id


def get_hash(password, salt):
    key = pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000,
        dklen=128
    )
    return key


async def deleter(file_to_delete):
    await sleep(30)
    remove(file_to_delete)
