import os
import iso8601


# class VismaModelBase(type):
#     """Metaclass for all VismaModels that will inject the api
#
#     Will read environment variables and instantiate a new VismaAPI object on all
#     model classes.
#
#     TODO: If it where a Django app we would have access to the settings all
#     across the application and we could use the same object and also maybe start
#     building in caching in the API model. But not really sure how to make a
#     simmilar thing when using in a script.
#     """
#
#     def __new__(cls, *args, **kwargs):
#         x = super().__new__(cls, *args, **kwargs)
#         is_initiated = bool(os.environ.get('VISMA_IS_INITIATED', default=None))
#         if is_initiated:
#             settings = cls.get_api_settings()
#             x.api = VismaAPI(**settings)
#
#         return x
#
#     @staticmethod
#     def get_api_settings():
#         access_token = os.environ.get('VISMA_ACCESS_TOKEN')
#         refresh_token = os.environ.get('VISMA_REFRESH_TOKEN')
#         token_expires = iso8601.parse_date(
#             os.environ.get('VISMA_TOKEN_EXPIRES'))
#         is_initiated = bool(os.environ.get('VISMA_IS_INITIATED'))
#         client_id = os.environ.get('VISMA_CLIENT_ID')
#         client_secret = os.environ.get('VISMA_CLIENT_SECRET')
#
#         settings = {'access_token': access_token,
#                     'refresh_token': refresh_token,
#                     'token_expires': token_expires,
#                     'is_initiated': is_initiated,
#                     'client_id': client_id,
#                     'client_secret': client_secret}
#         return settings

class VismaModel:

    def save(self):
        pass

    def serialize(self):
        pass

    @classmethod
    def deserialize(cls, data):
        pass

# TODO: Can I use Meta Class to attach an API object to all models?


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

    def __init__(self, customer,
                 customer_name=None,
                 postal_code=None,
                 city=None,
                 ):

        assert isinstance(customer, Customer)

        self.customer = customer
        self.customer_id = self.customer.id
        if customer_name is None:
            self.customer_name = self.customer.name
        else:
            self.customer_name = customer_name

        if postal_code is None:
            self.postal_code = self.customer.invoice_postal_code
        else:
            self.postal_code = postal_code

        if city is None:
            self.city = self.customer.invoice_city
        else:
            self.city = city

        self.customer_is_private_person = self.customer.is_private_person

        self.rot_reduced_invoicing_type = 0  # Normal
        self.eu_third_party = False
        self.country_code = 'SE'




