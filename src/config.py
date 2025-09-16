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
        env_file=".env", env_file_encoding="utf-8", extra="allow"
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
    secret_key: str
    algorithm: str
    access_token_expire_minutes: float

    # ===== Default Admin =====
    default_admin_email: str
    default_admin_phone_number: str
    default_admin_last_name: str
    default_admin_first_name: str
    default_admin_password: str
    default_admin_address: str

    # ===== Default Secretary =====
    default_secretary_email: str|None = None
    default_secretary_phone_number: str|None = None
    default_secretary_last_name: str|None = None
    default_secretary_first_name: str|None = None
    default_secretary_address: str|None = None
    default_secretary_password: str|None = None

    # ===== Default Customer =====
    default_customer_email: str|None = None
    default_customer_phone_number: str|None = None
    default_customer_last_name: str|None = None
    default_customer_first_name: str|None = None
    default_customer_address: str|None = None
    default_customer_password: str|None = None