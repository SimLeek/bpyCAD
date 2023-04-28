from bpycad.ui_3d import VtkVecCloud, render_vec_cloud
from bpycad.paths import twist_extrude_path
import numpy as np


def test_vec_pillar():
    v = VtkVecCloud()
    path = twist_extrude_path(10, 20, np.identity(3), 2 * np.pi / 10)
    for p in path:
        v.addVector(p[0], p[1][0, :], [255, 0, 0])
        v.addVector(p[0], p[1][1, :], [0, 255, 0])
        v.addVector(p[0], p[1][2, :], [0, 0, 255])

    render_vec_cloud(v)
