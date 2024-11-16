from dataclasses import dataclass


@dataclass(frozen=True)
class StateAndResult[State, Result]:
    state: State
    result: Result
