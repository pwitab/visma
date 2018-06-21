REST-ORM Framework
==================

Part of the client library might be suitable to break out into a separate
framework for building ORM clients to different API:s

We try to not couple the functions to hard to the Visma e-Accounting API.

Inspiration
-----------

When looking at the Visma e-Accouting API with the use of OData as filtering
query parameters it looks very much like accessing a database. Just over HTTP
REST. Normally in Python applications you have an ORM to access a database which
usually looks like:

>>> Model.objects.all()  # Django

We have written many integration where we just have a class that uses request to
get the relevant recource and parse the JSON into a dict for further processing.
To do this on this enrire API would be annoying. Especially since the Visma
e-Accounting API uses Pascal casing in their JSON.

So first we looked around for something to handle the Pascal to snake-case
serializing and found marshmallow. It did the job well but we had alot of
duplicate code when we wanted to parse data that looked exactly like our python
objects.

So with some inspiration from how Django hadles Model creation we made a
Metaclass that will use Marshmallow fields to generate a Python object with a
simmilar Marshmallow Schema attached.

Models
------

Models inherit from VismaModel.

.. code-block:: python

    MyClass(VismaModel):
        id = field.UUID()
        name = field.String()

Model Meta
----------

To set up how the class interacts with the API we specify the model meta

endpoint
    Specifies the main enpoint for a class.
allowed_methods
    Specifies the allowed methods on the class.
envelopes
    Specifies how to handle enveloped schemas on endpoints.


Endpoints and methods
---------------------

We assume for now that one is following normal REST API behaviour. We have some
thoughts on how in add specific handling but we have not had time to test other
more important features

If you specify and endpoint for example /customer, you will get the following
behaviour

list
    accessible via .all(). Does a get and get everything from /customers
get
    given an id it will do a GET on /customers/{id}
create
    if no id is set on the model it will POST to /customers to create the object on .save()
update
    if id is set on the model it will PUT to /customers/{id} to update the object on .save()
delete
    can be called on the object or on the model with an id to issue a DELETE to /customers/{id}

Some API endpoint does not have support of all methods so you have to list them in the Meta as a list.

Enveloped Schemas
-----------------

When communicating with an API the data sent might be more than the data you want to get or change.
For example getting a list of resources on an endpoint that supports pagination you might get meta data like number of pages and current page in a metadata section.

By defining a model for the outer data it is possible to handle this in a simple way by adding the envelope settings in the Meta data of the classes that uses envelope.

.. code-block:: python

    class PaginatedResponse(VismaModel):
        meta = fields.Nested('PaginationMetadataSchema', data_key='Meta')


    class PaginationMetadata(VismaModel):
        current_page = fields.Integer(data_key='CurrentPage')
        page_size = fields.Integer(data_key='PageSize')
        total_number_of_pages = fields.Integer(data_key='TotalNumberOfPages')
        total_number_of_results = fields.Integer(data_key='TotalNumberOfResults')
        server_time_utc = fields.DateTime(data_key='ServerTimeUtc')

    class Customer(VismaModel):
        name = fields.String(data_key='Name')

        class Meta:
            endpoint = '/customers'
            allowed_methods = ['list', 'create', 'delete']
            envelopes = {'list': {'class': PaginatedResponse,
                                  'data_attr': 'Data'}}

This will allow the following data response to return an object of Customer.

.. code-block:: bash

    {'Data': [{'Name': 'Customer-Name'},],
     'Meta': {'CurrentPage': 1,
              'PageSize': 50,
              'ServerTimeUtc': '2018-06-21T16:23:13.1083743Z',
              'TotalNumberOfPages': 1,
              'TotalNumberOfResults': 37}}




