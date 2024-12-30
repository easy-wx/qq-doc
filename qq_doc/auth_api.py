# https://docs.qq.com/open/document/app/oauth2/

"""
鉴权接口封装，用于用户相关的openid、access_token、refresh_token等信息的获取。
其长期保存和维护，需要开发者根据自己的存储情况，进行设计。
"""

from urllib.parse import urlencode

import requests

from .base import QQDocAPIBase


class AuthAPI(QQDocAPIBase):
    def __init__(self, client_id, client_secret, token_cache_file="cache.json"):
        super().__init__(client_id, client_secret, token_cache_file)

    def authorize(self, redirect_uri, state=None):
        """
        Initiate Tencent Docs OAuth2.0 authorization.
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "all"
        }
        if state:
            params["state"] = state

        request_url = f"{self.OAUTH_URL}?{urlencode(params)}"
        return request_url

    def get_user_access_token(self, code, redirect_uri):
        """
        Retrieve the Access Token and Refresh Token using the authorization code.
        https://docs.qq.com/open/document/app/oauth2/access_token.html
        """
        url = f"{self.BASE_URL}/oauth/v2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
            "code": code
        }
        response = requests.get(url, params=params, headers={"Accept": "application/json"})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_user_info(self, access_token):
        """
        Retrieve user information using the access token.
        https://docs.qq.com/open/document/app/oauth2/user_info.html
        """
        url = f"{self.BASE_URL}/oauth/v2/userinfo"
        params = {
            "access_token": access_token
        }
        response = requests.get(url, params=params, headers={"Accept": "application/json"})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def refresh_access_token(self, refresh_token):
        """
        Refresh the Access Token using the refresh token.
        """
        url = f"{self.BASE_URL}/oauth/v2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        response = requests.get(url, params=params, headers={"Accept": "application/json"})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
