==================
``query-selector``
==================

.. image:: https://travis-ci.org/solidsnack/query-selector.svg?branch=master
    :target: https://travis-ci.org/solidsnack/query-selector

Query selector allows one treat a file full of SQL queries as a record, with
one attribute for each annotated query. This makes working with long, ad-hoc
SQL queries more hygienic, and has the benefit of making it easy to find the
queries.

The ``QuerySelector`` constructor accepts a string, file handle or
``(<package>, <resource)`` pair and parses the SQL into groups annotated with
``--@ <name> <mode>``. The ``<name>`` is any Python compatible name; it will
become an attribute of the object. The ``<mode>`` is merely metadata, and can
be omitted; it describes whether a query should have one, none or many
results.

For example, a file like this:

.. code:: sql

    --@ t one
    SELECT * FROM now();

becomes an object with a single attribute ``t``:

.. code::

    >>> q.t
    Query(args=[], mode=u'one', text=u'SELECT * FROM now();')

