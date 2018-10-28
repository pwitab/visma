import pytest

from visma.models import Unit


class TestUnit:

    @pytest.fixture()
    def unit(self):

        yield Unit.objects.all().first()

    def test_list_units(self):

        units = Unit.objects.all()

        assert len(units) is not 0

    def test_get_unit(self, unit):

        to_compare_unit = Unit.objects.get(unit.id)

        assert unit.id == to_compare_unit.id