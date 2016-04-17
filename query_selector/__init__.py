"""Treat an annotated SQL file as a module of queries.

In the SQL file, every block that is marked with ``--@ <name> <mode>`` is
treated as a distinct query. The blocks may be any number of SQL statements.
For example:

.. code:: sql

    --@ server_time one
    SELECT now();

If the blocks contain ``%()s`` style interpolation, these parameters are
recognized and provided as metadata.

The ``<name>`` should be a valid Python function name, the ``<mode>`` should
be one of:

``none``
    Indicates there should never be any result rows. The return value is `None`
    or an assertion error is thrown.

``one?``
    Indicates there should be one or zero result rows. A single row or `None`
    is returned.

``one``
    Indicates there should always be one result row. A single row is returned
    or an assertion error is thrown.

``many``
    Indicates there may be multiple rows returned. An array (possibly empty) of
    rows is returned.

"""
from collections import namedtuple
import pkg_resources
import re

from oset import oset
import six
import sqlparse
from sqlparse.sql import Comment


class QuerySelector(object):
    """A collection of queries drawn from a SQL file.

    The queries are available as attributes. This class also provides an
    iterable instance, allowing the queries to be iterated over in the order
    they appear in the file.
    """
    def __init__(self, source):
        """
        :param source: A string, file-like object or ``(package, resource)``
                       pair that contains SQL text.
        :type  source: str | stream | (str, str)
        """
        parsed = obtain_sql(source)
        grouped = group_queries(parsed)
        translated = translate_query_signatures(grouped)
        self._queries = [(name, Query(args, mode, ro, text))
                         for name, args, mode, ro, text in translated]
        for name, val in self._queries:
            setattr(self, name, val)

    def __iter__(self):
        return iter(self._queries)


modes = set(['none', 'one?', 'one', 'many'])

signature = re.compile('^--@ ([a-zA-Z_][a-zA-Z0-9_]*)'
                       '( +([a-z][a-z][a-z]+[?]?))?( +(ro))? *')


class Query(namedtuple('Query', 'args mode readonly text')):
    """Contains the query text, mode string and the names of any ``%()s``
       parameters.
    """
    pass


def translate_query_signatures(grouped):
    for query_name, mode, ro, text in grouped:
        yield query_name, percent_expansions(text), mode, ro, text


def group_queries(statements):
    tokens = [token for statement in statements for token in statement.tokens]
    current = None
    mode = None
    group = ''
    readonly = False
    for token in tokens:
        if isinstance(token, Comment) and token.value.startswith('--@ '):
            if current is not None:
                yield current, mode, readonly, group.rstrip()
            match = signature.match(token.value)
            if not match:
                continue
            group = ''
            current, _, modestring, _, ro = match.groups()
            readonly = not not ro
            mode = modestring or 'many'
            assert mode in modes
            continue
        if current is None:
            continue
        group += str(token)
    yield current, mode, readonly, group.rstrip()


def obtain_sql(source):
    if isinstance(source, tuple):
        pkg, name = source
        return sqlparse.parse(pkg_resources.resource_stream(pkg, name))
    if isinstance(source, six.string_types):
        return sqlparse.parse(source)
    if isinstance(source, six.binary_type):
        return sqlparse.parse(source)
    with source as h:
        return sqlparse.parse(h.read())


def percent_expansions(text):
    references = oset(param_reference.findall(text))
    return [s.split('(')[1].split(')')[0] for s in references]


# Recognize ``%(param)s`` style references specified by Python's DBI 2.0
param_reference = re.compile('%[(][a-zA-Z_][a-zA-Z0-9_]*[)]s')
