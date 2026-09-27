from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    database_block_name: str
    app_name: str
    # log_level: str

    teams_webhook_url: str
    teams_block_name: str

    class Config:
        env_file = ".env"
        # Optional: Instead of adding fields,
        # you can tell Pydantic to ignore extras
        extra = "ignore"

settings = Settings()
