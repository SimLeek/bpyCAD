from bpycad.ui_2d import show_2d_shape

def test_show_2d_point_loop():
    from bpycad.shapes_2d import circle
    circ = circle(10)
    show_2d_shape(circ)
