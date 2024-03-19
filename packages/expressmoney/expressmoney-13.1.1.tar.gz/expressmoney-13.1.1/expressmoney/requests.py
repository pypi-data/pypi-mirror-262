"""
Клиент для http-запросов к сервисам expressmoney c автоматической авторизацией в Identity-Aware Proxy
"""

__all__ = ('Request',)

import os
import abc
import datetime
import re
from contextlib import suppress
from typing import Union
from urllib.parse import urlencode

import requests
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token


def is_informational(code):
    return 100 <= code <= 199


def is_success(code):
    return 200 <= code <= 299


def is_redirect(code):
    return 300 <= code <= 399


def is_client_error(code):
    return 400 <= code <= 499


def is_server_error(code):
    return 500 <= code <= 599


class _HttpClient(abc.ABC):
    """Abstract HTTP client"""

    _client = None
    _project = 'expressmoney' if os.getenv('IS_PROD_REQUESTS') or os.getenv('GAE_APPLICATION') else 'expressmoney-dev-1'

    def __init__(self,
                 service: str = None,
                 path: str = '/',
                 query_params: Union[None, dict] = None,
                 access_token: str = None,
                 timeout: tuple = (30, 30),
                 version: str = None,
                 ):
        """
        Common params for all http clients
        Args:
            service: 'default'
            path: '/user'
            access_token: 'Bearer DFD4345345D'
        """
        self._service = service
        self._path = path
        self._query_params = query_params
        self._access_token = access_token
        self._timeout = timeout
        self._version = version

    @abc.abstractmethod
    def get(self):
        pass

    @abc.abstractmethod
    def post(self, payload: dict):
        pass

    @abc.abstractmethod
    def put(self, payload: dict):
        pass


class Request(_HttpClient):
    """Base HTTP Client"""

    def get(self, url=None):
        response = requests.get(url if url else self.url, headers=self._headers, timeout=self._timeout)
        return response

    def delete(self):
        response = requests.delete(self.url, headers=self._headers, timeout=self._timeout)
        return response

    def post(self, payload: dict):
        response = requests.post(self.url, json=payload, headers=self._headers, timeout=self._timeout)
        return response

    def put(self, payload: dict = None):
        payload = {} if payload is None else payload
        response = requests.put(self.url, json=payload, headers=self._headers, timeout=self._timeout)
        return response

    def post_file(self, file, file_name: str, type_: int = 1, is_public=False):
        """
        Save file in Google Storage
        Args:
            file: BytesIO file
            file_name: "name_file.pdf"
            type_: 1 - other files. All types see in storage service
            is_public: True - access to file without auth.

        Returns:

        """
        if len(file_name.split('.')) == 0:
            raise Exception('File name in format "name_file.pdf"')

        ext = file_name.split('.')[-1]
        name = ''
        for value in file_name.split('.')[0:-1]:
            name += value
        name = f'{name}_{datetime.datetime.now().timestamp()}'
        name = re.sub('[^0-9a-zA-Z_]', '', name)
        new_file_name = f'{name}.{ext}'
        data = {
            'name': name,
            'type': type_,
            'is_public': is_public,

        }

        with suppress(Exception):
            file = getattr(file, 'file')

        response = requests.post(
            url=self.url,
            data=data,
            files={"file": (new_file_name, file)},
            headers=self._headers,
            timeout=self._timeout
        )
        if not any((is_success(response.status_code), is_client_error(response.status_code))):
            try:
                raise Exception(f'{response.status_code}:{response.url}:{response.json()}')
            except Exception:
                raise Exception(f'{response.status_code}:{response.url}:{response.text}')
        return response

    @property
    def url(self):
        local_url = 'http://127.0.0.1:8000'
        domain = f'https://{self._service}-dot-{self._project}.appspot.com' if self._service else local_url
        url = f'{domain}{self._path}'
        url_with_params = url if self._query_params is None else f'{url}?{urlencode(self._query_params)}'
        return url_with_params

    @property
    def _headers(self):
        headers = dict()
        headers.update(self._get_authorization())
        if self._version:
            headers.update({'Accept': f'application/json; version={self._version}'})
        return headers

    def _get_authorization(self) -> dict:
        authorization = {'X-Forwarded-Authorization': f'Bearer {self._access_token}'} if self._access_token else {}
        open_id_connect_token = id_token.fetch_id_token(GoogleRequest(), self._get_iap_client_id())
        iap_token = {'Authorization': f'Bearer {open_id_connect_token}'}
        authorization.update(iap_token)
        return authorization

    @staticmethod
    def _get_iap_client_id():
        return '1086735462412-c11726ttrnh7t33elp4gciine1uog21a.apps.googleusercontent.com'
