from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="src/.env",env_file_encoding = 'utf-8',extra = "allow")
    database_name: str 
    database_user: str 
    database_host: str 
    database_password: str 
    mail_password: str
    sender_email: str
    api_url: str
    ENV: str