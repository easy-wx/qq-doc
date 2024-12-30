# https://docs.qq.com/open/document/app/openapi/v2/file/
import json
import time

import requests


class QQDocAPIBase:
    BASE_URL = "https://docs.qq.com"
    API_URL = f"{BASE_URL}/openapi/drive/v2"
    OAUTH_URL = f"{BASE_URL}/oauth/v2/authorize"

    def __init__(self, client_id, client_secret, token_cache_file="cache.json"):
        """
        Initialize the QQDocsAPI with client_id and client_secret.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_cache_file = token_cache_file
        self.access_token = None
        self.open_id = None

        self._init_token_and_openid()

    def _get_app_account_token(self):
        """
        Retrieve the application account token using client_id and client_secret.
        """
        url = f"{self.BASE_URL}/oauth/v2/app-account-token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            ret = response.json()
            if ret.get("ret", None) is not None:
                raise Exception(f"Failed to get token: {ret}")
            return ret
        else:
            response.raise_for_status()

    def _init_token_and_openid(self):
        """
        Initialize the access_token and open_id by calling get_app_account_token.
        """
        try:
            self._load_token_from_cache()
        except Exception as e:
            token_info = self._get_app_account_token()
            token_info["req_time"] = time.time()
            token_info["client_id"] = self.client_id
            json.dump(token_info, open(self.token_cache_file, "w"))
            self._load_token_from_cache()

    def _load_token_from_cache(self):
        """
        Load the access_token and open_id from cache file.
        """
        with open(self.token_cache_file, "r") as file:
            cache = json.load(file)
            if self.client_id != cache.get("client_id", None):
                raise Exception("Client ID mismatch")
            self.access_token = cache["access_token"]
            self.open_id = cache["user_id"]
            req_time = cache["req_time"]
            if req_time + cache["expires_in"] < time.time():
                raise Exception("Token expired")

    def _get_headers(self):
        """
        Generate common headers for API requests using instance variables.
        """
        return {
            "Access-Token": self.access_token,
            "Client-Id": self.client_id,
            "Open-Id": self.open_id,
            "Accept": "application/json"
        }
