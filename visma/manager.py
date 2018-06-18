import json
import logging

from visma.api import VismaClientException

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

    def register_model(self, model, name):
        self.name = self.name or name
        self.model = model

    def register_schema(self, schema_klass):
        self._schema = schema_klass
        self.schema = self._schema()

    def verify_method(self, method):
        if method not in self.allowed_methods:
            raise VismaClientException(
                f'{method} is not an allowed method on this '
                'object')

    def all(self):
        self.verify_method('LIST')
        data = self.api.get(self.endpoint).json()
        r_data = data['Data']
        logger.debug(f'Received: {r_data}')
        return self.schema.load(data=r_data, many=True)

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


