import pytest

import proq


def test_proq_create_collect():
    assert proq.create([0, 1, 2, 3]).collect() == [0, 1, 2, 3]


def test_proq_create_map_collect():
    assert proq.create([0, 1, 2, 3]).map(lambda x: x + 1).collect() == [1, 2, 3, 4]


def test_proq_create_foreach_collect():
    array = []
    assert proq.create([0, 1, 2, 3]).foreach(array.append).collect() == array
    assert array == [0, 1, 2, 3]


def test_proq_create_filter_collect():
    assert proq.create([0, 1, 2, 3]).filter(lambda x: x % 2 == 0).collect() == [0, 2]


def test_proq_create_reduce_collect():
    assert proq.create([0, 1, 2, 3]).reduce(lambda x, y: x + y).collect() == [6]


def raise_foo(*args):
    raise Exception("foo")


def test_proq_map_is_lazy():
    p = proq.create([1, 2]).map(raise_foo)
    with pytest.raises(Exception, match="foo"):
        p.collect()


def test_proq_foreach_is_lazy():
    p = proq.create([1, 2]).foreach(raise_foo)
    with pytest.raises(Exception, match="foo"):
        p.collect()


def test_proq_filter_is_lazy():
    p = proq.create([1, 2]).filter(raise_foo)
    with pytest.raises(Exception, match="foo"):
        p.collect()


def test_proq_reduce_is_lazy():
    p = proq.create([1, 2]).reduce(raise_foo)
    with pytest.raises(Exception, match="foo"):
        p.collect()
