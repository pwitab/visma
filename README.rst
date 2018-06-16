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

The api is inspired from the Django ORM. The Visma API is well documented and
supports filtering according to Odata which makes the operations very similar
to database access. We want to be able interact with all objects as normal python objects


.. code-block:: python

    customers = Customer.objects.all()

    invoice = CustomerInvoiceDraft.objects.get('e629baaf-642b-4079-9180-1b8463d24dc2')
    invoice.your_reference = 'Mr finance guy'
    invoice.save()

    invoice2 = CustomerInvoiceDraft.objects.get('ff9839do-642b-4079-9180-1b8463d24dc2')
    invoice2.delete()

    # or

    CustomerInvoiceDraft.objects.delete('ff9839do-642b-4079-9180-1b8463d24dc2')


Supported functions:
    * Getting all objects
    * Getting single object
    * Saving new objects and updating existing via .save()
    * Deleting objects

Todo:
    * filtering via Odata parameters, should be similar to Django QuerySets
    * manage pagination


Available Objects
-----------------
Some objects we use and have tried out. But other code is made from generating
marshmallow schemas with `swagger-marshmallow-codegen
<https://github.com/podhmo/swagger-marshmallow-codegen/>`_.
We have not tried all of it since we wont have the use cases.
We would be happy to receive some comments if something is not working.

Tested
^^^^^
* Customer
* TermsOfPayment
* CustomerInvoiceDraft

Documentation
=============
Full documentation can be found at https://visma.readthedocs.io/ .


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
