from bpycad.shapes_2d import rectangle, circle
from bpycad.boolean import union, difference, intersection
from bpycad.ui_2d import show_2d_point_loop, show_2d_point_loops, show_2d_shape
from bpycad.pose import translate

from bpycad.shapes_3d import icosphere, cube
from bpycad.ui_3d import display_mesh


def test_union_2d():
    ci = circle(5)
    sq = rectangle(20, 6)
    ci_sq = union(ci, sq)
    show_2d_shape(ci_sq)


def test_diff_2d():
    ci = circle(5)
    sq = rectangle(20, 6)
    ci_sq = difference(sq, ci)
    show_2d_shape(ci_sq)


def test_inter_2d():
    ci = circle(5)
    sq = rectangle(20, 6)
    ci_sq = intersection(sq, ci)
    show_2d_shape(ci_sq)

def test_diff_2d_4_circ():
    sq = rectangle(20, 6)
    ci1 = translate(circle(2), [-4,0], copy=False)
    ci2 = translate(circle(2), [4,0], copy=False)
    ci3 = translate(circle(2), [0,2], copy=False)
    ci_sq = difference(sq, ci1, ci2, ci3)
    show_2d_shape(ci_sq)

def test_union_3d():
    sp = icosphere(5, 4, 'a', 'a')
    cu = cube(8, 'b', 'b')
    sp_cu = union(cu, sp)
    display_mesh(sp_cu)


def test_diff_3d():
    sp = icosphere(5, 4, 'a', 'a')
    cu = cube(7, 'b', 'b')
    sp_cu = difference(cu, sp)
    display_mesh(sp_cu)


def test_inter_3d():
    sp = icosphere(5, 4, 'a', 'a')
    cu = cube(8, 'b', 'b')
    sp_cu = intersection(cu, sp)
    display_mesh(sp_cu)
