import random
import time

from prefect import flow, get_run_logger, task
from prefect.exceptions import FailedRun

from src.core.logger import get_logger

# Module-scoped logger
logger = get_logger(__name__)


# Task that randomly fails, simulating an unreliable operation
@task(retries=3, retry_delay_seconds=5)
def fetch_user_info(user_id: int):
    # Simulate a random failure
    if random.choice([True, False]):
        logger.error(f"Fetching user info for {user_id} failed! Retrying...")
        raise FailedRun(f"Failed to fetch user info for user ID: {user_id}")

    time.sleep(2)  # Simulate fetching user data
    logger.info(f"Successfully fetched user info for user ID: {user_id}")
    return {"user_id": user_id, "name": "John Doe"}

@task
def check_account_balance(user_info: dict):
    log = get_run_logger()
    log.info(f"Checking account balance for {user_info['name']}...")
    time.sleep(3)  # Simulate checking account balance
    balance_info = f"{user_info['name']}, your account balance is: $1,234.56"
    log.info(f"Account balance retrieved: {balance_info}")
    return balance_info

@task
def send_notification(balance_info: str):
    log = get_run_logger()
    log.info(f"Sending notification: {balance_info}")
    time.sleep(1)  # Simulate sending email notification
    log.info("Notification sent successfully.")
    return f"Notification sent: {balance_info}"

# Flow to demonstrate retries, logging, and dependent task execution
@flow
def user_account_flow(user_id: int):
    log = get_run_logger()
    log.info(f"Starting user account flow for user ID: {user_id}")

    # Step 1: Fetch user info with retries if it fails
    user_info = fetch_user_info.submit(user_id)

    # Step 2: Check account balance (depends on user_info)
    balance_task = check_account_balance.submit(user_info.result())

    # Step 3: Send notification (depends on balance check being complete)
    notification_task = send_notification.submit(balance_task.result())

    # Collect results
    notification_result = notification_task.result()

    log.info("Flow completed successfully.")
    return notification_result

if __name__ == "__main__":
    # Run the flow
    result = user_account_flow(101)
    print(result)
