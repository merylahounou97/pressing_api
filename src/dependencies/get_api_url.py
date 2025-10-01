import requests

from ..config import Settings

config = Settings()


def get_api_url():
    """Get the API URL.

    Returns:
        str: The API URL.
    """

    if config.ENV == "prod":
        return config.api_url

    response = requests.get("http://ngrok:4040/api/tunnels", timeout=15)
    if response.status_code == 200:
        return response.json()["tunnels"][0]["public_url"]
