import json
import logging

from visma.api import VismaClientException
from visma.query import APIQuerySet

logger = logging.getLogger(__name__)


class Manager:

    def __init__(self):
        self.model = None
        self.name = None
        self.endpoint = None
        self.api = None
        self.allowed_methods = list()
        self.schema = None
        self._schema = None
        self.envelopes = dict()

    def register_model(self, model, name):
        self.name = self.name or name
        self.model = model

    def register_schema(self, schema_klass):
        self._schema = schema_klass
        self.schema = self._schema()

    def register_envelope(self, method, envelope_klass):
        self.envelopes[method.upper()] = envelope_klass._schema_klass()

    def verify_method(self, method):
        if method not in self.allowed_methods:
            raise VismaClientException(
                f'{method} is not an allowed method on this '
                'object')

    def use_envelope(self, method):
        return method in self.envelopes.keys()

    def _get_query_set(self, *args, **kwargs):
        return APIQuerySet(model=self.model, api=self.api, schema=self.schema, *args, **kwargs)

    def new_all(self):
        return self._get_query_set(envelope=self.envelopes['LIST'])

    def new_filter(self, **kwargs):
        return self._get_query_set(envelope=self.envelopes['LIST']).filter(**kwargs)

    def new_exclude(self, **kwargs):
        return self._get_query_set(envelope=self.envelopes['LIST']).exclude(**kwargs)

    # TODO: Should get, create update and delete also return querysets?
    # Then need to implement the handling of them

    def all(self, method='LIST'):
        self.verify_method(method)
        in_data = self.api.get(self.endpoint).json()
        logger.debug(f'Received: {in_data}')
        if self.use_envelope(method):
            objs = self.envelopes[method].load(in_data).data
        else:
            objs = self.schema.load(data=in_data, many=True)
        return objs

    def get(self, pk, method='GET'):
        self.verify_method(method)
        _endpoint = f'{self.endpoint}/{pk}'
        data = self.api.get(_endpoint).json()
        logger.debug(f'Received: {data}')
        obj = self.schema.load(data)
        return obj

    def create(self, obj, method='CREATE'):
        self.verify_method(method)
        out_data = self.schema.dump(obj)
        logger.debug(f'Sending: {out_data}')
        result = self.api.post(self.endpoint, json.dumps(out_data))
        in_data = result.json()
        logger.debug(f'Received {in_data}')
        new_obj = self.schema.load(in_data)
        return new_obj

    def update(self, obj, method='UPDATE'):
        self.verify_method(method)
        pk = obj.id
        _endpoint = f'{self.endpoint}/{pk}'
        out_data = self.schema.dump(obj)
        logger.debug(f'Sending {out_data}')
        result = self.api.put(_endpoint, json.dumps(out_data))
        in_data = result.json()
        logger.debug(f'Received {in_data}')
        updated_obj = self.schema.load(in_data)
        return updated_obj

    def delete(self, pk, method='DELETE'):
        self.verify_method(method)
        _endpoint = f'{self.endpoint}/{pk}'
        logger.debug(f'Deleting object at: {_endpoint}')
        result = self.api.delete(_endpoint)
        return result


