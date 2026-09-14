from prefect_sqlalchemy import ConnectionComponents, SqlAlchemyConnector, SyncDriver

from core.config import settings

connector = SqlAlchemyConnector(
    connection_info=ConnectionComponents(
        driver=SyncDriver.MSSQL_PYODBC,
        host=settings.database_hostname,
        port=settings.database_port,
        username=settings.database_username,
        password=settings.database_password,
        database=settings.database_name,
        query={"driver": "ODBC Driver 18 for SQL Server", "TrustServerCertificate": "yes"},
    ),
    # Passed directly to sqlalchemy.create_engine(..., connect_args={...})
    # connect_args={
    #     "driver": "ODBC Driver 18 for SQL Server",
    #     "TrustServerCertificate": "yes",
    # },
)

connector.save(settings.block_name, overwrite=True)


# Load the saved block that holds your credentials:
# from prefect_sqlalchemy import SqlAlchemyConnector

# SqlAlchemyConnector.load("mssql-database-block")



# from prefect.blocks.system import Secret

# my_secret_block = Secret(value="shhh!-it's-a-secret")
# my_secret_block.save(name="secret-thing")
