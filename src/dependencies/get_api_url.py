import requests

from ..config import Settings

config = Settings()


def get_api_url():

    if config.ENV == "dev":
        response = requests.get("http://ngrok:4040/api/tunnels")
        print(response.json())
        if response.status_code == 200:
            return response.json()["tunnels"][0]["public_url"]
    else:
        return config.api_url
