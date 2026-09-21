import time

from prefect import flow, task
from prefect.futures import wait
from prefect.task_runners import ThreadPoolTaskRunner


@task
def stop_at_floor(floor):
    print(f"elevator moving to floor {floor}")
    time.sleep(floor)
    print(f"elevator stops on floor {floor}")


@flow(task_runner=ThreadPoolTaskRunner(max_workers=2))
def elevator():
    floors = []

    for floor in range(3, 0, -1):
        floors.append(stop_at_floor.submit(floor))

    wait(floors)


if __name__ == "__main__":
    elevator()
