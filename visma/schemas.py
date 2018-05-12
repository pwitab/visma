from marshmallow import Schema, fields, post_load

from .models import TermsOfPayment, Customer, CustomerInvoiceDraft


class VismaSchema(Schema):
    pass


class TermsOfPaymentSchema(VismaSchema):
    id = fields.String(data_key='Id')
    name = fields.String(data_key='Name')
    available_for_purchase = fields.Boolean(data_key='AvailableForPurchase')
    available_for_sales = fields.Boolean(data_key='AvailableForSale')
    name_english = fields.String(data_key='NameEnglish')
    type_id = fields.Integer(data_key='TermsOfPaymentTypeId')
    # type_text = fields.String(data_key='TermsOfPaymentTypeText')
    # TODO: How to handel None types?

    @post_load
    def make_terms_of_payment(self, data):
        return TermsOfPayment(**data)


class CustomerSchema(VismaSchema):
    id = fields.Str(data_key='Id')
    customer_number = fields.Str(data_key='CustomerNumber')
    name = fields.Str(data_key='Name')
    invoice_city = fields.Str(data_key='InvoiceCity')
    invoice_postal_code = fields.Str(data_key='InvoicePostalCode')
    is_private_person = fields.Boolean(data_key='IsPrivatePerson')
    is_active = fields.Boolean(data_key='IsActive')
    terms_of_payment = fields.Nested(TermsOfPaymentSchema,
                                     data_key='TermsOfPayment')

    @post_load
    def make_customer(self, data):
        return Customer(**data)


class CustomerInvoiceDraftSchema(VismaSchema):

    id = fields.String(data_key='Id')
    customer_id = fields.String(data_key='CustomerId')
    rot_reduced_invoicing_type = fields.Integer(
        data_key='RotReducedInvoicingType')
    customer_name = fields.String(data_key='InvoiceCustomerName')
    postal_code = fields.String(data_key='InvoicePostalCode')
    city = fields.String(data_key='InvoiceCity')
    country_code = fields.String(data_key='InvoiceCountryCode')
    eu_third_party = fields.Boolean(data_key='EuThirdParty')
    customer_is_private_person = fields.Boolean(
        data_key='CustomerIsPrivatePerson')

    @post_load
    def make_customer_invoice_draft(self, data):
        return CustomerInvoiceDraft(**data)
