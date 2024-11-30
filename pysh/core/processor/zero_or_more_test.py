from pysh.core.processor.head import Head
from pysh.core.streams.stream import Stream


def test_zero_or_more(subtests):
    for stream, expected in [
        (Stream(), []),
        (Stream([1]), [1]),
        (Stream([1, 2, 3]), [1, 2, 3]),
    ]:
        with subtests.test(stream=stream, expected=expected):
            assert Head().zero_or_more()(stream) == (Stream(), expected)
