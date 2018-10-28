.. _usage:


Using the library
=================


Create object
-------------

You create object as you would normally in Python. To save the data in Visma you
need to call the .save() method

.. code-block:: python

    customer = Customer(
            invoice_city='Helsingborg',
            invoice_postal_code='25234',
            name='TestCustomer AB',
            terms_of_payment_id='8f9a8f7b-5ea9-44c6-9725-9b8a1addb036',
            is_private_person=False,
            is_active=True)

    customer.save()

Get objects
-----------

You can query the object endpoint by going via the manger on the object.

.. code-block:: python

   customers = Customer.objects.all()

If you just want a specific object that you know the primary key for you can use the .get()

.. code-block:: python

   customer = Customer.objects.get('8f9a8f7b-5ea9-44c6-9725-9b8a1addb036')

Update object
-------------

When updating an object you just need to get the object, make changes and save.

.. code-block:: python

   customer = Customer.objects.get('8f9a8f7b-5ea9-44c6-9725-9b8a1addb036')
   customer.name = 'New Name'
   customer.save()

Delete object
-------------

You can issue a delete on a collected object or use the .delete on the manager
if you know whe primary key.

.. code-block:: python

   customer = Customer.objects.get('8f9a8f7b-5ea9-44c6-9725-9b8a1addb036')
   customer.delete()

   # or

   Customer.objects.delete('8f9a8f7b-5ea9-44c6-9725-9b8a1addb036')

Filter objects
--------------

You can filter result on the API-side using .filter() and .exclude(). They are chainable so you can combine them.

.. code-block:: python

   # You don't need to use the .all()
   customers = Customer.objects.all().filter(name='Dave')
   # is the same as:
   customers = Customer.objects.filter(name='Dave')

   # You can combine filter and exclude
   customers = Customer.objects.filter(name='Dave').exclude(customer_number='1337').filter(delivery_invoice_country='Sweden')

Filtering functions
^^^^^^^^^^^^^^^^^^^

There are some special filtering functions that can be used. They can be used
in both .filter() and .exclude(). When using filtering functions in exclude
they are handled as the inverse of what would be included using .filter()

exact
    using {arg}__exact is the same as just suppling the arg.
    Ex name__exact='Dave' or name='Dave'. It will handle paramaters that match
    exactly.
not
    using {arg}_not will match to anything but the supplied value.
    (opposite to exact)
greater than
    using the {arg}__gt argname will translate into filter where greater than
    the supplied value.
greater than or equal
    using {args}__gte will translat into filter where greater than or equal the
    supplied value
less than
    using the {arg}__lt argname will translate into filter where less than
    the supplied value.
less than or equal
    using {args}__lte will translat into filter where less than or equal the
    supplied value

.. code-block:: python

    customers = Customer.objects.filter(name__not='Dave').exclude(invoice_zip_code__gte=27000)

    #querysets are lazy and can be changed until it has been evaluated.

    customers.filter(customer_number__lt=4).filter(invoice_country='Sweden)


Order by
--------

You can order result. To supply what arg you want the result to be ordered by
use .order_by(). Ex .order_by(name)

.. code-block:: python

    customers = Customer.objects.all().order_by(name)


Get first object
----------------

If you are interested in the first object of a result you can use normal list
handling of result[0] but you can also use the function .first() to make it
a bit more clear and so that the queryset retuns an object instead of a list of
objects.

.. code-block:: python

    customer = Customer.objects.filter(customer_number=1337).first()

