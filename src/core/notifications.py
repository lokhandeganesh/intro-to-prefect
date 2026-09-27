# src/core/notifications.py
from typing import Any

from prefect.blocks.notifications import MicrosoftTeamsWebhook

from core.config import settings
from src.core.logger import get_logger

logger = get_logger("notifications")


def send_teams_notification(
    message: str,
    subject: str = "Prefect Notification",
) -> bool:
    """Dispatches a notification to Microsoft Teams via a saved Prefect block.

    Fails gracefully by logging a warning so notification issues never break
    the underlying workflow.
    """
    target_block = settings.teams_block_name

    try:
        teams_block = MicrosoftTeamsWebhook.load(target_block)
        teams_block.notify(
            body=message,
            subject=subject,
        )
        logger.info(f"Teams alert successfully sent via block: '{target_block}'")
        return True
    except Exception as exc:
        logger.warning(
            f"Failed to dispatch Teams notification via '{target_block}': {exc}"
        )
        return False


def teams_failure_hook(flow_or_task: Any, run: Any, state: Any):
    """Automated Prefect hook for flow or task failures.

    Extracts runtime metadata (name, run ID, and error message) automatically.
    """
    name = getattr(flow_or_task, "name", "Workflow")
    run_id = getattr(run, "id", "unknown-run-id")
    error_msg = state.message or "No explicit error message provided."

    body = (
        f"**Pipeline:** `{name}`\n\n"
        f"**Run ID:** `{run_id}`\n\n"
        f"**State:** `FAILED`\n\n"
        f"**Details:**\n```{error_msg}```"
    )

    send_teams_notification(
        message=body,
        subject=f"[FAILURE] {name} Failed",
    )
