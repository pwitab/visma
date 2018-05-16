=====
Visma
=====

A Python Client library for integration to Visma e-Accounting, Visma e-Ekonomi

Installation
============

.. code-block:: python

    pip install visma


After installation you will need to set up access to the Visma E-Accounting API

As of now it is not possible to get access by yourself so you will need to contact
Visma at eaccountingApi@visma.com. When you contact them request redirect URI to
/redirect_receiver

They will first set up an account in their sandbox environment for you and after
you have tested you use cases you can request an account in the Visma Production
Environment

The focus of the library as of now is to be used in a command line tool for
generating invoices from data from our time reporting system. In the future we
might extend it to be a Django App.

Since we are focusing on command line tooling we run in to some "problems" with
authentication since Visma is using OAuth2. This requires you to go through a
website to get an access code and verify access rights in the Visma API.

We provide an entry point to open the correct webpage

.. code-block:: bash

    visma request_access  --client <client_id>

This will open a webpage where you log in and grant access to the application.
After you click OK you will be redirected to the /redirect_receiver url. You
need to take the code in the url and use it to feed into the authenticate
function

.. code-block:: bash

    visma get_token --code <auth_code> --client <client_id> --secret <client_secret> > /path/to/auth.json


This will return an access token and a renew token that will be used by the
client to make authenticated requests to the Visma API.

Using the library
=================

As of now we only implement a few features via simple methods on the API class

.. code-block:: python

    from visma.api import VismaAPI
    from visma.models import CustomerInvoiceDraft

    api = VismaAPI(token_path='path/to/auth.json', client_id='my_client_id', client_secret='my_client_secret', test=True)

    company_settings = api.get_company_settings()

    customer = api.get_customer(1)

    invoice = CustomerInvoiceDraft.with_customer(customer)

    api.new_customer_invoice_draft(invoice)


But this is not the API we want eventually. It isn't that "pythonic" as we see it.
What we would like is an API that is more like an ORM, for example the Django ORM.

.. code-block:: python

    customer = Customer.objects.get(id=1)

    invoice = CustomerInvoiceDraft(customer=customer)
    invoice.add_row(Row('article'))
    invocie.save()

But it is a bit harder to implement. If anyone has good ideas on how to structure it you are welcome to contact us.
We have fiddled a bit with meta classes to inject the API in a simmilar way as Django manager. But the Django managers contain alot of magic.
The visma API supports filtering and other operations via OData so wrapping them in a similar APi as the Django ORM would be very nice.


API reference
=============

https://eaccountingapi.vismaonline.com/swagger/ui/index


Visma Environments
==================

Test (Sandbox)
--------------

Visma eAccounting client
    https://eaccounting-sandbox.test.vismaonline.com
Visma eAccounting API
    https://eaccountingapi-sandbox.test.vismaonline.com/v2
Visma IdentityServer Authorization
    https://identity-sandbox.test.vismaonline.com/connect/authorize
Visma IdentityServer Token
    https://identity-sandbox.test.vismaonline.com/connect/token

Production
----------

Visma eAccounting client
    https://eaccounting.vismaonline.com
Visma eAccounting API
    https://eaccountingapi.vismaonline.com/v2
Visma IdentityServer Authorization
    https://identity.vismaonline.com/connect/authorize
Visma IdentityServer Token
    https://identity.vismaonline.com/connect/token
