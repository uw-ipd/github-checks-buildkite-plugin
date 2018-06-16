import pytest
import attr
import cattr

from typing import Optional, Union

from ..cattrs import ignore_unknown_attribs, ignore_optional_none


def test_ignore_unknown_attribs():
    standard = cattr.global_converter
    custom = cattr.Converter()

    @ignore_unknown_attribs(converter=custom)
    @attr.s(auto_attribs=True)
    class Foo:
        bar: int

    nofoo = dict()
    foo = {"bar": 1}
    fooplus = {"bar": 1, "bat": 2}

    with pytest.raises(TypeError):
        standard.structure(nofoo, Foo)
    assert Foo(1) == standard.structure(foo, Foo)
    with pytest.raises(TypeError):
        standard.structure(fooplus, Foo)

    with pytest.raises(TypeError):
        custom.structure(nofoo, Foo)
    assert Foo(1) == custom.structure(foo, Foo)
    assert Foo(1) == custom.structure(fooplus, Foo)


def test_ignore_optional_none():
    standard = cattr.global_converter
    custom = cattr.Converter()

    @ignore_optional_none(converter=custom)
    @attr.s(auto_attribs=True)
    class Foo:
        a: int
        b: Optional[int]
        c: Union[str, int, None]
        d: Union[str, int]

    assert standard.unstructure(Foo(1, 2, 3, 4)) == dict(a=1, b=2, c=3, d=4)
    assert standard.unstructure(Foo(None, 2, 3, 4)) == dict(
        a=None, b=2, c=3, d=4)
    assert standard.unstructure(Foo(1, None, 3, 4)) == dict(
        a=1, b=None, c=3, d=4)
    assert standard.unstructure(Foo(1, 2, None, 4)) == dict(
        a=1, b=2, c=None, d=4)
    assert standard.unstructure(Foo(1, 2, 3, None)) == dict(
        a=1, b=2, c=3, d=None)

    assert custom.unstructure(Foo(1, 2, 3, 4)) == dict(a=1, b=2, c=3, d=4)
    assert custom.unstructure(Foo(None, 2, 3, 4)) == dict(
        a=None, b=2, c=3, d=4)
    assert custom.unstructure(Foo(1, None, 3, 4)) == dict(a=1, c=3, d=4)
    assert custom.unstructure(Foo(1, 2, None, 4)) == dict(a=1, b=2, d=4)
    assert custom.unstructure(Foo(1, 2, 3, None)) == dict(
        a=1, b=2, c=3, d=None)
