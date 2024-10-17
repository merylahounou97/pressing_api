from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class to store all the environment variables

    Attributes:
        model_config (SettingsConfigDict): Configuration for the settings
        database_name (str): Database name
        database_user (str): Database user
        database_host (str): Database host
        database_password (str): Database password
        mail_password (str): Mail password
        sender_email (str): Sender email
        api_url (str): API URL
        ENV (str): Environment
        code_expiry_time (int): Code expiry time
    """

    model_config = SettingsConfigDict(
        env_file="src/.env", env_file_encoding="utf-8", extra="allow"
    )
    
    app_name: str
    database_name: str
    database_user: str
    database_host: str
    database_password: str
    mail_password: str
    sender_email: str
    api_url: str
    ENV: str
    code_expiry_time: int
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    support_address: str
    test_mode: bool = False
