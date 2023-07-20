from django.conf import settings

from hashlib import sha512
from secrets import token_hex



def my_hash(password, salt=None) -> [str, 146]:
    if not salt:
        salt = token_hex(settings.SALT_BYTE)
    salted_str = f"{salt}{password}".encode('utf-8')
    result_str = sha512(salted_str).hexdigest()
    return f"{salt}{settings.SALT_SEP}{result_str}"

def pw_check(password, target_str) -> bool:
    salt, _ = target_str.split(settings.SALT_SEP)
    if my_hash(password, salt=salt) == target_str:
        return True
    return False


'''
def _my_hash(password, salt=None) -> [str, 146]:
    if not salt:
        salt = token_hex(8)
    salted_str = f"{salt}{password}".encode('utf-8')
    result_str = sha512(salted_str).hexdigest()
    return f"{salt}::{result_str}"

def _pw_check(password, target_str) -> bool:
    salt, _ = target_str.split("::")
    if _my_hash(password, salt=salt) == target_str:
        return True
    return False
'''
