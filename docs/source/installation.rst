.. _installation

Installation
============

Using the library requires Python 3.6 or higher

.. code-block:: python

    pip install visma


Access to Visma API
===================

After installation you will need to set up access to the Visma E-Accounting API

As of now it is not possible to get access by yourself so you will need to contact
Visma at eaccountingapi@visma.com. When you contact them request redirect URI to
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

Environment Variables
=====================

To set up the API classes you need to supply give your Visma Client ID,
Visma Client Secret and the path to the tokens you saved before.

These settings are now supplied via the environment variables:

* VISMA_API_CLIENT_ID
* VISMA_API_CLIENT_SECRET
* VISMA_API_TOKEN_PATH

If you are using the test environment supplied from Visma API Team you need to
add the environment variable VISMA_API_ENV=test so that the paths are set up properly.
