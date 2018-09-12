from marshmallow.validate import OneOf, Length, Regexp, Range
from marshmallow import fields

from visma.base import VismaModel


class PaginatedResponse(VismaModel):
    """
    Represents the structure of paginated responses on all API endpoints that
    supports pagination.

    .. note::
       As of now this is overridden in model meta class.
       Had problem getting the attriutes to register on creation

    """
    meta = fields.Nested('PaginationMetadataSchema', data_key='Meta')


class PaginationMetadata(VismaModel):
    """
    Represents the data structure of the meta data for all paginated responses.

    :argument int current_page: The current page of the pagination.
    :argument int page_size: Number of object on page.
    :argument int total_number_of_pages: Number of pages
    :argument int total_number_of_results: Total of objects in results.
    :argument datetime.datetime server_time_utc: The servers time serving the
        request
    """
    current_page = fields.Integer(data_key='CurrentPage')
    page_size = fields.Integer(data_key='PageSize')
    total_number_of_pages = fields.Integer(data_key='TotalNumberOfPages')
    total_number_of_results = fields.Integer(data_key='TotalNumberOfResults')
    server_time_utc = fields.DateTime(data_key='ServerTimeUtc')


class Customer(VismaModel):
    """
    Models the customer object in Visma e-Accounting.

    endpoint
        /customers
    allowed_methods
        ['list', 'get', 'create', 'update', 'dlete']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
    scopes
        * ea:sales,
        * ea.local:mobile_user

    :argument uuid.UUID id: ``read-only`` Unique Id provided by eAccounting
    :argument str customer_number: Unique identifier for customer. If none is
        provided Visma eAccounting API will generate one on creation.
        Max length: 20 characters.
    :argument str corporate_identity_number: Legal identifier of the customer.
        If the customer is a private person this field should be their social
        number. Max lenght = 20 characters.
    :argument str contact_person_email: Email for the contact person at the
        customer. Max lenght = 255 characters
    :argument str contact_person_mobile: Customer contact person's mobile number
    :argument str contact_person_name: Customer contact person's name
    :argument str contact_person_phone: Customer contact person's phone number
    :argument str currency_code: The code of the currency used when dealing with
        this customer. Example SEK or EUR
        ``default = Currency code in company settings``
    :argument str gln: ``Obsolete`` Use :attr:`edi_gln_number` instead.
    :argument str email_address: Customer email address. Used for sending
        invoices.
    :argument str invoice_address1: ``Max length: 50 characters``
    :argument str invoice_address2: ``Max length: 50 characters``
    :argument str invoice_postal_code: ``Max length: 10 characters``
    :argument str invoice_city: ``Max length: 50 characters``
    :argument str invoice_country_code: ``Max length: 2 characters``
    :argument str delivery_customer_name: Use if name on deliver differs from
        customer name. ``Max length: 100 characters``
    :argument str delivery_address1: Use if delivery address differs from
        customer invoice address.  ``Max length: 50 characters``
    :argument str delivery_address2: Use if delivery address differs from
        customer invoice address.  ``Max length: 50 characters``
    :argument str delivery_city: Use if delivery address differs from customer
        invoice address.  ``Max length: 50 characters``
    :argument str delivery_country_code: Use if delivery address differs from
        customer invoice address.  ``Max length: 2 characters``
    :argument str delivery_postal_code: Use if delivery address differs from
        customer invoice address.  ``Max length: 10 characters``
    :argument uuid.UUID delivery_method_id: Reference to the
        :class:`DeliveryMethod` used.
    :argument uuid.UUID delivery_term_id: Referenct to the
        :class:`DeliveryTerm` used.
    :argument uuid.UUID pay_to_account_id: ``read-only`` Referece to
        :class:`Account` where payments are registered.
    :argument str name: Customer name. ``Max length: 50 characters``
    :argument str note: Note on customer. Free text.
        ``Max length: 4000 characters``
    :argument bool reverse_charge_on_construction_services: ``default=False``.
        If True, VatNumber must be set as well.
    :argument int webshop_customer_number: Reference to customer i webshop.
    :argument str mobile_phone: Customer mobile phone number.
        ``Max length: 50 characters``
    :argument str telephone: Customer mobile phone number.
        ``Max length: 50 characters``
    :argument uuid.UUID terms_of_payment_id: ``Required`` Reference to the
        :class:`TermsOfPayment` used.
    :argument TermsOfPayment terms_of_payment: ``read-only``
        The :class:`TermsOfPayment` used.
    :argument str vat_number: Customers VAT Number. Format: 2 character country
        code followed by 8-12 numbers. ``Max length: 20 characters``
    :argument str www_address: Customers website. ``Max length: 255 characters``
    :argument datetime.datetime last_invoice_date: ``read-only``
        Last invoice date.
    :argument bool is_private_person: ``required`` ``default=False``
    :argument discount_percentage: Customer wide discount specified like 0.9
        for 10% discount. Only allows 4 decimals.
    :argument datetime.datetime changed_utc: ``read-only`` Last date and time
        from when a change was made on the customer
    :argument bool is_active: ``required`` ``default=True``
    :argument bool force_bookkeep_vat: ``default=True`` Not entrirely sure what
        setting this to false will do. ``Usage Unknown``
    :argument sales_document_language: Language code for sales documents.
        ``Max length: 2 characters``
    :argument str edi_gln_number: What is this used for?? ``Unknown Use``
    :argument str electronic_address: ``Unknown Use`` Probarbly have something
        to do with sending and recieveing electronic invoices.
    :argument str electronic_reference: ``Unknown Use`` Probarbly have something
        to do with sending and recieveing electronic invoices.
    :argument str edi_service_deliverer_id: ``Unknown Use`` Probarbly have
        something to do with sending and recieveing electronic invoices.
    :argument datetime.datetime auto_invoice_activation_email_sent_date: Date when electronic
        invoicing was activated.
    :argument datetime.datetime auto_invoice_registration_request_sent_date:  Date when electronic
        invoicing was requested
    :argument list(str) email_addresses: List if email addresses.

    .. todo::

        Need to contact Visma API Team to get proper explanation on:

        * force_bookkeep_vat
        * edi_gln_number
        * electronic_address
        * electronic_reference
        * edi_service_deliverer_id
        * Which emails are used for invoicing? all?


    """

    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id', load_only=True, )
    customer_number = fields.String(description=('Max length: 20 characters. '
                                                 'Purpose: Unique identifier. '
                                                 'If not provided, eAccounting will provide one'),
                                    validate=[Length(min=0, max=16, )],
                                    data_key='CustomerNumber', allow_none=True)
    corporate_identity_number = fields.String(
        description='Max length: 20 characters',
        validate=[Length(min=0, max=20, )], data_key='CorporateIdentityNumber',
        allow_none=True)
    contact_person_email = fields.String(
        description='Max length: 255 characters',
        validate=[Length(min=0, max=255, )], data_key='ContactPersonEmail',
        allow_none=True)
    contact_person_mobile = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )], data_key='ContactPersonMobile',
        allow_none=True)
    contact_person_name = fields.String(
        description='Max length: 100 characters',
        validate=[Length(min=0, max=100, )], data_key='ContactPersonName',
        allow_none=True)
    contact_person_phone = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )], data_key='ContactPersonPhone',
        allow_none=True)
    currency_code = fields.String(description=('Max length: 3 characters. '
                                               'Default value: Currency of the user company'),
                                  validate=[Length(min=0, max=3, )],
                                  data_key='CurrencyCode', allow_none=True)
    gln = fields.String(
        description='NOTE: Obsolete. Please use EdiGlnNumber instead',
        validate=[Length(min=0, max=255, )], data_key='GLN', allow_none=True)
    email_address = fields.String(description='Max length: 255 characters',
                                  validate=[Length(min=0, max=255, )],
                                  data_key='EmailAddress', allow_none=True)
    invoice_address1 = fields.String(description='Max length: 50 characters',
                                     validate=[Length(min=0, max=50, )],
                                     data_key='InvoiceAddress1',
                                     allow_none=True)
    invoice_address2 = fields.String(description='Max length: 50 characters',
                                     validate=[Length(min=0, max=50, )],
                                     data_key='InvoiceAddress2',
                                     allow_none=True)
    invoice_city = fields.String(required=True,
                                 description='Max length: 50 characters',
                                 validate=[Length(min=0, max=50, )],
                                 data_key='InvoiceCity')
    invoice_country_code = fields.String(description='Max length: 2 characters',
                                         validate=[Length(min=0, max=2, )],
                                         data_key='InvoiceCountryCode',
                                         allow_none=True)
    invoice_postal_code = fields.String(required=True,
                                        description='Max length: 10 characters',
                                        validate=[Length(min=0, max=10, )],
                                        data_key='InvoicePostalCode',
                                        allow_none=True)
    delivery_customer_name = fields.String(
        description='Max length: 100 characters',
        validate=[Length(min=0, max=100, )], data_key='DeliveryCustomerName',
        allow_none=True)
    delivery_address1 = fields.String(
        description=('Max length: 50 characters. Purpose: Only used if invoice '
                     'address differs from delivery address'),
        validate=[Length(min=0, max=50, )], data_key='DeliveryAddress1',
        allow_none=True)
    delivery_address2 = fields.String(
        description=('Max length: 50 characters. Purpose: Only used if invoice '
                     'address differs from delivery address'),
        validate=[Length(min=0, max=50, )], data_key='DeliveryAddress2',
        allow_none=True)
    delivery_city = fields.String(
        description=('Max length: 50 characters. Purpose: Only used if invoice '
                     'city differs from delivery city'),
        validate=[Length(min=0, max=50, )], data_key='DeliveryCity',
        allow_none=True)
    delivery_country_code = fields.String(
        description=('Max length: 2 characters. Purpose: Only used if invoice '
                     'country code differs from delivery country code'),
        validate=[Length(min=0, max=2, )], data_key='DeliveryCountryCode',
        allow_none=True)
    delivery_postal_code = fields.String(
        description=('Max length: 10 characters. Purpose: Only used if invoice '
                     'postal code differs from delivery postal code'),
        validate=[Length(min=0, max=10, )], data_key='DeliveryPostalCode',
        allow_none=True)
    delivery_method_id = fields.UUID(
        description='Source: Get from /v2/deliverymethods',
        data_key='DeliveryMethodId', allow_none=True)
    delivery_term_id = fields.UUID(
        description='Source: Get from /v2/deliveryterms',
        data_key='DeliveryTermId', allow_none=True)
    pay_to_account_id = fields.UUID(
        description=('Read-only: The account Id on which payments are '
                     'registered'), data_key='PayToAccountId', load_only=True)
    name = fields.String(required=True, description='Max length: 50 characters',
                         validate=[Length(min=0, max=50, )], data_key='Name')
    note = fields.String(description='Max length: 4000 characters',
                         validate=[Length(min=0, max=4000, )], data_key='Note',
                         allow_none=True)
    reverse_charge_on_construction_services = fields.Boolean(
        description=('Default: false. '
                     'Purpose: If true, VatNumber must be set aswell'),
        data_key='ReverseChargeOnConstructionServices', default=False)
    webshop_customer_number = fields.Integer(data_key='WebshopCustomerNumber',
                                             allow_none=True)
    mobile_phone = fields.String(description='Max length: 50 characters',
                                 validate=[Length(min=0, max=50, )],
                                 data_key='MobilePhone', allow_none=True)
    telephone = fields.String(description='Max length: 50 characters',
                              validate=[Length(min=0, max=50, )],
                              data_key='Telephone', allow_none=True)
    terms_of_payment_id = fields.UUID(required=True,
                                      description='Source: Get from /v2/termsofpayment',
                                      data_key='TermsOfPaymentId')
    terms_of_payment = fields.Nested('TermsOfPaymentSchema',
                                     data_key='TermsOfPayment', allow_none=True,
                                     load_only=True)
    vat_number = fields.String(
        description=('Max length: 20 characters. Format: 2 character country '
                     'code followed by 8-12 numbers.'),
        validate=[Length(min=0, max=20, )], data_key='VatNumber',
        allow_none=True)
    www_address = fields.String(description='Max length: 255 characters',
                                validate=[Length(min=0, max=255, )],
                                data_key='WwwAddress', allow_none=True)
    last_invoice_date = fields.DateTime(
        description='Read-only. Purpose: Returns the last invoice date',
        data_key='LastInvoiceDate', load_only=True, allow_none=True)
    is_private_person = fields.Boolean(required=True,
                                       data_key='IsPrivatePerson',
                                       default=False)
    discount_percentage = fields.Number(description='Format: 4 decimals',
                                        validate=[Range(min=0, max=1, ),
                                                  # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,4})?'))
                                                  ],
                                        data_key='DiscountPercentage',
                                        default=0)
    changed_utc = fields.DateTime(
        description=('Read-only. Purpose: Returns the last date and time from '
                     'when a change was made on the customer'),
        data_key='ChangedUtc', load_only=True)
    is_active = fields.Boolean(required=True, data_key='IsActive', default=True)
    force_bookkeep_vat = fields.Boolean(data_key='ForceBookkeepVat',
                                        default=True, allow_none=True)
    edi_gln_number = fields.String(data_key='EdiGlnNumber', allow_none=True)
    sales_document_language = fields.String(
        description='Max length: 2 characters',
        validate=[Length(min=0, max=2, )], data_key='SalesDocumentLanguage',
        allow_none=True)
    electronic_address = fields.String(data_key='ElectronicAddress',
                                       allow_none=True)
    electronic_reference = fields.String(data_key='ElectronicReference',
                                         allow_none=True)
    edi_service_deliverer_id = fields.String(data_key='EdiServiceDelivererId',
                                             allow_none=True)
    auto_invoice_activation_email_sent_date = fields.DateTime(
        data_key='AutoInvoiceActivationEmailSentDate', allow_none=True)
    auto_invoice_registration_request_sent_date = fields.DateTime(
        data_key='AutoInvoiceRegistrationRequestSentDate', allow_none=True)
    email_addresses = fields.List(fields.String(), data_key='EmailAddresses',
                                  allow_none=True)

    customer_labels = fields.List(fields.Nested('CustomerLabelSchema'),
                                  data_key='CustomerLabels', allow_none=True)

    class Meta:
        endpoint = '/customers'
        allowed_methods = ['list', 'get', 'create', 'update', 'delete']
        envelope_class = PaginatedResponse
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class TermsOfPayment(VismaModel):
    """
    Describes a term of payment that can be set on customers.

    endpoint
        /termsofpayments
    allowed_methods
        ['list', 'get']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
    scopes
        * ea:sales
        * ea:sales_readonly
        * ea:purchase
        * ea:purchase_readonly
        * ea.local:mobile_user


    :argument uuid.UUID id: ``read-only`` Unique Id provided by eAccounting
    :argument str name: Name of term
    :argument str name_english: English name if term.
    :argument int number_of_days: Number of days until payment.
    :argument int terms_of_payment_type_id: Need more info on how to interpret.
        ``Unknown Use``
    :argument str terms_of_payment_type_text: Description of term.
    :argument bool available_for_sales: Indicates if term can be used for
        customer invoies.
    :argument bool available_for_purchase: Indicates if the term can be used for
        supplier invoices.

    .. todo::

        What different types of terms_of_payment_types are there?

    """

    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id', load_only=True)
    name = fields.String(data_key='Name')
    name_english = fields.String(data_key='NameEnglish')
    number_of_days = fields.Integer(data_key='NumberOfDays')
    terms_of_payment_type_id = fields.Integer(data_key='TermsOfPaymentTypeId')
    terms_of_payment_type_text = fields.String(
        data_key='TermsOfPaymentTypeText', allow_none=True)
    available_for_sales = fields.Boolean(data_key='AvailableForSales',
                                         allow_none=True)
    available_for_purchase = fields.Boolean(data_key='AvailableForPurchase')

    class Meta:
        endpoint = '/termsofpayments'
        allowed_methods = ['list', 'get']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class CustomerInvoiceDraft(VismaModel):
    """
    Represents a Customer Invoice Draft.

    endpoint
        /customerinvoicedrafts
    allowed_methods
        ['list', 'get', 'create', 'update', 'delete']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
    scope
        * ea:sales
        * ea:sales_readonly
        * ea.local:mobile_user


    :argument uuid.UUID id: ``read-only``  Unique Id provided by eAccounting
    :argument uuid.UUID customer_id: ``required`` Reference to :class:`Customer`
    :argument datetime.datetime created_utc: ``read-only`` Creation time. Is
        automatically set
    :argument bool is_credit_invoice: Indicates if the invoice is a credit
        invoice. ``default=False``
    :argument int rot_reduced_invoicing_type: Indicates the invoicing type in
        respect to ROT and RUT. (Sweden) 0 = Normal, 1 = ROT, 2 = RUT.
        ``default=0``
    :argument str rot_reduced_invoicing_property_name: ``Unknown use``
        ``Max length: 40 characters``
    :argument str rot_reduced_invoicing_org_number: ``Unknown use``
        ``Max length: 11 characters``
    :argument number rot_reduced_invoicing_amount: ``Unknown use``
        ``Format: 2 decimals``, ``default=0.00``
    :argument bool rot_reduced_invoicing_automatic_distribution: ``Unknown use``
        ``default=False``
    :argument int rot_property_type: ``Unknown use``
    :argument number house_work_other_costs: ``Unknown use``
    :argument list(CustomerInvoiceDraftRow) rows:  List of
        :class:`CustomerInvoiceDraftRow` with the details of the invoice.
        ``default=list()``
    :argument list(SalesDocumentRotRutReductionPerson) persons: List of
        :class:`SalesDocumentRotRutReductionPerson` when using ROT and RUT.
        ``Unknown use`` ``default=list()``
    :argument str your_reference: Customers reference.
        ``Max length: 100 characters``
    :argument str our_reference: Companys reference.
        ``Max length: 100 characters``
    :argument str invoice_customer_name: ``Read-only`` Customer name on invoice.
         ``Max length: 50 characters``
    :argument  str invoice_address1: Invoice address row 1
        ``Max length: 50 characters``
    :argument str invoice_address2: Invoice address row 2
        ``Max length: 50 characters``
    :argument str invoice_postal_code: = Invoice postal code.
        ``Max length: 10 characters``
    :argument str invoice_city: Invoice city. ``Max length: 50 characters``
    :argument str invoice_country_code:  Invoice country code.
        ``Max length: 2 characters``, ``default=SE``
    :argument str invoice_currency_code: ``read-only`` Invoice currency code
    :argument str delivery_customer_name:  ``Max length: 50 characters``
    :argument str delivery_address1: ``Max length: 50 characters``
    :argument str delivery_address2: ``Max length: 50 characters``
    :argument str delivery_postal_code: ``Max length: 10 characters``
    :argument str delivery_city: ``Max length: 50 characters``
    :argument str delivery_country_code: ``Max length: 2 characters``
    :argument str delivery_method_name: ``Max length: 50 characters``
    :argument str delivery_term_name: ``Max length: 50 characters``
    :argument str delivery_method_code: ``Max length: 20 characters``
    :argument str delivery_term_code: ``Max length: 50 characters``
    :argument bool eu_third_party: Indicates if the invoice is subject to rules
        about EU third pary invoicing. ``default=False``
    :argument bool customer_is_private_person: ``required`` Indicates if the
        reciever of the invoice is a private person. ``default=False``
    :argument bool reverse_charge_on_construction_services: ``read-only``
        ``Unknown use``  Need investigation.
    :argument list(uuid.UUID) sales_document_attachments: ``read-only`` List of
        references to attached documents.
    :argument datetime.datetime invoice_date: invoice date
    :argument datetime.datetime delivery_date: delivery date
    :argument number total_amount: ``read-only``  Calculated by eAccounting API
    :argument number total_vat_amount:  ``read-only`` Calculated by eAccounting
        API
    :argument number total_roundings: ``read-only`` Calculated by eAccounting
        API
    :argument number total_amount_base_currency:  ``read-only`` Calculated by
        eAccounting API
    :argument number total_vat_amount_base_currency: ``read-only`` Calculated by
        eAccounting API
    :argument str customer_number: ``read-only`` ``Max length: 16 characters``
    :argument bool includes_vat: ``read-only`` If true the unit prices on rows
        include VAT. The value is set upon creation depending whether "Show
        prices excl. VAT for private individuals" in company' settings is marked
        or not'

    .. todo::

        Contact Visma API Team about rules for ROT and RUT so it can be
        documented

    """

    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     load_only=True, data_key='Id')
    customer_id = fields.UUID(required=True,
                              description='Source: Get from /v2/customers',
                              data_key='CustomerId')
    created_utc = fields.DateTime(description='Read-only: Is automatically set',
                                  load_only=True, data_key='CreatedUtc')
    is_credit_invoice = fields.Boolean(data_key='IsCreditInvoice',
                                       default=False)
    rot_reduced_invoicing_type = fields.Integer(required=True,
                                                description='0 = Normal, 1 = Rot, 2 = Rut',
                                                validate=[
                                                    OneOf(choices=[0, 1, 2],
                                                          labels=[])],
                                                data_key='RotReducedInvoicingType',
                                                default=0)
    rot_reduced_invoicing_property_name = fields.String(
        description='Max length: 40 characters',
        validate=[Length(min=0, max=40)],
        data_key='RotReducedInvoicingPropertyName', allow_none=True)
    rot_reduced_invoicing_org_number = fields.String(
        description='Max length: 11 characters',
        validate=[Length(min=0, max=11)],
        data_key='RotReducedInvoicingOrgNumber', allow_none=True)
    rot_reduced_invoicing_amount = fields.Number(
        description='Format: 2 decimals',
        # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
        data_key='RotReducedInvoicingAmount', default=0.00)
    rot_reduced_invoicing_automatic_distribution = fields.Boolean(
        description='Default: False',
        data_key='RotReducedInvoicingAutomaticDistribution', default=False)
    rot_property_type = fields.Integer(data_key='RotPropertyType',
                                       allow_none=True)
    house_work_other_costs = fields.Number(data_key='HouseWorkOtherCosts',
                                           allow_none=True)
    rows = fields.List(fields.Nested('CustomerInvoiceDraftRowSchema'),
                       data_key='Rows', default=list())
    persons = fields.List(
        fields.Nested('SalesDocumentRotRutReductionPersonSchema'),
        data_key='Persons', default=list())
    your_reference = fields.String(description='Max length: 100 characters',
                                   validate=[Length(min=0, max=100)],
                                   data_key='YourReference', allow_none=True)
    our_reference = fields.String(description='Max length: 100 characters',
                                  validate=[Length(min=0, max=100)],
                                  data_key='OurReference', allow_none=True)
    invoice_customer_name = fields.String(load_only=True,
                                          description='Max length: 50 characters',
                                          validate=[Length(min=0, max=50)],
                                          data_key='InvoiceCustomerName')
    invoice_address1 = fields.String(description='Max length: 50 characters',
                                     validate=[Length(min=0, max=50)],
                                     data_key='InvoiceAddress1',
                                     allow_none=True)
    invoice_address2 = fields.String(description='Max length: 50 characters',
                                     validate=[Length(min=0, max=50)],
                                     data_key='InvoiceAddress2',
                                     allow_none=True)
    invoice_postal_code = fields.String(required=True,
                                        description='Max length: 10 characters',
                                        validate=[Length(min=0, max=10)],
                                        data_key='InvoicePostalCode')
    invoice_city = fields.String(required=True,
                                 description='Max length: 50 characters',
                                 validate=[Length(min=0, max=50, )],
                                 data_key='InvoiceCity')
    invoice_country_code = fields.String(required=True,
                                         description='Max length: 2 characters',
                                         validate=[Length(min=0, max=2, )],
                                         data_key='InvoiceCountryCode',
                                         default='SE')
    invoice_currency_code = fields.String(description='Read-only',
                                          data_key='InvoiceCurrencyCode',
                                          load_only=True)
    delivery_customer_name = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )], data_key='DeliveryCustomerName',
        allow_none=True)
    delivery_address1 = fields.String(description='Max length: 50 characters',
                                      validate=[Length(min=0, max=50, )],
                                      data_key='DeliveryAddress1',
                                      allow_none=True)
    delivery_address2 = fields.String(description='Max length: 50 characters',
                                      validate=[Length(min=0, max=50, )],
                                      data_key='DeliveryAddress2',
                                      allow_none=True)
    delivery_postal_code = fields.String(
        description='Max length: 10 characters',
        validate=[Length(min=0, max=10, )], data_key='DeliveryPostalCode',
        allow_none=True)
    delivery_city = fields.String(description='Max length: 50 characters',
                                  validate=[Length(min=0, max=50, )],
                                  data_key='DeliveryCity', allow_none=True)
    delivery_country_code = fields.String(
        description='Max length: 2 characters',
        validate=[Length(min=0, max=2, )], data_key='DeliveryCountryCode',
        allow_none=True)
    delivery_method_name = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50, )], data_key='DeliveryMethodName',
        allow_none=True)
    delivery_term_name = fields.String(description='Max length: 50 characters',
                                       validate=[Length(min=0, max=50, )],
                                       data_key='DeliveryTermName',
                                       allow_none=True)
    delivery_method_code = fields.String(
        description='Max length: 20 characters',
        validate=[Length(min=0, max=20, )], data_key='DeliveryMethodCode',
        allow_none=True)
    delivery_term_code = fields.String(description='Max length: 20 characters',
                                       validate=[Length(min=0, max=20, )],
                                       data_key='DeliveryTermCode',
                                       allow_none=True)
    eu_third_party = fields.Boolean(required=True, data_key='EuThirdParty',
                                    default=False)
    customer_is_private_person = fields.Boolean(required=True,
                                                data_key='CustomerIsPrivatePerson',
                                                default=False)
    reverse_charge_on_construction_services = fields.Boolean(
        description='Read-only', data_key='ReverseChargeOnConstructionServices',
        load_only=True)
    sales_document_attachments = fields.List(fields.UUID(),
                                             description='Read-only',
                                             data_key='SalesDocumentAttachments',
                                             load_only=True)
    invoice_date = fields.DateTime(data_key='InvoiceDate', allow_none=True)
    delivery_date = fields.DateTime(data_key='DeliveryDate', allow_none=True)
    total_amount = fields.Number(description='Read-only',
                                 data_key='TotalAmount', load_only=True)
    total_vat_amount = fields.Number(description='Read-only',
                                     data_key='TotalVatAmount', load_only=True)
    total_roundings = fields.Number(description='Read-only',
                                    data_key='TotalRoundings', load_only=True)
    total_amount_base_currency = fields.Number(description='Read-only',
                                               data_key='TotalAmountBaseCurrency',
                                               load_only=True)
    total_vat_amount_base_currency = fields.Number(description='Read-only',
                                                   data_key='TotalVatAmountBaseCurrency',
                                                   load_only=True)
    customer_number = fields.String(
        description='Read-only\r\nMax length: 16 characters', load_only=True,
        validate=[Length(min=0, max=16, )], data_key='CustomerNumber')
    includes_vat = fields.Boolean(
        description=('Read-only: If true the unit prices on rows include VAT. '
                     'The value is set upon creation depending whether "Show '
                     'prices excl. VAT for private individuals" in company '
                     'settings is marked or not'), data_key='IncludesVat',
        load_only=True)

    class Meta:
        # GET /v2/customerinvoicedrafts
        # Get all customer invoice drafts.
        # POST /v2/customerinvoicedrafts
        # Create a single customer invoice draft
        # GET /v2/customerinvoicedrafts/{invoiceDraftId}
        # Gets a customer invoice draft by id.
        # DELETE /v2/customerinvoicedrafts/{customerInvoiceDraftId}
        # Delete a customer invoice draft
        # PUT /v2/customerinvoicedrafts/{customerInvoiceDraftId}
        # Replace the data in a customer invoice draft.
        # POST /v2/customerinvoicedrafts/{customerInvoiceDraftId}/convert
        # Experimental Endpoint! This might be subject to changes.
        # Converts a CustomerInvoiceDraft to a CustomerInvoice.
        endpoint = '/customerinvoicedrafts'
        allowed_methods = ['list', 'get', 'create', 'update', 'delete']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class CustomerInvoiceDraftRow(VismaModel):
    """
    Represents a row on a :class:`CustomerInvoiceDraft`

    :argument int line_number: ``required`` Used to sort the rows. Nothing
        prevenst to have the same line numer on several rows. But the order of these
        will be random. ``Max=1000``
    :argument uuid.UUID article_id: Reference to :class:`Article` Required if is
        text_row=False,
    :argument str article_number: If not filled eAccouting will get the article
        number from the speicfied article ID.
    :argument bool is_text_row: Specifies if row i a text row or article row.
        ``default=False``
    :argument str text: Article name or Text if is_text_row=True. ``Max length:
        2000``
    :argument number unit_price: Use if you want to set a custom price on the
        article. If not set eAccounting will use the price from the article registry
        in creation. ``Format: 2 decimals``
    :argument number discount_percentage: Discount on the incoice row. Ex. 10%
        discount = 0.1 ``default=0.00``
    :argument number quantity: The amount of specified article.
        ``Format: 2 decimals``
    :argument int work_cost_type: Probarbly has with ROT and RUT to do.
        ``Unknown usage`` ``default=0``
    :argument bool is_work_cost: Probarbly has with ROT and RUT to do.
        ``Unknown usage`` ``default=False``
    :argument number  work_hours: Probarbly has with ROT and RUT to do.
        `Unknown usage``
    :argument number material_costs: Probarbly has with ROT and RUT to do.
        ``Unknown usage``
    :argument bool reversed_construction_services_vat_free: Probarbly has with
        ROT and RUT to do. ``Unknown usage`` ``default=False``
    :argument uuid.UUID cost_center_item_id1: reference to
        :class:`CostCenterItem` on invoice row
    :argument uuid.UUID cost_center_item_id2: reference to
        :class:`CostCenterItem` on invoice row
    :argument uuid.UUID cost_center_item_id3: reference to
        :class:`CostCenterItem` on invoice row
    :argument str unit_abbreviation: unit abbreviation of the article
    :argument str vat_rate_id: ``read-only`` source from
        :class:`ArticleAccountCoding`
    :argument str unit_name: Name of article unit
    :argument uuid.UUID project_id: reference to :class:`Project`

    .. todo::

        Contact Visma API Team about how to handle ROT and RUT.

    """
    line_number = fields.Integer(required=True,
                                 validate=[Range(min=0, max=1000)],
                                 data_key='LineNumber')
    article_id = fields.UUID(description=('Source: Get from /v2/articles. '
                                          'Required if IsTextRow is false'),
                             data_key='ArticleId')
    article_number = fields.String(
        description=('Purpose: Returns the article number '
                     'from the entered ArticleId'), allow_none=True,
        data_key='ArticleNumber')
    is_text_row = fields.Boolean(required=True, data_key='IsTextRow',
                                 default=False)
    text = fields.String(required=True,
                         description='Max length: 2000. Sets the article name',
                         validate=[Length(min=0, max=2000)], data_key='Text')
    unit_price = fields.Number(
        description=("Format: 2 decimals allowed\r\nDefault: The price that is "
                     "set on the article's register. For using a custom price,"
                     " use this property"),
        # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
        data_key='UnitPrice')
    discount_percentage = fields.Number(
        description='Format: 4 decimals allowed', validate=[Range(min=0, max=1),
                                                            # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,4})?'))
                                                            ],
        data_key='DiscountPercentage', default=0.00)
    quantity = fields.Number(description='Format: 2 decimals',
                             # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
                             data_key='Quantity')
    work_cost_type = fields.Integer(data_key='WorkCostType', default=0)
    is_work_cost = fields.Boolean(data_key='IsWorkCost', default=False)
    work_hours = fields.Number(data_key='WorkHours', allow_none=True)
    material_costs = fields.Number(data_key='MaterialCosts', allow_none=True)
    reversed_construction_services_vat_free = fields.Boolean(required=True,
                                                             data_key='ReversedConstructionServicesVatFree',
                                                             default=False)
    cost_center_item_id1 = fields.UUID(
        description='Source: Get from /v2/costcenteritems',
        data_key='CostCenterItemId1', allow_none=True)
    cost_center_item_id2 = fields.UUID(
        description='Source: Get from /v2/costcenteritems',
        data_key='CostCenterItemId2', allow_none=True)
    cost_center_item_id3 = fields.UUID(
        description='Source: Get from /v2/costcenteritems',
        data_key='CostCenterItemId3', allow_none=True)
    unit_abbreviation = fields.String(data_key='UnitAbbreviation',
                                      allow_none=True)
    vat_rate_id = fields.String(
        description='Source: Get from /v2/articleaccountcodings \r\nRead-only',
        data_key='VatRateId', load_only=True)
    unit_name = fields.String(data_key='UnitName', allow_none=True)
    project_id = fields.UUID(data_key='ProjectId', allow_none=True)

    def __str__(self):
        return '%s object (%s)' % (self.__class__.__name__, self.line_number)


class FiscalYear(VismaModel):
    """
    Represents a fiscal year.

    Fiscal years must be created in sequence. For example if you only have 2018
    you can't create 2020 until you have created 2019. If you want to create
    earlier fiscal year they aslo have to be adjacent to an existing fiscal year

    endpoint
        /fiscalyears
    allowed_methods
        ['list', 'create', 'get']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    :argument uuid.UUID id: ``read-only`` Unique Id provided by eAccounting
    :argument datetime.date start_date: ``required``
    :argument datetime.date end_date: ``required``
    :argument bool is_locked_for_accounting: ``read-only`` Indicates if it is
        still possible bookkeep on the year.
    :argument int bookkeeping_method: ``read-only`` 0 = Invoicing, 1 = Cash,
        2 = NoBookkeeping. When posting fiscalyear, previous years bookkeeping
        method is chosen. '

    """
    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     load_only=True, data_key='Id')
    start_date = fields.Date(data_key='StartDate', required=True, )
    end_date = fields.Date(data_key='EndDate', required=True, )
    is_locked_for_accounting = fields.Boolean(description='Read-only',
                                              load_only=True,
                                              data_key='IsLockedForAccounting')
    bookkeeping_method = fields.Integer(description=('Read-only: '
                                                     'When posting fiscalyear, previous years bookkeeping'
                                                     ' method is chosen. '
                                                     '0 = Invoicing, '
                                                     '1 = Cash, '
                                                     '2 = NoBookkeeping'),
                                        load_only=True, validate=[
            OneOf(choices=[0, 1, 2], labels=[])], data_key='BookkeepingMethod')

    class Meta:
        # GET /v2/fiscalyears Get a list of fiscal years.
        # POST /v2/fiscalyears Create a fiscal year.
        # GET /v2/fiscalyears/{id} Get a singel fiscal year.
        endpoint = '/fiscalyears'
        allowed_methods = ['list', 'create', 'get']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class VatCode(VismaModel):
    """
    Represents the diffent VAT Codes used in eAccounting.

    endpoint
        /vatcodes
    allowed_methods
        ['list', 'get']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


    :argument uuid.UUID id: ``read-only`` Unique Id provided by eAccounting
    :argument str code: VAT code
    :argument str description: Description
    :argument number vat_rate: VAT Rate (in percentage??)
    :argument RelatedAccounts related_accounts: A :class:`RelatedAccounts`
        object that holds the accounts related to this VAT code.


    .. todo::

        How is vat rate represented? 0.25 or 25 for 25% VAT?

    """

    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     load_only=True, data_key='Id')
    code = fields.String(description='Returns the VAT code', data_key='Code')
    description = fields.String(data_key='Description')
    vat_rate = fields.Number(data_key='VatRate')
    related_accounts = fields.Nested('RelatedAccountsSchema',
                                     data_key='RelatedAccounts',
                                     allow_none=True)

    class Meta:
        # GET /v2/vatcodes Gets a list of all Vat Codes
        # GET /v2/vatcodes/{id} Get a vat code item by it's id
        endpoint = '/vatcodes'
        allowed_methods = ['list', 'get']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    # TODO: remove the need to add schema into nested fields.


class RelatedAccounts(VismaModel):
    """
    Holds collected information about related accounts.

    :argument int account_number1: Account Number 1
    :argument int account_number2: Account Number 2
    :argument int account_number3: Account Number 3

    """

    account_number1 = fields.Integer(data_key='AccountNumber1', allow_none=True)
    account_number2 = fields.Integer(data_key='AccountNumber2', allow_none=True)
    account_number3 = fields.Integer(data_key='AccountNumber3', allow_none=True)

    class Meta:
        # No endpoint
        pass


class Account(VismaModel):
    """ Represents a Bookkeeping Account in eAccounting

    endpoint
        /accounts
    allowed_methods
        ['list', 'create']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    .. todo::

        There is more special cases endpoint for this objects that is not
        handled yet by the framework.


    :argument str name: The name of the account ``Max length: 100 characters``
    :argument str number: ``required`` The account number
    :argument uuid.UUID vat_code_id: = Reference to the :class:`VatCode` that is
        associated with the account
    :argument str vat_code_description: ``read-only`` Describes the
        :class:`VatCode` that is associated with the account
    :argument uuid.UUID fiscal_year_id: ``required`` Reference to the
        :class:`FiscalYear` that the account belongs to.
    :argument str reference_code: ``read-only`` The reference code on the
        account. ``Dutch companies only``
    :argument int type: ``read-only`` The account type number.
        ``Dutch companies only``
    :argument str type_description:  ``read-only`` The account type descripion.
        ``Dutch companies only``
    :argument datetime.datetime modified_utc: ``read_only`` Modifed date.
    :argument bool is_active: ``required`` Indicates if the account is active.
        ``default=False``
    :argument bool is_project_allowed: Indicates if the account can be used for
        project bookkeeping. ``default=False``
    :argument bool is_cost_center_allowed: Indicates if the account can be used
        for cost center bookkeeping. ``default=False``
    :argument bool is_blocked_for_manual_booking: Indicates if the account can
        be used for manual verification registering.

    """

    name = fields.String(required=True,
                         description='Max length: 100 characters. '
                                     'The name of the account',
                         validate=[Length(min=0, max=100)], data_key='Name')
    number = fields.String(required=True, description='The account number',
                           data_key='Number')
    vat_code_id = fields.UUID(
        description=('The Id of the VAT code that is associated with the '
                     'account'), allow_none=True, data_key='VatCodeId')
    vat_code_description = fields.String(
        description=('Read-only. Describes what kind of VAT that is associated '
                     'with the account'), load_only=True,
        data_key='VatCodeDescription')
    fiscal_year_id = fields.UUID(required=True,
                                 description='The Id of the Fiscal year that '
                                             'the account belongs to',
                                 data_key='FiscalYearId')
    reference_code = fields.String(
        description=('Read-only. Returns the reference code on the account. '
                     'This feature is for dutch companies only'),
        load_only=True, data_key='ReferenceCode')
    type = fields.Integer(
        description='Read-only. Returns account type number. Netherlands only',
        load_only=True, data_key='Type')
    type_description = fields.String(
        description='Read-only. Returns account type descripion',
        load_only=True, data_key='TypeDescription')
    modified_utc = fields.DateTime(description='Read-only.', load_only=True,
                                   data_key='ModifiedUtc')
    is_active = fields.Boolean(required=True, default=False,
                               data_key='IsActive')
    is_project_allowed = fields.Boolean(data_key='IsProjectAllowed',
                                        default=False)
    is_cost_center_allowed = fields.Boolean(data_key='IsCostCenterAllowed',
                                            default=False)
    is_blocked_for_manual_booking = fields.Boolean(
        data_key='IsBlockedForManualBooking', default=False)

    class Meta:
        # GET /v2/accounts
        # Get a list of accounts from all fiscalyears
        # POST/v2/accounts
        # Add account
        # GET /v2/accounts/standardaccounts   (just for dutch companies)
        # GET /v2/accounts/{fiscalyearId}
        # Get a list of accounts for a spcific fiscalyear
        # GET /v2/accounts/{fiscalyearId}/{accountNumber}
        # Get a single account by account number
        # PUT /v2/accounts/{fiscalyearId}/{accountNumber}
        # Replaces a account in a given fiscalyear
        endpoint = '/accounts'
        allowed_methods = ['list', 'create']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

        # TODO: how to handle the special cases?


class AccountType(VismaModel):
    """
    Default Account Types. This is applicable on all countries but most
    relevant for the Netherlands

    endpoint
        /accounttypes
    allowed_methods
        ['list']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    :argument int type: Account type number.
    :argument str type_description: Account type description

    """
    type = fields.Integer(data_key='Type')
    type_description = fields.String(data_key='TypeDescription')

    class Meta:
        # GET /v2/accounttypes
        # Gets the default account types.
        # This is applicable on all countries but most relevant for the
        #  Netherlands
        endpoint = '/accounttypes'
        allowed_methods = ['list']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class ArticleAccountCoding(VismaModel):
    """
    Represents article account coding


    endpoint
        /articleaccountcodings
    allowed_methods
        ['list', 'get']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    :argument uuid.UUID id: ``read-only`` Unique Id provided by eAccounting
    :argument string name:  Name
    :argument string name_english: English Name
    :argument string type: Type
    :argument string vat_rate: VAT rate
    :argument bool is_active: Indicates if the Article account coding is active.
    :argument number vat_rate_percent: VAT rate in percentage.
    :argument int domestic_sales_subject_to_reversed_construction_vat_account_number: Account
        number for domestic sales subject to reversed construction VAT
    :argument int domestic_sales_subject_to_vat_account_number: Account number
        for domestic sales subject to VAT.
    :argument int domestic_sales_vat_exempt_account_number: Account number for
        domestic sales that are exempt from VAT.
    :argument int foreign_sales_subject_to_moss_account_number: Account number
        for foreign sales subject to MOSS.
    :argument int foreign_sales_subject_to_third_party_sales_account_number: Account
        number for foreign sales subject to third parrt sales rules.
    :argument int foreign_sales_subject_to_vat_within_eu_account_number: Account
        number for foreign sales subject to VAT within EU.
    :argument int foreign_sales_vat_exempt_outside_eu_account_number: Account
        number for foreign sales that are exempt VAT outside of EU.
    :argument int foreign_sales_vat_exempt_within_eu_account_number: Account
        number for foreign sales that are exempt VAT within EU.
    :argument int domestic_sales_vat_code_exempt_account_number: Account number
        for domestic sales exempt a VAT Code.
    :argument datetime.datetime changed_utc: ``read-only`` Last Changed Time

    .. todo::

        It is not yet supported to filter on date for the account.

    """
    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id', load_only=True)
    name = fields.String(data_key='Name')
    name_english = fields.String(data_key='NameEnglish')
    type = fields.String(data_key='Type')
    vat_rate = fields.String(data_key='VatRate')
    is_active = fields.Boolean(data_key='IsActive')
    vat_rate_percent = fields.Number(data_key='VatRatePercent')
    domestic_sales_subject_to_reversed_construction_vat_account_number = fields.Integer(
        data_key='DomesticSalesSubjectToReversedConstructionVatAccountNumber',
        allow_none=True)
    domestic_sales_subject_to_vat_account_number = fields.Integer(
        data_key='DomesticSalesSubjectToVatAccountNumber', allow_none=True)
    domestic_sales_vat_exempt_account_number = fields.Integer(
        data_key='DomesticSalesVatExemptAccountNumber', allow_none=True)
    foreign_sales_subject_to_moss_account_number = fields.Integer(
        data_key='ForeignSalesSubjectToMossAccountNumber', allow_none=True)
    foreign_sales_subject_to_third_party_sales_account_number = fields.Integer(
        data_key='ForeignSalesSubjectToThirdPartySalesAccountNumber',
        allow_none=True)
    foreign_sales_subject_to_vat_within_eu_account_number = fields.Integer(
        data_key='ForeignSalesSubjectToVatWithinEuAccountNumber',
        allow_none=True)
    foreign_sales_vat_exempt_outside_eu_account_number = fields.Integer(
        data_key='ForeignSalesVatExemptOutsideEuAccountNumber', allow_none=True)
    foreign_sales_vat_exempt_within_eu_account_number = fields.Integer(
        data_key='ForeignSalesVatExemptWithinEuAccountNumber', allow_none=True)
    domestic_sales_vat_code_exempt_account_number = fields.Integer(
        data_key='DomesticSalesVatCodeExemptAccountNumber', allow_none=True)
    changed_utc = fields.DateTime(description='Read-only',
                                  data_key='ChangedUtc', load_only=True)

    class Meta:
        # GET /v2/articleaccountcodings
        # Get a list of article account codings.
        # Vat rates are on present UTC time.
        # Specify date (yyyy-MM-dd) to get for specific date.
        # GET /v2/articleaccountcodings/{articleAccountCodingId}
        # Get a single article account coding.
        #  Vat rates are on present UTC time.
        # Specify date (yyyy-MM-dd) to get for specific date.
        endpoint = '/articleaccountcodings'
        allowed_methods = ['list', 'get']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

        # TODO: How to handle custom query parameters?


class ArticleLabel(VismaModel):
    """
    Represents an Article Label in eAccounting.

    endpoint
        /articlelabels
    allowed_methods
        ['list', 'create', 'get', 'update', 'delete']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    :argument uuid.UUID id: ``read-only`` Unique Id provided by eAccounting
    :argument str name: Article label name ``Max length: 50 characters``
    :argument str description: Article label description
        ``Max length: 400 characters``

    """

    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id', load_only=True)
    name = fields.String(required=True, description='Max length: 50 characters',
                         validate=[Length(min=0, max=50)], data_key='Name')
    description = fields.String(description='Max length: 400 characters',
                                validate=[Length(min=0, max=400)],
                                data_key='Description', default='')

    class Meta:
        # GET /v2/articlelabels
        # Gets articlelabels.
        # POST /v2/articlelabels
        # Create an articlelabel.
        # DELETE /v2/articlelabels/{articleLabelId}
        # Deletes an aticlelabel.
        # GET /v2/articlelabels/{articleLabelId}
        # Gets an articlelabel by id.
        # PUT /v2/articlelabels/{articleLabelId}
        # Replace content of an articlelabel.
        endpoint = '/articlelabels'
        allowed_methods = ['list', 'create', 'get', 'update', 'delete']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


# TODO: Document that read only fields should have load_only=True and Boolean should always have a default value


class Article(VismaModel):
    """
    Represents an Article in eAccounting.


    endpoint
        /articles
    allowed_methods
        ['list', 'get', 'create', 'update']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


    :argument uuid.UUID id:  ``read-only``  Unique Id provided by eAccounting.
    :argument bool is_active: ``required`` Indicates if the article is active.
        ``default=True``
    :argument str number: ``required`` Article number
        ``Max length: 40 characters``
    :argument str name: ``required`` Article name ``Max length: 50 characters``
    :argument str name_english: Article name in english
        ``Max length: 50 characters``
    :argument number net_price: Net price of article
        ``Max Value: 10000000, Format: Max 2 decimals, default=0``
    :argument number gross_price: Gross price of article
        ``Max Value: 10000000, Format: Max 2 decimals, default=0``
    :argument uuid.UUID coding_id: ``required`` Reference to
        :class:`ArticleAccountCoding` used for the article.
    :argument str coding_name: ``read-only`` Article account coding name.
    :argument uuid.UUID unit_id: ``required`` Reference to :class:`Unit` used
        for the article.
    :argument str unit_name: ``read-only`` Name of unit specified in unit_id.
    :argument str unit_abbreviation: ``read-only`` Unit abbreviation of unit
        specified in unit_id.
    :argument number stock_balance: Stock balance for the article. ``default=0``
    :argument datetime.datetime stock_balance_manually_changed_utc: ``read-only``
        Set when the stock balance is changed manually, for
        example after an inventory check.
    :argument number stock_balance_reserved: ``read-only`` The reserved stock
        balance for the article.
    :argument number stock_balance_available: ``read-only``  The available
        stock balance for the article.
    :argument datetime.datetime changed_utc: Date and time from when the last
        changes was made on the article
    :argument int house_work_type: House Work Type
    :argument number purchase_price: Purchase price ``default=0``
    :argument datetime.datetime purchase_price_manually_changed_utc: ``read-only``
        Set when the purchase price is changed manually
    :argument bool send_to_webshop: If True , will send article to VismaWebShop
        (If company has the integration). ``default=True``
    :argument list(ArticleLabel) article_labels: A list of :class:`ArticleLabel`


    .. todo::

        work_house_type is not documented. Need to contact Visma API Team.

    """

    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id', load_only=True)
    is_active = fields.Boolean(required=True, data_key='IsActive', default=True)
    number = fields.String(required=True,
                           description='Max length: 40 characters',
                           validate=[Length(min=0, max=40)], data_key='Number')
    name = fields.String(required=True, description='Max length: 50 characters',
                         validate=[Length(min=0, max=50)], data_key='Name')
    name_english = fields.String(description='Max length: 50 characters',
                                 validate=[Length(min=0, max=50)],
                                 data_key='NameEnglish', default='')
    net_price = fields.Number(description='Format: Max 2 decimals',
                              validate=[Range(min=0, max=10000000),
                                        # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))
                                        ], data_key='NetPrice', default=0)
    gross_price = fields.Number(description='Format: Max 2 decimals',
                                validate=[Range(min=0, max=10000000),
                                          # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))
                                          ], data_key='GrossPrice', default=0)
    coding_id = fields.UUID(required=True,
                            description='Source: Get from /v1/articleaccountcodings',
                            data_key='CodingId')
    coding_name = fields.String(description='Read-only', data_key='CodingName',
                                load_only=True)
    unit_id = fields.UUID(required=True,
                          description='Source: Get from /v1/units',
                          data_key='UnitId')
    unit_name = fields.String(
        description='Read-only: Returns the unit name entered from UnitId',
        data_key='UnitName', load_only=True)
    unit_abbreviation = fields.String(
        description=('Read-only: Returns the unit abbreviation entered from '
                     'UnitId'), data_key='UnitAbbreviation', load_only=True)
    stock_balance = fields.Number(
        description=('Default: 0. Purpose: Sets the stock balance for this '
                     'article'),
        # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
        data_key='StockBalance', default=0)
    stock_balance_manually_changed_utc = fields.DateTime(
        description='Read-only: Set when the stock balance is changed manually',
        data_key='StockBalanceManuallyChangedUtc', load_only=True,
        allow_none=True)
    stock_balance_reserved = fields.Number(
        description=('Purpose: Returns the reserved stock balance for this '
                     'article'), data_key='StockBalanceReserved',
        load_only=True)
    stock_balance_available = fields.Number(
        description=('Purpose: Returns the available stock balance for this '
                     'article'), data_key='StockBalanceAvailable',
        load_only=True)
    changed_utc = fields.DateTime(
        description=('Purpose: Returns the last date and time from when a '
                     'change was made on the article'), data_key='ChangedUtc',
        load_only=True)
    # TODO: what is house_work_type. Not documented?
    house_work_type = fields.Integer(data_key='HouseWorkType', allow_none=True)
    purchase_price = fields.Number(data_key='PurchasePrice', default=0)
    purchase_price_manually_changed_utc = fields.DateTime(
        description=('Read-only: '
                     'Set when the purchase price is changed manually'),
        data_key='PurchasePriceManuallyChangedUtc', load_only=True,
        allow_none=True)
    send_to_webshop = fields.Boolean(
        description=('Purpose: If true, will send article to VismaWebShop '
                     '(If company has the integration). Default: True'),
        data_key='SendToWebshop', default=True)
    article_labels = fields.List(fields.Nested('ArticleLabelSchema'),
                                 data_key='ArticleLabels', default=list())

    class Meta:
        # GET /v2/articles
        # Gets articles.
        # POST /v2/articles
        # Create a single article.
        # GET /v2/articles/{articleId}
        # Gets an article by id.
        # PUT /v2/articles/{articleId}
        # Replace the data in an article.
        endpoint = '/articles'
        allowed_methods = ['list', 'get', 'create', 'update']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class BankAccount(VismaModel):
    """
    Represents a bank account in eAccounting.

    endpoint
        /bankaccounts
    allowed_methods
        ['list', 'create', 'get', 'update', 'delete']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    :argument uuid.UUID id: ``read-only`` Unique Id provided by eAccounting
    :argument uuid.UUID bank: Reference to a :class:`Bank`. Not required for
        bank accounts of cash or tax account type
    :argument int bank_account_type: ``required`` 1 = ChequeAccount,
        2 = CashAccount, 3 = SavingsAccount, 4 = CurrencyAccount,
        5 = DigitalWalletAccount, 6 = CashCreditAccount, 7 = TaxAccount
    :argument str bank_account_type_description: ``read-only`` Description of
        the Bank Account type
    :argument str bban: Bank Account number. Not required for bank accounts of
        cash or tax account type
    :argument str iban: IBAN number
    :argument str name: Name of Bank account.
    :argument bool is_active: Indicates if the account is active.
        ``default=False``
    :argument int ledger_account_number: ``required`` Account number to do
        bookkeeping on for the bank account.
    :argument bool has_active_bank_agreement: Indicates if the bank account has
        an active bank agreement. ``default=False``
    :argument bool is_default_cheque_account: Indicates if the account is the
        default cheque account. Only used when having several cheque accounts.
        ``default=False``

    """

    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id', load_only=True)
    bank = fields.UUID(description=('Not required for bank accounts of cash or '
                                    'tax account type'), data_key='Bank',
                       allow_none=True)
    bank_account_type = fields.Integer(required=True,
                                       description=('1 = ChequeAccount, '
                                                    '2 = CashAccount, '
                                                    '3 = SavingsAccount, '
                                                    '4 = CurrencyAccount, '
                                                    '5 = DigitalWalletAccount,'
                                                    '6 = CashCreditAccount,'
                                                    '7 = TaxAccount'),
                                       validate=[
                                           OneOf(choices=[1, 2, 3, 4, 5, 6, 7],
                                                 labels=[])],
                                       data_key='BankAccountType')
    bank_account_type_description = fields.String(
        description='Read-only: Description of Bank Account type',
        data_key='BankAccountTypeDescription', load_only=True)
    bban = fields.String(
        description=('Also known as Bank Account number. Not required for bank '
                     'accounts of cash or tax account type'),
        validate=[Length(min=0, max=35)], data_key='Bban', allow_none=True)
    iban = fields.String(validate=[Length(min=0, max=35)], data_key='Iban',
                         allow_none=True)
    name = fields.String(required=True, validate=[Length(min=0, max=200)],
                         data_key='Name')
    is_active = fields.Boolean(data_key='IsActive', default=False)
    ledger_account_number = fields.Integer(required=True,
                                           data_key='LedgerAccountNumber')
    has_active_bank_agreement = fields.Boolean(
        data_key='HasActiveBankAgreement', default=False)
    is_default_cheque_account = fields.Boolean(
        description='Purpose: Only used when having several cheque accounts',
        data_key='IsDefaultChequeAccount', default=False)

    class Meta:
        # GET /v2/bankaccounts
        # Get bank accounts.
        # POST /v2/bankaccounts
        # Add a bank account.
        # DELETE /v2/bankaccounts/{bankAccountId}
        # Delete a bank account.
        # GET /v2/bankaccounts/{bankAccountId}
        # Get a specific bank account.
        # PUT /v2/bankaccounts/{bankAccountId}
        # Replace the data in a bank account.
        endpoint = '/bankaccounts'
        allowed_methods = ['list', 'create', 'get', 'update', 'delete']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class Bank(VismaModel):
    """
    Represents a bank in eAccounting

    endpoint
        /banks
    allowed_methods
        ['list']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    :argument uuid.UUID id: Unique Id provided by eAccounting
    :argument str name: Bank name


    """
    id = fields.UUID(data_key='Id')
    name = fields.String(data_key='Name')

    class Meta:
        # GET /v2/banks
        # Get banks.
        endpoint = '/banks'
        allowed_methods = ['list']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class CompanySettings(VismaModel):
    """
    The company settings for current user

    endpoint
        /companysettings
    allowed_methods
        ['list', 'update']

    .. note::

        As of now there is no special way to handle an endpoint that only
        contains a singel object accesses without an id. So even if it is a
        single object you will need to use the following to get the data.

        >>> company_settings = CompanySettings.objects.all().first()

    :argument uuid.UUID id: Is set to empty string. This is to allow for updates
        on the model.
    :argument str name: ``required`` Company name.
    :argument str email: Company email.
    :argument str phone: Company phone.
    :argument str mobile_phone: Company mobile phone.
    :argument str address1: Company address, Row 1
    :argument str address2: Company address, Row 2
    :argument str country_code: Country code.
    :argument str postal_code: Company postal code.
    :argument str city: Company city.
    :argument str website: Company website.
    :argument str currency_code: Standard Currency code.
    :argument uuid.UUID terms_of_payment_id: Reference to standard
        :class:`TermsOfPayment` for company.
    :argument str corporate_identity_number: ``read-only`` Corporate Identity
        Number
    :argument str vat_code:  VAT identification number
    :argument str bank_giro: Bankgiro number. Only used in Sweden.
    :argument str plus_giro: Plusgiro number. Only used in Sweden.
    :argument str bank_account: Bank account number.
    :argument str iban: IBAN number.
    :argument datetime.datetime accounting_locked_to: Datetime where the
        accounting is locked to.
    :argument str gln:  Global Location Number.
    :argument int product_variant: ``read-only`` Variant of eAccounting.
        1 = Standard/Smart, 2 = Invoicing, 3 = Bookkeeping, 4 = Start/Solo,
        5 = Pro, 6 = InvoicingCollaboration
    :argument int type_of_business: ``read-only`` Indicates the companys
        business type. 1 = Corporation, 2 = SoleProprietorship,
        3 = EconomicAssociation, 4 = NonProfitOrganization,
        5 = GeneralPartnership, 6 = LimitedPartnership,
        7 = Cooperatives, 9 = PublicLimited
    :argument int vat_period: ``read-only``  Period when VAT report should be
        sent. 1 = OnceAMonth12th, 2 = OnceAMonth26th, 3 = OnceAQuarter,
        4 = OnceAYear, 5 = Never, 6 = Bimonthly, 7 = OnceAMonth, 8 = TwiceAYear,
        9 = OnceAQuarterFloating
    :argument list(str) activated_modules: List of activated modules.
    :argument CompanyText company_text: A :class:`CompanyText`: object.
    :argument int next_customer_number: ``read-only`` Next customer number in
        sequence.
    :argument int next_supplier_number: ``read-only`` Next supplier number in
        sequence.
    :argument int next_customer_invoice_number: ``read-only`` Next customer
        invoice number in sequence.
    :argument int next_quote_number: ``read-only`` Next quote number in sequence.
    :argument bool show_prices_excl_vat_pc: Indicates if prices should be shown
        excluding VAT for private individuals/customers.



    """

    # TODO: How to handle a single entity endpoint?

    id = ''  # needs to be empty string to allow for update on a non id model.

    name = fields.String(required=True, validate=[Length(min=0, max=100)],
                         data_key='Name')
    email = fields.String(validate=[Length(min=0, max=255)], data_key='Email')
    phone = fields.String(validate=[Length(min=0, max=20)], data_key='Phone')
    mobile_phone = fields.String(validate=[Length(min=0, max=20)],
                                 data_key='MobilePhone')
    address1 = fields.String(validate=[Length(min=0, max=40)],
                             data_key='Address1')
    address2 = fields.String(validate=[Length(min=0, max=40)],
                             data_key='Address2')
    country_code = fields.String(required=True, validate=[Length(min=0, max=2)],
                                 data_key='CountryCode')
    postal_code = fields.String(validate=[Length(min=0, max=10)],
                                data_key='PostalCode')
    city = fields.String(validate=[Length(min=0, max=40)], data_key='City')
    website = fields.String(validate=[Length(min=0, max=255)],
                            data_key='Website', allow_none=True)
    currency_code = fields.String(validate=[Length(min=0, max=3)],
                                  data_key='CurrencyCode')
    terms_of_payment_id = fields.UUID(data_key='TermsOfPaymentId')
    corporate_identity_number = fields.String(description='Read-only',
                                              data_key='CorporateIdentityNumber',
                                              load_only=True)
    vat_code = fields.String(description='VAT identification number',
                             data_key='VatCode')
    bank_giro = fields.String(description='Only used in Sweden.',
                              data_key='BankGiro')
    plus_giro = fields.String(description='Only used in Sweden.',
                              data_key='PlusGiro')
    bank_account = fields.String(data_key='BankAccount')
    iban = fields.String(data_key='Iban')
    accounting_locked_to = fields.DateTime(data_key='AccountingLockedTo')
    gln = fields.String(description='Global Location Number', data_key='Gln',
                        allow_none=True)
    product_variant = fields.Integer(
        description=('Read-only: Variant of eAccouting. '
                     '1 = Standard/Smart, '
                     '2 = Invoicing, '
                     '3 = Bookkeeping, '
                     '4 = Start/Solo, '
                     '5 = Pro, '
                     '6 = InvoicingCollaboration'), validate=[
            OneOf(choices=[1, 2, 3, 4, 5, 6],
                  labels=['Standard/Smart', 'Invoicing', 'Bookkeeping',
                          'Start/Solo', 'Pro', 'InvoicingCollaboration'])],
        data_key='ProductVariant', load_only=True)
    type_of_business = fields.Integer(description=('Read-only: '
                                                   '1 = Corporation, '
                                                   '2 = SoleProprietorship, '
                                                   '3 = EconomicAssociation, '
                                                   '4 = NonProfitOrganization, '
                                                   '5 = GeneralPartnership, '
                                                   '6 = LimitedPartnership, '
                                                   '7 = Cooperatives, '
                                                   '9 = PublicLimited'),
                                      validate=[OneOf(
                                          choices=[1, 2, 3, 4, 5, 6, 7, 9],
                                          labels=['Corporation',
                                                  'SoleProprietorship',
                                                  'EconomicAssociation',
                                                  'NonProfitOrganization',
                                                  'GeneralPartnership',
                                                  'LimitedPartnership',
                                                  'Cooperatives',
                                                  'PublicLimited'])],
                                      data_key='TypeOfBusiness', load_only=True)
    vat_period = fields.Integer(description=('Read-only: '
                                             'Period when VAT report should be sent. '
                                             '1 = OnceAMonth12th, '
                                             '2 = OnceAMonth26th, '
                                             '3 = OnceAQuarter, '
                                             '4 = OnceAYear, '
                                             '5 = Never, '
                                             '6 = Bimonthly, '
                                             '7 = OnceAMonth, '
                                             '8 = TwiceAYear, '
                                             '9 = OnceAQuarterFloating'),
                                validate=[
                                    OneOf(choices=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                                          labels=['OnceAMonth12th',
                                                  'OnceAMonth26th',
                                                  'OnceAQuarter', 'OnceAYear',
                                                  'Never', 'Bimonthly',
                                                  'OnceAMonth', 'TwiceAYear',
                                                  'OnceAQuarterFloating'])],
                                data_key='VatPeriod', load_only=True)
    activated_modules = fields.List(fields.String(),
                                    data_key='ActivatedModules')
    company_text = fields.Nested('CompanyTextsSchema', data_key='CompanyText')
    next_customer_number = fields.Integer(description='Read-only',
                                          data_key='NextCustomerNumber',
                                          load_only=True)
    next_supplier_number = fields.Integer(description='Read-only',
                                          data_key='NextSupplierNumber',
                                          load_only=True)
    next_customer_invoice_number = fields.Integer(description='Read-only',
                                                  data_key='NextCustomerInvoiceNumber',
                                                  load_only=True)
    next_quote_number = fields.Integer(description='Read-only',
                                       data_key='NextQuoteNumber',
                                       load_only=True)
    show_prices_excl_vat_pc = fields.Boolean(description=('Read-only: '
                                                          'Show prices excluding VAT for private individuals'),
                                             data_key='ShowPricesExclVatPC',
                                             load_only=True)

    class Meta:
        # /v2/companysettings Get company settings.
        # PUT /v2/companysettings Replace company settings
        endpoint = '/companysettings'
        allowed_methods = ['list', 'update']


class CompanyTexts(VismaModel):
    """
    Collects company wide texts.

    :argument str customer_invoice_text_domestic: Text used for domestic
        invoices. ``Max length: 180 characters``
    :argument str customer_invoice_text_foreign: Text used for foreign
        invoices. ``Max length: 180 characters``
    :argument str order_text_domestic: Text used for domestic orders.
        ``Max length: 180 characters``
    :argument str order_text_foreign: Text used for foreign orders.
        ``Max length: 180 characters``
    :argument str over_due_text_domestic: Text used for domestic over due
        invoices. ``Max length: 180 characters``
    :argument str over_due_text_foreign: Text used for foreign over due
        invoices. ``Max length: 180 characters``

    """
    customer_invoice_text_domestic = fields.String(
        description='Max length: 180 characters',
        validate=[Length(min=0, max=180)],
        data_key='CustomerInvoiceTextDomestic', allow_none=True)
    customer_invoice_text_foreign = fields.String(
        description='Max length: 180 characters',
        validate=[Length(min=0, max=180)],
        data_key='CustomerInvoiceTextForeign', allow_none=True)
    order_text_domestic = fields.String(
        description='Max length: 180 characters',
        validate=[Length(min=0, max=180)], data_key='OrderTextDomestic',
        allow_none=True)
    order_text_foreign = fields.String(description='Max length: 180 characters',
                                       validate=[Length(min=0, max=180)],
                                       data_key='OrderTextForeign',
                                       allow_none=True)
    over_due_text_domestic = fields.String(
        description='Max length: 180 characters',
        validate=[Length(min=0, max=180)], data_key='OverDueTextDomestic',
        allow_none=True)
    over_due_text_foreign = fields.String(
        description='Max length: 180 characters',
        validate=[Length(min=0, max=180)], data_key='OverDueTextForeign',
        allow_none=True)


class CostCenterItem(VismaModel):
    """
    The actual cost center item in a cost center where the expence gets booked.

    endpoint
        /costcenteritems
    allowed_methods
        'create', 'get', 'update']

    :argument uuid.UUID id = ``read-only`` Unique Id provided by eAccounting.
    :argument uuid.UUID cost_center_id: ``required`` Reference to
    :class:`CostCenter` holding the cost center item.
    :argument str name: Name of cost center item. ``Max length: 50 characters``
    :argument str short_name: Short name of cost center item.
    ``Max length: 9 characters``
    :argument bool is_active: Indicates if the cost center item is active.

    """

    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id', load_only=True)
    cost_center_id = fields.UUID(required=True,
                                 description='Source: Get from /v2/costcenters',
                                 data_key='CostCenterId')
    name = fields.String(required=True, description='Max length: 50 characters',
                         validate=[Length(min=0, max=50)], data_key='Name')
    short_name = fields.String(required=True,
                               description='Max length: 9 characters',
                               validate=[Length(min=0, max=9)],
                               data_key='ShortName')
    is_active = fields.Boolean(required=True, data_key='IsActive',
                               default=False)

    class Meta:
        # GET /v2/costcenteritems/{itemId}
        # Get a specific CostCenterItem.
        # POST /v2/costcenteritems
        # Create a single CostCenterItem.
        # PUT /v2/costcenteritems/{costCenterItemId}
        # Replace the data in an CostCenterItem.
        endpoint = '/costcenteritems'
        allowed_methods = ['create', 'get', 'update']


class CostCenter(VismaModel):
    """
    Represents a cost center. A cost center is a way of splitting up costs and
    earnings between different parts of the company so it is possible to follow
    up better.

    endpoint
        /costcenters
    allowed_methods
        ['list', 'update']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    :argument uuid.UUID id: ``read-only`` Unique Id provided by eAccounting.
    :argument str name: Cost center name.
    :argument int number: Cost center number.
    :argument bool is_active: Indicates if the cost center is active.
        ``default=False``
    :argument list(CostCenterItem) items: List of :class:`CostCenterItem`
        belonging to the cost center.

    """
    id = fields.UUID(data_key='Id', load_only=True)
    name = fields.String(validate=[Length(min=0, max=20)], data_key='Name')
    number = fields.Integer(data_key='Number')
    is_active = fields.Boolean(data_key='IsActive', default=False)
    items = fields.List(fields.Nested('CostCenterItemSchema'), data_key='Items')

    class Meta:
        # GET /v2/costcenters Get a list of Cost Centers
        # PUT /v2/costcenters/{id} Replace content in a cost center.
        endpoint = '/costcenters'
        allowed_methods = ['list', 'update']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class Country(VismaModel):
    """
    Countries available in eAccounting.

    endpoint
        /countries
    allowed_methods
        ['list']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    :argument str name: Country Name.
    :argument str code: Country Code.
    :argument bool is_eu_member: Indicates if the country is a member of the EU.

    """
    name = fields.String(data_key='Name')
    code = fields.String(data_key='Code')
    is_eu_member = fields.Boolean(data_key='IsEuMember')

    class Meta:
        # GET /v2/countries Get a list of Countries.
        # GET /v2/countries/{countrycode} Get a single country.
        endpoint = '/countries'
        allowed_methods = ['list']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

        # TODO: need functionality to set other attribute to primary key to enable get


class Currency(VismaModel):
    """
    Currency available in eAccounting

    endpoint
        /currencies
    allowed_methods
        ['list']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    :argument str code: Currency code.

    """
    code = fields.String(data_key='Code')

    class Meta:
        # GET /v2/currencies Get a list of Currencies
        endpoint = '/currencies'
        allowed_methods = ['list']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class CustomerLabel(VismaModel):
    """
    Customer labels. Labels to attach to a customer.

    endpoint
        /customerlabels
    allowed_methods
        ['list', 'create', 'get', 'update', 'delete']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    :argument uuid.UUID id: ``read-only`` Unique Id provided by eAccounting
    :argument str name: Label name.
    :argument str description: Label description.

    """
    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id', load_only=True)
    name = fields.String(required=True, description='Max length: 50 characters',
                         validate=[Length(min=0, max=50)], data_key='Name')
    description = fields.String(description='Max length: 400 characters',
                                validate=[Length(min=0, max=400)],
                                data_key='Description')

    class Meta:
        # GET /v2/customerlabels
        # Gets customerlabels.
        # POST /v2/customerlabels
        # Create an customerlabel.
        # DELETE /v2/customerlabels/{customerLabelId}
        # Deletes an aticlelabel.
        # GET /v2/customerlabels/{customerLabelId}
        # Gets an customerlabel by id.
        # PUT /v2/customerlabels/{customerLabelId}
        # Replace content of an articlelabel.
        endpoint = '/customerlabels'
        allowed_methods = ['list', 'create', 'get', 'update', 'delete']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class DeliveryMethod(VismaModel):
    """
    Represents a delivery method in eAccounting.

    endpoint
        /deliverymethods
    allowed_methods
        ['list', 'get']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

    :argument uuid.UUID id: Unique Id provided by eAccounting.
    :argument str name: Name of delivery method.
    :argument str code: Delivery method code.

    """

    id = fields.UUID(data_key='Id', load_only=True)
    name = fields.String(data_key='Name')
    code = fields.String(data_key='Code')

    class Meta:
        # GET /v2/deliverymethods
        # Get delivery methods.
        # GET /v2/deliverymethods/{deliveryMethodId}
        # Get a delivery method.
        endpoint = '/deliverymethods'
        allowed_methods = ['list', 'get']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class DeliveryTerm(VismaModel):
    """
        Represents a delivery term in eAccounting.

        endpoint
            /deliveryterms
        allowed_methods
            ['list', 'get']
        envelopes
            {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

        :argument uuid.UUID id: Unique Id provided by eAccounting.
        :argument str name: Name of delivery term.
        :argument str code: Delivery term code.

        """
    id = fields.UUID(data_key='Id')
    name = fields.String(data_key='Name')
    code = fields.String(data_key='Code')

    class Meta:
        # GET /v2/deliveryterms
        # Get a list of delivery terms
        # GET /v2/deliveryterms/{deliveryTermId}
        # Get single delivery term
        endpoint = '/deliveryterms'
        allowed_methods = ['list', 'get']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class Supplier(VismaModel):
    """
    Represents a Supplier in eAccounting.

    endpoint
        /suppliers
    allowed_methods
        ['list', 'create', 'get', 'update', 'delete']
    envelopes
        {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


    :argument uuid.UUID id: ``read-only``  Unique Id provided by eAccounting
    :argument str supplier_number: Unique identifier. If not provided,
        eAccounting will provide one. ``Max length: 16 characters``
    :argument str address1: Supplier address row 1.
        ``Max length: 50 characters``
    :argument str address2: Supplier address row 1.
        ``Max length: 50 characters``
    :argument bool automatic_payment_service: Sweden only. Indicates if the
        supplier is paid by an automatic payment service. Supplier invoices to
        such suppliers will not be sent to the bank via the bank integration.
        ``default=False``
    :argument str bank_account_number:  Only used in norwegian and danish
        eAccounting for domestic payments.``Max length: 50 characters``
    :argument str  bank_bban: Used on foreign payments to identify a bankaccount
        together with Bank Code (SupplierBankCode)'
        ``Format NO: 11 characters, Format DK: 11-14 characters``
    :argument str bank_bic: Used on foreign payments to identify a bankaccount
        together with IBAN (SupplierBankIban) Format: 6 letters followed by 2
        or 5 characters (total length 8 or 11)
    :argument str bank_code: Used on foreign payments to identify a bankaccount
        together with BBAN (SupplierBankBban)
        ``Format: 2 letters followed by at least 3 characters``
    :argument str bank_country_code: Bank country code.
        ``default=Country of the supplier``
    :argument str bankgiro_number: Only used in swedish eAccounting, for
        swedish suppliers. ``Max length: 10 characters``
    :argument str bank_iban:  Used on foreign payments to identify a bankaccount
        together with BIC (SupplierBankBic). Format: 2 letters for country code,
        2 control digits, 3 characters for bank identification
    :argument str bank_name: Bank name. ``Max length: 50 characters``
    :argument str city: Supplier city. ``Max length: 50 characters``
    :argument str contact_person_email: ``Max length: 255 characters``
    :argument str contact_person_mobile: ``Max length: 50 characters``
    :argument str contact_person_name: ``Max length: 50 characters``
    :argument str contact_person_phone: ``Max length: 50 characters``
    :argument str corporate_identity_number: ``Max length: 20 characters``
    :argument str country_code: Country code: ``Max length: 2 characters``
    :argument datetime.datetime created_utc: ``read-only`` Supplier creation
        time.
    :argument str currency_code: Currency of the supplier.
        ``default=Currency of the user company``
    :argument str email_address: ``Max length: 255 characters``
    :argument str mobile_phone: ``Max length: 255 characters``
    :argument datetime.datetime modified_utc: ``read-only`` Last modified time.
    :argument str name: Supplier name ``Max length: 50 characters``
    :argument str note: Supplier notes. ``Max length: 4000 characters``
    :argument str plusgiro_number: Only used in swedish eAccounting, for
        swedish suppliers.
    :argument str postal_code: ``Max length: 10 characters``
    :argument str telephone: ``Max length: 50 characters``
    :argument uuid.UUID terms_of_payment_id: ``required`` Reference to
        :class:`TermsOfPayment` used for supplier.
    :argument str www_address: Supplier website. ``Max length: 255 characters``
    :argument int bank_fee_code: Used for foreign payments to determine which
        party that pays for aditional bank fees. 0 = Not set,
        1 = SenderPaysAllBankCharges, 2 = RecieverPaysAllBankCharges,
        3 = RecieverPaysForeignCosts (Choices taken from app js sourcecode)
        ``default=0``
    :argument uuid.UUID pay_from_bank_account_id: Reference to the
        :class:`BankAccount` is used for foreign payments.
    :argument uuid.UUID foreign_payment_code_id: Reference to
        :class:`ForeignPaymentCode`. Used for categorization of foreign
        purchases (NO and SE only)
    :argument bool uses_payment_reference_numbers: ``required`` True if the
        supplier uses payment reference numbers. (OCR, KID etc.)
        ``default=True``
    :argument bool is_active: ``default=True``
    :argument bool self_employed_without_fixed_address: ``default=False``

    """
    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id', load_only=True)
    supplier_number = fields.String(description=('Max length: 16 characters. '
                                                 'Purpose: Unique identifier. '
                                                 'If not provided, '
                                                 'eAccounting will provide one'),
                                    validate=[Length(min=0, max=16)],
                                    data_key='SupplierNumber', allow_none=True)
    address1 = fields.String(description='Max length: 50 characters',
                             validate=[Length(min=0, max=50)],
                             data_key='Address1', allow_none=True)
    address2 = fields.String(description='Max length: 50 characters',
                             validate=[Length(min=0, max=50)],
                             data_key='Address2', allow_none=True)
    automatic_payment_service = fields.Boolean(description=(
        'Purpose: SE only. Indicates if the supplier is paid by an '
        'automatic payment service. Supplier invoices to such '
        'suppliers will not be sent to the bank via the bank '
        'integration\r\n'
        'Default value: false'), data_key='AutomaticPaymentService',
        default=False)
    bank_account_number = fields.String(
        description=('Max length: 50 characters. '
                     'Purpose: Only used in norwegian and danish eAccounting '
                     'for domestic payments'), validate=[Length(min=0, max=50)],
        data_key='BankAccountNumber', allow_none=True)
    bank_bban = fields.String(
        description=('Purpose: Used on foreign payments to identify a '
                     'bankaccount together with Bank Code (SupplierBankCode)'
                     'Format NO: 11 characters, Format DK: 11-14 characters'),
        validate=[Length(min=0, max=50),
                  # Regexp(regex=re.compile('^[a-zA-Z0-9]{1,35}$'))
                  ], data_key='BankBban', allow_none=True)
    bank_bic = fields.String(
        description=('Purpose: Used on foreign payments to identify a '
                     'bankaccount together with IBAN (SupplierBankIban)'
                     'Format: 6 letters followed by 2 or 5 characters '
                     '(total length 8 or 11)'),
        validate=[Length(min=0, max=50),
                                                          # Regexp(regex=re.compile('^[a-zA-Z]{6}([a-zA-z0-9]{2}|[a-zA-z0-9]{5})$'))
                                                          ], data_key='BankBic',
        allow_none=True)
    bank_code = fields.String(
        description=('Purpose: Used on foreign payments to identify a '
                     'bankaccount together with BBAN (SupplierBankBban)\r\n'
                     'Format: 2 letters followed by at least 3 characters'),
        validate=[Length(min=0, max=50),
                  # Regexp(regex=re.compile('^([a-zA-Z]{2})[a-zA-Z0-9]{3,}$'))
                  ], data_key='BankCode', allow_none=True)
    bank_country_code = fields.String(
        description=('Max length: 2 characters. Default value: Country of the '
                     'supplier'), validate=[Length(min=0, max=2)],
        data_key='BankCountryCode', allow_none=True)
    bankgiro_number = fields.String(
        description=('Max length: 10 characters. Purpose: Only used in swedish '
                     'eAccounting, for swedish suppliers'),
        validate=[Length(min=0, max=10)], data_key='BankgiroNumber',
        allow_none=True)
    bank_iban = fields.String(
        description=('Purpose: Used on foreign payments to identify a'
                     ' bankaccount together with BIC (SupplierBankBic)\r\n'
                     'Format: 2 letters for country code, 2 control digits, '
                     '3 characters for bank identification'),
        validate=[Length(min=0, max=50),
                  # Regexp(regex=re.compile('^[a-zA-Z]{2}[0-9]{2}[a-zA-z0-9]{1,}$'))
                  ], data_key='BankIban', allow_none=True)
    bank_name = fields.String(description='Max length: 50 characters',
                              validate=[Length(min=0, max=50)],
                              data_key='BankName', allow_none=True)
    city = fields.String(description='Max length: 50 characters',
                         validate=[Length(min=0, max=50)], data_key='City',
                         allow_none=True)
    contact_person_email = fields.String(
        description='Max length: 225 characters',
        validate=[Length(min=0, max=255)], data_key='ContactPersonEmail',
        allow_none=True)
    contact_person_mobile = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50)], data_key='ContactPersonMobile',
        allow_none=True)
    contact_person_name = fields.String(description='Max length: 50 characters',
                                        validate=[Length(min=0, max=50)],
                                        data_key='ContactPersonName',
                                        allow_none=True)
    contact_person_phone = fields.String(
        description='Max length: 50 characters',
        validate=[Length(min=0, max=50)], data_key='ContactPersonPhone',
        allow_none=True)
    corporate_identity_number = fields.String(
        description='Max length: 20 characters',
        validate=[Length(min=0, max=20)], data_key='CorporateIdentityNumber',
        allow_none=True)
    country_code = fields.String(validate=[Length(min=0, max=2)],
                                 data_key='CountryCode', allow_none=True)
    created_utc = fields.DateTime(data_key='CreatedUtc', load_only=True,
                                  allow_none=True)
    currency_code = fields.String(description=('Max length: 3 characters. '
                                               'Default value: Currency of the user company'),
                                  validate=[Length(min=0, max=3)],
                                  data_key='CurrencyCode', allow_none=True)
    email_address = fields.String(description='Max length: 225 characters',
                                  validate=[Length(min=0, max=255)],
                                  data_key='EmailAddress', allow_none=True)
    mobile_phone = fields.String(description='Max length: 50 characters',
                                 validate=[Length(min=0, max=50)],
                                 data_key='MobilePhone', allow_none=True)
    modified_utc = fields.DateTime(data_key='ModifiedUtc', load_only=True)
    name = fields.String(required=True, description='Max length: 50 characters',
                         validate=[Length(min=0, max=50)], data_key='Name')
    note = fields.String(description='Max length: 400 characters',
                         validate=[Length(min=0, max=4000)], data_key='Note',
                         allow_none=True)
    plusgiro_number = fields.String(description=('Max length: 10 characters. '
                                                 'Purpose: Only used in swedish eAccounting, '
                                                 'for swedish suppliers',),
                                    allow_none=True,
                                    validate=[Length(min=0, max=10)],
                                    data_key='PlusgiroNumber')
    postal_code = fields.String(description='Max length: 10 characters',
                                validate=[Length(min=0, max=10)],
                                data_key='PostalCode', allow_none=True)
    telephone = fields.String(description='Max length: 50 characters',
                              validate=[Length(min=0, max=50)],
                              data_key='Telephone', allow_none=True)
    terms_of_payment_id = fields.UUID(required=True,
                                      description='Source: Get from /v1/termsofpayment',
                                      data_key='TermsOfPaymentId')
    www_address = fields.String(description='Max length: 255 characters',
                                validate=[Length(min=0, max=255)],
                                data_key='WwwAddress', allow_none=True)
    bank_fee_code = fields.Integer(
        description=('Purpose: Used for foreign payments to determine which '
                     'party that pays for aditional bank fees. '
                     '0 = Not set, '
                     '1 = SenderPaysAllBankCharges, '
                     '2 = RecieverPaysAllBankCharges, '
                     '3 = RecieverPaysForeignCosts'),
        # Choices taken from app js sourcecode
        validate=[OneOf(choices=[0, 1, 2, 3], labels=[])],
        data_key='BankFeeCode', default=0)
    pay_from_bank_account_id = fields.UUID(
        description=('Source: Get from /v1/bankaccounts. Purpose: Used for '
                     'foreign payments to determine which bankaccount the'
                     ' payment will be from'), data_key='PayFromBankAccountId',
        allow_none=True)
    foreign_payment_code_id = fields.UUID(
        description=('Source: Get from /v1/foreignpaymentcodes. '
                     'Purpose: Used for categorization of foreign purchases '
                     '(NO and SE only).'), data_key='ForeignPaymentCodeId',
        allow_none=True)
    uses_payment_reference_numbers = fields.Boolean(required=True, description=(
        'Purpose: Used if the supplier uses payment reference '
        'numbers. (OCR, KID etc.)'), data_key='UsesPaymentReferenceNumbers',
                                                    default=False)
    is_active = fields.Boolean(description='Default: true', data_key='IsActive',
                               default=True)
    self_employed_without_fixed_address = fields.Boolean(
        data_key='SelfEmployedWithoutFixedAddress', default=False)

    class Meta:
        # GET /v2/suppliers Get a list of suppliers.
        # POST /v2/suppliers Post a supplier
        # DELETE /v2/suppliers/{supplierId} Deletes a supplier
        # GET /v2/suppliers/{supplierId} Get a specific supplier.
        # PUT /v2/suppliers/{supplierId} Replace a supplier
        endpoint = '/suppliers'
        allowed_methods = ['list', 'create', 'get', 'update', 'delete']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class ForeignPaymentCodes(VismaModel):
    """
    Holds available Foreign Payment Codes.

    :argument uuid.UUID id: Unique identifier provided by eAccounting.
    :argument int code: Enum for the payment code.
    :argument str description: Description of the payment code.
    :argument str country_code: Country code.

    """

    id = fields.UUID(data_key='Id')
    code = fields.Integer(data_key='Code')
    description = fields.String(data_key='Description')
    country_code = fields.String(data_key='CountryCode')

    class Meta:
        # GET /v2/foreignpaymentcodes Gets a list of foreign payment codes.
        endpoint = '/foreignpaymentcodes'
        allowed_methods = ['list']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class Unit(VismaModel):
    """
    Hold available units. Mostly used for articles.

    :argument uuid.UUID id: Unique identifier provided by eAccounting.
    :argument str name: Name
    :argument str code: Code
    :argument str abbreviation: Abbreviation.

    """
    id = fields.UUID(data_key='Id')
    name = fields.String(data_key='Name')
    code = fields.String(data_key='Code')
    abbreviation = fields.String(data_key='Abbreviation')

    class Meta:
        # GET /v2/units Get a list of Units
        # GET /v2/units/{id} Get a single unit.
        endpoint = '/units'
        allowed_methods = ['list', 'get']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class User(VismaModel):
    """
    Represents a User in eAccounting

    :argument uuid.UUID id: Unique identifier.
    :argument str email:  Email.
    :argument str first_name: First name.
    :argument str last_name: Last name.
    :argument bool is_active: Indicates if the user is active.
    :argument bool is_current_user: Indicate if the user is the one set up with
        the current API session.
    :argument bool is_consultant: Indicates if the user is a hired consultant.

    """

    id = fields.UUID(data_key='Id')
    email = fields.String(data_key='Email')
    first_name = fields.String(data_key='FirstName')
    last_name = fields.String(data_key='LastName')
    is_active = fields.Boolean(data_key='IsActive')
    is_current_user = fields.Boolean(data_key='IsCurrentUser')
    is_consultant = fields.Boolean(data_key='IsConsultant')

    class Meta:
        # GET /v2/users Get a list of users
        endpoint = '/users'
        allowed_methods = ['list']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class VatReport(VismaModel):
    """
    Represents a VAT Report

    :argument uuid.UUID id: Unique identifier.
    :argument str name: Name.
    :argument datetime.datetime start_date: Start date of the report.
    :argument datetime.datetim end_date: End date of the report.
    :argument int document_approval_status: Describes the vat reports approval
        status. 0 = None, 1 = Approved, 2 = Rejected, 3 = ReadyForApproval
    :argument uuid.UUID document_id: Reference to the :class:`Document`.
    :argument datetime.datetime created_utc: Creatin time in UTC.
    :argument bool is_regretted: Indicates whether the vat report was undone
    :argument uuid.UUID regretted_by_user_id: Reference to the :class:`User`
        that undid the report.
    :argument datetime.datetime regretted_date: Date the report was undone.
    :argument datetime.datetime modified_utc: Last modified datetime.
    :argument uuid.UUID sent_for_approval_by_user_id: Reference to :class:`User`
        that send the report for approval.
    :argument uuid.UUID voucher_id: Reference to :class:`Voucher`
    :argument number total_amount: Predicted vat amount to pay or be refunded.
    :argument list(DocumentApprovalEvent) approval_events_history: List of
        references to :class:`DocumentApprovalEvent` to show the approval
        history of the VAT Report.

    """
    id = fields.UUID(data_key='Id')
    name = fields.String(data_key='Name')
    start_date = fields.DateTime(data_key='StartDate')
    end_date = fields.DateTime(data_key='EndDate')
    document_approval_status = fields.Integer(
        description='0 = None, 1 = Approved, 2 = Rejected, 3 = ReadyForApproval',
        validate=[OneOf(choices=[0, 1, 2, 3], labels=[])],
        data_key='DocumentApprovalStatus')
    document_id = fields.UUID(
        description='Purpose: Use for GET /v2/documents/{id}',
        data_key='DocumentId', allow_none=True)
    created_utc = fields.DateTime(data_key='CreatedUtc')
    is_regretted = fields.Boolean(
        description='Indicates whether the vat report was undone',
        data_key='IsRegretted')
    regretted_by_user_id = fields.UUID(
        description=('If the vat report was undone this indicates the user '
                     'id that did the action'), data_key='RegrettedByUserId',
        allow_none=True)
    regretted_date = fields.DateTime(
        description=('If the vat report was undone this indicates the date of '
                     'the action'), data_key='RegrettedDate', allow_none=True)
    modified_utc = fields.DateTime(data_key='ModifiedUtc')
    sent_for_approval_by_user_id = fields.UUID(
        data_key='SentForApprovalByUserId', allow_none=True)
    voucher_id = fields.UUID(description=('Purpose: '
                                          'Use for GET /v2/vouchers/{fiscalyearId}/{voucherId}'),
                             data_key='VoucherId', allow_none=True)
    total_amount = fields.Number(
        description='Predicted vat amount to pay or be refunded',
        data_key='TotalAmount')
    approval_events_history = fields.List(
        fields.Nested('DocumentApprovalEventSchema'),
        description='The history of approval events of the vat report.',
        data_key='ApprovalEventsHistory')

    class Meta:
        # GET /v2/vatreports Gets a list of all vat reports
        # GET /v2/vatreports/{id} Get a vat report item by id.
        endpoint = '/vatreports'
        allowed_methods = ['list', 'get']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class DocumentApprovalEvent(VismaModel):
    """
    Represents a Document Approval Event

    :argument int document_approval_status: Describes the status if the
        document. 0 = None, 1 = Approved, 2 = Rejected, 3 = ReadyForApproval
    :argument datetime.datetime created_utc: Created time
    :argument uuid.UUID created_by_user_id: Reference to :class:`User` that
        created the event.

    """
    document_approval_status = fields.Integer(description=('0 = None, '
                                                           '1 = Approved, '
                                                           '2 = Rejected, '
                                                           '3 = ReadyForApproval'),
        validate=[OneOf(choices=[0, 1, 2, 3], labels=[])],
        data_key='DocumentApprovalStatus')
    created_utc = fields.DateTime(data_key='CreatedUtc')
    created_by_user_id = fields.UUID(data_key='CreatedByUserId')

    class Meta:
        # no endpoint
        pass


class Project(VismaModel):
    """
    Represents a Project in eAccounting

    :argument uuid.UUID id: ``read-only``  Unique Id provided by eAccounting'
    :argument str number: Project number. ``Max length: 9 characters``
    :argument str name: ``required`` Project name.
        ``Max length: 50 characters``
    :argument datetime.datetime start_date: ``required`` Project start. Will turn a datetime
        into date automatically.
    :argument datetime.datetime end_date: Project end.
    :argument uuid.UUID customer_id: Reference to :class:`Customer` for project.
    :argument str customer_name: ``read-only``  Customer name depending on
        customer_id
    :argument str notes: Notes ``Max length: 500 characters``
    :argument int status: Project status. 1 = Ongoing, 2 = Finished
    :argument datetime.datetime modified_utc: Last modufied datetime in UTC.

    # TODO: make custom field to handle the parsing and printing of dates.

    """

    id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
                     data_key='Id', load_only=True)
    number = fields.String(required=True,
                           description='Max length: 9 characters',
                           validate=[Length(min=0, max=9)], data_key='Number')
    name = fields.String(required=True, description='Max length: 50 characters',
                         validate=[Length(min=0, max=50)], data_key='Name')
    # TODO: make custom field to handle the parsing and printing of dates.
    start_date = fields.DateTime(required=True, format='%Y-%m-%d',
                                 data_key='StartDate')
    end_date = fields.DateTime(data_key='EndDate', allow_none=True)
    customer_id = fields.UUID(data_key='CustomerId', allow_none=True)
    customer_name = fields.String(
        description='Read-only: CustomerName depending on CustomerId',
        data_key='CustomerName', load_only=True, allow_none=True)
    notes = fields.String(description='Max length: 500 characters',
                          validate=[Length(min=0, max=500)], data_key='Notes',
                          allow_none=True)
    status = fields.Integer(description='1 = Ongoing, 2 = Finished',
                            validate=[OneOf(choices=[1, 2], labels=[])],
                            data_key='Status', default=1)
    modified_utc = fields.DateTime(
        description='Read-only: Is automatically set', data_key='ModifiedUtc',
        load_only=True)

    class Meta:
        # GET /v2/projects Get a list of projects.
        # POST /v2/projects Create a new project.
        # GET /v2/projects/{id} Get a specific project.
        # PUT /v2/projects/{id} Replace content in a project.
        endpoint = '/projects'
        allowed_methods = ['list', 'create', 'get', 'update']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}


class OpeningBalances(VismaModel):
    """
    Represents opening balances

    :argument str name: Name
    :argument int number: Account number.
    :argument number balance: Account balance.

    """

    name = fields.String(data_key='Name')
    number = fields.Integer(data_key='Number')
    balance = fields.Number(data_key='Balance')

    class Meta:
        # GET /v2/fiscalyears/openingbalances
        # Gets the opening balances of the first fiscal year.
        # If you want balances of following years,
        # use the GET /accountbalances instead.
        endpoint = '/fiscalyears/openingbalances'
        allowed_methods = ['list']
        envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}

# ########################################################################
# Models below need moderating, generated from swagger-marshmallow-codegen
# ########################################################################

# class AccountBalance(VismaModel):
#     account_number = fields.Integer(description='Read-only. The account number',
#                                     data_key='AccountNumber', load_only=True)
#     account_name = fields.String(
#         description='Read-only. The name of the account',
#         data_key='AccountName', load_only=True)
#     balance = fields.Number(description='Read-only. The account balance',
#                             data_key='Balance', load_only=True)
#
#     class Meta:
#         # GET /v2/accountbalances/{date}
#         # GET /v2/accountbalances/{accountNumber}/{date}
#
#         # TODO: how to handle endpoints that doesn't use a pk?
#         pass


# TODO: make it possible to have another field as primary key.
# TODO: in accpunt the number is the primary key.
# TODO: add a function to Account that is balance that will get the balance of the accoount on certain date.


# class PartnerResourceLink(VismaModel):
#     id = fields.UUID(description='Read-only: Id provided by eAccounting',
#                      data_key='Id', load_only=True)
#     resource_id = fields.UUID(required=True,
#                               description='Purpose: Link to the resource in eAccounting',
#                               data_key='ResourceId')
#     resource_type = fields.Integer(required=True, description=('0 = Article, '
#                                                                '1 = Customer, '
#                                                                '2 = Supplier, '
#                                                                '3 = CustomerInvoice, '
#                                                                '4 = SupplierInvoice,\r\n'
#                                                                '5 = CustomerInvoiceDraft, '
#                                                                '6 = SupplierInvoiceDraft'),
#                                    validate=[
#                                        OneOf(choices=[0, 1, 2, 3, 4, 5, 6],
#                                              labels=[])],
#                                    data_key='ResourceType')
#     href = fields.String(required=True,
#                          description='Link to the third party solution page',
#                          data_key='Href')
#     partner_company_name = fields.String(required=True,
#                                          data_key='PartnerCompanyName')
#     partner_system_name = fields.String(required=True,
#                                         data_key='PartnerSystemName')
#
#     class Meta:
#         # GET /v2/partnerresourcelinks
#         # Get a list of partner resource links.
#         # POST /v2/partnerresourcelinks
#         # Create a partner resource link
#         # DELETE /v2/partnerresourcelinks/{partnerResourceLinkId}
#         # Delete a partner resource link
#         # GET /v2/partnerresourcelinks/{partnerResourceLinkId}
#         # Get a partner resource link by id.
#         # PUT /v2/partnerresourcelinks/{partnerResourceLinkId}
#         # Update a partner resource link
#         endpoint = '/partnerresourcelinks'
#         allowed_methods = ['list', 'create', 'get', 'update', 'delete']
#         envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
#
#
# class AllocationPeriod(VismaModel):
#     id = fields.UUID(data_key='Id')
#     supplier_invoice_id = fields.UUID(data_key='SupplierInvoiceId')
#     supplier_invoice_row = fields.Integer(data_key='SupplierInvoiceRow')
#     manual_voucher_id = fields.UUID(data_key='ManualVoucherId')
#     manual_voucher_row = fields.Integer(data_key='ManualVoucherRow')
#     allocation_period_source_type = fields.Integer(
#         description='0 = SupplierInvoice, 1 = ManualVoucher',
#         validate=[OneOf(choices=[0, 1], labels=[])],
#         data_key='AllocationPeriodSourceType')
#     status = fields.Integer(description='0 = Pending, 1 = Revoked, 2 = Booked',
#                             validate=[OneOf(choices=[0, 1, 2], labels=[])],
#                             data_key='Status')
#     cost_center_item_id1 = fields.UUID(data_key='CostCenterItemId1')
#     cost_center_item_id2 = fields.UUID(data_key='CostCenterItemId2')
#     cost_center_item_id3 = fields.UUID(data_key='CostCenterItemId3')
#     project_id = fields.UUID(data_key='ProjectId')
#     bookkeeping_date = fields.DateTime(data_key='BookkeepingDate')
#     created_utc = fields.DateTime(data_key='CreatedUtc')
#     rows = fields.List(fields.Nested('AllocationPeriodRowSchema'),
#                        required=True, data_key='Rows')
#     debit_account_number = fields.Integer(dump_only=True,
#                                           data_key='DebitAccountNumber')
#     credit_account_number = fields.Integer(dump_only=True,
#                                            data_key='CreditAccountNumber')
#     amount = fields.Number(dump_only=True, data_key='Amount')
#
#     class Meta:
#         # GET /v2/allocationperiods
#         # Get allocation periods.
#         # POST /v2/allocationperiods  uses AllocationPlan
#         # Add allocation periods for voucher or supplier invoice.
#         # GET /v2/allocationperiods/{allocationPeriodId}
#         # Get single allocation period.
#         endpoint = '/allocationperiods'
#         allowed_methods = ['list', 'create', 'get']
#         envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
#
#         # TODO: How to handle different schemas on post and get?
#
#
# class AllocationPlan(VismaModel):
#     supplier_invoice_id = fields.UUID(data_key='SupplierInvoiceId')
#     supplier_invoice_row = fields.Integer(data_key='SupplierInvoiceRow')
#     voucher_id = fields.UUID(data_key='VoucherId')
#     voucher_row = fields.Integer(data_key='VoucherRow')
#     bookkeeping_start_date = fields.DateTime(required=True,
#                                              data_key='BookkeepingStartDate')
#     amount_to_allocate = fields.Number(required=True,
#                                        validate=[Range(min=0, max=1000000000),
#                                                  # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))
#                                                  ], data_key='AmountToAllocate')
#     quantity_to_allocate = fields.Number(
#         # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#         data_key='QuantityToAllocate')
#     weight_to_allocate = fields.Number(
#         # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#         data_key='WeightToAllocate')
#     allocation_account_number = fields.Integer(required=True, validate=[
#         Range(min=0, max=9999)], data_key='AllocationAccountNumber')
#     number_of_allocation_periods = fields.Integer(required=True,
#                                                   data_key='NumberOfAllocationPeriods')
#
#
# class AllocationPeriodRow(VismaModel):
#     id = fields.UUID(data_key='Id')
#     allocation_period_id = fields.UUID(data_key='AllocationPeriodId')
#     account_number = fields.Integer(required=True, data_key='AccountNumber')
#     amount = fields.Number(required=True, data_key='Amount')
#     debit_credit = fields.Integer(required=True,
#                                   validate=[OneOf(choices=[1, 2], labels=[])],
#                                   data_key='DebitCredit')
#     quantity = fields.Number(data_key='Quantity')
#     weight = fields.Number(data_key='Weight')
#
#     class Meta:
#         # no endpoint
#         pass
#
#
# # TODO: Maybe split into 2 subclasses to separate endpoints for vat and invoices and useage.
# # TODO: How to make abstract classes?
# # class Approval(VismaModel):
# #     document_approval_status = fields.Integer(
# #         required=True,
# #         description='1 = Approved, 2 = Rejected, 3 = ReadyForApproval',
# #         validate=[OneOf(choices=[0, 1, 2, 3], labels=[])],
# #         data_key='DocumentApprovalStatus')
# #     rejection_message = fields.String(
# #         description=('Purpose: The message sent to users when rejecting a '
# #                      'document. '
# #                      'Empty if DocumentApprovalStatus is not 2 = Rejected.\r\n'
# #                      'Max length: 200 characters'),
# #         validate=[Length(min=0, max=200)],
# #         data_key='RejectionMessage')
# #     rejection_message_receivers = fields.List(
# #         fields.UUID(),
# #         description=('Purpose: The recipients of the rejection message. '
# #                      'Empty if DocumentApprovalStatus is not 2 = Rejected. '
# #                      'List of user ids.'),
# #         data_key='RejectionMessageReceivers')
# #
# #     class Meta:
# #         # PUT /v2/approval/vatreport/{id}
# #         # Update the approval status of a vat report
# #         # PUT /v2/approval/supplierinvoice/{id}
# #         # Update the approval status of a invoice draft
# #         pass
#
#
# class CustomerLedgerItem(VismaModel):
#     currency_code = fields.String(required=True,
#                                   description='Max length: 3 characters',
#                                   validate=[Length(min=0, max=3)],
#                                   data_key='CurrencyCode')
#     currency_rate = fields.Number(data_key='CurrencyRate')
#     currency_rate_unit = fields.Integer(data_key='CurrencyRateUnit')
#     customer_id = fields.UUID(required=True,
#                               description='Source: Get from /v1/customerlistitems.',
#                               data_key='CustomerId')
#     due_date = fields.DateTime(required=True, description='Format: YYYY-MM-DD',
#                                data_key='DueDate')
#     id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
#                      data_key='Id')
#     invoice_date = fields.DateTime(required=True,
#                                    description='Format: YYYY-MM-DD',
#                                    data_key='InvoiceDate')
#     invoice_number = fields.Integer(required=True, data_key='InvoiceNumber')
#     is_credit_invoice = fields.Boolean(required=True,
#                                        data_key='IsCreditInvoice')
#     payment_reference_number = fields.String(validate=[Length(min=0, max=50)],
#                                              data_key='PaymentReferenceNumber')
#     remaining_amount_invoice_currency = fields.Number(required=True, validate=[
#         Range(min=-1000000000, max=1000000000)],
#                                                       data_key='RemainingAmountInvoiceCurrency')
#     roundings_amount_invoice_currency = fields.Number(required=True, validate=[
#         Range(min=-1, max=1)], data_key='RoundingsAmountInvoiceCurrency')
#     total_amount_invoice_currency = fields.Number(required=True, validate=[
#         Range(min=-1000000000, max=1000000000)],
#                                                   data_key='TotalAmountInvoiceCurrency')
#     vat_amount_invoice_currency = fields.Number(required=True, validate=[
#         Range(min=-1000000000, max=1000000000)],
#                                                 data_key='VATAmountInvoiceCurrency')
#     voucher_id = fields.UUID(required=True,
#                              description='Source: Get from v1/vouchers/{fiscalyearid}.',
#                              data_key='VoucherId')
#     modified_utc = fields.DateTime(data_key='ModifiedUtc')
#
#     class Meta:
#         # GET /v2/customerledgeritems
#         # Get a list of customer ledger items
#         # POST /v2/customerledgeritems
#         # Create a customer ledger item.
#         # GET /v2/customerledgeritems/{customerLedgerItemId}
#         # Get a customer ledger item by id.
#         endpoint = '/customerledgeritems'
#         allowed_methods = ['list', 'create', 'get']
#         envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
#
#
# class VatApproval(VismaModel):
#     document_approval_status = fields.Integer(required=True,
#                                               description='1 = Approved, 2 = Rejected, 3 = ReadyForApproval',
#                                               validate=[
#                                                   OneOf(choices=[0, 1, 2, 3],
#                                                         labels=[])],
#                                               data_key='DocumentApprovalStatus')
#     rejection_message = fields.String(
#         description=('Purpose: The message sent to users when rejecting a '
#                      'document. '
#                      'Empty if DocumentApprovalStatus is not 2 = Rejected.\r\n'
#                      'Max length: 200 characters'),
#         validate=[Length(min=0, max=200)], data_key='RejectionMessage')
#     rejection_message_receivers = fields.List(fields.UUID(), description=(
#         'Purpose: The recipients of the rejection message. '
#         'Empty if DocumentApprovalStatus is not 2 = Rejected. '
#         'List of user ids.'), data_key='RejectionMessageReceivers')
#
#     class Meta:
#         # PUT /v2/approval/vatreport/{id}
#         # Update the approval status of a vat report
#         # PUT /v2/approval/supplierinvoice/{id}
#         # Update the approval status of a invoice draft
#         endpoint = '/approvals/vatreport'
#         allowed_methods = ['update']
#
#
# class SupplierInvoiceApproval(VismaModel):
#     document_approval_status = fields.Integer(required=True,
#                                               description='1 = Approved, 2 = Rejected, 3 = ReadyForApproval',
#                                               validate=[
#                                                   OneOf(choices=[0, 1, 2, 3],
#                                                         labels=[])],
#                                               data_key='DocumentApprovalStatus')
#     rejection_message = fields.String(
#         description=('Purpose: The message sent to users when rejecting a '
#                      'document. '
#                      'Empty if DocumentApprovalStatus is not 2 = Rejected.\r\n'
#                      'Max length: 200 characters'),
#         validate=[Length(min=0, max=200)], data_key='RejectionMessage')
#     rejection_message_receivers = fields.List(fields.UUID(), description=(
#         'Purpose: The recipients of the rejection message. '
#         'Empty if DocumentApprovalStatus is not 2 = Rejected. '
#         'List of user ids.'), data_key='RejectionMessageReceivers')
#
#     class Meta:
#         # PUT /v2/approval/supplierinvoice/{id}
#         # Update the approval status of a invoice draft
#         endpoint = '/approvals/supplierinvoice'
#         allowed_methods = ['update']
#
#
# class AttachmentLink(VismaModel):
#     document_id = fields.UUID(
#         description='The Id of the corresponding linked document',
#         data_key='DocumentId')
#     document_type = fields.Integer(required=True, description=('0 = None, '
#                                                                '1 = SupplierInvoice, '
#                                                                '2 = Receipt, '
#                                                                '3 = Voucher, '
#                                                                '4 = SupplierInvoiceDraft, '
#                                                                '5 = AllocationPeriod, '
#                                                                '6 = Transfer'),
#                                    validate=[
#                                        OneOf(choices=[0, 1, 2, 3, 4, 5, 6],
#                                              labels=[])],
#                                    data_key='DocumentType')
#     attachment_ids = fields.List(fields.UUID(), required=True,
#                                  data_key='AttachmentIds')
#
#     class Meta:
#         # POST /v2/attachmentlinks
#         # Create a new links between a document and a set of attachments.
#         # DELETE /v2/attachmentlinks/{attachmentId}
#         # Delete the link to an attachment.
#         endpoint = '/attachmentlinks'
#         allowed_methods = ['create', 'delete']
#
#
# # TODO: How to handle when different schemas are used for Post and get?
# class AttachmentResult(VismaModel):
#     id = fields.UUID(data_key='Id')
#     content_type = fields.String(data_key='ContentType')
#     document_id = fields.UUID(data_key='DocumentId')
#     attached_document_type = fields.Integer(description=('0 = None, '
#                                                          '1 = SupplierInvoice, '
#                                                          '2 = Receipt, '
#                                                          '3 = Voucher, '
#                                                          '4 = SupplierInvoiceDraft, '
#                                                          '5 = AllocationPeriod, '
#                                                          '6 = Transfer'),
#                                             validate=[OneOf(
#                                                 choices=[0, 1, 2, 3, 4, 5, 6],
#                                                 labels=[])],
#                                             data_key='AttachedDocumentType')
#     file_name = fields.String(data_key='FileName')
#     temporary_url = fields.String(data_key='TemporaryUrl')
#     comment = fields.String(data_key='Comment')
#     supplier_name = fields.String(data_key='SupplierName')
#     amount_invoice_currency = fields.Number(data_key='AmountInvoiceCurrency')
#     type = fields.Integer(description='0 = Invoice, 1 = Receipt, 2 = Document',
#                           validate=[OneOf(choices=[0, 1, 2], labels=[])],
#                           data_key='Type')
#     attachment_status = fields.Integer(description='0 = Matched, 1 = Unmatched',
#                                        validate=[
#                                            OneOf(choices=[0, 1], labels=[])],
#                                        data_key='AttachmentStatus')
#     uploaded_by = fields.String(description='Read-only', data_key='UploadedBy')
#     image_date = fields.DateTime(description='Read-only', data_key='ImageDate')
#
#     class Meta:
#         # GET /v2/attachments
#         # Fetch attachments.
#         # POST uses AttachemantUpload!
#         # DELETE /v2/attachments/{attachmentId}
#         # Delete an attachment.
#         # GET /v2/attachments/{attachmentId}
#         # Get a specific attachment.
#         endpoint = '/attachments'
#         allowed_methods = ['list', 'get', 'delete']
#         envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
#
#
# class AttachmentUpload(VismaModel):
#     id = fields.UUID(data_key='Id')
#     content_type = fields.String(required=True, description=(
#         "= ['image/jpeg' or 'image/png' or 'image/tiff' or "
#         "'application/pdf']"), validate=[Length(min=0, max=15)],
#                                  data_key='ContentType')
#     file_name = fields.String(required=True, data_key='FileName')
#     data = fields.String(
#         description='Format: Must be Base64 encoded byte array.',
#         data_key='Data')
#     url = fields.String(description='Must be public URL', data_key='Url')
#
#     class Meta:
#         # is used for uploading attachements
#         endpoint = '/attachments'
#         allowed_methods = ['create']
#
#
# class SalesDocumentRotRutReductionPerson(VismaModel):
#     ssn = fields.String(required=True,
#                         description=('Max length: 50 characters. '
#                                      'Purpose: Social security number'),
#                         validate=[Length(min=0, max=50)], data_key='Ssn')
#     amount = fields.Number(data_key='Amount')
#
#     class Meta:
#         # No endpoint
#         pass
#
#
# class CustomerInvoice(VismaModel):
#     id = fields.UUID(description=('Read-only: '
#                                   'This is automatically generated by eAccounting upon '
#                                   'creation'), data_key='Id')
#     eu_third_party = fields.Boolean(required=True, data_key='EuThirdParty')
#     is_credit_invoice = fields.Boolean(data_key='IsCreditInvoice')
#     currency_code = fields.String(description='Read-only',
#                                   data_key='CurrencyCode')
#     currency_rate = fields.Number(description=('Default: '
#                                                'Automatic calculation of the currency rate. '
#                                                'Enter this value to provide a custom rate'),
#                                   data_key='CurrencyRate')
#     created_by_user_id = fields.UUID(description='Read-only',
#                                      data_key='CreatedByUserId')
#     total_amount = fields.Number(description='Read-only',
#                                  data_key='TotalAmount')
#     total_vat_amount = fields.Number(description='Read-only',
#                                      data_key='TotalVatAmount')
#     total_roundings = fields.Number(description='Read-only',
#                                     data_key='TotalRoundings')
#     total_amount_invoice_currency = fields.Number(description='Read-only',
#                                                   data_key='TotalAmountInvoiceCurrency')
#     total_vat_amount_invoice_currency = fields.Number(description='Read-only',
#                                                       data_key='TotalVatAmountInvoiceCurrency')
#     customer_id = fields.UUID(required=True, data_key='CustomerId')
#     rows = fields.List(fields.Nested('CustomerInvoiceRowSchema'), required=True,
#                        data_key='Rows')
#     invoice_date = fields.DateTime(data_key='InvoiceDate')
#     due_date = fields.DateTime(data_key='DueDate')
#     delivery_date = fields.DateTime(data_key='DeliveryDate')
#     rot_reduced_invoicing_type = fields.Integer(required=True,
#                                                 description='0 = Normal, 1 = Rot, 2 = Rut',
#                                                 validate=[Range(min=0, max=2, ),
#                                                           OneOf(
#                                                               choices=[0, 1, 2],
#                                                               labels=[])],
#                                                 data_key='RotReducedInvoicingType')
#     rot_reduced_invoicing_amount = fields.Number(description=('Default: '
#                                                               'Automatic tax reduction calculation. '
#                                                               'Used for the manual input of the deducted tax reduction'),
#                                                  # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                                  data_key='RotReducedInvoicingAmount')
#     rot_reduced_invoicing_percent = fields.Number(description='Read-only',
#                                                   data_key='RotReducedInvoicingPercent')
#     rot_reduced_invoicing_property_name = fields.String(description=('Default: '
#                                                                      'The name of the property type. '
#                                                                      'Used for providing a custom name'),
#                                                         data_key='RotReducedInvoicingPropertyName')
#     rot_reduced_invoicing_org_number = fields.String(
#         validate=[Length(min=0, max=11)],
#         data_key='RotReducedInvoicingOrgNumber')
#     persons = fields.List(
#         fields.Nested('SalesDocumentRotRutReductionPersonSchema'),
#         description='Required for ROT/RUT invoices only', data_key='Persons')
#     rot_reduced_invoicing_automatic_distribution = fields.Boolean(
#         description='Read-only',
#         data_key='RotReducedInvoicingAutomaticDistribution')
#     electronic_reference = fields.String(data_key='ElectronicReference')
#     electronic_address = fields.String(description='Read-only',
#                                        data_key='ElectronicAddress')
#     edi_service_deliverer_id = fields.String(validate=[Length(min=0, max=50)],
#                                              data_key='EdiServiceDelivererId')
#     our_reference = fields.String(validate=[Length(min=0, max=50)],
#                                   data_key='OurReference')
#     your_reference = fields.String(validate=[Length(min=0, max=50)],
#                                    data_key='YourReference')
#     invoice_customer_name = fields.String(description='Read-only',
#                                           data_key='InvoiceCustomerName')
#     invoice_address1 = fields.String(description='Read-only',
#                                      data_key='InvoiceAddress1')
#     invoice_address2 = fields.String(description='Read-only',
#                                      data_key='InvoiceAddress2')
#     invoice_postal_code = fields.String(description='Read-only',
#                                         data_key='InvoicePostalCode')
#     invoice_city = fields.String(description='Read-only',
#                                  data_key='InvoiceCity')
#     invoice_country_code = fields.String(description='Read-only',
#                                          data_key='InvoiceCountryCode')
#     delivery_customer_name = fields.String(description='Read-only',
#                                            data_key='DeliveryCustomerName')
#     delivery_address1 = fields.String(description='Read-only',
#                                       data_key='DeliveryAddress1')
#     delivery_address2 = fields.String(validate=[Length(min=0, max=50)],
#                                       data_key='DeliveryAddress2')
#     delivery_postal_code = fields.String(description='Read-only',
#                                          data_key='DeliveryPostalCode')
#     delivery_city = fields.String(description='Read-only',
#                                   data_key='DeliveryCity')
#     delivery_country_code = fields.String(description='Read-only',
#                                           data_key='DeliveryCountryCode')
#     delivery_method_name = fields.String(description='Read-only',
#                                          data_key='DeliveryMethodName')
#     delivery_term_name = fields.String(description='Read-only',
#                                        data_key='DeliveryTermName')
#     delivery_method_code = fields.String(description='Read-only',
#                                          data_key='DeliveryMethodCode')
#     delivery_term_code = fields.String(description='Read-only',
#                                        data_key='DeliveryTermCode')
#     customer_is_private_person = fields.Boolean(description='Read-only',
#                                                 data_key='CustomerIsPrivatePerson')
#     terms_of_payment_id = fields.UUID(description='Read-only',
#                                       data_key='TermsOfPaymentId')
#     customer_email = fields.String(description='Read-only',
#                                    data_key='CustomerEmail')
#     invoice_number = fields.Integer(description='Read-only',
#                                     data_key='InvoiceNumber')
#     customer_number = fields.String(description='Read-only',
#                                     data_key='CustomerNumber')
#     payment_reference_number = fields.String(description='Read-only',
#                                              data_key='PaymentReferenceNumber')
#     rot_property_type = fields.Integer(
#         description='1 = Apartment, 2 = Property',
#         validate=[Range(min=1, max=2)], data_key='RotPropertyType')
#     sales_document_attachments = fields.List(fields.UUID(),
#                                              description='Read-only',
#                                              data_key='SalesDocumentAttachments')
#     has_auto_invoice_error = fields.Boolean(description='Read-only',
#                                             data_key='HasAutoInvoiceError')
#     is_not_delivered = fields.Boolean(description='Read-only',
#                                       data_key='IsNotDelivered')
#     reverse_charge_on_construction_services = fields.Boolean(
#         description='Read-only', data_key='ReverseChargeOnConstructionServices')
#     work_house_other_costs = fields.Number(data_key='WorkHouseOtherCosts')
#     remaining_amount = fields.Number(description='Read-only',
#                                      data_key='RemainingAmount')
#     remaining_amount_invoice_currency = fields.Number(description='Read-only',
#                                                       data_key='RemainingAmountInvoiceCurrency')
#     referring_invoice_id = fields.UUID(description='Read-only',
#                                        data_key='ReferringInvoiceId')
#     voucher_number = fields.String(description='Read-only',
#                                    data_key='VoucherNumber')
#     voucher_id = fields.UUID(description='Read-only', data_key='VoucherId')
#     created_utc = fields.DateTime(description='Read-only',
#                                   data_key='CreatedUtc')
#     modified_utc = fields.DateTime(description='Read-only',
#                                    data_key='ModifiedUtc')
#     reversed_construction_vat_invoicing = fields.Boolean(
#         description='Read-only', data_key='ReversedConstructionVatInvoicing')
#     includes_vat = fields.Boolean(description=('Read-only: '
#                                                'If true the unit prices on rows include VAT. '
#                                                'The value is set upon creation depending whether '
#                                                '"Show prices excl. VAT for private individuals" in '
#                                                'company settings is marked or not'),
#                                   data_key='IncludesVat')
#     send_type = fields.Integer(description='Work in progress.', validate=[
#         OneOf(choices=[0, 1, 2, 3], labels=[])], data_key='SendType')
#
#     class Meta:
#         # GET /v2/customerinvoices
#         # Get all customer invoices
#         # POST /v2/customerinvoices
#         # Create a single customer invoice.
#         # GET /v2/customerinvoices/{invoiceId}
#         # Gets a customer invoice with a specific id.
#         # GET /v2/customerinvoices/{invoiceId}/pdf
#         # Gets a customer invoice in Portable Document Format (PDF)
#         # POST /v2/customerinvoices/{invoiceId}/payments
#         # Post a payment towards a bookkept customer invoice.
#         # Use factoring fee and account number in order to pay with factoring
#         endpoint = '/customerinvoices'
#         allowed_methods = ['list', 'create', 'get']
#         envelopes = {'list': {'class': PaginatedResponse,
#                               'data_attr': 'Data'}}  # TODO: Handle special cases. Subclassing?
#
#
# class CustomerInvoiceRow(VismaModel):
#     id = fields.UUID(description='Read-only', data_key='Id')
#     article_number = fields.String(description='Read-only',
#                                    data_key='ArticleNumber')
#     article_id = fields.UUID(description='Null if text row',
#                              data_key='ArticleId')
#     amount_no_vat = fields.Number(description='Read-only',
#                                   data_key='AmountNoVat')
#     percent_vat = fields.Number(description='Read-only', data_key='PercentVat')
#     line_number = fields.Integer(description='Read-only', data_key='LineNumber')
#     is_text_row = fields.Boolean(description='Read-only', data_key='IsTextRow')
#     text = fields.String(description="Default: The article's name",
#                          data_key='Text')
#     unit_price = fields.Number(
#         # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#         data_key='UnitPrice')
#     unit_abbreviation = fields.String(description='Read-only',
#                                       data_key='UnitAbbreviation')
#     unit_abbreviation_english = fields.String(description='Read-only',
#                                               data_key='UnitAbbreviationEnglish')
#     discount_percentage = fields.Number(description='Format: 4 decimals',
#                                         validate=[Range(min=0, max=1),
#                                                   # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,4})?'))
#                                                   ],
#                                         data_key='DiscountPercentage')
#     quantity = fields.Number(
#         # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#         data_key='Quantity')
#     is_work_cost = fields.Boolean(description='Read-only',
#                                   data_key='IsWorkCost')
#     is_vat_free = fields.Boolean(data_key='IsVatFree')
#     cost_center_item_id1 = fields.UUID(data_key='CostCenterItemId1')
#     cost_center_item_id2 = fields.UUID(data_key='CostCenterItemId2')
#     cost_center_item_id3 = fields.UUID(data_key='CostCenterItemId3')
#     unit_id = fields.UUID(description='Read-only', data_key='UnitId')
#     project_id = fields.UUID(data_key='ProjectId')
#     work_cost_type = fields.Integer(
#         description='Only used for ROT/RUT invoices', data_key='WorkCostType')
#     work_hours = fields.Number(description='Only used for ROT/RUT invoices',
#                                data_key='WorkHours')
#     material_costs = fields.Number(description='Only used for ROT/RUT invoices',
#                                    data_key='MaterialCosts')
#
#     class Meta:
#         # No endpoint
#         pass
#
#
# class CustomerLedgerItemWithVoucher(VismaModel):
#     currency_code = fields.String(required=True,
#                                   description='Max length: 3 characters',
#                                   validate=[Length(min=0, max=3)],
#                                   data_key='CurrencyCode')
#     currency_rate = fields.Number(data_key='CurrencyRate')
#     currency_rate_unit = fields.Integer(data_key='CurrencyRateUnit')
#     customer_id = fields.UUID(required=True,
#                               description='Source: Get from /customerlistitems.',
#                               data_key='CustomerId')
#     due_date = fields.DateTime(required=True, description='Format: YYYY-MM-DD',
#                                data_key='DueDate')
#     id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
#                      data_key='Id')
#     invoice_date = fields.DateTime(required=True,
#                                    description='Format: YYYY-MM-DD',
#                                    data_key='InvoiceDate')
#     invoice_number = fields.Integer(required=True, data_key='InvoiceNumber')
#     is_credit_invoice = fields.Boolean(required=True,
#                                        data_key='IsCreditInvoice')
#     payment_reference_number = fields.String(validate=[Length(min=0, max=50)],
#                                              data_key='PaymentReferenceNumber')
#     remaining_amount_invoice_currency = fields.Number(required=True, validate=[
#         Range(min=-1000000000, max=1000000000)],
#                                                       data_key='RemainingAmountInvoiceCurrency')
#     roundings_amount_invoice_currency = fields.Number(required=True, validate=[
#         Range(min=-1, max=1)], data_key='RoundingsAmountInvoiceCurrency')
#     total_amount_invoice_currency = fields.Number(required=True, validate=[
#         Range(min=-1000000000, max=1000000000)],
#                                                   data_key='TotalAmountInvoiceCurrency')
#     vat_amount_invoice_currency = fields.Number(required=True, validate=[
#         Range(min=-1000000000, max=1000000000)],
#                                                 data_key='VATAmountInvoiceCurrency')
#     voucher = fields.Nested('VoucherSchema', required=True, data_key='Voucher')
#     modified_utc = fields.DateTime(data_key='ModifiedUtc')
#
#     class Meta:
#         # Only used on one endpoint
#         # POST /v2/customerledgeritems/customerledgeritemswithvoucher
#         # Create a customer ledger item and a voucher included.
#         # endpoint = '/'
#         # allowed_methods = ['list', 'create', 'get', 'update', 'delete']
#         # TODO: how to handle this case?
#         pass
#
#
# class Document(VismaModel):
#     id = fields.UUID(data_key='Id')
#     content_type = fields.String(data_key='ContentType')
#     created_utc = fields.DateTime(data_key='CreatedUtc')
#     name = fields.String(data_key='Name')
#     name_without_extension = fields.String(data_key='NameWithoutExtension')
#     size = fields.Integer(description='Calculated in bytes', data_key='Size')
#     type = fields.Integer(description=('0 = SupplierInvoiceDraftAttachment, '
#                                        '1 = SupplierInvoiceAttachment, '
#                                        '2 = SupplierInvoiceXml,\r\n'
#                                        '10 = CustomerInvoiceXml, '
#                                        '11 = CustomerInvoicePdf, '
#                                        '12 = CustomerInvoicePaymentReminderPdf,\r\n'
#                                        '13 = CompanyLogo, '
#                                        '14 = DocumentBackgroundPdf, '
#                                        '20 = PhotoReceipt,'
#                                        ' 21 = PhotoSupplierInvoice,\r\n'
#                                        '30 = AutoInvoiceAssembly, '
#                                        '40 = FinvoiceReceiverInfoXml, '
#                                        '41 = VatReportPdf'), validate=[
#         OneOf(choices=[0, 1, 2, 10, 11, 12, 13, 14, 20, 21, 30, 40, 41],
#               labels=[])], data_key='Type')
#     temporary_url = fields.String(
#         description=('This is a temporary url that will expire and should not '
#                      'be stored.'), data_key='TemporaryUrl')
#
#     class Meta:
#         # GET /v2/documents/{id} Get a vat report pdf by document id.
#         endpoint = '/documents'
#         allowed_methods = ['get']
#
#
# class MessageThread(VismaModel):
#     id = fields.UUID(description='Read-Only', data_key='Id')
#     document_type = fields.Integer(validate=[OneOf(
#         choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
#         labels=[])], data_key='DocumentType')
#     document_id = fields.UUID(data_key='DocumentId')
#     document_number = fields.String(description='Read-Only',
#                                     data_key='DocumentNumber')
#     subject = fields.String(validate=[Length(min=0, max=40)],
#                             data_key='Subject')
#     modified_utc = fields.DateTime(description='Read-Only',
#                                    data_key='ModifiedUtc')
#     is_closed = fields.Boolean(description='Read-Only', data_key='IsClosed')
#     message_receivers = fields.List(fields.Nested('MessageReceiverSchema'),
#                                     data_key='MessageReceivers')
#
#     class Meta:
#         # GET /v2/messagethreads
#         # Gets all messages threads.
#         # GET /v2/messagethreads/{messageThreadId}
#         # Retrives a message thread.
#         # POST /v2/messagethreads/{messageThreadId}
#         # Replies to a message thread.
#         # PUT /v2/messagethreads/{messageThreadId}
#         # Marks a specific message thread.
#         endpoint = '/messagethreads'
#         allowed_methods = ['list', 'create', 'get', 'update']
#         envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
#
#
# class MessageReceiver(VismaModel):
#     user_id = fields.UUID(required=True, data_key='UserId')
#     status = fields.Integer(description='Read-Only', validate=[
#         OneOf(choices=[0, 1, 2, 3, 4], labels=[])], data_key='Status')
#     is_current_user = fields.Boolean(description='Read-Only',
#                                      data_key='IsCurrentUser')
#
#     class Meta:
#         # No endpoint
#         pass
#
#
# class Message(VismaModel):
#     id = fields.UUID(description='Read-Only', data_key='Id')
#     text = fields.String(validate=[Length(min=0, max=256)], data_key='Text')
#     modified_utc = fields.DateTime(description='Read-Only',
#                                    data_key='ModifiedUtc')
#     created_utc = fields.DateTime(description='Read-Only',
#                                   data_key='CreatedUtc')
#     created_by_user_id = fields.UUID(description='Read-Only',
#                                      data_key='CreatedByUserId')
#     modified_by_user_id = fields.UUID(description='Read-Only',
#                                       data_key='ModifiedByUserId')
#     message_thread_id = fields.UUID(description='Read-Only',
#                                     data_key='MessageThreadId')
#
#     class Meta:
#         # GET /v2/messagethreads/{messageThreadId}/messages
#         # Retrives the messages of a message thread.
#         # GET /v2/messagethreads/messages
#         # Gets all the messages of the threads.
#         endpoint = '/messagethreads/messages'
#         allowed_methods = ['list']
#         envelopes = {'list': {'class': PaginatedResponse,
#                               'data_attr': 'Data'}}  # TODO: how to handle this case?
#
#
# class MessageStatus(VismaModel):
#     status = fields.Integer(required=True, validate=[
#         OneOf(choices=[0, 1, 2, 3, 4], labels=[])], data_key='Status')
#
#     class Meta:
#         # No endpoint
#         pass
#
#
# class MessageToPost(VismaModel):
#     message = fields.String(required=True, validate=[Length(min=0, max=256)],
#                             data_key='Message')
#     subject = fields.String(required=True, validate=[Length(min=0, max=40)],
#                             data_key='Subject')
#     document_type = fields.Integer(required=True,
#                                    validate=[Range(min=0, max=16), OneOf(
#                                        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
#                                                 10, 11, 12, 13, 14, 15, 16],
#                                        labels=[])], data_key='DocumentType')
#     document_id = fields.UUID(data_key='DocumentId')
#     message_receivers = fields.List(fields.Nested('MessageReceiverSchema'),
#                                     data_key='MessageReceivers')
#
#     class Meta:
#         # used only for posting messages
#         # POST /v2/messagethreads Create a new message thread.
#         endpoint = '/messagethreads'
#         allowed_methods = ['create']
#
#
# class Note(VismaModel):
#     id = fields.UUID(description='Read-Only', data_key='Id')
#     user_id = fields.UUID(description='Read-Only', data_key='UserId')
#     attached_to = fields.UUID(
#         description='The document Id to which the note can be attached',
#         data_key='AttachedTo')
#     text = fields.String(validate=[Length(min=0, max=256)], data_key='Text')
#     subject = fields.String(validate=[Length(min=0, max=40)],
#                             data_key='Subject')
#     document_type = fields.Integer(
#         description=('The document type to which the note is attached \r\n'
#                      'None = 0, '
#                      'CustomerInvoice = 1, '
#                      'CustomerInvoiceDraft = 2, '
#                      'SupplierInvoice = 3, '
#                      'Voucher = 4, '
#                      'Quotation = 5, '
#                      'Order = 6, '
#                      'SupplierInvoiceDraft = 7, '
#                      'WebshopOrder = 8, '
#                      'Customer = 9, '
#                      'Receipt = 10, '
#                      'Article = 11, '
#                      'VatReport = 12, '
#                      'Supplier = 13, '
#                      'Inventory = 14, '
#                      'Employee = 15, '
#                      'Payslip = 16'), validate=[Range(min=0, max=16), OneOf(
#             choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
#             labels=[])], data_key='DocumentType')
#     created_utc = fields.DateTime(description='Read-Only',
#                                   data_key='CreatedUtc')
#     modified_utc = fields.DateTime(description='Read-Only',
#                                    data_key='ModifiedUtc')
#     is_done = fields.Boolean(description='Read-Only', data_key='IsDone')
#
#     class Meta:
#         # GET /v2/notes Get all notes.
#         # POST /v2/notes Create a new note.
#         # GET /v2/notes/{noteId} Get a specific note.
#         # PUT /v2/notes/{noteId} Updates a note.
#         endpoint = '/notes'
#         allowed_methods = ['list', 'create', 'get', 'update']
#         envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
#
#
# class Order(VismaModel):
#     id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
#                      data_key='Id')
#     amount = fields.Number(required=True, description='Format: 2 decimals',
#                            # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                            data_key='Amount')
#     customer_id = fields.UUID(required=True, data_key='CustomerId')
#     currency_code = fields.String(required=True,
#                                   description='Max length: 3 characters',
#                                   validate=[Length(min=0, max=3)],
#                                   data_key='CurrencyCode')
#     created_utc = fields.DateTime(description='Read-Only',
#                                   data_key='CreatedUtc')
#     vat_amount = fields.Number(required=True, description='Format: 2 decimals',
#                                # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                data_key='VatAmount')
#     roundings_amount = fields.Number(required=True,
#                                      description='Format: 2 decimals',
#                                      # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                      data_key='RoundingsAmount')
#     delivered_amount = fields.Number(description='Format: 2 decimals',
#                                      # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                      data_key='DeliveredAmount')
#     delivered_vat_amount = fields.Number(description='Format: 2 decimals',
#                                          # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                          data_key='DeliveredVatAmount')
#     delivered_roundings_amount = fields.Number(description='Format: 2 decimals',
#                                                # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                                data_key='DeliveredRoundingsAmount')
#     delivery_customer_name = fields.String(
#         description='Max length: 50 characters',
#         validate=[Length(min=0, max=50)], data_key='DeliveryCustomerName')
#     delivery_address1 = fields.String(description='Max length: 50 characters',
#                                       validate=[Length(min=0, max=50)],
#                                       data_key='DeliveryAddress1')
#     delivery_address2 = fields.String(description='Max length: 50 characters',
#                                       validate=[Length(min=0, max=50)],
#                                       data_key='DeliveryAddress2')
#     delivery_postal_code = fields.String(
#         description='Max length: 10 characters',
#         validate=[Length(min=0, max=10)], data_key='DeliveryPostalCode')
#     delivery_city = fields.String(description='Max length: 50 characters',
#                                   validate=[Length(min=0, max=50)],
#                                   data_key='DeliveryCity')
#     delivery_country_code = fields.String(
#         description='Max length: 2 characters', validate=[Length(min=0, max=2)],
#         data_key='DeliveryCountryCode')
#     your_reference = fields.String(description='Max length: 50 characters',
#                                    validate=[Length(min=0, max=50)],
#                                    data_key='YourReference')
#     our_reference = fields.String(description='Max length: 50 characters',
#                                   validate=[Length(min=0, max=50)],
#                                   data_key='OurReference')
#     invoice_address1 = fields.String(description='Max length: 50 characters',
#                                      validate=[Length(min=0, max=50)],
#                                      data_key='InvoiceAddress1')
#     invoice_address2 = fields.String(description='Max length: 50 characters',
#                                      validate=[Length(min=0, max=50)],
#                                      data_key='InvoiceAddress2')
#     invoice_city = fields.String(required=True, data_key='InvoiceCity')
#     invoice_country_code = fields.String(required=True,
#                                          description='Max length: 2 characters',
#                                          validate=[Length(min=0, max=2)],
#                                          data_key='InvoiceCountryCode')
#     invoice_customer_name = fields.String(required=True,
#                                           description='Max length: 50 characters',
#                                           validate=[Length(min=0, max=50)],
#                                           data_key='InvoiceCustomerName')
#     invoice_postal_code = fields.String(required=True,
#                                         description='Max length: 10 characters',
#                                         validate=[Length(min=0, max=10)],
#                                         data_key='InvoicePostalCode')
#     delivery_method_name = fields.String(
#         description='Max length: 50 characters',
#         validate=[Length(min=0, max=50)], data_key='DeliveryMethodName')
#     delivery_method_code = fields.String(
#         description='Max length: 50 characters',
#         validate=[Length(min=0, max=20)], data_key='DeliveryMethodCode')
#     delivery_term_name = fields.String(description='Max length: 50 characters',
#                                        validate=[Length(min=0, max=50)],
#                                        data_key='DeliveryTermName')
#     delivery_term_code = fields.String(description='Max length: 50 characters',
#                                        validate=[Length(min=0, max=20)],
#                                        data_key='DeliveryTermCode')
#     eu_third_party = fields.Boolean(required=True, data_key='EuThirdParty')
#     customer_is_private_person = fields.Boolean(required=True,
#                                                 data_key='CustomerIsPrivatePerson')
#     order_date = fields.DateTime(required=True,
#                                  description='Format: YYYY-MM-DD',
#                                  data_key='OrderDate')
#     status = fields.Integer(required=True,
#                             description='1 = Draft, 2 = Ongoing, 3 = Shipped, 4 = Invoiced',
#                             validate=[Range(min=1, max=4),
#                                       OneOf(choices=[1, 2, 3, 4], labels=[])],
#                             data_key='Status')
#     number = fields.Integer(data_key='Number')
#     modified_utc = fields.DateTime(description='Read-Only',
#                                    data_key='ModifiedUtc')
#     delivery_date = fields.DateTime(
#         description='Format: YYYY-MM-DD. Default: null',
#         data_key='DeliveryDate')
#     house_work_amount = fields.Number(data_key='HouseWorkAmount')
#     house_work_automatic_distribution = fields.Boolean(
#         data_key='HouseWorkAutomaticDistribution')
#     house_work_corporate_identity_number = fields.String(
#         description='Max length: 20 characters',
#         validate=[Length(min=0, max=20)],
#         data_key='HouseWorkCorporateIdentityNumber')
#     house_work_property_name = fields.String(
#         description='Max length: 100 characters',
#         validate=[Length(min=0, max=100)], data_key='HouseWorkPropertyName')
#     rows = fields.List(fields.Nested('OrderRowSchema'), data_key='Rows')
#     shipped_date_time = fields.DateTime(
#         description='Format: YYYY-MM-DD. Default: null',
#         data_key='ShippedDateTime')
#     rot_reduced_invoicing_type = fields.Integer(required=True,
#                                                 description='0 = None, 1 = Rot, 2 = Rut',
#                                                 validate=[
#                                                     OneOf(choices=[0, 1, 2],
#                                                           labels=[])],
#                                                 data_key='RotReducedInvoicingType')
#     rot_property_type = fields.Integer(data_key='RotPropertyType')
#     persons = fields.List(
#         fields.Nested('SalesDocumentRotRutReductionPersonSchema'),
#         data_key='Persons')
#     reverse_charge_on_construction_services = fields.Boolean(required=True,
#                                                              data_key='ReverseChargeOnConstructionServices')
#
#     class Meta:
#         # GET /v2/orders Get orders.
#         # POST /v2/orders Create order.
#         # DELETE /v2/orders/{id} Delete an order.
#         # GET /v2/orders/{id} Get order
#         # PUT /v2/orders/{id} Replace content in an order.
#         endpoint = '/orders'
#         allowed_methods = ['list', 'create', 'get', 'update', 'delete']
#         envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
#
#
# class OrderRow(VismaModel):
#     line_number = fields.Integer(required=True,
#                                  validate=[Range(min=0, max=1000)],
#                                  data_key='LineNumber')
#     delivered_quantity = fields.Number(description='Format: 2 decimals',
#                                        # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                        data_key='DeliveredQuantity')
#     article_id = fields.UUID(data_key='ArticleId')
#     article_number = fields.String(description='Max length: 40 characters',
#                                    validate=[Length(min=0, max=40)],
#                                    data_key='ArticleNumber')
#     is_text_row = fields.Boolean(required=True, data_key='IsTextRow')
#     text = fields.String(description='Max length: 2000 characters',
#                          validate=[Length(min=0, max=2000)], data_key='Text')
#     unit_price = fields.Number(description='Format: 2 decimals',
#                                # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                data_key='UnitPrice')
#     discount_percentage = fields.Number(description='Format: 4 decimals',
#                                         validate=[Range(min=0, max=1),
#                                                   # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,4})?'))
#                                                   ],
#                                         data_key='DiscountPercentage')
#     quantity = fields.Number(description='Format: 4 decimals',
#                              # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,4})?'))],
#                              data_key='Quantity')
#     work_cost_type = fields.Integer(data_key='WorkCostType')
#     is_work_cost = fields.Boolean(required=True, data_key='IsWorkCost')
#     eligible_for_reverse_charge_on_vat = fields.Boolean(required=True,
#                                                         data_key='EligibleForReverseChargeOnVat')
#     cost_center_item_id1 = fields.UUID(
#         description='Source: Get from /v2/costcenters',
#         data_key='CostCenterItemId1')
#     cost_center_item_id2 = fields.UUID(
#         description='Source: Get from /v2/costcenters',
#         data_key='CostCenterItemId2')
#     cost_center_item_id3 = fields.UUID(
#         description='Source: Get from /v2/costcenters',
#         data_key='CostCenterItemId3')
#     id = fields.UUID(data_key='Id')
#     project_id = fields.UUID(data_key='ProjectId')
#
#     class Meta:
#         # No endpoint
#         pass
#
#
# class SalesDocumentAttachment(VismaModel):
#     id = fields.UUID(data_key='Id')
#     document_id = fields.UUID(data_key='DocumentId')
#     document_type = fields.Integer(
#         validate=[OneOf(choices=[0, 1, 2, 3, 4], labels=[])],
#         data_key='DocumentType')
#     original_filename = fields.String(data_key='OriginalFilename')
#     document_size = fields.Integer(data_key='DocumentSize')
#     created_utc = fields.DateTime(data_key='CreatedUtc')
#     thumbnail = fields.String(data_key='Thumbnail')
#
#     class Meta:
#         # POST /v2/salesdocumentattachments/customerinvoicedraft
#         # Create a sales document attached to a customer invoice draft.
#         # POST /v2/salesdocumentattachments/customerinvoice
#         # Create a sales document attached to a customer invoice
#         # (including customer ledger items).
#         # DELETE /v2/salesdocumentattachments/customerinvoicedraft/{customerInvoiceDraftId}/{attachmentId}
#         # Delete a document attached to a customer invoice draft.
#         # DELETE /v2/salesdocumentattachments/customerinvoice/{customerInvoiceId}/{attachmentId}
#         # Delete a document attached to a customer invoice (including customer ledger items).
#         # TODO: Maybe subclass so separte between invoicedraft and invoice
#         # endpoint = '/'
#         # allowed_methods = ['list', 'create', 'get', 'update', 'delete']
#         # envelopes = {
#         #     'list': {'class': PaginatedResponse,
#         #              'data_attr': 'Data'}
#         # }
#         pass
#
#
# class SupplierInvoiceDraft(VismaModel):
#     id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
#                      data_key='Id')
#     supplier_id = fields.UUID(required=True,
#                               description='Source: Get from /supplierlistitems',
#                               data_key='SupplierId')
#     bank_account_id = fields.UUID(
#         description=('Source: Get from /bankaccounts, '
#                      'if not provided the supplier bank account will be used.'),
#         data_key='BankAccountId')
#     invoice_date = fields.DateTime(
#         description="Format: YYYY-MM-DD. Default: Today's date",
#         data_key='InvoiceDate')
#     payment_date = fields.DateTime(description='Format: YYYY-MM-DD',
#                                    data_key='PaymentDate')
#     due_date = fields.DateTime(description=('Format: YYYY-MM-DD. '
#                                             'Default: Date based on the suppliers Terms of payment'),
#                                data_key='DueDate')
#     invoice_number = fields.String(description='Max length: 50 characters',
#                                    validate=[Length(min=0, max=50)],
#                                    data_key='InvoiceNumber')
#     total_amount = fields.Number(description='Format: Max 2 decimals',
#                                  # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                  data_key='TotalAmount')
#     vat = fields.Number(description='Format: Max 2 decimals',
#                         # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                         data_key='Vat')
#     vat_high = fields.Number(description='Format: Max 2 decimals',
#                              # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                              data_key='VatHigh')
#     vat_medium = fields.Number(description='Format: Max 2 decimals',
#                                # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                data_key='VatMedium')
#     vat_low = fields.Number(description='Format: Max 2 decimals',
#                             # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                             data_key='VatLow')
#     is_credit_invoice = fields.Boolean(required=True,
#                                        data_key='IsCreditInvoice')
#     currency_code = fields.String(description='Max length: 3 characters',
#                                   validate=[Length(min=0, max=3)],
#                                   data_key='CurrencyCode')
#     currency_rate = fields.Number(
#         description=("Purpose: If currency code is domestic and currency rate "
#                      "isn't included it will be fetched from eAccounting"),
#         data_key='CurrencyRate')
#     ocr_number = fields.String(description='Max length: 25 characters',
#                                validate=[Length(min=0, max=25)],
#                                data_key='OcrNumber')
#     message = fields.String(description='Max length: 25 characters',
#                             validate=[Length(min=0, max=25)],
#                             data_key='Message')
#     rows = fields.List(fields.Nested('SupplierInvoiceDraftRowSchema'),
#                        required=True, data_key='Rows')
#     supplier_name = fields.String(description='Max length: 50 characters',
#                                   validate=[Length(min=0, max=50)],
#                                   data_key='SupplierName')
#     supplier_number = fields.String(description='Max length: 50 characters',
#                                     validate=[Length(min=0, max=50)],
#                                     data_key='SupplierNumber')
#     self_employed_without_fixed_address = fields.Boolean(
#         data_key='SelfEmployedWithoutFixedAddress')
#     is_quick_invoice = fields.Boolean(data_key='IsQuickInvoice')
#     is_domestic = fields.Boolean(data_key='IsDomestic')
#     approval_status = fields.Integer(description=('0 = None, '
#                                                   '1 = Approved, '
#                                                   '2 = Rejected, '
#                                                   '3 = ReadyForApproval'),
#                                      validate=[OneOf(choices=[0, 1, 2, 3],
#                                                      labels=[])],
#                                      data_key='ApprovalStatus')
#     allocation_periods = fields.List(fields.Nested('AllocationPeriodSchema'),
#                                      description=('Read-only: Post to '
#                                                   '/supplierinvoicedrafts/{supplierInvoiceDraftId}/'
#                                                   'allocationperiods/'),
#                                      data_key='AllocationPeriods')
#     attachments = fields.Nested('AttachmentLinkSchema', data_key='Attachments')
#
#     class Meta:
#         # GET /v2/supplierinvoicedrafts
#         # Get a paginated list of all supplier invoice drafts.
#         # POST /v2/supplierinvoicedrafts
#         # Create a supplier invoice draft
#         # DELETE /v2/supplierinvoicedrafts/{supplierInvoiceDraftId}
#         # Deletes a supplier invoice draft
#         # GET /v2/supplierinvoicedrafts/{supplierInvoiceDraftId}
#         # Get a single supplier invoice draft.
#         # PUT /v2/supplierinvoicedrafts/{supplierInvoiceDraftId}
#         # Relpace content in a supplier invoice draft.
#         endpoint = '/supplierinvoicedrafts'
#         allowed_methods = ['list', 'create', 'get', 'update', 'delete']
#         envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
#
#
# class SupplierInvoiceDraftRow(VismaModel):
#     id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
#                      data_key='Id')
#     account_number = fields.Integer(validate=[Range(min=1, max=None)],
#                                     data_key='AccountNumber')
#     account_name = fields.String(data_key='AccountName')
#     vat_code_id = fields.UUID(description=('Purpose: '
#                                            'Returns the Vat code id from the provided account number'),
#                               data_key='VatCodeId')
#     cost_center_item_id1 = fields.UUID(
#         description='Source: Get from /costcenters',
#         data_key='CostCenterItemId1')
#     cost_center_item_id2 = fields.UUID(
#         description='Source: Get from /costcenters',
#         data_key='CostCenterItemId2')
#     cost_center_item_id3 = fields.UUID(
#         description='Source: Get from /costcenters',
#         data_key='CostCenterItemId3')
#     project_id = fields.UUID(data_key='ProjectId')
#     debit_amount = fields.Number(description='Format: Max 2 decimals',
#                                  # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                  data_key='DebitAmount')
#     credit_amount = fields.Number(description='Format: Max 2 decimals',
#                                   # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                   data_key='CreditAmount')
#     transaction_text = fields.String(data_key='TransactionText')
#     line_number = fields.Integer(description='Default: 1',
#                                  data_key='LineNumber')
#     quantity = fields.Number(description=('Format: Max 2 decimals\r\n'
#                                           'Purpose: '
#                                           'This feature is for dutch companies only which enabled a'
#                                           'griculture support'),
#                              # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                              data_key='Quantity')
#     weight = fields.Number(description=('Format: Max 2 decimals\r\n'
#                                         'Purpose: This feature is for dutch companies only which '
#                                         'enabled agriculture support'),
#                            # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                            data_key='Weight')
#     delivery_date = fields.DateTime(description=('Format: YYYY-MM-DD\r\n'
#                                                  'Purpose: This feature is for dutch companies only which '
#                                                  'enabled agriculture support'),
#                                     data_key='DeliveryDate')
#     harvest_year = fields.Integer(
#         description=('Purpose: This feature is for dutch companies only which '
#                      'enabled agriculture support'), data_key='HarvestYear')
#
#     class Meta:
#         # no endpoint
#         pass
#
#
# class SupplierInvoice(VismaModel):
#     id = fields.UUID(description=(
#         'Read-only: This is automatically generated by eAccounting '
#         'upon creation'), data_key='Id')
#     supplier_id = fields.UUID(required=True,
#                               description='Source: Get from /v2/suppliers.',
#                               data_key='SupplierId')
#     bank_account_id = fields.UUID(description='Read-Only',
#                                   data_key='BankAccountId')
#     invoice_date = fields.DateTime(description='Format: YYYY-MM-DD',
#                                    data_key='InvoiceDate')
#     payment_date = fields.DateTime(description='Read-Only',
#                                    data_key='PaymentDate')
#     due_date = fields.DateTime(description=("Format: YYYY-MM-DD. "
#                                             "Default: Date based on the supplier's terms of payment"),
#                                data_key='DueDate')
#     invoice_number = fields.String(data_key='InvoiceNumber')
#     total_amount = fields.Number(data_key='TotalAmount')
#     vat = fields.Number(data_key='Vat')
#     vat_high = fields.Number(description='Only for Norway', data_key='VatHigh')
#     vat_medium = fields.Number(description='Only for Norway',
#                                data_key='VatMedium')
#     vat_low = fields.Number(description='Only for Norway', data_key='VatLow')
#     is_credit_invoice = fields.Boolean(data_key='IsCreditInvoice')
#     currency_code = fields.String(data_key='CurrencyCode')
#     currency_rate = fields.Number(data_key='CurrencyRate')
#     ocr_number = fields.String(data_key='OcrNumber')
#     message = fields.String(data_key='Message')
#     created_utc = fields.DateTime(description='Read-only',
#                                   data_key='CreatedUtc')
#     modified_utc = fields.DateTime(description='Read-only',
#                                    data_key='ModifiedUtc')
#     plus_giro_number = fields.String(description='Read-only',
#                                      data_key='PlusGiroNumber')
#     bank_giro_number = fields.String(description='Read-only',
#                                      data_key='BankGiroNumber')
#     rows = fields.List(fields.Nested('SupplierInvoiceRowSchema'),
#                        data_key='Rows')
#     supplier_name = fields.String(description='Read-only',
#                                   data_key='SupplierName')
#     supplier_number = fields.String(description='Read-only',
#                                     data_key='SupplierNumber')
#     is_quick_invoice = fields.Boolean(description='Read-only',
#                                       data_key='IsQuickInvoice')
#     is_domestic = fields.Boolean(description='Read-only', data_key='IsDomestic')
#     remaining_amount = fields.Number(description='Read-only',
#                                      data_key='RemainingAmount')
#     remaining_amount_invoice_currency = fields.Number(description='Read-only',
#                                                       data_key='RemainingAmountInvoiceCurrency')
#     voucher_number = fields.String(description='Read-only',
#                                    data_key='VoucherNumber')
#     voucher_id = fields.UUID(description='Read-only', data_key='VoucherId')
#     created_from_draft_id = fields.UUID(description='Read-only',
#                                         data_key='CreatedFromDraftId')
#     self_employed_without_fixed_address = fields.Boolean(
#         description='Read-only', data_key='SelfEmployedWithoutFixedAddress')
#     allocation_periods = fields.List(fields.Nested('AllocationPeriodSchema'),
#                                      description='Read-only. For create use POST /v2/allocationperiods',
#                                      data_key='AllocationPeriods')
#     auto_credit_debit_pairing = fields.Boolean(
#         data_key='AutoCreditDebitPairing')
#     attachments = fields.List(fields.UUID(), data_key='Attachments')
#
#     class Meta:
#         # GET /v2/supplierinvoices
#         # Get a list of supplier invoices
#         # POST /v2/supplierinvoices
#         # Create a supplier invoice.
#         # GET /v2/supplierinvoices/{supplierInvoiceId}
#         # Get a supplier
#         # POST /v2/supplierinvoices/{invoiceId}/payments
#         # Post a payment towards a bookkept supplier invoice
#         endpoint = '/supplierinvoices'
#         allowed_methods = ['list', 'create', 'get', 'update']
#         envelopes = {'list': {'class': PaginatedResponse,
#                               'data_attr': 'Data'}}  # TODO: How to handle the payment
#
#
# class SupplierInvoiceRow(VismaModel):
#     id = fields.UUID(
#         description=('Read-only: This is automatically generated by '
#                      'eAccounting upon creation'), data_key='Id')
#     account_number = fields.Integer(data_key='AccountNumber')
#     account_name = fields.String(description='Read-only',
#                                  data_key='AccountName')
#     vat_code_id = fields.UUID(description='Only for Denmark and Netherlands',
#                               data_key='VatCodeId')
#     vat_amount = fields.Number(description='Only for Denmark and Netherlands',
#                                data_key='VatAmount')
#     cost_center_item_id1 = fields.UUID(
#         description='Source: Get from /v2/costcenters.',
#         data_key='CostCenterItemId1')
#     cost_center_item_id2 = fields.UUID(
#         description='Source: Get from /v2/costcenters.',
#         data_key='CostCenterItemId2')
#     cost_center_item_id3 = fields.UUID(
#         description='Source: Get from /v2/costcenters.',
#         data_key='CostCenterItemId3')
#     quantity = fields.Number(data_key='Quantity')
#     weight = fields.Number(data_key='Weight')
#     delivery_date = fields.DateTime(data_key='DeliveryDate')
#     harvest_year = fields.Integer(data_key='HarvestYear')
#     debet_amount = fields.Number(description='Format: Max 2 decimals',
#                                  # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                  data_key='DebetAmount')
#     credit_amount = fields.Number(description='Format: Max 2 decimals',
#                                   # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                                   data_key='CreditAmount')
#     line_number = fields.Integer(description='Read-only', data_key='LineNumber')
#     project_id = fields.UUID(description='Source: Get from /v2/projects.',
#                              data_key='ProjectId')
#     transaction_text = fields.String(data_key='TransactionText')
#
#     class Meta:
#         # No endpoint
#         pass
#
#
# class Voucher(VismaModel):
#     id = fields.UUID(description='Read-only: Unique Id provided by eAccounting',
#                      data_key='Id')
#     voucher_date = fields.DateTime(required=True,
#                                    description='Format: yyyy-mm-dd',
#                                    data_key='VoucherDate')
#     voucher_text = fields.String(required=True,
#                                  description='Max length: 100 characters',
#                                  validate=[Length(min=0, max=100)],
#                                  data_key='VoucherText')
#     rows = fields.List(fields.Nested('VoucherRowSchema'), required=True,
#                        data_key='Rows')
#     number_and_number_series = fields.String(
#         description='Purpose: Returns the voucher number.',
#         data_key='NumberAndNumberSeries')
#     number_series = fields.String(description=('Purpose: '
#                                                'Returns the number series. '
#                                                'Use parameter useDefaultNumberSeries with false value '
#                                                'to set Series.'),
#                                   data_key='NumberSeries')
#     attachments = fields.Nested('AttachmentLinkSchema', data_key='Attachments')
#     modified_utc = fields.DateTime(data_key='ModifiedUtc')
#     voucher_type = fields.Integer(description=('2 = ManualVoucher, '
#                                                '5 = BankAccountTransferDeposit, '
#                                                '6 = BankAccountTransferWithDrawal, \r\n'
#                                                '7 = PurchaseReceipt, '
#                                                '8 = VatReport, '
#                                                '9 = SieImport, '
#                                                '10 = BankTransactionDeposit, '
#                                                '11 = BankTransactionWithdrawal,\r\n'
#                                                '12 = SupplierInvoiceDebit, '
#                                                '13 = SupplierInvoiceCredit, 1'
#                                                '4 = CustomerInvoiceDebit, '
#                                                '15 = CustomerInvoiceCredit,\r\n'
#                                                '16 = ClaimOnCardAcquirer, '
#                                                '17 = TaxReturn, '
#                                                '18 = AllocationPeriod, '
#                                                '19 = AllocationPeriodCorrection, \r\n'
#                                                '20 = InventoryEvent, '
#                                                '21 = EmployerReport, '
#                                                '22 = Payslip, '
#                                                '23 = CustomerQuickInvoiceDebit,\r\n'
#                                                '24 = CustomerQuickInvoiceCredit, '
#                                                '25 = SupplierQuickInvoiceDebit, '
#                                                '26 = SupplierQuickInvoiceCredit, \r\n'
#                                                '27 = IZettleVoucher'),
#                                   validate=[OneOf(
#                                       choices=[2, 5, 6, 7, 8, 9, 10, 11, 12, 13,
#                                                14, 15, 16, 17, 18, 19, 20, 21,
#                                                22, 23, 24, 25, 26, 27],
#                                       labels=[])], data_key='VoucherType')
#     source_id = fields.UUID(data_key='SourceId')
#
#     class Meta:
#         # GET /v2/vouchers
#         # Get all vouchers from all fiscal years.
#         # POST /v2/vouchers
#         # Create a voucher.
#         # GET /v2/vouchers/{fiscalyearId}
#         # Get all vouchers in a given fiscal year.
#         # GET /v2/vouchers/{fiscalyearId}/{voucherId}
#         # Get a single voucher from a given fiscal year
#         endpoint = '/vouchers'
#         allowed_methods = ['list', 'create']
#         envelopes = {'list': {'class': PaginatedResponse,
#                               'data_attr': 'Data'}}  # TODO: how to handle voucher and fiscal year?
#
#
# class VoucherRow(VismaModel):
#     account_number = fields.Integer(required=True,
#                                     validate=[Range(min=1, max=None)],
#                                     data_key='AccountNumber')
#     account_description = fields.String(description='Read-only',
#                                         data_key='AccountDescription')
#     debit_amount = fields.Number(description='Format: Max 2 decimals',
#                                  validate=[Range(min=0, max=1000000000),
#                                            # Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))
#                                            ], data_key='DebitAmount')
#     credit_amount = fields.Number(description='Format: Max 2 decimals',
#                                   validate=[Range(min=0, max=1000000000),
#                                             # Regexp(regex=re.compile( '[-]?\\d+(.\\d{1,2})?'))
#                                             ], data_key='CreditAmount')
#     transaction_text = fields.String(description='Max length: 50 characters',
#                                      validate=[Length(min=0, max=50)],
#                                      data_key='TransactionText')
#     cost_center_item_id1 = fields.UUID(
#         description='Source: Get from /costcenters',
#         data_key='CostCenterItemId1')
#     cost_center_item_id2 = fields.UUID(
#         description='Source: Get from /costcenters',
#         data_key='CostCenterItemId2')
#     cost_center_item_id3 = fields.UUID(
#         description='Source: Get from /costcenters',
#         data_key='CostCenterItemId3')
#     vat_code_id = fields.UUID(data_key='VatCodeId')
#     vat_code_and_percent = fields.String(data_key='VatCodeAndPercent')
#     quantity = fields.Number(description=('Format: Max 2 decimals\r\n'
#                                           'Purpose: This feature is for dutch companies only which '
#                                           'enabled agriculture support'),
#                              # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#                              data_key='Quantity')
#     weight = fields.Number(
#         description=('Format: Max 2 decimals\r\nPurpose: This feature is for '
#                      'dutch companies only which enabled agriculture support'),
#         # validate=[Regexp(regex=re.compile('[-]?\\d+(.\\d{1,2})?'))],
#         data_key='Weight')
#     delivery_date = fields.DateTime(
#         description=('Format: YYYY-MM-DD\r\nPurpose: This feature is for dutch '
#                      'companies only which enabled agriculture support'),
#         data_key='DeliveryDate')
#     harvest_year = fields.Integer(
#         description=('Purpose: This feature is for dutch companies only which '
#                      'enabled agriculture support'), data_key='HarvestYear')
#     project_id = fields.UUID(description='Source: Get from /projects',
#                              data_key='ProjectId')
#
#     class Meta:
#         # No endpoint
#         pass
#
#
# class WebshopOrder(VismaModel):
#     id = fields.UUID(data_key='Id')
#     base_currency_code = fields.String(data_key='BaseCurrencyCode')
#     name = fields.String(data_key='Name')
#     number = fields.String(data_key='Number')
#     order_currency_code = fields.String(data_key='OrderCurrencyCode')
#     order_date = fields.DateTime(data_key='OrderDate')
#     order_number = fields.String(data_key='OrderNumber')
#     note = fields.String(data_key='Note')
#     total_amount_base_currency = fields.Number(
#         data_key='TotalAmountBaseCurrency')
#     total_amount_order_currency = fields.Number(
#         data_key='TotalAmountOrderCurrency')
#     rows = fields.List(fields.Nested('WebshopOrderRowSchema'), data_key='Rows')
#
#     class Meta:
#         # GET /v2/webshoporders Get webshop orders.
#         # GET /v2/webshoporders/{webshopOrderId} Get a single webshop order.
#         # POST /v2/webshoporders/{webshopOrderId}/convert
#         # Converts a webshop order to a invoice.
#         #  The resulted invoice will appear as paid in the sales invoice list.
#         endpoint = '/webshoporders'
#         allowed_methods = ['list', 'get']
#         envelopes = {'list': {'class': PaginatedResponse, 'data_attr': 'Data'}}
#
#
# class WebshopOrderRow(VismaModel):
#     id = fields.UUID(data_key='Id')
#     article_name = fields.String(data_key='ArticleName')
#     article_number = fields.String(data_key='ArticleNumber')
#     price_per_unit_invoice_currency = fields.Number(
#         data_key='PricePerUnitInvoiceCurrency')
#     quantity = fields.Number(data_key='Quantity')
#     unit_abbreviation = fields.String(data_key='UnitAbbreviation')
#     sum = fields.Number(data_key='Sum')
#
#     class Meta:
#         # No endpoint
#         pass

# TODO: Some fields are references to other models primary keys. It would be interesting to have functionallity to fetch the model on evaluation of the attribute and return a whole model instance instead of just the key.
