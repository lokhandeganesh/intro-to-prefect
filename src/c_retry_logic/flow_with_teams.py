import random

from prefect import flow, task

from src.core.logger import get_logger
from src.core.notifications import send_teams_notification, teams_failure_hook

logger = get_logger("notification-flow")


@task
def sync_orders():
    # Processing logic
    orders_processed = 1450

    send_teams_notification(
        message=f"Successfully synchronized **{orders_processed}** orders to the warehouse.",
        subject="Sync Completed",
    )


@task(retries=1, retry_delay_seconds=5)
def process_user_records(user_id: int):
    logger.info(f"Processing user {user_id}...")

    if random.choice([101, 102, 103]) != user_id:
    # if user_id == 101:
        raise ValueError("Invalid user record encountered!")
    return {"status": "ok"}


# Hook automatically catches any unhandled failure and sends a Teams card
@flow(name="user-account-flow", on_failure=[teams_failure_hook])
# @flow(name="user-account-flow")
def run_pipeline():
    logger.info("Starting pipeline execution")
    sync_orders()
    process_user_records(101)


if __name__ == "__main__":
    run_pipeline()
