import pytest

from visma.api import VismaAPIException
from visma.models import Customer, CustomerInvoiceDraft, TermsOfPayment


class TestCRUDCustomerInvoiceDraft:

    invoice_id = None

    @pytest.fixture()
    def terms_of_payment_id(self):
        """
        Doesn't matter what term it is just that the id exists.
        """
        top = TermsOfPayment.objects.all()[0]
        yield top.id

    @pytest.fixture()
    def customer(self, terms_of_payment_id):
        customer = Customer(
            invoice_city='Helsingborg',
            invoice_postal_code='25234',
            name='TestCustomer AB',
            terms_of_payment_id=terms_of_payment_id,
            is_private_person=False,
            is_active=True)
        customer.save()
        yield customer
        customer.delete()

    @pytest.fixture()
    def customer_invoice_draft_id(self, customer):

            invoice = CustomerInvoiceDraft(customer_id=customer.id,
                                           invoice_customer_name='test_name',
                                           invoice_postal_code='25269',
                                           invoice_city='Helsingborg',
                                           customer_is_private_person=False,
                                           your_reference='Reference')
            invoice.save()

            yield invoice.id

            invoice.delete()


    def test_create_customer_invoice_draft(self, customer):
        invoice = CustomerInvoiceDraft(customer_id=customer.id,
                                       invoice_customer_name='test_name',
                                       invoice_postal_code='25269',
                                       invoice_city='Helsingborg',
                                       customer_is_private_person=False)

        invoice.save()

        assert invoice.id is not None

    def test_read_customer_invoice_draft(self, customer_invoice_draft_id):

        invoice = CustomerInvoiceDraft.objects.get(customer_invoice_draft_id)

        assert invoice.id == customer_invoice_draft_id

    def test_update_customer_invoice_draft(self, customer_invoice_draft_id):

        invoice = CustomerInvoiceDraft.objects.get(customer_invoice_draft_id)

        new_name = 'Updated Name'
        invoice.your_reference = new_name
        invoice.save()

        updated_invoice = CustomerInvoiceDraft.objects.get(customer_invoice_draft_id)

        assert updated_invoice.your_reference == new_name

    def test_delete_customer_invoice_draft(self, customer):
        # dont use the fixture since that deletes automatically.
        invoice = CustomerInvoiceDraft(customer_id=customer.id,
                                       invoice_customer_name='test_name',
                                       invoice_postal_code='25269',
                                       invoice_city='Helsingborg',
                                       customer_is_private_person=False)
        invoice.save()

        invoice_id = invoice.id

        invoice_to_delete = CustomerInvoiceDraft.objects.get(invoice_id)

        invoice_to_delete.delete()

        with pytest.raises(VismaAPIException):
            check_deleted = CustomerInvoiceDraft.objects.get(invoice_id)





class TestCustomerInvoiceDrafts:

    def test_get_all_customer_invoice_drafts(self):
        """should not raise exception"""
        invoices = CustomerInvoiceDraft.objects.all()
