import pytest

from visma.models import VatCode


class TestCRUDVATCode:

    @pytest.fixture()
    def vat_code_id(self):
        vat_code = VatCode.objects.all()[0]
        yield vat_code.id

    def test_create_vat_code(self):
        # Not allowed
        pass

    def test_read_vat_code(self, vat_code_id):
        vat_code = VatCode.objects.get(vat_code_id)

        assert vat_code.id == vat_code_id

    def test_update_vat_code(self):
        # Not allowed
        # TODO: Should raise Exception
        pass

    def test_delete_vat_code(self):
        # Not allowed
        # TODO: Should raise Exception
        pass

    def test_list_vat_code(self):
        vat_codes = VatCode.objects.all()
        assert len(vat_codes) is not 0



