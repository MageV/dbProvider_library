import asyncio
import logging

from sqlalchemy.exc import IntegrityError

from appconfig import config
from appconfig.config import SEC_DB_OPERATION
from models.role import Role
from providers.DbProvider import DbProvider

if __name__ == '__main__':
    dbprovider = DbProvider(connstr=config.sqlite_str)
    asyncio.run(dbprovider.create_engine())
    print("!!!GET_USERS!!!")
    resultset = asyncio.run(dbprovider.get_users(with_role=True, sec_user='Black Queen',
                                                 sec_values_list=dbprovider.get_preloaded(),
                                                 sec_user_ops=SEC_DB_OPERATION.SDO_CREATE))
    print(resultset)
    #   print("!!!GET_USERS_WITH_ROLE!!!")
    #   resultset = asyncio.run(dbprovider.get_users_of_role(role='administrator'))
    #   print(resultset)
    #   print("!!!GET_USERS_DETAIL!!!")
    #   resultset = asyncio.run(dbprovider.get_user_detail(id=1))
    #   print(resultset)
    #   print("!!!GET_ROLES!!!")
    #   resultset = asyncio.run(dbprovider.get_roles())
    #   print(resultset)
    #   print("!!!GET_TASKS!!!")
    #   resultset = asyncio.run(dbprovider.get_tasks())
    #   print(resultset)
    #   print("!!!GET_TASKS_OF_USERNAME!!!")
    #   resultset = asyncio.run(dbprovider.get_tasks_of_username(username='Horror'))
    #  print(resultset)
    #  print("!!!GET_USERS_OF_USERNAME!!!")
    #   resultset = asyncio.run(dbprovider.get_users_of_taskname(taskname='Busy'))
    #   print(resultset)
    #   print("!!!GET_ROLE_DETAILS!!!")
    #   resultset = asyncio.run(dbprovider.get_role_detail(name='administrator'))
    #   print(resultset)
    #   try:
    #       roles_to_create_list = list([{"name": "administrator", "active": 1, "operations": "RWED"},
    #                                    {"name": "gu_operator", "active": 1, "operations": "R"}])
    #       asyncio.run(dbprovider.create_roles(roles_to_create_list))
    #   except:
    #       print('error')

    #users_to_create_list = list(
    #      [{"teleg_id": "000235", "username": "Martial Rabbit", "mail": "rabbit@nonedomain.com", "role": "gu_operator"},
    #      {"teleg_id": "000310", "username": "Swaggle Sword", "mail": "sws@nonedomain.com", "role": "administrator"}])
    #asyncio.run(dbprovider.create_users(users_to_create_list))

    #    try:
    #        task_to_create_list = list([{"name": "busy", "active": 1}, {"name": "stat", "active": 1}])
    #        asyncio.run(dbprovider.create_tasks(task_to_create_list))
    #    except:
    #        print("error")
    try:
        grants_to_create_list = list(
            [{"username": "Swaggle Sword", "task": "stat"}])
        asyncio.run(dbprovider.create_grants(grants_to_create_list))
    except IntegrityError as ex:
        logging.log(msg=f"Insertion row error.Values not unique. {ex.__str__()}",level=logging.ERROR)

    #asyncio.run(dbprovider.destroy_engine())
