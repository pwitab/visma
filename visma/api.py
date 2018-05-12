import json
import datetime
import iso8601
import requests

from pprint import pprint

from .schemas import CustomerSchema, CustomerInvoiceDraftSchema


class VismaAPIException(Exception):
    """An error occurred in the Visma API """
    pass


class VismaClientException(Exception):
    """An error occured in the Visma Client"""
    pass


class VismaAPI:
    """
    Class containing methods to interact with the Visma E-Accounting API
    """

    TOKEN_URL_TEST = 'https://identity-sandbox.test.vismaonline.com/connect/token'
    TOKEN_URL = 'https://identity.vismaonline.com/connect/token'

    API_URL = 'https://eaccountingapi.vismaonline.com/v2'
    API_URL_TEST = 'https://eaccountingapi-sandbox.test.vismaonline.com/v2'

    def __init__(self, client_id, client_secret, token_path=None,
                 access_token=None, refresh_token=None, token_expires=None,
                 test=False):

        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.refresh_token = None
        self.token_expires = None
        self.token_path = token_path
        self.test = test

        if token_path is not None:
            self._load_tokens()
            if self.token_expired:
                self._refresh_token()
        else:
            self.access_token = access_token
            self.refresh_token = refresh_token
            self.token_expires = token_expires

    # TODO: Can I make a decorator to handle errors from the API?

    def _get(self, endpoint, params=None, **kwargs):

        url = self._format_url(endpoint)
        r = requests.get(url, params, headers=self.api_headers, **kwargs)
        return r

    def _post(self, endpoint, data, *args, **kwargs):
        url = self._format_url(endpoint)
        r = requests.post(url, data, *args, headers=self.api_headers, **kwargs)
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
                                    f'{response.content}')
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

    def get_accounts(self):

        accounts = self._get('/accounts').json()
        return accounts

    def get_customer_invoices(self):
        return self._get('/customerinvoices').json()

    def get_company_settings(self):
        return self._get('/companysettings').json()

    def new_customer_invoice_draft(self, invoice_draft):
        schema = CustomerInvoiceDraftSchema()

        data = json.dumps(schema.dump(invoice_draft))

        pprint(data)

        resp = self._post('/customerinvoicedrafts', data=data)

        return resp.json()

    def get_customer_invoice_drafts(self):
        r = self._get('/customerinvoicedrafts')

        r_data = r.json()
        pprint(r_data)
        schema = CustomerInvoiceDraftSchema()
        invoices = schema.load(data=r_data['Data'], many=True)

        return invoices

    def get_customer(self, customer_number):
        response = self._get(
            f"/customers?$filter= CustomerNumber eq '{customer_number}'")

        response_data = response.json()
        pprint(response_data)

        customer_schema = CustomerSchema()
        customer = customer_schema.load(data=response_data['Data'][0])

        return customer

    # TODO: Make a general way of passing filtering options.

