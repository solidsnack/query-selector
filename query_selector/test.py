from query_selector import QuerySelector


def test_not_crashing():
    QuerySelector(('query_selector', 'example.sql'))


def test_finds_args():
    q = QuerySelector(('query_selector', 'example.sql'))
    assert 'farm' in q.get_farm.args


def test_modes():
    q = QuerySelector(('query_selector', 'example.sql'))
    assert q.get_farm.mode == 'one?'
    assert q.get_farm.readonly
    assert q.farms.mode == 'many'
    assert q.farms.readonly


def test_order():
    q = QuerySelector(('query_selector', 'example.sql'))
    names = list(name for name, _ in q)
    assert names[:3] == ['init', 'ready', 'make_tables']
