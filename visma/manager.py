import json
from pprint import pprint

from visma.api import VismaClientException


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
        pprint(r_data)
        pprint(self.schema)
        return self.schema.load(data=r_data, many=True)

    def get(self, pk):
        self.verify_method('GET')
        _endpoint = f'{self.endpoint}/{pk}'
        data = self.api.get(_endpoint).json()
        pprint(data)
        obj = self.schema.load(data)
        return obj

    def create(self, obj):
        self.verify_method('CREATE')
        data = self.schema.dump(obj)
        pprint(data)
        result = self.api.post(self.endpoint, json.dumps(data))
        pprint(result.json())
        new_obj = self.schema.load(result.json())
        return new_obj

    def update(self, obj):
        self.verify_method('UPDATE')
        pk = obj.id
        _endpoint = f'{self.endpoint}/{pk}'
        pprint(f'PUT {_endpoint}')
        data = self.schema.dump(obj)
        pprint(data)
        result = self.api.put(_endpoint, json.dumps(data))
        pprint(result.json())
        return result

    def delete(self, pk):
        self.verify_method('DELETE')
        _endpoint = f'{self.endpoint}/{pk}'
        result = self.api.delete(_endpoint)
        return result


