from visma.models import TermsOfPayment, CustomerInvoiceDraft


def test_customer_model_has_manager():

    from visma.manager import Manager

    terms_o_p = TermsOfPayment(name='test_terms_of_payment')

    obj = getattr(terms_o_p, 'objects', None)

    assert obj is not None
    assert isinstance(obj, Manager)

    assert issubclass(terms_o_p.objects.model, TermsOfPayment)


def test_model_endpoint():

    terms_o_p = TermsOfPayment(name='test_terms_of_payment')

    obj = getattr(terms_o_p, 'objects', None)

    assert obj.endpoint == '/termsofpayment'



# TODO: test allowed methods. But how to do it without API access? Maybe need to mock the api?