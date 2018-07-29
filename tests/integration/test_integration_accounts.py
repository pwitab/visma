import pytest

from visma.models import Account, FiscalYear


class TestCRUDAccount:

    @pytest.fixture()
    def fiscal_year_id(self):
        fiscal_year = FiscalYear.objects.all()[0]  # last one

        yield fiscal_year.id

    def test_create_account(self, fiscal_year_id):
        # account = Account(name='Test Account', number='6668',
        #                   fiscal_year_id=fiscal_year_id)
        #
        # account.save()
        #
        # assert account.modified_utc is not None

        # After a tests has been done the account is available in eAccounting
        # and we can't delete it. So better not to run these tests all the time.
        # TODO: Can we set up a case where we clean the Sandbox completely and mark the tests that can only be run on a clean environment?
        pass

    def test_read_account(self):
        # TODO: needs a way of handling adding the fiscal year in the url.
        # TODO: needs a way of having another field be pk.
        pass

    def test_update_account(self):
        # Not allowed
        # TODO: Should raise Exception
        pass

    def test_delete_account(self):
        # Not allowed
        # TODO: Should raise Exception
        pass

    def test_list_accounts(self):

        accounts = Account.objects.all()

        assert len(accounts) is not 0
