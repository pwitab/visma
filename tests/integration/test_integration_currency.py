import pytest

from visma.models import Currency


class TestCurrency:

    def test_list_currency(self):
        curr = Currency.objects.all()

        assert len(curr) is not 0


