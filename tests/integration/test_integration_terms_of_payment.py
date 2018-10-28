import pytest

from visma.api import VismaClientException
from visma.models import TermsOfPayment


class TestTermsOfPayment:

    def test_get_termsofpayment(self):
        top = TermsOfPayment.objects.all()
        assert len(top) > 0

    def test_no_update_allowed(self):
        with pytest.raises(VismaClientException):
            top = TermsOfPayment.objects.all()[0]
            top.number_of_days = 20
            top.save()
