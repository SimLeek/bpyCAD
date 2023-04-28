from .mesh_object import MeshObject
import numpy as np
import bpy
from mathutils import Matrix


def set_origin(mo: MeshObject, location):
    mo.obj.location = location


def translate_3d(mo, distance):
    mo.obj.location += distance


def translate_2d(pts, vector):
    transformed_points = [transformed_point + vector for transformed_point in pts]
    return transformed_points


def translate(obj, vec):
    if isinstance(obj, MeshObject):
        translate_3d(obj, vec)
    else:
        translate_2d(obj, vec)


def _rotate_matrix(mo: MeshObject, matrix3x3):
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


def _rotate_euler(mo: MeshObject, euler_angles):
    mo.obj.rotation_mode = 'XYZ'
    mo.obj.rotation_euler = euler_angles


def rotate_3d(obj: MeshObject, *rot):
    rot_np, axis, angle = None
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
        elif shape == (3,):
            euler = bpy.data.euler.Euler(rot_np, 'XYZ')
            _rotate_euler(obj, euler)
        elif shape == (3, 3):
            matrix = Matrix(rot_np)
            _rotate_matrix(obj, matrix)
    else:
        assert axis is not None and angle is not None
        raise NotImplementedError("axis angle rotation not implemented yet")


def rotate_2d(pts: np.array, angle):
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])
    transformed_points = [np.matmul(rotation_matrix, point) for point in pts]
    return transformed_points


def rotate(obj, *rot):
    if isinstance(obj, MeshObject):
        rotate_3d(obj, rot)
    else:
        obj_np = np.asarray(obj)
        if obj.shape[-1] == 2 and len(obj.shape) == 2:  # assert 2d points
            rotate_2d(obj_np, rot)
        else:
            raise NotImplementedError(f"Rotating {type(obj)} not supported yet")


def set_scale(self, scale):
    self.obj.scale = scale
