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
    SELECT now();

becomes an object with a single attribute ``t``:

.. code:: pycon

    >>> q.t
    Query(args=[], mode=u'one', readonly=False, text=u'SELECT * FROM now();')

A ``QuerySelector`` object is iterable, providing pairs of name and query in
the order that the queries originally appeared in the file.

.. code:: pycon

    >>> for name, q in qs:
    ...     print '%s: %s' % (name, q)
    t: Query(args=[], mode=u'one', readonly=True, text='SELECT now();')

--------------------
The Query Convention
--------------------

If you have a script `task.py` and a SQL file `task.sql`, or a module in a
package `package/module.py` and a SQL file `package/module.sql`, QuerySelector
has a shortcut for you:

.. code:: python

    from query_selector.magic import queries


    for q in queries:
        print q

The ``magic`` module overrides the normal module loading machinery to
determine which script or module is importing it and locate an adjacent SQL
file. This magic is in a separate module to make it stricly opt-in!

-----
Modes
-----

Modes can be one of ``none``, ``one``, ``one?`` and ``many``. When not
specified, default is ``many``. A mode string can also be followed with the
single word ``ro`` as a clue that the query is read-only.

Realistically, ``SELECT now()`` is a read-only query. We can annotate it as
such, the resulting query datastructure records this:

.. code:: pycon

    >>> QuerySelector("""
    ...   --@ t one ro
    ...   SELECT now();
    ... """).t
    Query(args=[], mode=u'one', readonly=True, text=u'SELECT * FROM now();')

----------
Parameters
----------

``query-selector`` recognizes the ``%(...)s`` style parameter references
defined in Python DBI 2.0. Say that we'd like to pass a timezone
when selecting the server time. We can do so by adding ``AT TIME ZONE %(tz)s``
to our query. The presence of this parameter is stored in the ``args`` field
of the parsed result. (The parameters in ``.args`` are listed in the order of
their first appearance in the query.)

.. code:: pycon

    >>> QuerySelector("""
    ...     --@ t one ro
    ...     SELECT now() AT TIME ZONE %(tz)s AS t;
    ... """).t
    Query(args=[u'tz'], mode=u'one', readonly=True,
          text=u'SELECT now() AT TIME ZONE %(tz)s AS t;')
