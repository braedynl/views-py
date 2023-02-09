# Changelog

## v2.0.0

### Some Reorganization

After working with my own library for some time, it became clear to me that there may be scenarios in which a window can be undesirable in an effort to conserve time and memory. Thus, a decision to *split* the `View` class of version 1.0.0 was made - and with it, comes some reorganization.

The abstract base class, `SequenceView`, has been renamed to `SequenceViewLike`.

A new type of sequence view, `SequenceView`, has been added. It's almost identical to the [`SequenceView` class of the more-itertools library](https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.SequenceView), except that it produces a windowed view for `slice` indices.

The windowed sequence viewer, `View`, has been renamed to `SequenceWindow`, and derives from `SequenceView`. Its behavior remains mostly the same.

### Miscellaneous

- Enhanced backwards compatibility for Python 3.9.
- `SequenceViewLike` (formerly, `SequenceView`) is now [slotted](https://docs.python.org/3/reference/datamodel.html#slots) - this was an unintentional omission in version 1.0.0.
- `SequenceWindow` (formerly, `View`) may now compare equal with instances of `SequenceView` due to its new inheritance structure.
- Misc. changes to class/function docstrings throughout.

### Migration from v1.0.0

You may safely replace the following names in your code:
- `SequenceView -> SequenceViewLike`
- `View -> SequenceWindow`

That's it!

If you need a view on a *whole* sequence (that is, without the omission of *any* elements), using an instance of the new `SequenceView` class is recommended. This class conserves much more time and memory over its `SequenceWindow` relative.

## v1.0.0

First official version of Views-Py.
