from .mesh_object import MeshObject, _default_name
import bpy
import bmesh
import string
import random



def cylinder(radius, depth, segments, mesh_name=None, object_name=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=segments)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if mesh_name==None:
        mesh_name = _default_name()
    obj.data.name = mesh_name
    if object_name==None:
        object_name = _default_name()
    obj.name = object_name
    return MeshObject.from_existing_object(obj)


def cone(radius1, radius2, depth, segments, mesh_name=None, object_name=None):
    bpy.ops.mesh.primitive_cone_add(radius1=radius1, radius2=radius2, depth=depth, vertices=segments)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if mesh_name == None:
        mesh_name = _default_name()
    obj.data.name = mesh_name
    if object_name == None:
        object_name = _default_name()
    obj.name = object_name
    return MeshObject.from_existing_object(obj)


def cube(size, mesh_name=None, object_name=None, center=False):
    if isinstance(size, (float, int)):
        if not center:
            location = [size/2, size/2, size/2]
        else:
            location = [0,0,0]
        bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    elif isinstance(size, (list, tuple)):
        if not center:
            location = [size[0]/2, size[1]/2, size[2]/2]
        else:
            location = [0,0,0]
        bpy.ops.mesh.primitive_cube_add(size=1, scale=size, location=location)
    else:
        raise NotImplementedError()
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if mesh_name == None:
        mesh_name = _default_name()
    obj.data.name = mesh_name
    if object_name == None:
        object_name = _default_name()
    obj.name = object_name
    return MeshObject.from_existing_object(obj)


def uv_sphere(radius, segments, rings, mesh_name=None, object_name=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=segments, ring_count=rings)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if mesh_name == None:
        mesh_name = _default_name()
    obj.data.name = mesh_name
    if object_name == None:
        object_name = _default_name()
    obj.name = object_name
    return MeshObject.from_existing_object(obj)


def icosphere(radius, subdivisions, mesh_name=None, object_name=None):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=radius, subdivisions=subdivisions)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if mesh_name == None:
        mesh_name = _default_name()
    obj.data.name = mesh_name
    if object_name == None:
        object_name = _default_name()
    obj.name = object_name
    return MeshObject.from_existing_object(obj)


def plane(size, mesh_name=None, object_name=None):
    bpy.ops.mesh.primitive_plane_add(size=size)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if mesh_name == None:
        mesh_name = _default_name()
    obj.data.name = mesh_name
    if object_name == None:
        object_name = _default_name()
    obj.name = object_name
    return MeshObject.from_existing_object(obj)

def polyhedron(points, faces, mesh_name=None, object_name=None):
    m = MeshObject(mesh_name, object_name)
    m.update_mesh(points, faces)
    m.obj_from_mesh()

    return m

def flip_normals(mo:MeshObject):
    # because OpenSCAD programmer don't care

    obj = mo.obj

    # Ensure the object is a mesh
    if obj and obj.type == 'MESH':
        # Select the object
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        # Switch to face selection mode
        bpy.ops.mesh.select_all(action='SELECT')

        # Invert face normals
        bpy.ops.mesh.flip_normals()

        # Switch back to object mode
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print("Selected object is not a mesh.")
    mo.update_vertices_faces_from_mesh()