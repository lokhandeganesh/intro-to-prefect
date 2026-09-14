from prefect import flow, task
from prefect_sqlalchemy import SqlAlchemyConnector


@task
def fetch_data(block_name: str) -> list:
    all_rows = []
    with SqlAlchemyConnector.load(block_name) as connector:
        while True:
            # Repeated fetch* calls using the same operation will
            # skip re-executing and instead return the next set of results
            new_rows = connector.fetch_many("SELECT * FROM Production.Product", size=2)
            if len(new_rows) == 0:
                break
            all_rows.append(new_rows)
    return all_rows


@flow
def sqlalchemy_flow(block_name: str) -> list:
    all_rows = fetch_data(block_name)
    return all_rows


if __name__ == "__main__":
    sqlalchemy_flow("mssql-database-block")