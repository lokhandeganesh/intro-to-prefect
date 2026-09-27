from prefect.blocks.notifications import MicrosoftTeamsWebhook

from core.config import settings

# Initialize block with incoming webhook URL
teams_block = MicrosoftTeamsWebhook(
    url=settings.teams_webhook_url,
)

# Register/Save the block to Prefect Server / Cloud
teams_block.save(settings.teams_block_name, overwrite=True)
print(f"Block '{settings.teams_block_name}' successfully registered.")
