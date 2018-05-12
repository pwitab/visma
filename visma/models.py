import os
import iso8601


class VismaModel:

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


class TermsOfPayment:

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

    @classmethod
    def with_customer(cls, customer, *args, **kwargs):
        assert isinstance(customer, Customer)

        return cls(customer_id=customer.id, customer_name=customer.name,
                   postal_code=customer.invoice_postal_code,
                   city=customer.invoice_city,
                   customer_is_private_person=customer.is_private_person,
                   *args, **kwargs)







