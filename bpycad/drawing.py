from mathutils import Vector
import numpy as np
from .mesh_object import MeshObject
import bmesh


def to_face(points):
    # create a new vertex for each point
    vertices = []
    assert len(points[0]) == 3, "Points need to be 3D. Use to_plane to convert 2d to 3d."
    for point in points:
        vertex = Vector(point)
        vertices.append(vertex)

    # create a new face using the vertices
    face = tuple(range(len(points)))

    return face


def linear_extrude(face, x, y, z):
    m = MeshObject('a', 'b')
    m.update_mesh(face, [i for i in range(len(face))])
    bmesh.ops.extrude_face_region(m.mesh, geom=[f for f in m.mesh.faces], use_keep_orig=False, use_duplicate=True)
    for face in m.mesh.faces:
        if face.select:
            bmesh.ops.translate(m.mesh, vec=Vector((x, y, z)), verts=face.verts)
    m.update_vertices_faces_from_mesh()

def to_plane(points,
             point=(0, 0, 0),
             normal=np.asarray([
                 [1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1],
             ])):
    pts3d = np.asarray([[p[0], p[1], 0] for p in points])
    pts3d = pts3d @ np.asarray(normal) + np.asarray(point)
    return pts3d
