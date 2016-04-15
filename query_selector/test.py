from query_selector import QuerySelector


def test_not_crashing():
    QuerySelector(('query_selector', 'example.sql'))


def test_finds_args():
    q = QuerySelector(('query_selector', 'example.sql'))
    assert 'farm' in q.get_farm.args
