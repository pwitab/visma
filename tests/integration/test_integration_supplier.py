import pytest

from visma.api import VismaAPIException
from visma.models import Supplier, ForeignPaymentCodes, TermsOfPayment


class TestSupplier:

    @pytest.fixture()
    def terms_of_payment(self):
        yield TermsOfPayment.objects.all().first()

    @pytest.fixture()
    def foreign_payment_code(self):
        yield ForeignPaymentCodes.objects.all().first()

    @pytest.fixture()
    def supplier(self, terms_of_payment):
        supplier = Supplier(name='test supplier 1',
                            terms_of_payment_id=terms_of_payment.id)

        supplier.save()
        yield supplier
        supplier.delete()

    def test_list_suppliers(self, supplier):
        suppliers = Supplier.objects.all()

        assert len(suppliers) is not 0

    def test_get_supplier(self, supplier):
        to_compare = Supplier.objects.get(supplier.id)

        assert to_compare.id == supplier.id

    def test_create_supplier(self, terms_of_payment):
        supplier = Supplier(name='test supplier 3',
                            terms_of_payment_id=terms_of_payment.id)

        supplier.save()

        assert supplier.id is not None

    def test_update_supplier(self, supplier):
        new_name = 'Update Name'
        supplier.name = new_name
        supplier.save()

        updated_supplier = Supplier.objects.get(supplier.id)

        assert updated_supplier.name == new_name

    def test_delete_supplier(self, terms_of_payment):
        supplier = Supplier(name='test supplier 2',
                            terms_of_payment_id=terms_of_payment.id)

        supplier.save()

        saved_supplier = Supplier.objects.get(supplier.id)
        saved_supplier.delete()

        with pytest.raises(VismaAPIException):
            x = Supplier.objects.get(supplier.id)
