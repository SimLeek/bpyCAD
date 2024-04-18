from .mesh_object import MeshObject
import numpy as np
import bpy
from mathutils import Matrix, Vector, Euler
from .shapes_2d import Shape2D

def set_origin(mo: MeshObject, location):
    mo.obj.location = location

def set_mesh_xform(mo):
    mb = mo.obj.matrix_basis
    if hasattr(mo.obj.data, "transform"):
        mo.obj.data.transform(mb)
    for c in mo.obj.children:
        c.matrix_local = mb @ c.matrix_local
    mo.obj.matrix_basis.identity()

def translate_3d(mo, distance, copy=True):
    if copy:
        mo = mo.copy(mo)
    mo.obj.location += Vector(distance)

    set_mesh_xform(mo)

    mo.update_vertices_faces_from_obj()
    return mo


def translate_2d(pts:Shape2D, vector, copy=True):
    if copy:
        transformed_points = [transformed_point + vector for transformed_point in pts]
        return Shape2D(transformed_points, pts.faces)
    else:
        for pt in pts.vertices:
            pt += vector
        return pts


def translate(obj, vec, copy=True):
    if isinstance(obj, MeshObject):
        return translate_3d(obj, vec, copy=copy)
    else:
        return translate_2d(obj, vec, copy=copy)


def _rotate_matrix(mo: MeshObject, matrix3x3):
    if copy:
        mo = mo.copy(mo)

    mo.obj.rotation_mode = 'MATRIX'
    # matrix4x4rot = np.identity(4)
    # matrix4x4rot[:3, :3] = matrix3x3
    # Get the existing transformation matrix
    existing_matrix = mo.obj.matrix_world

    # Get the existing location and scale
    existing_location, existing_scale = existing_matrix.decompose()[1:]

    # Construct a new transformation matrix from the rotation matrix and the existing location and scale
    new_matrix = Matrix.Translation(existing_location) @ matrix3x3.to_4x4() @ Matrix.Scale(existing_scale[0], 4)

    # Set the new transformation matrix
    mo.obj.matrix_world = new_matrix

    set_mesh_xform(mo)

    return mo


def _rotate_euler(mo: MeshObject, euler_angles, copy=True):
    if copy:
        mo = mo.copy(mo)
    mo.obj.rotation_mode = 'XYZ'
    mo.obj.rotation_euler = euler_angles

    set_mesh_xform(mo)

    return mo

def rotate_3d(obj: MeshObject, *rot, copy=True):
    rot_np, axis, angle = None, None, None
    if len(rot) == 1:
        rot_np = np.asarray(rot[0])
    elif len(rot) == 2:
        axis = np.asarray(rot[0])
        angle = rot[1]
    else:
        raise NotImplementedError("Unknown rotation type")

    if rot_np is not None:
        shape = rot_np.shape
        if shape == (4,):
            raise NotImplementedError("Quaternion rotation not implemented yet")
        elif shape == (1,3):
            euler = Euler(rot_np[0], 'XYZ')
            return _rotate_euler(obj, euler, copy=copy)
        elif shape == (3,):
            euler = Euler(rot_np, 'XYZ')
            return _rotate_euler(obj, euler, copy=copy)
        elif shape == (3, 3):
            matrix = Matrix(rot_np)
            return _rotate_matrix(obj, matrix, copy=copy)
    else:
        assert axis is not None and angle is not None
        raise NotImplementedError("axis angle rotation not implemented yet")


def rotate_2d(pts: Shape2D, angle, copy=True):
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])
    rotation_matrix = rotation_matrix.squeeze()
    if copy:
        transformed_points = [np.matmul(rotation_matrix, point) for point in pts.vertices]
        return Shape2D(transformed_points, pts.faces)
    else:
        for point in pts.vertices:
            point = np.matmul(rotation_matrix, point)
        return pts


def rotate(obj, *rot, copy=True):
    if isinstance(obj, MeshObject):
        return rotate_3d(obj, rot, copy=copy)
    else:
        return rotate_2d(obj, rot, copy=copy)
        #obj_np = np.asarray(obj.vertices)
        #if obj.vertices.shape[-1] == 2 and len(obj.vertices.shape) == 2:  # assert 2d points
        #    return rotate_2d(obj_np, rot, copy=copy)
        #else:
        #    raise NotImplementedError(f"Rotating {type(obj)} not supported yet")


def set_scale(self, scale):
    self.obj.scale = scale
