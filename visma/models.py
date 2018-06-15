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


#
# ########################################################################
# Models below need moderating, generated from swagger-marshmallow-codegen
# ########################################################################


class AccountBalance(VismaModel):
    account_number = fields.Integer(
        description='Read-only. The account number',
        data_key='AccountNumber',
        load_only=True)
    account_name = fields.String(
        description='Read-only. The name of the account',
        data_key='AccountName',
        load_only=True)
    balance = fields.Number(
        description='Read-only. The account balance',
        data_key='Balance',
        load_only=True)

    class Meta:
        # GET /v2/accountbalances/{date}
        # GET /v2/accountbalances/{accountNumber}/{date}

        # TODO: Meta should state available HTTP Methods. And handling for several endpoints.
        # or just use main endpoint and filter?

        pass


class Account(VismaModel):
    name = fields.String(
        required=True,
        description='Max length: 100 characters. The name of the account',
        validate=[Length(min=0, max=100)],
        data_key='Name')
    number = fields.String(
        required=True,
        description='The account number',
        data_key='Number')
    vat_code_id = fields.UUID(
        description='The Id of the VAT code that is associated with the account',
        data_key='VatCodeId')
    vat_code_description = fields.String(
        description='Read-only. Describes what kind of VAT that is associated with the account',
        data_key='VatCodeDescription')
    fiscal_year_id = fields.UUID(
        required=True,
        description='The Id of the Fiscal year that the account belongs to',
        data_key='FiscalYearId')
    reference_code = fields.String(
        description='Read-only. Returns the reference code on the account. This feature is for dutch companies only',
        data_key='ReferenceCode')
    type = fields.Integer(
        description='Read-only. Returns account type number. Netherlands only',
        data_key='Type')
    type_description = fields.String(
        description='Read-only. Returns account type descripion',
        data_key='TypeDescription')
    modified_utc = fields.DateTime(
        description='Read-only.',
        data_key='ModifiedUtc')
    is_active = fields.Boolean(
        required=True,
        data_key='IsActive')
    is_project_allowed = fields.Boolean(data_key='IsProjectAllowed')
    is_cost_center_allowed = fields.Boolean(data_key='IsCostCenterAllowed')
    is_blocked_for_manual_booking = fields.Boolean(
        data_key='IsBlockedForManualBooking')

    class Meta:
        # GET /v2/accounts     Get a list of accounts from all fiscalyears
        # POST/v2/accounts    Add account
        # GET /v2/accounts/standardaccounts   (just for dutch companies)
        # GET /v2/accounts/{fiscalyearId}   Get a list of accounts for a spcific fiscalyear
        # GET /v2/accounts/{fiscalyearId}/{accountNumber}  Get a single account by account number
        # PUT /v2/accounts/{fiscalyearId}/{accountNumber} Replaces a account in a given fiscalyear
        pass


class AccountType(VismaModel):
    type = fields.Integer(data_key='Type')
    type_description = fields.String(data_key='TypeDescription')

    class Meta:
        # GET /v2/accountTypes Gets the default account types. This is applicable on all countries but most relevant for the Netherlands
        pass


class AllocationPeriod(VismaModel):
    id = fields.UUID(data_key='Id')
    supplier_invoice_id = fields.UUID(data_key='SupplierInvoiceId')
    supplier_invoice_row = fields.Integer(data_key='SupplierInvoiceRow')
    manual_voucher_id = fields.UUID(data_key='ManualVoucherId')
    manual_voucher_row = fields.Integer(data_key='ManualVoucherRow')
    allocation_period_source_type = fields.Integer(
        description='0 = SupplierInvoice, 1 = ManualVoucher',
        validate=[OneOf(choices=[0, 1], labels=[])],
        data_key='AllocationPeriodSourceType')
    status = fields.Integer(
        description='0 = Pending, 1 = Revoked, 2 = Booked',
        validate=[OneOf(choices=[0, 1, 2], labels=[])],
        data_key='Status')
    cost_center_item_id1 = fields.UUID(data_key='CostCenterItemId1')
    cost_center_item_id2 = fields.UUID(data_key='CostCenterItemId2')
    cost_center_item_id3 = fields.UUID(data_key='CostCenterItemId3')
    project_id = fields.UUID(data_key='ProjectId')
    bookkeeping_date = fields.DateTime(data_key='BookkeepingDate')
    created_utc = fields.DateTime(data_key='CreatedUtc')
    rows = fields.List(fields.Nested('AllocationPeriodRowApi'),
                       required=True, data_key='Rows')
    debit_account_number = fields.Integer(dump_only=True,
                                          data_key='DebitAccountNumber')
    credit_account_number = fields.Integer(dump_only=True,
                                           data_key='CreditAccountNumber')
    amount = fields.Number(dump_only=True, data_key='Amount')

    class Meta:
        # GET /v2/allocationperiods Get allocation periods.
        # POST /v2/allocationperiods Add allocation periods for voucher or supplier invoice.
        # GET /v2/allocationperiods/{allocationPeriodId} Get single allocation period.
        pass


class Approval(VismaModel):
    document_approval_status = fields.Integer(
        required=True,
        description='1 = Approved, 2 = Rejected, 3 = ReadyForApproval',
        validate=[OneOf(choices=[0, 1, 2, 3], labels=[])],
        data_key='DocumentApprovalStatus')
    rejection_message = fields.String(
        description='Purpose: The message sent to users when rejecting a document. Empty if DocumentApprovalStatus is not 2 = Rejected.\r\nMax length: 200 characters',
        validate=[Length(min=0, max=200)],
        data_key='RejectionMessage')
    rejection_message_receivers = fields.List(
        fields.UUID(),
        description='Purpose: The recipients of the rejection message. Empty if DocumentApprovalStatus is not 2 = Rejected. List of user ids.',
        data_key='RejectionMessageReceivers')

    class Meta:
        # TODO: Maybe split into 2 subclasses to separate endpoints for vat and invoices and useage.
        # PUT /v2/approval/vatreport/{id} Update the approval status of a vat report
        # PUT /v2/approval/supplierinvoice/{id} Update the approval status of a invoice draft
        pass


class ArticleAccountCoding(VismaModel):
    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id')
    name = fields.String(data_key='Name')
    name_english = fields.String(data_key='NameEnglish')
    type = fields.String(data_key='Type')
    vat_rate = fields.String(data_key='VatRate')
    is_active = fields.Boolean(data_key='IsActive')
    vat_rate_percent = fields.Number(data_key='VatRatePercent')
    domestic_sales_subject_to_reversed_construction_vat_account_number = fields.Integer(
        data_key='DomesticSalesSubjectToReversedConstructionVatAccountNumber')
    domestic_sales_subject_to_vat_account_number = fields.Integer(
        data_key='DomesticSalesSubjectToVatAccountNumber')
    domestic_sales_vat_exempt_account_number = fields.Integer(
        data_key='DomesticSalesVatExemptAccountNumber')
    foreign_sales_subject_to_moss_account_number = fields.Integer(
        data_key='ForeignSalesSubjectToMossAccountNumber')
    foreign_sales_subject_to_third_party_sales_account_number = fields.Integer(
        data_key='ForeignSalesSubjectToThirdPartySalesAccountNumber')
    foreign_sales_subject_to_vat_within_eu_account_number = fields.Integer(
        data_key='ForeignSalesSubjectToVatWithinEuAccountNumber')
    foreign_sales_vat_exempt_outside_eu_account_number = fields.Integer(
        data_key='ForeignSalesVatExemptOutsideEuAccountNumber')
    foreign_sales_vat_exempt_within_eu_account_number = fields.Integer(
        data_key='ForeignSalesVatExemptWithinEuAccountNumber')
    domestic_sales_vat_code_exempt_account_number = fields.Integer(
        data_key='DomesticSalesVatCodeExemptAccountNumber')
    changed_utc = fields.DateTime(
        description='Read-only',
        data_key='ChangedUtc')

    class Meta:
        # GET /v2/articleaccountcodings Get a list of article account codings. Vat rates are on present UTC time. Specify date (yyyy-MM-dd) to get for specific date.
        # GET /v2/articleaccountcodings/{articleAccountCodingId} Get a single article account coding. Vat rates are on present UTC time. Specify date (yyyy-MM-dd) to get for specific date.
        pass


class ArticleLabel(VismaModel):
    id = fields.UUID(
        description='Read-only: Unique Id provided by eAccounting',
        data_key='Id')
    name = fields.String(
        required=True,
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50)],
        data_key='Name')
    description = fields.String(
        description='Max length: 400 characters',
        validate=[Length(min=0, max=400)],
        data_key='Description')

    class Meta:
        # GET /v2/articlelabels Gets articlelabels.
        # POST /v2/articlelabels Create an articlelabel.
        # DELETE /v2/articlelabels/{articleLabelId} Deletes an aticlelabel.
        # GET /v2/articlelabels/{articleLabelId} Gets an articlelabel by id.
        # PUT /v2/articlelabels/{articleLabelId} Replace content of an articlelabel.
        pass


class Article(VismaModel):
    id = fields.UUID(
        description='Read-only: Unique Id provided by eAccounting',
        data_key='Id')
    is_active = fields.Boolean(
        required=True,
        data_key='IsActive')
    number = fields.String(
        required=True,
        description='Max length: 40 characters',
        validate=[Length(min=0, max=40)],
        data_key='Number')
    name = fields.String(
        required=True,
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50)],
        data_key='Name')
    name_english = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50)],
        data_key='NameEnglish')
    net_price = fields.Number(
        description='Format: Max 2 decimals',
        validate=[Range(min=0, max=10000000),
                  # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))
                  ],
        data_key='NetPrice')
    gross_price = fields.Number(
        description='Format: Max 2 decimals',
        validate=[
            Range(min=0, max=10000000),
            # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))
        ],
        data_key='GrossPrice')
    coding_id = fields.UUID(
        required=True,
        description='Source: Get from /v1/articleaccountcodings',
        data_key='CodingId')
    coding_name = fields.String(description='Read-only', data_key='CodingName')
    unit_id = fields.UUID(
        required=True,
        description='Source: Get from /v1/units',
        data_key='UnitId')
    unit_name = fields.String(
        description='Read-only: Returns the unit name entered from UnitId',
        data_key='UnitName')
    unit_abbreviation = fields.String(
        description='Read-only: Returns the unit abbreviation entered from UnitId',
        data_key='UnitAbbreviation')
    stock_balance = fields.Number(
        description='Default: 0. Purpose: Sets the stock balance for this article',
        # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
        data_key='StockBalance')
    stock_balance_manually_changed_utc = fields.DateTime(
        description='Read-only: Set when the stock balance is changed manually',
        data_key='StockBalanceManuallyChangedUtc')
    stock_balance_reserved = fields.Number(
        description='Purpose: Returns the reserved stock balance for this article',
        data_key='StockBalanceReserved')
    stock_balance_available = fields.Number(
        description='Purpose: Returns the available stock balance for this article',
        data_key='StockBalanceAvailable')
    changed_utc = fields.DateTime(
        description='Purpose: Returns the last date and time from when a change was made on the article',
        data_key='ChangedUtc')
    house_work_type = fields.Integer(data_key='HouseWorkType')
    purchase_price = fields.Number(data_key='PurchasePrice')
    purchase_price_manually_changed_utc = fields.DateTime(
        description='Read-only: Set when the purchase price is changed manually',
        data_key='PurchasePriceManuallyChangedUtc')
    send_to_webshop = fields.Boolean(
        description='Purpose: If true, will send article to VismaWebShop (If company has the integration). Default: True',
        data_key='SendToWebshop')
    article_labels = fields.List(fields.Nested('ArticleLabelApi'),
                                 data_key='ArticleLabels')

    class Meta:
        # GET /v2/articles Gets articles.
        # POST /v2/articles Create a single article.
        # GET /v2/articles/{articleId} Gets an article by id.
        # PUT /v2/articles/{articleId} Replace the data in an article.
        pass


class AttachmentLink(VismaModel):
    document_id = fields.UUID(
        description='The Id of the corresponding linked document',
        data_key='DocumentId')
    document_type = fields.Integer(
        required=True,
        description='0 = None, 1 = SupplierInvoice, 2 = Receipt, 3 = Voucher, 4 = SupplierInvoiceDraft, 5 = AllocationPeriod, 6 = Transfer',
        validate=[OneOf(choices=[0, 1, 2, 3, 4, 5, 6], labels=[])],
        data_key='DocumentType')
    attachment_ids = fields.List(fields.UUID(),
                                 required=True,
                                 data_key='AttachmentIds')

    class Meta:
        # POST /v2/attachmentlinks Create a new links between a document and a set of attachments.
        #DELETE /v2/attachmentlinks/{attachmentId} Delete the link to an attachment.
        pass


# TODO: How to handle when different schemas are used for Post and get?
class AttachmentResult(VismaModel):
    id = fields.UUID(data_key='Id')
    content_type = fields.String(data_key='ContentType')
    document_id = fields.UUID(data_key='DocumentId')
    attached_document_type = fields.Integer(
        description='0 = None, 1 = SupplierInvoice, 2 = Receipt, 3 = Voucher, 4 = SupplierInvoiceDraft, 5 = AllocationPeriod, 6 = Transfer',
        validate=[OneOf(choices=[0, 1, 2, 3, 4, 5, 6], labels=[])],
        data_key='AttachedDocumentType')
    file_name = fields.String(data_key='FileName')
    temporary_url = fields.String(data_key='TemporaryUrl')
    comment = fields.String(data_key='Comment')
    supplier_name = fields.String(data_key='SupplierName')
    amount_invoice_currency = fields.Number\
        (data_key='AmountInvoiceCurrency')
    type = fields.Integer(
        description='0 = Invoice, 1 = Receipt, 2 = Document',
        validate=[OneOf(choices=[0, 1, 2], labels=[])],
        data_key='Type')
    attachment_status = fields.Integer(
        description='0 = Matched, 1 = Unmatched',
        validate=[OneOf(choices=[0, 1], labels=[])],
        data_key='AttachmentStatus')
    uploaded_by = fields.String(description='Read-only', data_key='UploadedBy')
    image_date = fields.DateTime(description='Read-only', data_key='ImageDate')

    class Meta:
        # GET /v2/attachments Fetch attachments.
        # POST uses AttachemantUpload!
        # DELETE /v2/attachments/{attachmentId} Delete an attachment.
        # GET /v2/attachments/{attachmentId} Get a specific attachment.
        pass


class AttachmentUpload(VismaModel):
    id = fields.UUID(data_key='Id')
    content_type = fields.String(
        required=True, description="= ['image/jpeg' or 'image/png' or 'image/tiff' or 'application/pdf']",
        validate=[Length(min=0, max=15)],
        data_key='ContentType')
    file_name = fields.String(required=True, data_key='FileName')
    data = fields.String(
        description='Format: Must be Base64 encoded byte array.',
        data_key='Data')
    url = fields.String(description='Must be public URL', data_key='Url')

    class Meta:
        # is used for uploading attachements
        pass


class BankAccount(VismaModel):
    bank = fields.UUID(
        description='Not required for bank accounts of cash or tax account type',
        data_key='Bank')
    bank_account_type = fields.Integer(
        required=True,
        description='1 = ChequeAccount, 2 = CashAccount, 3 = SavingsAccount, 4 = CurrencyAccount, 5 = DigitalWalletAccount,\r\n6 = CashCreditAccount, 7 = TaxAccount',
        validate=[OneOf(choices=[1, 2, 3, 4, 5, 6, 7], labels=[])],
        data_key='BankAccountType')
    bank_account_type_description = fields.String(
        description='Read-only: Description of Bank Account type',
        data_key='BankAccountTypeDescription')
    bban = fields.String(
        description='Also known as Bank Account number. Not required for bank accounts of cash or tax account type',
        validate=[Length(min=0, max=35)],
        data_key='Bban')
    iban = fields.String(validate=[Length(min=0, max=35)],
                         data_key='Iban')
    name = fields.String(required=True,
                         validate=[Length(min=0, max=200)],
                         data_key='Name')
    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id')
    is_active = fields.Boolean(data_key='IsActive')
    ledger_account_number = fields.Integer(required=True,
                                           data_key='LedgerAccountNumber')
    has_active_bank_agreement = fields.Boolean(
        data_key='HasActiveBankAgreement')
    is_default_cheque_account = fields.Boolean(
        description='Purpose: Only used when having several cheque accounts',
        data_key='IsDefaultChequeAccount')

    class Meta:
        # GET /v2/bankaccounts Get bank accounts.
        # POST /v2/bankaccounts Add a bank account.
        # DELETE /v2/bankaccounts/{bankAccountId} Delete a bank account.
        # GET /v2/bankaccounts/{bankAccountId} Get a specific bank account.
        # PUT /v2/bankaccounts/{bankAccountId} Replace the data in a bank account.
        pass

class Bank(VismaModel):
    id = fields.UUID(data_key='Id')
    name = fields.String(data_key='Name')

    class Meta:
        # GET /v2/banks Get banks.
        pass












