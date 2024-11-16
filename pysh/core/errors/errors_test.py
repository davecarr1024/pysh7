from dataclasses import dataclass

from pysh.core.errors import Error, Errorable


def test_error():
    object = Errorable()
    assert object._error(
        msg="a msg",
    ) == Error(
        object=object,
        msg="a msg",
    )


def test_custom_type():
    @dataclass(
        frozen=True,
        kw_only=True,
        repr=False,
    )
    class _Error(Error):
        value: int

    object = Errorable()
    error_: _Error = object._error(
        type=_Error,
        value=1,
        msg="a msg",
    )
    assert error_ == _Error(
        object=object,
        value=1,
        msg="a msg",
    )


def test_try():
    object = Errorable()

    def f() -> None:
        raise object._error(msg="inner error")

    try:
        object._try(f, msg="outer error")
    except Error as e:
        assert e == object._error(
            msg="outer error",
            children=[
                object._error(
                    msg="inner error",
                ),
            ],
        )
    else:
        raise AssertionError("failed to throw")
