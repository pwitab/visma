import pytest

from visma.models import Country


class TestCountry:

    def test_list_county(self):
        countries = Country.objects.all()

        assert len(countries) is not 0


