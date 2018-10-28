import json
import datetime
import iso8601
import requests
from os import environ

from marshmallow import fields

from visma.query import QueryCompiler, FilterParser


class GreaterThanFilterParser(FilterParser):

    def parse(self):
        return f'{self.field.data_key} gt {self.value}'


class GreaterOrEqualThanFilterParser(FilterParser):

    def parse(self):
        return f'{self.field.data_key} ge {self.value}'


class LessThanFilterParser(FilterParser):

    def parse(self):
        return f'{self.field.data_key} lt {self.value}'


class LessOrEqualThanFilterParser(FilterParser):

    def parse(self):
        return f'{self.field.data_key} le {self.value}'


class EqualFilterParser(FilterParser):

    def parse(self):
        if isinstance(self.field, fields.UUID):
            return f'{self.field.data_key} eq {self.value}'

        elif isinstance(self.field, fields.String):
            return f'{self.field.data_key} eq \'{self.value}\''

        else:
            return f'{self.field.data_key} eq {self.value}'


class NotEqualFilterParser(FilterParser):

    def parse(self):
        if isinstance(self.value, str):
            return f'{self.field.data_key} ne {self.value}'
        else:
            return f'{self.field.data_key} ne {self.value}'


class OrderByFilterParser(FilterParser):

    def parse(self):
        return self.field.data_key


class VismaQueryCompiler(QueryCompiler):
    equals_parser_class = EqualFilterParser
    not_equals_parser_class = NotEqualFilterParser
    greater_than_parser_class = GreaterThanFilterParser
    greater_or_equal_parser_class = GreaterOrEqualThanFilterParser
    less_than_parser_class = LessThanFilterParser
    less_or_equal_parser_class = LessOrEqualThanFilterParser
    order_by_parser_class = OrderByFilterParser


class VismaAPIException(Exception):
    """An error occurred in the Visma API """
    pass


class VismaClientException(Exception):
    """An error occurred in the Visma Client"""
    pass


class VismaAPI:
    """
    Class containing methods to interact with the Visma E-Accounting API
    """

    TOKEN_URL_TEST = 'https://identity-sandbox.test.vismaonline.com/connect/token'
    TOKEN_URL = 'https://identity.vismaonline.com/connect/token'

    API_URL = 'https://eaccountingapi.vismaonline.com/v2'
    API_URL_TEST = 'https://eaccountingapi-sandbox.test.vismaonline.com/v2'

    QUERY_COMPILER_CLASS = VismaQueryCompiler

    def __init__(self, client_id, client_secret,
                 access_token, refresh_token, token_expires, token_path=None,
                 test=False):

        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires = token_expires
        self.token_path = token_path
        self.test = test

        if self.token_expired:
            self._refresh_token()

    # TODO: Can I make a decorator to handle errors from the API?

    def get(self, endpoint, params=None, **kwargs):
        url = self._format_url(endpoint)
        headers = self.api_headers

        r = requests.get(url, params, headers=headers, **kwargs)
        if not r.ok:
            raise VismaAPIException(
                f'GET {r.request.url} :: HTTP:{r.status_code}, {r.content}')
        return r

    def post(self, endpoint, data, *args, **kwargs):
        url = self._format_url(endpoint)
        r = requests.post(url, data, *args, headers=self.api_headers, **kwargs)
        if not r.ok:
            raise VismaAPIException(
                f'POST :: HTTP:{r.status_code}, {r.content}')
        return r

    def put(self, endpoint, data, **kwargs):
        url = self._format_url(endpoint)
        r = requests.put(url, data, headers=self.api_headers, **kwargs)
        if not r.ok:
            raise VismaAPIException(
                f'PUT :: HTTP:{r.status_code}, {r.content}')
        return r

    def delete(self, endpoint, **kwargs):
        url = self._format_url(endpoint)
        r = requests.delete(url, headers=self.api_headers, **kwargs)
        if not r.ok:
            raise VismaAPIException(
                f'DELETE :: HTTP:{r.status_code}, {r.content}')
        return r

    def _format_url(self, endpoint):
        if self.test:
            url = self.API_URL_TEST + endpoint
        else:
            url = self.API_URL + endpoint
        return url

    @property
    def api_headers(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json'
        }
        return headers

    @property
    def token_expired(self):
        if datetime.datetime.now(tz=datetime.timezone.utc) > self.token_expires:
            return True
        else:
            return False

    def _refresh_token(self):

        if self.test:
            url = self.TOKEN_URL_TEST
        else:
            url = self.TOKEN_URL

        data = f'grant_type=refresh_token&refresh_token={self.refresh_token}'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        response = requests.post(url, data,
                                 auth=(self.client_id, self.client_secret),
                                 headers=headers)

        if response.status_code != 200:
            raise VismaAPIException(f'Couldn\'t refresh token: '
                                    f'{response.content}, Client_id={self.client_id}')
        else:
            auth_info = response.json()

            self.access_token = auth_info['access_token']
            self.refresh_token = auth_info['refresh_token']

            now = datetime.datetime.now(tz=datetime.timezone.utc)
            # removes a minute so we don't end up not being authenticated
            # because of time difference between client and server.
            expiry_time = datetime.timedelta(
                seconds=(auth_info['expires_in'] - 60))
            expires = now + expiry_time
            self.token_expires = expires

        self._save_tokens()

    def _load_tokens(self):
        """
        Load tokens from json file
        """
        with open(self.token_path) as cred_file:
            tokens = json.load(cred_file)
            self.access_token = tokens['access_token']
            self.refresh_token = tokens['refresh_token']
            self.token_expires = iso8601.parse_date(tokens['expires'])

    def _save_tokens(self):
        """
        Save tokens to json file
        """
        tokens = {'access_token': self.access_token,
                  'refresh_token': self.refresh_token,
                  'expires': self.token_expires.isoformat()}

        with open(self.token_path, 'w') as token_file:
            json.dump(tokens, token_file)

    @classmethod
    def load(cls):
        """
        Load tokens from json file
        """

        env = cls.get_api_settings_from_env()

        access_token = None
        refresh_token = None
        token_expires = None

        if env['token_path'] is not None:

            with open(env['token_path']) as token_file:
                tokens = json.load(token_file)
                access_token = tokens['access_token']
                refresh_token = tokens['refresh_token']
                token_expires = iso8601.parse_date(tokens['expires'])

        return cls(env['client_id'], env['client_secret'],
                   access_token=access_token,
                   refresh_token=refresh_token,
                   token_expires=token_expires,
                   token_path=env['token_path'],
                   test=env['test'])

    @staticmethod
    def get_api_settings_from_env():
        settings = {'token_path': environ.get('VISMA_API_TOKEN_PATH'),
                    'client_id': environ.get('VISMA_API_CLIENT_ID'),
                    'client_secret': environ.get('VISMA_API_CLIENT_SECRET')}

        if environ.get('VISMA_API_ENV') == 'test':
            settings['test'] = True

        else:
            settings['test'] = False

        return settings

class NoAPI:

    @classmethod
    def load(cls):
        return cls

