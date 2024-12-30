# https://docs.qq.com/open/document/app/openapi/v2/file/
import os
import time

import requests

from .base import QQDocAPIBase


def _get_file_md5(file_path):
    """
    Calculate the MD5 hash of a file.
    """
    import hashlib
    with open(file_path, "rb") as file:
        md5 = hashlib.md5()
        while chunk := file.read(8192):
            md5.update(chunk)
    return md5.hexdigest()


class DocAPI(QQDocAPIBase):

    def __init__(self, client_id, client_secret, token_cache_file="cache.json"):
        super().__init__(client_id, client_secret, token_cache_file)

    def get_file_permission(self, file_id):
        """
        Get the permission details of a specific file.
        """
        url = f"{self.API_URL}/files/{file_id}/permission"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def create_folder(self, title, parent_folder=None):
        """
        Create a new folder with the specified title.
        """
        url = f"{self.API_URL}/folders"
        headers = self._get_headers()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = {
            "title": title
        }
        if parent_folder:
            data["parentfolderID"] = parent_folder

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()['data']
        else:
            response.raise_for_status()

    def get_folder_metadata(self, folder_id):
        """
        Retrieve metadata of a specific folder.
        """
        url = f"{self.API_URL}/folders/{folder_id}/metadata"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def list_folder_contents(self, folder_id=None, sort_type="browse", asc=0, start=0, limit=20):
        """
        List the contents of a folder with optional sorting and pagination.
        """
        url = f"{self.API_URL}/folders"
        if folder_id:
            url += f"/{folder_id}"
        params = {
            "sortType": sort_type,
            "asc": asc,
            "start": start,
            "limit": limit
        }
        headers = self._get_headers()
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", {}).get("list", [])
        else:
            response.raise_for_status()

    def delete_folder(self, folder_id, list_type="folder", origin_folder_id=None):
        """
        Delete a specific folder or move it to trash.
        """
        url = f"{self.API_URL}/folders/{folder_id}"
        headers = self._get_headers()
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

    def get_folder_by_name(self, folder_name):
        """
        Get the folder metadata by folder name.
        """
        folder_list = self.list_folder_contents()
        ret = []
        for folder in folder_list:
            if folder["title"] == folder_name:
                ret.append(folder)
        return ret

    def create_folder_if_not_exist(self, folder_name):
        """
        Create a folder if it does not exist.
        """
        folder_list = self.get_folder_by_name(folder_name)
        if not folder_list:
            return self.create_folder(folder_name)
        return folder_list[0]

    def create_import_info(self, file_md5, file_name, file_size, upload_type=None):
        """
        Create import information for uploading a document.
        """
        url = f"{self.API_URL}/files/upload-url"
        headers = self._get_headers()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        data = {
            "fileMD5": file_md5,
            "fileName": file_name,
            "fileSize": file_size,
        }
        if upload_type:
            data["uploadType"] = upload_type

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def upload_file_to_cos(self, file_path, cos_put_url):
        """
        Upload a file to COS using the provided URL.
        """
        headers = {'Content-Type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
        with open(file_path, 'rb') as file:
            try:
                response = requests.put(cos_put_url, headers=headers, data=file)
                if response.status_code == 200:
                    return response.text
            except Exception as e:
                print("Failed to upload file to COS: %s" % str(e))
                response.raise_for_status()

    def async_import_document(self, file_md5, file_name, cos_file_key, parent_folder_id=None, file_password=None):
        """
        Asynchronously import a document after successful upload to Tencent Cloud COS.
        """
        url = f"{self.API_URL}/files/async-import"
        headers = self._get_headers()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        data = {
            "fileMD5": file_md5,
            "fileName": file_name,
            "COSFileKey": cos_file_key
        }
        if parent_folder_id:
            data["parentfolderID"] = parent_folder_id
        if file_password:
            data["filePassword"] = file_password

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_import_progress(self, progress_query_id):
        """
        Query the import progress of a document.
        """
        url = f"{self.API_URL}/files/import-progress"
        headers = self._get_headers()
        params = {
            "progressQueryID": progress_query_id
        }

        while True:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                if response.json()["ret"] != 0 or response.json()["data"].get("ID", None) is None:
                    print("uploading...")
                    time.sleep(1)
                    continue
                return response.json()["data"]
            else:
                response.raise_for_status()

    def upload_file(self, file_path, parent_folder_id=None, file_password=None):
        """
        Upload a file to QQDocs.
        """
        file_md5 = _get_file_md5(file_path)
        file_name = file_path.split("/")[-1]
        cos_info = self.create_import_info(file_md5, file_name, file_size=os.path.getsize(file_path))
        cos_put_url, cos_file_key = cos_info["data"]["COSPutURL"], cos_info["data"]["COSFileKey"]
        self.upload_file_to_cos(file_path, cos_put_url)
        import_info = self.async_import_document(file_md5, file_name, cos_file_key, parent_folder_id, file_password)
        progress_query_id = import_info["data"]["progressQueryID"]
        return self.get_import_progress(progress_query_id)

    # --- 文档权限 ---
    def get_file_access(self, file_id):
        """
        Get the access permissions of a specific file.
        """
        url = f"{self.API_URL}/files/{file_id}/access"
        headers = self._get_headers()

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            response.raise_for_status()

    def add_collaborators(self, file_id, collaborators):
        """
        Add collaborators to a specific file.
        """
        url = f"{self.API_URL}/files/{file_id}/collaborators"
        headers = self._get_headers()
        headers["Content-Type"] = "application/json"

        data = {
            "collaborators": collaborators
        }

        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def set_file_permission(self, file_id, policy=None, copy_enabled=True, reader_comment_enabled=True):
        """
        Set the sharing permissions of a specific file.
        """
        url = f"{self.API_URL}/files/{file_id}/permission"
        headers = self._get_headers()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        data = {
            "copyEnabled": copy_enabled,
            "readerCommentEnabled": reader_comment_enabled
        }
        if policy:
            data["policy"] = policy

        response = requests.patch(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_collaborators(self, file_id):
        """
        Query the list of collaborators for a specific file.
        """
        url = f"{self.API_URL}/files/{file_id}/collaborators"
        headers = self._get_headers()

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]["collaborators"]
        else:
            response.raise_for_status()
