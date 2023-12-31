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
                values_list = kwargs["sec_values_list"]
                user = kwargs["sec_user"]
                user_ops = kwargs["sec_user_ops"]
                for item in values_list:
                    if user in item:
                        has_found = item[user].find(str(user_ops.value))
                        if has_found >= 0:
                            return await func(*args, **kwargs)
        else:
            def wrapper(*args, **kwargs):
                values_list = kwargs["sec_values_list"]
                user = kwargs["sec_user"]
                user_ops = kwargs["sec_user_ops"]
                for item in values_list:
                    if user in item:
                        has_found = item[user].find(user_ops.value)
                        if has_found:
                            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def validate_user(func):
        if asyncio.iscoroutinefunction(func):
            async def wrapper(*args, **kwargs):
                sec_key = UUID().__str__().encode()
                users = kwargs["sec_users"]
                username = kwargs["username"]
                for item in users:
                    sec_item = hmac.digest(sec_key, item, 'sha256')
                    sec_user_vrf = hmac.digest(sec_key, username, 'sha256')
                    if hmac.compare_digest(sec_item, sec_user_vrf):
                        return await func(*args, **kwargs)

            return wrapper
        else:
            def wrapper(*args, **kwargs):
                sec_key = UUID().__str__().encode()
                users = kwargs["sec_users"]
                username = kwargs["username"]
                for item in users:
                    sec_item = hmac.digest(sec_key, item, 'sha256')
                    sec_user_vrf = hmac.digest(sec_key, username, 'sha256')
                    if hmac.compare_digest(sec_item, sec_user_vrf):
                        return func(*args, **kwargs)

            return wrapper
