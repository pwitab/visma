=====
Visma
=====

A Python Client/ORM library for integration to Visma e-Accounting, Visma e-Ekonomi

Installation
============

.. code-block:: python

    pip install visma


Access to Visma API
===================

After installation you will need to set up access to the Visma E-Accounting API

As of now it is not possible to get access by yourself so you will need to contact
Visma at eaccountingapi@visma.com.

See full documentation for more info on how to get access and how to set it up.


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
