import asyncio
import functools
import hmac
from uuid import UUID

from appconfig.config import SEC_DB_OPERATION


class SecurityProvider:
    @staticmethod
    def allowed(func):
        if asyncio.iscoroutinefunction(func):
            async def wrapper(*args, **kwargs):
                values_list = kwargs["values_list"]
                user = kwargs["user"]
                user_ops = kwargs["user_ops"]
                for item in values_list:
                    if user in item:
                        has_found = item[user].find(str(user_ops.value))
                        if has_found >= 0:
                            return await func(*args, **kwargs)
        else:
            def wrapper(*args, **kwargs):
                values_list = kwargs["values_list"]
                user = kwargs["user"]
                user_ops = kwargs["user_ops"]
                for item in values_list:
                    if user in item:
                        has_found = item[user].find(user_ops.value)
                        if has_found:
                            return func(*args, **kwargs)
        return wrapper



def validate_user(func, users: list, username):
    sec_key = UUID().__str__().encode()
    for item in users:
        sec_item = hmac.digest(sec_key, item, 'sha256')
        sec_user_vrf = hmac.digest(sec_key, username, 'sha256')
        if hmac.compare_digest(sec_item, sec_user_vrf):
            func()
    raise ConnectionError('User not authenticated')


# values_list: list,user:str, user_ops: SEC_DB_OPERATION):

