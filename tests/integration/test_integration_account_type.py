import pytest

from visma.models import AccountType


class TestAccountTypes:

    def test_list_account_types(self):

        account_types = None

        account_types = AccountType.objects.all()

        assert account_types is not None