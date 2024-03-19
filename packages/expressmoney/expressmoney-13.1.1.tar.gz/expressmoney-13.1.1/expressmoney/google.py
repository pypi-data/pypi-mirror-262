"""
Клиенты для простого доступа к Google Cloud API из приложений Django.
Альтернатива  тяжелым пакетам от Google.
"""

import base64
import json
import os

import requests
from django.utils.module_loading import import_string
from google.auth import default
from google.auth.transport.requests import AuthorizedSession
from rest_framework import status
from rest_framework.status import is_success, HTTP_404_NOT_FOUND


class GoogleCloudServiceError(Exception):
    pass


class VertexAIError(GoogleCloudServiceError):
    pass


def download_object(object_name: str, return_url: bool = False):
    """
    Скачивает файлы с Google Cloud Storage
    @param object_name: Пример pets/dog.png, Символ / заменить на %2F pets%2Fdog.png.
                        Символы требующие замены смотреть здесь
                        https://cloud.google.com/storage/docs/request-endpoints#encoding
    @return: Бинарный файл
    """
    bucket_name = 'expressmoney'
    if object_name[:17] == 'gs://expressmoney':
        object_name = object_name[18:]
    object_name = object_name.replace('/', '%2F')
    url = f'https://storage.googleapis.com/storage/v1/b/{bucket_name}/o/{object_name}?alt=media'
    credentials, project = default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
    authed_session = AuthorizedSession(credentials)
    response = authed_session.get(url)
    if not is_success(response.status_code):
        if response.status_code == HTTP_404_NOT_FOUND:
            raise GoogleCloudServiceError(response.text)
        else:
            raise GoogleCloudServiceError(response.json())
    if return_url:
        return response.content, url
    else:
        return response.content


def get_secret(secret_key):
    endpoint = 'https://secretmanager.googleapis.com'
    project = "1086735462412" if not os.getenv('PROJECT') else os.getenv('PROJECT')
    uri = f'/v1/projects/{project}/secrets/{secret_key}/versions/latest:access'
    url = f'{endpoint}{uri}'
    credentials, project = default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
    authed_session = AuthorizedSession(credentials)
    response = authed_session.get(url)
    if not is_success(response.status_code):
        raise GoogleCloudServiceError(response.json())
    secret_bytes = response.json().get('payload').get('data')
    secret = base64.b64decode(secret_bytes).decode('utf-8')
    return secret


class VertexAI:
    """Google Cloud VertexAI """

    REGION = 'europe-west1'
    PROJECT_ID = '1086735462412'

    def get_score(self):
        if self._action == 'explain':
            self._set_explanations()
        response = self._request()
        predictions = response.json().get('predictions')[0]
        for target_index, target_value in enumerate(predictions['classes']):
            if target_value == 'true':
                score = predictions.get('scores')[target_index]
                return score

        raise VertexAIError("Not found target 'true' in prediction result")

    def _request(self):
        if self.__response is None:
            data = dict()
            data['instances'] = []
            data['instances'].append(self._features_sample)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.bearer}',
            }
            self.__response = requests.post(self.url, json=data, headers=headers)
            if not status.is_success(self.__response.status_code):
                error = f'VertexAI prediction error: {self.__response.status_code}: {self.__response.text}'
                raise VertexAIError(error)
        return self.__response

    def _set_explanations(self):
        """Получить значимость фичей в расчете скора"""
        response = self._request().json()
        target_name = response.get('explanations')[0].get('attributions')[0].get('outputDisplayName')
        explanations = response.get('explanations')[0].get('attributions')[0].get('featureAttributions')
        multiplier = 1000 if target_name == 'true' else -1000
        explanations = {key: multiplier * value for key, value in explanations.items()}
        explanations = {k: v for k, v in sorted(explanations.items(), key=lambda item: item[1], reverse=True)}
        self.explanations = explanations

    @staticmethod
    def _get_token():
        if os.getenv('GAE_APPLICATION'):
            # when we are in GAE env:
            metadata_url = 'http://metadata.google.internal/computeMetadata/v1/'
            metadata_headers = {'Metadata-Flavor': 'Google'}
            service_account = 'default'

            url = '{}instance/service-accounts/{}/token'.format(
                metadata_url, service_account)

            # Request an access token from the metadata server.
            r = requests.get(url, headers=metadata_headers)
            r.raise_for_status()

            # Extract the access token from the response.
            access_token = r.json()['access_token']
        else:
            # when running locally:
            stream = os.popen('gcloud auth application-default print-access-token')
            access_token = stream.read().strip()

        return access_token

    def __init__(self, endpoint_id, features_sample: dict, action='predict'):
        self.explanations = None
        self._action = action
        self.endpoint_id = endpoint_id
        self.url = f'https://{self.REGION}-aiplatform.googleapis.com/v1/projects/{self.PROJECT_ID}/locations/' \
                   f'{self.REGION}/endpoints/{self.endpoint_id}:{action}'
        self.bearer = self._get_token()
        self._features_sample = features_sample
        self.__response = None


class Tasks:
    """Google Cloud Tasks"""

    SERVICE_ENDPOINT = 'https://cloudtasks.googleapis.com'
    SERVICE_ENDPOINT_URI = '/v2/projects/expressmoney/locations/europe-west1/queues/default/tasks/'

    def __init__(self, service: str, uri: str, user: None, ):
        """
        Укажите параметры точки сервиса Expressmoney к которому будет направлен запрос.
        Args:
            service (str): Название сервис ExpressMoney. Пример: loans
            service (str): Путь до точки. Пример: /orders/order . Слэш в начале и нет в конце
            user (None, int, User): От имени какого юзера будет авторизован запрос.
        """

        credentials, _ = default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
        self.authed_session = AuthorizedSession(credentials)
        self._response = None
        self._create_task(service, uri)
        self._add_access_token(user)

    def post(self, payload: dict):
        self._add_http_method('POST')
        self._add_body(payload)
        self._request()

    def get(self):
        self._add_http_method('GET')
        self._request()

    def put(self, payload: dict):
        self._add_http_method('PUT')
        self._add_body(payload)
        self._request()

    def _request(self):
        self._response = self.authed_session.post(self._servie_url, json.dumps(self._task))
        if not is_success(self._response.status_code):
            raise GoogleCloudServiceError(self._response.json())

    @property
    def _servie_url(self):
        return f'{self.SERVICE_ENDPOINT}{self.SERVICE_ENDPOINT_URI}'

    def _create_task(self, service, uri):
        self._task = {
            'task': {
                'appEngineHttpRequest': {
                    'appEngineRouting': {
                        'service': service
                    },
                    'relativeUri': uri,
                    'headers': {'Content-Type': 'application/json'},
                },
            },
        }

    def _add_access_token(self, user):
        get_user_model = import_string('django.contrib.auth.get_user_model')
        refresh_token_class = import_string('rest_framework_simplejwt.tokens.RefreshToken')
        user_class = get_user_model()
        user = None if user is None else user if isinstance(user, user_class) else user_class.objects.get(pk=user)
        if user:
            access_token = refresh_token_class.for_user(user).access_token
            headers = self._task['task']['appEngineHttpRequest']['headers']
            headers.update({'X-Forwarded-Authorization': f'Bearer {access_token}'})

    def _add_http_method(self, http_method):
        self._task['task']['appEngineHttpRequest'].update({'httpMethod': http_method})

    def _add_body(self, payload: dict):
        payload_json = json.dumps(payload)
        payload_string_bytes = payload_json.encode('ascii')
        payload_bytes = base64.b64encode(payload_string_bytes)
        body = payload_bytes.decode('ascii')
        self._task['task']['appEngineHttpRequest'].update({'body': body})
