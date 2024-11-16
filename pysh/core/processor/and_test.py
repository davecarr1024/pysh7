from pysh.core.processor.literal import Literal


def test_and(subtests):
    for rule, expected in [
        (Literal(1) & Literal(2), [1, 2]),
        (Literal(1) & Literal(2) & Literal(3), [1, 2, 3]),
        ((Literal(1) & Literal(2)) & Literal(3), [1, 2, 3]),
        (Literal(1) & (Literal(2) & Literal(3)), [1, 2, 3]),
        ((Literal(1) & Literal(2)) & (Literal(3) & Literal(4)), [1, 2, 3, 4]),
    ]:
        with subtests.test(rule=rule, expected=expected):
            assert rule(None).result == expected
