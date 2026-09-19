from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    block_name: str

    class Config:
        env_file = ".env"
        # Optional: Instead of adding fields,
        # you can tell Pydantic to ignore extras
        extra = "ignore"

settings = Settings()