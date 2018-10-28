import pytest

from visma.models import VatReport


class TestVatReport:

    @pytest.fixture()
    def vat_report(self):

        yield VatReport.objects.all().first()

    def test_list_vat_reports(self):

        vat_reports = VatReport.objects.all()

        assert len(vat_reports) is not 0

    def test_get_vat_report(self, vat_report):

        to_compare_report = VatReport.objects.get(vat_report.id)

        assert to_compare_report.id == vat_report.id