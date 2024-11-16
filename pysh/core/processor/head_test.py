from pysh.core.processor.head import Head
from pysh.core.processor.state_and_result import StateAndResult
from pysh.core.streams.stream import Stream


def test_head():
    assert Head()(Stream([1, 2, 3])) == StateAndResult(Stream([2, 3]), 1)
