import pytest

from visma.models import DeliveryTerm


class TestDeliveryTerm:

    @pytest.fixture()
    def term(self):
        yield DeliveryTerm.objects.all().first()

    def test_list_delivery_terms(self):
        terms = DeliveryTerm.objects.all()

        assert len(terms) is not 0

    def test_get_delivery_term(self, term):
        delivery_term = DeliveryTerm.objects.get(term.id)

        assert delivery_term.id == term.id