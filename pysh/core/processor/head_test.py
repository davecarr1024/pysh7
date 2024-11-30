from pysh.core.processor.head import Head
from pysh.core.streams.stream import Stream


def test_head():
    assert Head()(Stream([1, 2, 3])) == (Stream([2, 3]), 1)
