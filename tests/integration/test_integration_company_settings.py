import pytest
import datetime
from visma.models import CompanySettings



class TestCompanySettings:

    def test_list_company_settings(self):
        company_settings = CompanySettings.objects.all().first()

        assert company_settings.name is not None

    def test_update_company_settings(self):

        company_settings = CompanySettings.objects.all().first()

        address1 = 'test' + datetime.datetime.now().isoformat()

        company_settings.address1 = address1

        company_settings.save()

        updated_company_settings = CompanySettings.objects.all().first()

        assert updated_company_settings.address1 == address1

