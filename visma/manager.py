import json
import logging

from visma.api import VismaClientException

logger = logging.getLogger(__name__)
import pprint

class Manager:
    def __init__(self):
        self.model = None
        self.name = None
        self.endpoint = None
        self.api = None
        self.allowed_methods = list()
        self.schema = None
        self._schema = None
        self.envelope = None
        self._envelope = None
        self.envelope_on = list()

    def register_model(self, model, name):
        self.name = self.name or name
        self.model = model

    def register_schema(self, schema_klass):
        self._schema = schema_klass
        self.schema = self._schema()

    def register_envelope(self, envelope_klass):
        self._envelope = envelope_klass._schema_klass
        self.envelope = self._envelope()

    def verify_method(self, method):
        if method not in self.allowed_methods:
            raise VismaClientException(
                f'{method} is not an allowed method on this '
                'object')

    def use_envelope(self, method):
        return method in self.envelope_on

    def all(self):
        self.verify_method('LIST')
        in_data = self.api.get(self.endpoint).json()
        logger.debug(f'Received: {in_data}')
        pprint.pprint(in_data)
        if self.use_envelope('LIST'):
            objs = self.envelope.load(in_data).data
        else:
            objs = self.schema.load(data=in_data, many=True)
        return objs

    def get(self, pk):
        self.verify_method('GET')
        _endpoint = f'{self.endpoint}/{pk}'
        data = self.api.get(_endpoint).json()
        logger.debug(f'Received: {data}')
        obj = self.schema.load(data)
        return obj

    def create(self, obj):
        self.verify_method('CREATE')
        out_data = self.schema.dump(obj)
        logger.debug(f'Sending: {out_data}')
        result = self.api.post(self.endpoint, json.dumps(out_data))
        in_data = result.json()
        logger.debug(f'Received {in_data}')
        new_obj = self.schema.load(in_data)
        return new_obj

    def update(self, obj):
        self.verify_method('UPDATE')
        pk = obj.id
        _endpoint = f'{self.endpoint}/{pk}'
        out_data = self.schema.dump(obj)
        logger.debug(f'Sending {out_data}')
        result = self.api.put(_endpoint, json.dumps(out_data))
        in_data = result.json()
        logger.debug(f'Received {in_data}')
        updated_obj = self.schema.load(in_data)
        return updated_obj

    def delete(self, pk):
        self.verify_method('DELETE')
        _endpoint = f'{self.endpoint}/{pk}'
        logger.debug(f'Deleting object at: {_endpoint}')
        result = self.api.delete(_endpoint)
        return result


