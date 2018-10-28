import pytest
import iso8601

from visma.models import FiscalYear


class TestCRUDFiscalYear:

    @pytest.fixture()
    def fiscal_year_id(self):
        fiscal_year = FiscalYear.objects.all()[0]
        yield fiscal_year.id

    def test_create_fiscal_year(self):
        # START_DATE = iso8601.parse_date('2020-01-01')
        # END_DATE = iso8601.parse_date('2020-12-31')
        #
        # fiscal_year = FiscalYear(start_date=START_DATE, end_date=END_DATE)
        # fiscal_year.save()
        #
        # assert fiscal_year.id is not None

        # As we cannot delete a fiscal year. Adding it to the tests we would
        # need to keep on adding new fiscal years since they are not allowed
        # to be overlapping and you have to create them adjacent to another
        # fiscal year.
        pass

    def test_read_fiscal_year(self, fiscal_year_id):
        fiscal_year = FiscalYear.objects.get(fiscal_year_id)

        assert fiscal_year.id == fiscal_year_id

    def test_update_fiscal_year(self):
        # Not allowed
        # TODO: Should raise Exception
        pass

    def test_delete_fiscal_year(self):
        # Not allowed
        # TODO: Should raise Exception
        pass

    def test_list_fiscal_year(self):

        fiscal_years = FiscalYear.objects.all()

        assert len(fiscal_years) is not 0



