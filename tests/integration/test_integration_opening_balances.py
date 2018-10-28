import pytest

from visma.models import OpeningBalances


class TestOpeningBalances:

    def test_list_opening_balances(self):

        ob = OpeningBalances.objects.all()

        assert len(ob) is not 0
