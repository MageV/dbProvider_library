import asyncio

from appconfig import config
from models.role import Role
from providers.DbProvider import DbProvider

if __name__ == '__main__':
    dbprovider = DbProvider(connstr=config.sqlite_str)
    asyncio.run(dbprovider.create_engine())
    role: Role = Role(name='operator', operations='RX', active='1')
    #   asyncio.run(dbprovider.create_row(table=DataDictionary.DD_ROLE,data=[role]))
    resultset = asyncio.run(dbprovider.get_users())
    print(resultset)
    resultset = asyncio.run(dbprovider.get_users_with_role(role='admin'))
    print(resultset)
    resultset = asyncio.run(dbprovider.get_user_detail(id=1))
    print(resultset)
    resultset = asyncio.run(dbprovider.get_roles())
    print(resultset)
    resultset = asyncio.run(dbprovider.get_tasks())
    print(resultset)
    resultset = asyncio.run(dbprovider.get_tasks_of_username(username='Horror'))
    print(resultset)
    resultset = asyncio.run(dbprovider.get_users_of_taskname(taskname='Busy'))
    print(resultset)


    asyncio.run(dbprovider.destroy_engine())
