# https://docs.qq.com/open/document/app/oauth2/app_account_token.html
import json
import time

import requests


class QQDocsAPI:
    BASE_URL = "https://docs.qq.com"

    def __init__(self, client_id, client_secret, token_cache_file="cache.json"):
        """
        Initialize the QQDocsAPI with client_id and client_secret.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_cache_file = token_cache_file
        self.access_token = None
        self.open_id = None

        self.init_token_and_openid()

    def init_token_and_openid(self):
        """
        Initialize the access_token and open_id by calling get_app_account_token.
        """
        try:
            self.load_token_from_cache()
        except Exception as e:
            token_info = self.get_app_account_token()
            token_info["req_time"] = time.time()
            json.dump(token_info, open(self.token_cache_file, "w"))
            self.init_token_and_openid()

    def load_token_from_cache(self):
        """
        Load the access_token and open_id from cache file.
        """
        with open(self.token_cache_file, "r") as file:
            cache = json.load(file)
            self.access_token = cache["access_token"]
            self.open_id = cache["user_id"]
            req_time = cache["req_time"]
            if req_time + cache["expires_in"] < time.time():
                raise Exception("Token expired")

    def _get_headers(self, access_token, open_id):
        """
        Generate common headers for API requests.
        """
        return {
            "Access-Token": access_token,
            "Client-Id": self.client_id,
            "Open-Id": open_id,
            "Accept": "application/json"
        }

    def get_app_account_token(self):
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
            return response.json()
        else:
            response.raise_for_status()

    def get_file_permission(self, file_id, access_token, open_id):
        """
        Get the permission details of a specific file.
        """
        url = f"{self.BASE_URL}/openapi/drive/v2/files/{file_id}/permission"
        headers = self._get_headers(access_token, open_id)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def create_folder(self, title, access_token, open_id, parentfolderID=None):
        """
        Create a new folder with the specified title.
        """
        url = f"{self.BASE_URL}/openapi/drive/v2/folders"
        headers = self._get_headers(access_token, open_id)
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = {
            "title": title
        }
        if parentfolderID:
            data["parentfolderID"] = parentfolderID

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_folder_metadata(self, folder_id, access_token, open_id):
        """
        Retrieve metadata of a specific folder.
        """
        url = f"{self.BASE_URL}/openapi/drive/v2/folders/{folder_id}/metadata"
        headers = self._get_headers(access_token, open_id)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def list_folder_contents(self, access_token, open_id, folder_id=None, sort_type="browse", asc=0, start=0, limit=20):
        """
        List the contents of a folder with optional sorting and pagination.
        """
        url = f"{self.BASE_URL}/openapi/drive/v2/folders"
        if folder_id:
            url += f"/{folder_id}"
        params = {
            "sortType": sort_type,
            "asc": asc,
            "start": start,
            "limit": limit
        }
        headers = self._get_headers(access_token, open_id)
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def delete_folder(self, folder_id, access_token, open_id, list_type="folder", origin_folder_id=None):
        """
        Delete a specific folder or move it to trash.
        """
        url = f"{self.BASE_URL}/openapi/drive/v2/folders/{folder_id}"
        headers = self._get_headers(access_token, open_id)
        params = {
            "listType": list_type
        }
        if list_type == "trash" and origin_folder_id:
            params["originFolderID"] = origin_folder_id

        response = requests.delete(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

