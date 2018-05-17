import os
import iso8601
from visma.utils import import_string, get_api_settings_from_env
from visma.api import VismaAPI
from pprint import pprint


class Manager:
    def __init__(self):

        self.model = None
        self.name = None
        self.endpoint = None
        self.api = None
        self.schema = None

    def register_model(self, model, name):
        self.name = self.name or name
        self.model = model

    def all(self):
        data = self.api._get(self.endpoint).json()
        r_data = data['Data']
        _schema = self.schema()
        return _schema.load(data=r_data, many=True)

    def get(self, pk):

        _endpoint = f'{self.endpoint}/{pk}'

        data = self.api._get(_endpoint).json()
        _schema = self.schema()
        return _schema.load(data=data)





class VismaModelMeta(type):
    """Base metaclass for all VismaModels"""

    def __new__(mcs, name, bases, attrs):

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, VismaModelMeta)]
        if not parents:
            return super().__new__(mcs, name, bases, attrs)


        new_attrs = attrs
        # TODO: add meta data

        new_class = super().__new__(mcs, name, bases, new_attrs)

        attr_meta = attrs.pop('Meta', None)
        meta = attr_meta or getattr(new_class, 'Meta', None)

        manager = Manager()
        manager.register_model(new_class, 'objects')
        manager.endpoint = getattr(meta, 'endpoint')
        manager.schema = import_string(getattr(meta, 'schema'))
        manager.api = VismaAPI.with_token_file(**get_api_settings_from_env())
        new_class.objects = manager

        return new_class
        

class VismaModel(metaclass=VismaModelMeta):

    id = None

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)

    def __str__(self):
        return '%s object (%s)' % (self.__class__.__name__, self.id)


class Customer(VismaModel):

    def __init__(self, customer_number, invoice_city, invoice_postal_code,
                 terms_of_payment, name, is_private_person, is_active, id=None):
        assert isinstance(terms_of_payment, TermsOfPayment)

        self.id = id
        self.customer_number = customer_number
        self.invoice_city = invoice_city
        self.invoice_postal_code = invoice_postal_code
        self.name = name
        self.terms_of_payment = terms_of_payment
        self.is_private_person = is_private_person
        self.is_active = is_active

    class Meta:
        endpoint = '/customers'
        schema = 'visma.schemas.CustomerSchema'


class TermsOfPayment(VismaModel):

    def __init__(self, name, available_for_purchase=None,
                 available_for_sales=None, id=None, name_english=None,
                 type_id=None, type_text=None):

        self.id = id
        self.name = name
        self.available_for_purchase = available_for_purchase
        self.available_for_sales = available_for_sales
        self.name_english = name_english
        self.type_id = type_id
        self.type_text = type_text

    class Meta:
        endpoint = '/termsofpayment'
        schema = 'visma.schemas.TermsOfPaymentSchema'



class CustomerInvoiceDraft(VismaModel):

    def __init__(self, customer_id, customer_name=None, postal_code=None,
                 city=None, rot_reduced_invoicing_type=0, eu_third_party=False,
                 country_code='SE', customer_is_private_person=None, id=None):

        self.id = id
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.postal_code = postal_code
        self.city = city
        self.customer_is_private_person = customer_is_private_person
        self.rot_reduced_invoicing_type = rot_reduced_invoicing_type
        self.eu_third_party = eu_third_party
        self.country_code = country_code

    class Meta:
        endpoint = '/customerinvoicedrafts'
        schema = 'visma.schemas.CustomerInvoiceDraftSchema'

    @classmethod
    def with_customer(cls, customer, *args, **kwargs):
        assert isinstance(customer, Customer)

        return cls(customer_id=customer.id, customer_name=customer.name,
                   postal_code=customer.invoice_postal_code,
                   city=customer.invoice_city,
                   customer_is_private_person=customer.is_private_person,
                   *args, **kwargs)







