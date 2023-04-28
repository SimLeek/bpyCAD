from bpycad.ui_3d import *


def test_vec_cloud():
    v = VtkVecCloud()
    for _ in range(10000):
        pt = (np.random.rand(3)) * 10
        vec = (np.random.rand(3) * 2 - 1) * 1
        col = ((np.random.rand(3) * 255).astype(np.uint8))
        v.addVector(pt, vec, col)

    render_vec_cloud(v)


from bpycad.paths import twist_extrude_path


def test_pt_cloud():
    v = VtkPointCloud()
    for _ in range(10000):
        pt = (np.random.rand(3)) * 10
        col = ((np.random.rand(3) * 255).astype(np.uint8))
        v.addPoint(pt, col)

    render_vec_cloud(v)


def test_mesh():
    from bpycad.shapes_3d import uv_sphere
    sphere = uv_sphere(10, 10, 10, "sphere_10", "sphere_10")
    display_mesh(sphere)
