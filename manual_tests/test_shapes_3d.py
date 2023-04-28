from bpycad.ui_3d import display_mesh
from bpycad.shapes_3d import uv_sphere, icosphere, plane, cube, cone, cylinder


def test_uv_sphere():
    sphere = uv_sphere(10, 20, 20, "sphere_10", "sphere_10")
    display_mesh(sphere)


def test_ico_sphere():
    sphere = icosphere(10, 4, "sphere_10", "sphere_10")
    display_mesh(sphere)


def test_plane():
    plan = plane(10, "sphere_10", "sphere_10")
    display_mesh(plan)


def test_cube():
    c = cube(10, "sphere_10", "sphere_10")
    display_mesh(c)


def test_cone():
    c = cone(10, 3, 15, 24, "sphere_10", "sphere_10")
    display_mesh(c)


def test_cylinder():
    c = cylinder(10, 15, 24, "sphere_10", "sphere_10")
    display_mesh(c)
