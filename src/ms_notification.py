from prefect import flow, task
from prefect.blocks.notifications import MicrosoftTeamsWebhook

# from prefect.exceptions import FailedRun

# teams_webhook_block = MicrosoftTeamsWebhook.load("ms-teams-webhook")
# teams_webhook_block.notify("Hello from Prefect!")

@task
def unstable_database_task():
    # Simulating a logic failure or data bug
    raise ValueError("Database connection timed out after 30 seconds.")

@flow
def production_data_pipeline():
    unstable_database_task()

if __name__ == "__main__":
    # Create the teams notification block payload
    teams_webhook = MicrosoftTeamsWebhook.load("ms-teams-webhook")

    try:
        production_data_pipeline()
        # raise FailedRun("Flow failed")
    except ValueError as e:
        # 1. Format the alert as a rich markdown string
        message_body = (
            "🚨 **Prefect Pipeline Failure**\n\n"
            "--- \n"
            f"**Flow Name:** `production_data_pipeline`\n"
            f"**Error Details:** *{e}*\n\n"
            "👉 [Click here to view logs in Prefect Cloud](https://prefect.cloud)"
        )

        # Send the rich card directly to your channel
        teams_webhook.notify(subject="Pipeline Failure Alert", body=message_body)

