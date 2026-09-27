from prefect import flow, task

from src.core.logger import logger


@task
def my_task():
    logger.info("Task log: processing item")
    return 42

@flow
def my_flow():
    logger.info("Flow log: workflow started")
    my_task()

if __name__ == "__main__":
    my_flow()