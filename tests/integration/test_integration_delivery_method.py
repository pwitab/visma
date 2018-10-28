import pytest

from visma.models import DeliveryMethod


class TestDeliveryMethod:

    @pytest.fixture()
    def method(self):
        yield DeliveryMethod.objects.all().first()

    def test_list_delivery_methods(self):

        methods = DeliveryMethod.objects.all()

        assert len(methods) is not 0

    def test_get_delivery_method(self, method):

        delivery_method = DeliveryMethod.objects.get(method.id)

        assert delivery_method.id == method.id