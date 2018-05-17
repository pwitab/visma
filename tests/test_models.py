from visma.models import TermsOfPayment, CustomerInvoiceDraft


def test_customer_model_has_manager():

    from visma.models import Manager

    terms_o_p = TermsOfPayment(name='test_terms_of_payment')

    obj = getattr(terms_o_p, 'objects', None)

    assert obj is not None
    assert isinstance(obj, Manager)

    assert issubclass(terms_o_p.objects.model, TermsOfPayment)


def test_model_endpoint():

    terms_o_p = TermsOfPayment(name='test_terms_of_payment')

    obj = getattr(terms_o_p, 'objects', None)

    assert obj.endpoint == '/termsofpayment'

def test_model_schema():

    from visma.schemas import TermsOfPaymentSchema
    terms_o_p = TermsOfPayment(name='test_terms_of_payment')

    obj = getattr(terms_o_p, 'objects', None)

    assert issubclass(obj.schema, TermsOfPaymentSchema)


