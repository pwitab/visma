from marshmallow import Schema, fields, post_load

from visma.utils import import_string


class VismaSchema(Schema):
    visma_model = None

    @post_load
    def make_instance(self, data):
        klass = import_string(self.visma_model)
        return klass(**data)


class TermsOfPaymentSchema(VismaSchema):

    visma_model = 'visma.models.TermsOfPayment'

    id = fields.String(data_key='Id', load_only=True)
    name = fields.String(data_key='Name')
    available_for_purchase = fields.Boolean(data_key='AvailableForPurchase')
    available_for_sales = fields.Boolean(data_key='AvailableForSale')
    name_english = fields.String(data_key='NameEnglish')
    type_id = fields.Integer(data_key='TermsOfPaymentTypeId')
    # type_text = fields.String(data_key='TermsOfPaymentTypeText')
    # TODO: How to handel None types?


class CustomerSchema(VismaSchema):

    visma_model = 'visma.models.Customer'


    id = fields.Str(data_key='Id', load_only=True)
    customer_number = fields.Str(data_key='CustomerNumber')
    name = fields.Str(data_key='Name')
    invoice_city = fields.Str(data_key='InvoiceCity')
    invoice_postal_code = fields.Str(data_key='InvoicePostalCode')
    is_private_person = fields.Boolean(data_key='IsPrivatePerson')
    is_active = fields.Boolean(data_key='IsActive')
    terms_of_payment = fields.Nested(TermsOfPaymentSchema,
                                     data_key='TermsOfPayment')


class CustomerInvoiceDraftSchema(VismaSchema):

    visma_model = 'visma.models.CustomerInvoiceDraft'

    id = fields.String(data_key='Id', load_only=True)  # Not true when issueing PUT
    customer_id = fields.String(data_key='CustomerId')
    #customer_number = fields.String(data_key='CustomerNumber')
    customer_name = fields.String(data_key='InvoiceCustomerName')
    #date = fields.Date(data_key='InvoiceDate', allow_none=True)

    #created = fields.DateTime(data_key='CreatedUtc')
    is_credit_invoice = fields.String('IsCreditInvoice')

    #delivery_address_1 = fields.String(data_key='DeliveryAddress1',
    #                                   allow_none=True)
    #delivery_address_2 = fields.String(data_key='DeliveryAddress2',
    #                                   allow_none=True)
    #delivery_city = fields.String(data_key='DeliveryCity',
    #                                   allow_none=True)
   # delivery_country_code = fields.String(data_key='DeliveryCountryCode',
    #                                      allow_none=True)
    #delivery_customer_name = fields.String(data_key='DeliveryCustomerName',
    #                                       allow_none=True)
    #delivery_date = fields.Date(data_key='DeliveryDate', allow_none=True)
    #delivery_method_code = fields.String(data_key='DeliveryMethodCode', allow_none=True)  # TODO: is this integer?
    #delivery_method_name = fields.String(data_key='DeliveryMethodName', allow_none=True)
    #delivery_term_code = fields.String(data_key='DeliveryTermCode', allow_none=True)  # TODO: is this integer?
    #delivery_term_name = fields.String(data_key='DeliveryTermName', allow_none=True)

    #address_1 = fields.String(data_key='InvoiceAddress1', allow_none=True)
    #address_2 = fields.String(data_key='InvoiceAddress2', allow_none=True)

    #our_reference = fields.String(data_key='OurReference', allow_none=True)

    persons = None

    rows = None

    sales_document_attachment = None

    postal_code = fields.String(data_key='InvoicePostalCode')
    city = fields.String(data_key='InvoiceCity')
    country_code = fields.String(data_key='InvoiceCountryCode')
    #currency_code = fields.String(data_key='InvoiceCurrencyCode')
    eu_third_party = fields.Boolean(data_key='EuThirdParty')
    #house_work_other_costs = fields.String(data_key='HouseWorkOtherCosts', allow_none=True)
    #reverse_charge_on_construction_services = fields.Boolean(data_key='ReverseChargeOnConstructionServices')
    #rot_property_type = fields.Boolean(data_key='RotPropertyType', allow_none=True)
    #rot_reduced_invoicing_amount = fields.Float(data_key='RotReducedInvoicingAmount')
    #rot_reduced_invoicing_automatic_distribution = fields.Boolean(data_key='RotReducedInvoicingAutomaticDistribution')
    #rot_reduced_invoicing_org_number = fields.String(data_key='RotReducedInvoicingOrgNumber', allow_none=True)
    #rot_reduced_invoicing_property_name = fields.String(data_key='RotReducedInvoicingPropertyName', allow_none=True)
    rot_reduced_invoicing_type = fields.Integer(
        data_key='RotReducedInvoicingType')
    #includes_vat = fields.Boolean(data_key='IncludesVat')
    customer_is_private_person = fields.Boolean(
        data_key='CustomerIsPrivatePerson')

    #total_amount = fields.Float(data_key='TotalAmount')
    #total_amount_base_currency = fields.Float(data_key='TotalAmountBaseCurrency')
    #total_roundings = fields.Float(data_key='TotalRoundings')
    #total_vat_amount = fields.Float(data_key='TotalVatAmount')
    #total_vat_amount_base_currency = fields.Float(data_key='TotalVatAmountBaseCurrency')
    your_reference = fields.String(data_key='YourReference', allow_none=True)


# TODO: Create a custom field that takes the id. This should handle contexts.
# when context is create (Post) it should not output the id. But when updating
# (PUT) we want to send the id.