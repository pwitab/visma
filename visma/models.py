import re

from marshmallow.validate import OneOf, Length, Regexp, Range

from visma.base import VismaModel
from marshmallow import fields


# TODO: Should I use Float instead of Number since I can specify places? And no need for regex


class Customer(VismaModel):
    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id',
                     load_only=True)
    customer_number = fields.String(
        description=('Max length: 20 characters. '
                     'Purpose: Unique identifier. '
                     'If not provided, eAccounting will provide one'),
        validate=[Length(min=0, max=16, )],
        data_key='CustomerNumber')
    corporate_identity_number = fields.String(
        description='Max length: 20 characters',
        validate=[Length(min=0, max=20, )],
        data_key='CorporateIdentityNumber')
    contact_person_email = fields.String(
        description='Max length: 255 characters',
        validate=[Length(min=0, max=255, )],
        data_key='ContactPersonEmail')
    contact_person_mobile = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )],
        data_key='ContactPersonMobile')
    contact_person_name = fields.String(
        description='Max length: 100 characters',
        validate=[Length(min=0, max=100, )],
        data_key='ContactPersonName')
    contact_person_phone = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )],
        data_key='ContactPersonPhone')
    currency_code = fields.String(
        description=('Max length: 3 characters. '
                     'Default value: Currency of the user company'),
        validate=[Length(min=0, max=3, )],
        data_key='CurrencyCode')
    gln = fields.String(
        description='NOTE: Obsolete. Please use EdiGlnNumber instead',
        validate=[Length(min=0, max=255, )],
        data_key='GLN',
        allow_none=True)
    email_address = fields.String(
        description='Max length: 255 characters',
        validate=[Length(min=0, max=255, )],
        data_key='EmailAddress')
    invoice_address1 = fields.String(
        description='Max length: 50 characters',
        validate=[
            Length(min=0, max=50, )],
        data_key='InvoiceAddress1')
    invoice_address2 = fields.String(
        description='Max length: 50 characters',
        validate=[
            Length(min=0, max=50, )],
        data_key='InvoiceAddress2')
    invoice_city = fields.String(
        required=True,
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )],
        data_key='InvoiceCity')
    invoice_country_code = fields.String(
        description='Max length: 2 characters',
        validate=[
            Length(min=0, max=2, )],
        data_key='InvoiceCountryCode')
    invoice_postal_code = fields.String(
        required=True,
        description='Max length: 10 characters',
        validate=[
            Length(min=0, max=10, )],
        data_key='InvoicePostalCode')
    delivery_customer_name = fields.String(
        description='Max length: 100 characters',
        validate=[Length(min=0, max=100, )],
        data_key='DeliveryCustomerName',
        allow_none=True)
    delivery_address1 = fields.String(
        description=('Max length: 50 characters. Purpose: Only used if invoice '
                     'address differs from delivery address'),
        validate=[Length(min=0, max=50, )],
        data_key='DeliveryAddress1',
        allow_none=True)
    delivery_address2 = fields.String(
        description=('Max length: 50 characters. Purpose: Only used if invoice '
                     'address differs from delivery address'),
        validate=[Length(min=0, max=50, )],
        data_key='DeliveryAddress2',
        allow_none=True)
    delivery_city = fields.String(
        description=('Max length: 50 characters. Purpose: Only used if invoice '
                     'city differs from delivery city'),
        validate=[Length(min=0, max=50, )],
        data_key='DeliveryCity',
        allow_none=True)
    delivery_country_code = fields.String(
        description=('Max length: 2 characters. Purpose: Only used if invoice '
                     'country code differs from delivery country code'),
        validate=[Length(min=0, max=2, )],
        data_key='DeliveryCountryCode',
        allow_none=True)
    delivery_postal_code = fields.String(
        description=('Max length: 10 characters. Purpose: Only used if invoice '
                     'postal code differs from delivery postal code'),
        validate=[Length(min=0, max=10, )],
        data_key='DeliveryPostalCode',
        allow_none=True)
    delivery_method_id = fields.UUID(
        description='Source: Get from /v2/deliverymethods',
        data_key='DeliveryMethodId',
        allow_none=True)
    delivery_term_id = fields.UUID(
        description='Source: Get from /v2/deliveryterms',
        data_key='DeliveryTermId',
        allow_none=True)
    pay_to_account_id = fields.UUID(
        description='Read-only: The account Id on which payments are registered',
        data_key='PayToAccountId',
        load_only=True)
    name = fields.String(required=True, description='Max length: 50 characters',
                         validate=[Length(min=0, max=50, )],
                         data_key='Name')
    note = fields.String(description='Max length: 4000 characters',
                         validate=[Length(min=0, max=4000, )],
                         data_key='Note')
    reverse_charge_on_construction_services = fields.Boolean(
        description=('Default: false. '
                     'Purpose: If true, VatNumber must be set aswell'),
        data_key='ReverseChargeOnConstructionServices',
        default=False)
    webshop_customer_number = fields.Integer(
        data_key='WebshopCustomerNumber',
        allow_none=True)
    mobile_phone = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )],
        data_key='MobilePhone')
    telephone = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )],
        data_key='Telephone')
    terms_of_payment_id = fields.UUID(
        required=True,
        description='Source: Get from /v2/termsofpayment',
        data_key='TermsOfPaymentId')
    terms_of_payment = fields.Nested('TermsOfPaymentSchema',
                                     data_key='TermsOfPayment')
    vat_number = fields.String(
        description=('Max length: 20 characters. Format: 2 character country '
                     'code followed by 8-12 numbers.'),
        validate=[Length(min=0, max=20, )], data_key='VatNumber')
    www_address = fields.String(
        description='Max length: 255 characters',
        validate=[Length(min=0, max=255, )],
        data_key='WwwAddress')
    last_invoice_date = fields.DateTime(
        description='Read-only. Purpose: Returns the last invoice date',
        data_key='LastInvoiceDate')
    is_private_person = fields.Boolean(
        required=True,
        data_key='IsPrivatePerson',
        default=False)
    discount_percentage = fields.Number(
        description='Format: 4 decimals',
        validate=[Range(min=0, max=1, ),
                  # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,4})?'))
                  ],
        data_key='DiscountPercentage')
    changed_utc = fields.DateTime(
        description=('Read-only. Purpose: Returns the last date and time from '
                     'when a change was made on the customer'),
        data_key='ChangedUtc',
        load_only=True)
    is_active = fields.Boolean(
        required=True,
        data_key='IsActive',
        default=True)
    force_bookkeep_vat = fields.Boolean(
        data_key='ForceBookkeepVat',
        default=True)
    edi_gln_number = fields.String(data_key='EdiGlnNumber')
    sales_document_language = fields.String(
        description='Max length: 2 characters',
        validate=[Length(min=0, max=2, )],
        data_key='SalesDocumentLanguage')
    electronic_address = fields.String(data_key='ElectronicAddress')
    electronic_reference = fields.String(data_key='ElectronicReference')
    edi_service_deliverer_id = fields.String(data_key='EdiServiceDelivererId')
    auto_invoice_activation_email_sent_date = fields.DateTime(
        data_key='AutoInvoiceActivationEmailSentDate',
        allow_none=True)
    auto_invoice_registration_request_sent_date = fields.DateTime(
        data_key='AutoInvoiceRegistrationRequestSentDate',
        allow_none=True)
    email_addresses = fields.List(fields.String(), data_key='EmailAddresses')
    # customer_labels = fields.List(fields.Nested('CustomerLabelSchema'),
    #                              data_key='CustomerLabels')

    class Meta:
        endpoint = '/customers'


class TermsOfPayment(VismaModel):
    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id',
                     load_only=True)
    name = fields.String(data_key='Name')
    name_english = fields.String(data_key='NameEnglish')
    number_of_days = fields.Integer(data_key='NumberOfDays')
    terms_of_payment_type_id = fields.Integer(data_key='TermsOfPaymentTypeId')
    terms_of_payment_type_text = fields.String(
        data_key='TermsOfPaymentTypeText',
        allow_none=True)
    available_for_sales = fields.Boolean(
        data_key='AvailableForSales',
        allow_none=True)
    available_for_purchase = fields.Boolean(data_key='AvailableForPurchase')

    class Meta:
        endpoint = '/termsofpayment'


class CustomerInvoiceDraftRow(VismaModel):
    line_number = fields.Integer(
        required=True,
        validate=[Range(min=0, max=1000)],
        data_key='LineNumber')
    article_id = fields.UUID(
        description=('Source: Get from /v2/articles. '
                     'Required if IsTextRow is false'),
        data_key='ArticleId')
    article_number = fields.String(
        description=('Purpose: Returns the article number '
                     'from the entered ArticleId'),
        allow_none=True,
        data_key='ArticleNumber')
    is_text_row = fields.Boolean(
        required=True,
        data_key='IsTextRow',
        default=False)
    text = fields.String(
        required=True,
        description='Max length: 2000. Sets the article name',
        validate=[Length(min=0, max=2000)],
        data_key='Text')
    unit_price = fields.Number(
        description=("Format: 2 decimals allowed\r\nDefault: The price that is "
                     "set on the article's register. For using a custom price,"
                     " use this property"),
        # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
        data_key='UnitPrice')
    discount_percentage = fields.Number(
        description='Format: 4 decimals allowed',
        validate=[Range(min=0, max=1),
                  # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,4})?'))
                  ],
        data_key='DiscountPercentage',
        default=0.00)
    quantity = fields.Number(
        description='Format: 2 decimals',
        # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
        data_key='Quantity')
    work_cost_type = fields.Integer(data_key='WorkCostType', default=0)
    is_work_cost = fields.Boolean(data_key='IsWorkCost', default=False)
    work_hours = fields.Number(data_key='WorkHours', allow_none=True)
    material_costs = fields.Number(data_key='MaterialCosts', allow_none=True)
    reversed_construction_services_vat_free = fields.Boolean(
        required=True,
        data_key='ReversedConstructionServicesVatFree',
        default=False)
    cost_center_item_id1 = fields.UUID(
        description='Source: Get from /v2/costcenteritems',
        data_key='CostCenterItemId1',
        allow_none=True)
    cost_center_item_id2 = fields.UUID(
        description='Source: Get from /v2/costcenteritems',
        data_key='CostCenterItemId2',
        allow_none=True)
    cost_center_item_id3 = fields.UUID(
        description='Source: Get from /v2/costcenteritems',
        data_key='CostCenterItemId3',
        allow_none=True)
    unit_abbreviation = fields.String(
        data_key='UnitAbbreviation',
        allow_none=True)
    vat_rate_id = fields.String(
        description='Source: Get from /v2/articleaccountcodings \r\nRead-only',
        data_key='VatRateId',
        load_only=True)
    unit_name = fields.String(data_key='UnitName', allow_none=True)
    project_id = fields.UUID(data_key='ProjectId', allow_none=True)

    def __str__(self):
        return '%s object (%s)' % (self.__class__.__name__, self.line_number)


class CustomerInvoiceDraft(VismaModel):
    id = fields.UUID(
        description='Read-only: Unique Id provided by eAccounting',
        load_only=True,
        data_key='Id')
    customer_id = fields.UUID(
        required=True,
        description='Source: Get from /v2/customers',
        data_key='CustomerId')
    created_utc = fields.DateTime(
        description='Read-only: Is automatically set',
        load_only=True,
        data_key='CreatedUtc')
    is_credit_invoice = fields.Boolean(data_key='IsCreditInvoice',
                                       default=False)
    rot_reduced_invoicing_type = fields.Integer(
        required=True,
        description='0 = Normal, 1 = Rot, 2 = Rut',
        validate=[
            OneOf(choices=[0, 1, 2],
                  labels=[])],
        data_key='RotReducedInvoicingType',
        default=0)
    rot_reduced_invoicing_property_name = fields.String(
        description='Max length: 40 characters',
        validate=[Length(min=0, max=40)],
        data_key='RotReducedInvoicingPropertyName',
        allow_none=True)
    rot_reduced_invoicing_org_number = fields.String(
        description='Max length: 11 characters',
        validate=[Length(min=0, max=11)],
        data_key='RotReducedInvoicingOrgNumber',
        allow_none=True)
    rot_reduced_invoicing_amount = fields.Number(
        description='Format: 2 decimals',
        # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
        data_key='RotReducedInvoicingAmount',
        default=0.00)
    rot_reduced_invoicing_automatic_distribution = fields.Boolean(
        description='Default: False',
        data_key='RotReducedInvoicingAutomaticDistribution',
        default=False)
    rot_property_type = fields.Integer(data_key='RotPropertyType',
                                       allow_none=True)
    house_work_other_costs = fields.Number(data_key='HouseWorkOtherCosts',
                                           allow_none=True)
    rows = fields.List(fields.Nested('CustomerInvoiceDraftRowSchema'),
                       data_key='Rows')
    persons = None
    # persons = fields.List(
    #    fields.Nested('SalesDocumentRotRutReductionPersonApi'),
    #    data_key='Persons')
    your_reference = fields.String(
        description='Max length: 100 characters',
        validate=[
            Length(min=0, max=100)],
        data_key='YourReference',
        allow_none=True)
    our_reference = fields.String(
        description='Max length: 100 characters',
        validate=[Length(min=0, max=100)],
        data_key='OurReference',
        allow_none=True)
    invoice_customer_name = fields.String(
        required=True,
        allow_none=True,
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50)],
        data_key='InvoiceCustomerName')
    invoice_address1 = fields.String(
        description='Max length: 50 characters',
        validate=[
            Length(min=0, max=50)],
        data_key='InvoiceAddress1',
        allow_none=True)
    invoice_address2 = fields.String(
        description='Max length: 50 characters',
        validate=[
            Length(min=0, max=50)],
        data_key='InvoiceAddress2',
        allow_none=True)
    invoice_postal_code = fields.String(
        required=True,
        description='Max length: 10 characters',
        validate=[
            Length(min=0, max=10)],
        data_key='InvoicePostalCode')
    invoice_city = fields.String(
        required=True,
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )],
        data_key='InvoiceCity')
    invoice_country_code = fields.String(
        required=True,
        description='Max length: 2 characters',
        validate=[
            Length(min=0, max=2, )],
        data_key='InvoiceCountryCode',
        default='SE')
    invoice_currency_code = fields.String(
        description='Read-only',
        data_key='InvoiceCurrencyCode',
        load_only=True)
    delivery_customer_name = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )],
        data_key='DeliveryCustomerName',
        allow_none=True)
    delivery_address1 = fields.String(
        description='Max length: 50 characters',
        validate=[
            Length(min=0, max=50, )],
        data_key='DeliveryAddress1',
        allow_none=True)
    delivery_address2 = fields.String(
        description='Max length: 50 characters',
        validate=[
            Length(min=0, max=50, )],
        data_key='DeliveryAddress2',
        allow_none=True)
    delivery_postal_code = fields.String(
        description='Max length: 10 characters',
        validate=[Length(min=0, max=10, )],
        data_key='DeliveryPostalCode',
        allow_none=True)
    delivery_city = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )],
        data_key='DeliveryCity',
        allow_none=True)
    delivery_country_code = fields.String(
        description='Max length: 2 characters',
        validate=[Length(min=0, max=2, )],
        data_key='DeliveryCountryCode',
        allow_none=True)
    delivery_method_name = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )],
        data_key='DeliveryMethodName',
        allow_none=True)
    delivery_term_name = fields.String(
        description='Max length: 50 characters',
        validate=[
            Length(min=0, max=50, )],
        data_key='DeliveryTermName',
        allow_none=True)
    delivery_method_code = fields.String(
        description='Max length: 20 characters',
        validate=[Length(min=0, max=20, )],
        data_key='DeliveryMethodCode',
        allow_none=True)
    delivery_term_code = fields.String(
        description='Max length: 20 characters',
        validate=[
            Length(min=0, max=20, )],
        data_key='DeliveryTermCode',
        allow_none=True)
    eu_third_party = fields.Boolean(
        required=True,
        data_key='EuThirdParty',
        default=False)
    customer_is_private_person = fields.Boolean(
        required=True,
        data_key='CustomerIsPrivatePerson')
    reverse_charge_on_construction_services = fields.Boolean(
        description='Read-only',
        data_key='ReverseChargeOnConstructionServices',
        load_only=True)
    sales_document_attachments = fields.List(
        fields.UUID(),
        description='Read-only',
        data_key='SalesDocumentAttachments',
        load_only=True)
    invoice_date = fields.DateTime(data_key='InvoiceDate', allow_none=True)
    delivery_date = fields.DateTime(data_key='DeliveryDate', allow_none=True)
    total_amount = fields.Number(
        description='Read-only',
        data_key='TotalAmount',
        load_only=True)
    total_vat_amount = fields.Number(
        description='Read-only',
        data_key='TotalVatAmount',
        load_only=True)
    total_roundings = fields.Number(
        description='Read-only',
        data_key='TotalRoundings',
        load_only=True)
    total_amount_base_currency = fields.Number(
        description='Read-only',
        data_key='TotalAmountBaseCurrency',
        load_only=True)
    total_vat_amount_base_currency = fields.Number(
        description='Read-only',
        data_key='TotalVatAmountBaseCurrency',
        load_only=True)
    customer_number = fields.String(
        description='Read-only\r\nMax length: 16 characters',
        load_only=True,
        validate=[Length(min=0, max=16, )],
        data_key='CustomerNumber')
    includes_vat = fields.Boolean(
        description=('Read-only: If true the unit prices on rows include VAT. '
                     'The value is set upon creation depending whether "Show '
                     'prices excl. VAT for private individuals" in company '
                     'settings is marked or not'),
        data_key='IncludesVat',
        load_only=True)

    class Meta:
        endpoint = '/customerinvoicedrafts'
