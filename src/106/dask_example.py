import asyncio

from prefect import flow, task
from prefect_dask.task_runners import DaskTaskRunner


@task
async def say_hello(name):
    print(f"hello {name}")


@task
async def say_goodbye(name):
    print(f"goodbye {name}")


@flow(task_runner=DaskTaskRunner())
async def greetings(names):
    for name in names:
        await say_hello(name)
        await say_goodbye(name)


if __name__ == "__main__":
    asyncio.run(greetings(["arthur", "trillian", "ford", "marvin"]))
