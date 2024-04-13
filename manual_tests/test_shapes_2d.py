from bpycad.ui_2d import show_2d_point_loop, show_2d_shape
from bpycad.shapes_2d import circle, text, square, rectangle


def test_show_circle():
    circ = circle(10)
    show_2d_shape(circ)


def test_show_square():
    sq = square(10)
    show_2d_shape(sq)


def test_show_rectangle():
    sq = rectangle(12, 8)
    show_2d_shape(sq)


def test_show_char():
    a = text('まさか!?', font=None)
    # a = text('☺')
    show_2d_shape(a)
