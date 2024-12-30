from .auth_api import AuthAPI
from .file_mgr_api import DocAPI


class QQDocAPI(DocAPI, AuthAPI):
    def __init__(self, client_id, client_secret, token_cache_file="cache.json"):
        super().__init__(client_id, client_secret, token_cache_file)


__all__ = ['QQDocAPI']
