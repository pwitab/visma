import pytest

from visma.models import Customer


class TestCRUDCustomer:
    customer_number = 'test_customer'

    customer_id = None

    def test_create_customer(self):
        customer = Customer(
            invoice_city='Helsingborg',
            invoice_postal_code='25234',
            name='TestCustomer AB',
            terms_of_payment_id='8f9a8f7b-5ea9-44c6-9725-9b8a1addb036',
            is_private_person=False,
            is_active=True)
        customer.save()

        self.customer_id = customer.id

    def test_update_customer(self):
        pass

    def test_delete_customer(self):
        pass

    def test_get_customer(self):
        pass
