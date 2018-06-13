from visma.base import VismaModel
from marshmallow import fields


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

