from dataclasses import dataclass
import pytest
from pysh.core.streams.stream import Stream


def test_len(subtests):
    for stream, expected in [
        (Stream(), 0),
        (Stream([]), 0),
        (Stream([1, 2, 3]), 3),
    ]:
        with subtests.test(
            stream=stream,
            expected=expected,
        ):
            assert len(stream) == expected


def test_empty(subtests):
    for stream, expected in [
        (Stream(), True),
        (Stream([]), True),
        (Stream([1, 2, 3]), False),
    ]:
        with subtests.test(
            stream=stream,
            expected=expected,
        ):
            assert stream.empty() == expected


def test_head(subtests):
    for stream, expected in [
        (Stream(), None),
        (Stream([]), None),
        (Stream([1, 2, 3]), 1),
    ]:
        with subtests.test(
            stream=stream,
            expected=expected,
        ):
            if expected is None:
                with pytest.raises(Stream.EmptyError):
                    stream.head()
            else:
                assert stream.head() == expected


def test_tail(subtests):
    for stream, expected in [
        (Stream(), None),
        (Stream([]), None),
        (Stream([1]), Stream()),
        (Stream([1, 2, 3]), Stream([2, 3])),
    ]:
        with subtests.test(
            stream=stream,
            expected=expected,
        ):
            if expected is None:
                with pytest.raises(Stream.EmptyError):
                    stream.tail()
            else:
                assert stream.tail() == expected


def test_tail_with_type():
    class _Stream(Stream): ...

    assert _Stream([1, 2, 3]).tail() == _Stream([2, 3])
