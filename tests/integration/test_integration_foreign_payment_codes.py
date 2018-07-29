from visma.models import ForeignPaymentCodes


class TestForeignPaymentCodes:

    def test_list_foregin_payment_codes(self):
        codes = ForeignPaymentCodes.objects.all()

        assert len(codes) is not 0
