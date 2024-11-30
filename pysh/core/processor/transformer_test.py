from pysh.core.processor.literal import Literal
from pysh.core.processor.transformer import transformer


def test_transformer():
    assert Literal(1).transform(str)(None) == (None, "1")
