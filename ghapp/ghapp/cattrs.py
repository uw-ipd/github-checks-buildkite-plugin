import typing

import attr
import cattr

def _register_ignore_unknown_attribs(cls, converter=None):
    if converter is None:
        converter = cattr.global_converter

    if not attr.has(cls):
        raise TypeError("class does not have attrs: %s" % cls)

    prev_structure = converter._structure_func.dispatch(cls)
    attr_names = {f.name for f in attr.fields(cls)}

    def structure_ignoring_unknown(obj, cls):
        obj = obj.copy()
        for k in set(obj.keys()).difference(attr_names):
            del obj[k]
        return prev_structure(obj, cls)

    converter.register_structure_hook(cls, structure_ignoring_unknown)

def ignore_unknown_attribs(maybe_cls = None, converter=None):
    """Register a "tolerant" cattr.structure overload for the classk."""
    def bound(cls):
        _register_ignore_unknown_attribs(cls, converter = converter)
        return cls

    if maybe_cls:
        return bound(maybe_cls)
    else:
        return bound

def _register_ignore_optional_none(cls, converter=None):
    if converter is None:
        converter = cattr.global_converter

    if not attr.has(cls):
        raise TypeError("class does not have attrs: %s" % cls)

    prev_unstructure = converter._unstructure_func.dispatch(cls)
    optional_attrs = {
        f.name for f in attr.fields(cls)
        if isinstance(f.type, typing._Union) and type(None) in f.type.__args__
    }

    def unstructure_ignoring_optional_none(obj):
        unstructured = prev_unstructure(obj)

        for a in optional_attrs:
            if a in unstructured and unstructured[a] is None:
                del unstructured[a]
        return unstructured

    converter.register_unstructure_hook(cls, unstructure_ignoring_optional_none)

def ignore_optional_none(maybe_cls = None, converter=None):
    def bound(cls):
        _register_ignore_optional_none(cls, converter)
        return cls

    if maybe_cls:
        return bound(maybe_cls)
    else:
        return bound
