from pysh.core.processor.literal import Literal


def test_literal():
    assert Literal(1)(None) == (None, 1)
