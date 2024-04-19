from mathutils import Vector
import numpy as np
from .mesh_object import MeshObject
import bmesh
from .shapes_2d import Shape2D
import bpy

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


def linear_extrude(not_2d:Shape2D, x, y, z):
    m = to_mesh(not_2d)

    bpy.context.view_layer.objects.active = m.obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.select_mode(type='FACE')
    # doesn't work:
    #   bpy.ops.mesh.duplicate()
    #   bpy.ops.mesh.flip_normals()
    TRANSFORM_OT_translate = {"value": (x, y, z), "constraint_axis": (False, False, False)}
    # does the same as extrude region move:
    #   bpy.ops.mesh.extrude_manifold(TRANSFORM_OT_translate=TRANSFORM_OT_translate)
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False},TRANSFORM_OT_translate=TRANSFORM_OT_translate)
    bpy.ops.mesh.select_all(action='SELECT')
    # SHOULD work, but doesn't. The mesh edit->mesh->normals->recalc outside option in blender works.
    # bmesh also doesn't work.
    # however, afaik, the normals don't actually need to be 100% correct
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    m.update_vertices_faces_from_mesh()
    return m

def remove_faulty_triangles(mesh_object):
    new_faces = []
    for face in mesh_object.faces:
        if len(face) == 3:  # Only consider triangles
            if len(set(face)) == 3:  # Check for unique vertices
                new_faces.append(face)
    mesh_object.update_mesh(mesh_object.vertices, new_faces)
    mesh_object.obj_from_mesh()

def to_mesh(not_2d:Shape2D):
    m = MeshObject('a', 'b')
    m.update_mesh(not_2d.vertices, [f[:-1] for f in not_2d.faces])
    m.obj_from_mesh()
    bpy.context.view_layer.objects.active = m.obj
    bpy.ops.object.modifier_add(type='TRIANGULATE')
    bpy.ops.object.modifier_apply(modifier="Triangulate")

    #bpy.context.view_layer.objects.active = m.obj
    #bpy.ops.object.modifier_add(type='TRIANGULATE')
    #bpy.ops.object.modifier_apply(modifier="Triangulate")
    m.update_vertices_faces_from_mesh()
    remove_faulty_triangles(m)
    m.update_vertices_faces_from_mesh()
    return m

def to_plane(points:Shape2D,
             point=(0, 0, 0),
             normal=np.asarray([
                 [1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1],
             ])):
    not_2d = Shape2D(np.asarray([[pts[0], pts[1], 0] for pts in points.vertices]) @ np.asarray(normal) + np.asarray(point),
                     points.faces)

    return not_2d
