from pysh.core.processor.state_and_result import StateAndResult
from pysh.core.processor.state_exractor import state_extractor


def test_extractor():
    assert state_extractor(str)(1) == StateAndResult(1, "1")
