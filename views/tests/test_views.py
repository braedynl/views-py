from unittest import TestCase

from ..views import View

__all__ = ["TestView"]


class TestView(TestCase):
    """Tests for the `View` class

    Most of the `View` class implementation circulates the `subwindow()`
    method. Everything else relies on built-ins.
    """

    def test_subwindow(self):
        target = ['a', 'b', 'c', 'd', 'e']

        view = View(target, window=range(0, len(target), 1))
        self.assertEqual(view.subwindow(), view.window)

        view = View(target, window=range(len(target) - 1, -1, -1))
        self.assertEqual(view.subwindow(), view.window)

        view = View(target, window=range(0, 3, 1))
        self.assertEqual(view.subwindow(), view.window)

        view = View(target, window=range(2, len(target), 1))
        self.assertEqual(view.subwindow(), view.window)

        view = View(target, window=range(-1, -4, -1))
        self.assertEqual(view.subwindow(), view.window)

        view = View(target, window=range(-3, -len(target) - 1, -1))
        self.assertEqual(view.subwindow(), view.window)

        view = View(target, window=range(0, 100, 1))
        self.assertEqual(view.subwindow(), range(0, len(target)))

        view = View(target, window=range(-1, -100, -1))
        self.assertEqual(view.subwindow(), range(-1, -len(target) - 1, -1))

        view = View(target, window=range(100, 200, 1))
        self.assertEqual(view.subwindow(), range(0, 0))

        view = View(target, window=range(-100, -200, -1))
        self.assertEqual(view.subwindow(), range(0, 0))

        view = View(target, window=range(0, len(target), -1))
        self.assertEqual(view.subwindow(), view.window)

        view = View(target, window=range(len(target) - 1, -1, 1))
        self.assertEqual(view.subwindow(), view.window)
