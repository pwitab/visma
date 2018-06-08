import os
import iso8601
from visma.utils import import_string, get_api_settings_from_env
from visma.api import VismaAPI
from pprint import pprint
import json
from marshmallow.base import FieldABC
from marshmallow import Schema, post_load
from marshmallow.utils import _Missing
from marshmallow import fields
import copy


class VismaSchema(Schema):
    visma_model = None

    @post_load
    def make_instance(self, data):
        pprint(data)
        return self.visma_model(**data)


def is_instance_or_subclass(val, class_):
    """Return True if ``val`` is either a subclass or instance of ``class_``."""
    try:
        return issubclass(val, class_)
    except TypeError:
        return isinstance(val, class_)


def _get_fields(attrs, field_class):
    fields = [
        (field_name, field_value)
        for field_name, field_value in attrs.items()
        if is_instance_or_subclass(field_value, field_class)
    ]

    return fields


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
        data = self.api.get(self.endpoint).json()
        r_data = data['Data']
        _schema = self.schema()
        pprint(r_data)
        pprint(_schema)
        return _schema.load(data=r_data, many=True)

    def get(self, pk):
        _endpoint = f'{self.endpoint}/{pk}'

        data = self.api.get(_endpoint).json()
        pprint(data)
        _schema = self.schema()
        obj = _schema.load(data)
        return obj

    def create(self, obj):
        _schema = self.schema()
        data = _schema.dump(obj)
        pprint(data)
        result = self.api.post(self.endpoint, json.dumps(data))

        pprint(result.json())
        new_obj = _schema.load(result.json())

        return new_obj

    def update(self, obj):
        pk = obj.id
        _endpoint = f'{self.endpoint}/{pk}'

        _schema = self.schema()
        data = _schema.dump(obj)
        result = self.api.put(_endpoint, json.dumps(data))

        pprint(result.json())
        return result

    def delete(self, pk):
        _endpoint = f'{self.endpoint}/{pk}'

        result = self.api.delete(_endpoint)

        return result

    def _delete(self, obj):
        pk = obj.id
        _endpoint = f'{self.endpoint}/{pk}'

        result = self.api.delete(_endpoint)

        return result


class VismaModelMeta(type):
    """Base metaclass for all VismaModels"""

    def __new__(mcs, name, bases, attrs):

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, VismaModelMeta)]
        if not parents:
            return super().__new__(mcs, name, bases, attrs)

        schema_attrs = _get_fields(attrs, FieldABC)
        # print(f'All attrs: {attrs}')

        # print(f'Schema attrs: {schema_attrs}')

        new_attrs = attrs
        # TODO: add meta data

        new_class = super().__new__(mcs, name, bases, new_attrs)
        schema_name = name + 'Schema'
        schema_dict = dict(schema_attrs)
        new_class._schema_items = dict(schema_attrs)
        schema_dict['visma_model'] = new_class

        schema_klass = type(schema_name, (VismaSchema,), schema_dict)

        attr_meta = attrs.pop('Meta', None)
        meta = attr_meta or getattr(new_class, 'Meta', None)
        try:
            endpoint = getattr(meta, 'endpoint')
            manager = Manager()
            manager.register_model(new_class, 'objects')
            manager.endpoint = endpoint
            manager.schema = schema_klass
            manager.api = VismaAPI.with_token_file(
                **get_api_settings_from_env())
            new_class.objects = manager

        except AttributeError:
            pass

        return new_class


class VismaModel(metaclass=VismaModelMeta):
    id = None

    def __init__(self, *args, **kwargs):
        self.schema_fields = copy.deepcopy(self._schema_items)
        # TODO: go throuhg and create all items and fill them with data.

        # There is two ways to create the object. Either directly suing
        # ModelName(etc) or we get a new object from the APIs serializer. Both
        # will call the __init__() with a couple of kwargs. The first initializer
        # might not have all values. but the seiralizer will. So first thing
        # should be to set all values to None and then update them with the kwargs.

        # If we write a function for updating the fields it could be reused after
        # we post things to the API and get back new info. Like id etc. The
        # serializer would then retun a new object and we should go through
        # that object and update the fileds on the current object. Marshmallow
        # do this so we can get ideas there

        self._init_fields(kwargs=kwargs)

        # TODO: As of now we are just using the marshmallow fields. We would
        # want to be sure when we are creating an object from scratch that we
        # have all the necessary data to be able to create it.  We can do this by
        # checking if all fields exept the load only has been filled. And alos
        # check if allow_none is on the field.

    def _init_fields(self, kwargs=None):

        for field_name, field_value in self.schema_fields.items():
            try:
                value = kwargs[field_name]
            except KeyError:
                value = field_value.default
                if is_instance_or_subclass(value, _Missing):
                    value = None

            allow_none = field_value.allow_none or field_value.load_only

            if value is None and not allow_none:
                raise AttributeError(
                    f'{self.__class__.__name__} :: {field_name} '
                    f'is not allowed to be None')

            setattr(self, field_name, value)

    def _update_value(self, obj=None):

        if obj is None:
            return

        else:
            for field_name, field_value in self.schema_fields.items():
                value = getattr(obj, field_name)
                setattr(self, field_name, value)

    def save(self):

        if self.id is None:
            # create a new model
            print('Saving data')
            updated_obj = self.objects.create(self)
            self._update_value(obj=updated_obj)

        else:
            # update model
            print('Updating object')
            self.objects.update(self)

    def delete(self):
        print('Deleting object ')
        self.objects._delete(self)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)

    def __str__(self):
        return '%s object (%s)' % (self.__class__.__name__, self.id)


class Customer(VismaModel):
    id = fields.Str(data_key='Id', load_only=True)
    customer_number = fields.Str(data_key='CustomerNumber')
    name = fields.Str(data_key='Name')
    invoice_city = fields.Str(data_key='InvoiceCity')
    invoice_postal_code = fields.Str(data_key='InvoicePostalCode')
    is_private_person = fields.Boolean(data_key='IsPrivatePerson')
    is_active = fields.Boolean(data_key='IsActive')
    terms_of_payment = fields.Nested('TermsOfPaymentSchema',
                                     data_key='TermsOfPayment')

    class Meta:
        endpoint = '/customers'


class TermsOfPayment(VismaModel):
    id = fields.String(data_key='Id', load_only=True)
    name = fields.String(data_key='Name')
    available_for_purchase = fields.Boolean(data_key='AvailableForPurchase')
    available_for_sales = fields.Boolean(data_key='AvailableForSale',
                                         allow_none=True)
    name_english = fields.String(data_key='NameEnglish')
    type_id = fields.Integer(data_key='TermsOfPaymentTypeId')

    type_text = fields.String(data_key='TermsOfPaymentTypeText',
                              allow_none=True)

    class Meta:
        endpoint = '/termsofpayment'


class Row(VismaModel):
    line_nr = fields.Integer(data_key='LineNumber')
    article_id = fields.String(data_key='ArticleId')
    article_number = fields.String(data_key='ArticleNumber', allow_none=True)
    is_text_row = fields.Boolean(data_key='IsTextRow', default=False)
    text = fields.String(data_key='Text')
    unit_price = fields.Float(data_key='UnitPrice', places=2)
    discount_percentage = fields.Float(data_key='DiscountPercentage', default=0,
                                       places=4)
    quantity = fields.Float(data_key='Quantity', places=2)
    work_cost_type = fields.Integer(data_key='WorkCostType', default=0)
    is_work_cost = fields.Boolean(data_key='IsWorkCost', default=False)
    work_hours = fields.Float(data_key='WorkHours', allow_none=True)
    material_costs = fields.Float(data_key='MaterialCosts', allow_none=True)
    reversed_construction_service_vat_free = fields.Boolean(
        data_key='ReversedConstructionServicesVatFree', default=False)
    cost_center_id_1 = fields.String(data_key='CostCenterId1', allow_none=True)
    cost_center_id_2 = fields.String(data_key='CostCenterId2', allow_none=True)
    cost_center_id_3 = fields.String(data_key='CostCenterId3', allow_none=True)
    unit_name = fields.String(data_key='UnitName', allow_none=True)
    unit_abbreviation = fields.String(data_key='UnitAbbreviation',
                                      allow_none=True)
    vat_rate_id = fields.String(data_key='VatRateId', load_only=True)
    project_id = fields.String(data_key='ProjectId', allow_none=True)

    def __str__(self):
        return '%s object (%s)' % (self.__class__.__name__, self.line_nr)


class CustomerInvoiceDraft(VismaModel):
    id = fields.String(data_key='Id',
                       load_only=True)  # Not true when issueing PUT
    customer_id = fields.UUID(data_key='CustomerId')
    customer_number = fields.String(data_key='CustomerNumber', load_only=True)
    customer_name = fields.String(data_key='InvoiceCustomerName', allow_none=True)
    date = fields.Date(data_key='InvoiceDate', allow_none=True)

    created = fields.DateTime(data_key='CreatedUtc', load_only=True)
    is_credit_invoice = fields.Boolean(data_key='IsCreditInvoice',
                                       default=False)

    delivery_address_1 = fields.String(data_key='DeliveryAddress1',
                                       allow_none=True)
    delivery_address_2 = fields.String(data_key='DeliveryAddress2',
                                       allow_none=True)
    delivery_city = fields.String(data_key='DeliveryCity',
                                  allow_none=True)
    delivery_country_code = fields.String(data_key='DeliveryCountryCode',
                                          allow_none=True)
    delivery_customer_name = fields.String(data_key='DeliveryCustomerName',
                                           allow_none=True)
    delivery_date = fields.Date(data_key='DeliveryDate', allow_none=True)
    delivery_method_code = fields.String(data_key='DeliveryMethodCode',
                                         allow_none=True)  # TODO: is this integer?
    delivery_method_name = fields.String(data_key='DeliveryMethodName',
                                         allow_none=True)
    delivery_term_code = fields.String(data_key='DeliveryTermCode',
                                       allow_none=True)  # TODO: is this integer?
    delivery_term_name = fields.String(data_key='DeliveryTermName',
                                       allow_none=True)

    address_1 = fields.String(data_key='InvoiceAddress1', allow_none=True)
    address_2 = fields.String(data_key='InvoiceAddress2', allow_none=True)

    our_reference = fields.String(data_key='OurReference', allow_none=True)

    persons = None

    rows = fields.Nested('RowSchema', data_key='Rows', default=list(),
                         many=True)

    sales_document_attachment = None

    postal_code = fields.String(data_key='InvoicePostalCode')
    city = fields.String(data_key='InvoiceCity')
    country_code = fields.String(data_key='InvoiceCountryCode', default='SE')
    currency_code = fields.String(data_key='InvoiceCurrencyCode',
                                  allow_none=True)
    eu_third_party = fields.Boolean(data_key='EuThirdParty', default=1)
    house_work_other_costs = fields.String(data_key='HouseWorkOtherCosts',
                                           allow_none=True)
    reverse_charge_on_construction_services = fields.Boolean(
        data_key='ReverseChargeOnConstructionServices', default=False)
    rot_property_type = fields.Boolean(data_key='RotPropertyType',
                                       allow_none=True)
    rot_reduced_invoicing_amount = fields.Float(
        data_key='RotReducedInvoicingAmount', default=0)
    rot_reduced_invoicing_automatic_distribution = fields.Boolean(
        data_key='RotReducedInvoicingAutomaticDistribution', default=True)
    rot_reduced_invoicing_org_number = fields.String(
        data_key='RotReducedInvoicingOrgNumber', allow_none=True)
    rot_reduced_invoicing_property_name = fields.String(
        data_key='RotReducedInvoicingPropertyName', allow_none=True)
    rot_reduced_invoicing_type = fields.Integer(
        data_key='RotReducedInvoicingType', default=1)
    includes_vat = fields.Boolean(data_key='IncludesVat', default=False)
    customer_is_private_person = fields.Boolean(
        data_key='CustomerIsPrivatePerson')

    total_amount = fields.Float(data_key='TotalAmount', load_only=True)
    total_amount_base_currency = fields.Float(
        data_key='TotalAmountBaseCurrency', load_only=True)
    total_roundings = fields.Float(data_key='TotalRoundings', load_only=True)
    total_vat_amount = fields.Float(data_key='TotalVatAmount', load_only=True)
    total_vat_amount_base_currency = fields.Float(
        data_key='TotalVatAmountBaseCurrency', load_only=True)
    your_reference = fields.String(data_key='YourReference', allow_none=True)

    class Meta:
        endpoint = '/customerinvoicedrafts'

