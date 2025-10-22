import requests

from src.config import get_settings



def get_api_url():
    """Get the API URL.

    Returns:
        str: The API URL.
    """
    config = get_settings()

    if config.ENV == "prod":
        return config.api_url

    response = requests.get("http://ngrok:4040/api/tunnels", timeout=15)
    if response.status_code == 200:
        return response.json()["tunnels"][0]["public_url"]
