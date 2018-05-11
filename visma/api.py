import json
import datetime
import iso8601
import requests

class VismaAPIException(BaseException):
    """An error occurred in the Visma API Client """

class VismaAPI:
    """
    Class containing methods to interact with the Visma E-Accounting API
    """

    TOKEN_URL_TEST = 'https://identity-sandbox.test.vismaonline.com/connect/token'
    TOKEN_URL = 'https://identity.vismaonline.com/connect/token'

    API_URL = 'https://eaccountingapi.vismaonline.com/v2'
    API_URL_TEST = 'https://eaccountingapi-sandbox.test.vismaonline.com/v2'

    def __init__(self, client_id, client_secret, cred_path, test=False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.cred_path = cred_path
        self.access_token = None
        self.refresh_token = None
        self.token_expires = None
        self.test = test

        self._load_credentials()
        if self.token_expired:
            self._refresh_token()

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
                                    f'{response.content}')
        else:
            auth_info = response.json()

            self.access_token = auth_info['access_token']
            self.refresh_token = auth_info['refresh_token']

            now = datetime.datetime.now(tz=datetime.timezone.utc)
            # removes a minute so we don't end up not being authenticated
            # because of time difference between client and server.
            expires = now + datetime.timedelta(
                seconds=(auth_info['expires_in'] - 60))
            self.token_expires = expires

        self._save_credentials()

    def _load_credentials(self, ):
        with open(self.cred_path) as cred_file:
            tokens = json.load(cred_file)
            self.access_token = tokens['access_token']
            self.refresh_token = tokens['refresh_token']
            self.token_expires = iso8601.parse_date(tokens['expires'])

    def _save_credentials(self):
        tokens = {'access_token': self.access_token,
                  'refresh_token': self.refresh_token,
                  'expires': self.token_expires.isoformat()}

        with open(self.cred_path, 'w') as cred_file:
            json.dump(tokens, cred_file)
