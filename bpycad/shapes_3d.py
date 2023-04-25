from .mesh_object import MeshObject
import bpy


def cylinder(radius, depth, segments, mesh_name, object_name):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=segments)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.name = mesh_name
    obj.name = object_name
    return MeshObject.from_existing_object(obj)


def cone(radius1, radius2, depth, segments, mesh_name, object_name):
    bpy.ops.mesh.primitive_cone_add(radius1=radius1, radius2=radius2, depth=depth, vertices=segments)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.name = mesh_name
    obj.name = object_name
    return MeshObject.from_existing_object(obj)


def cube(size, mesh_name, object_name):
    bpy.ops.mesh.primitive_cube_add(size=size)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.name = mesh_name
    obj.name = object_name
    return MeshObject.from_existing_object(obj)


def uv_sphere(radius, segments, rings, mesh_name, object_name):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=segments, ring_count=rings)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.name = mesh_name
    obj.name = object_name
    return MeshObject.from_existing_object(obj)


def icosphere(radius, subdivisions, mesh_name, object_name):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=radius, subdivisions=subdivisions)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.name = mesh_name
    obj.name = object_name
    return MeshObject.from_existing_object(obj)


def plane(size, mesh_name, object_name):
    bpy.ops.mesh.primitive_plane_add(size=size)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.name = mesh_name
    obj.name = object_name
    return MeshObject.from_existing_object(obj)
