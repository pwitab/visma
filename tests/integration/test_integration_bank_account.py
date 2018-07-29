import datetime

import pytest

from visma.models import Bank, BankAccount


class TestBank:

    def test_list_banks(self):
        banks = Bank.objects.all()

        assert len(banks) is not 0


class TestBankAccount:

    @pytest.fixture()
    def bank(self):
        bank = Bank.objects.all().first()

        yield bank

    @pytest.fixture()
    def bank_account(self):
        bank_account = BankAccount.objects.all().first()

        yield bank_account

    @pytest.fixture()
    def new_bank_account(self, bank):
        account = BankAccount(bank_account_type=3, name='testbankaccount',
                              ledger_account_number=1910, bank=bank.id,
                              is_active=True)
        account.save()
        yield account
        account.delete()

    def test_list_bank_account(self):
        account = BankAccount.objects.all()

        assert len(account) is not 0

    def test_create_bank_account(self, bank):
        # creating a bank account needs a valid account in the correct fiscal year. We cant delete accounts so it is not possible to run the test over and over.
        # Also there is a lot of special rules around bank account that makes it even harder to test.
        # TODO: Can we make a hook before we create an object that allows us to change input data to __init__ so we can apply custom logic? like validate in DRF
        pass

        # account = BankAccount(bank_account_type=3, name='testbankaccount', ledger_account_number=1910, bank=bank.id, is_active=True)
        # account.save()
        #
        # assert account.id is not None
        #
        # account.delete()

    def test_read_bank_account(self, bank_account):
        ba = BankAccount.objects.get(bank_account.id)

        assert ba.id == bank_account.id

    def test_update_bank_account(self, bank_account):
        new_name = datetime.datetime.now().isoformat()[-10:-1]
        bank_account.name = new_name
        bank_account.save()

        assert bank_account.name == new_name

    def test_delete_bank_account(self):
        # done in create?
        pass
