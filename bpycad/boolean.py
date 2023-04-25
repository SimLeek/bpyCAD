from enum import Enum
from .mesh_object import MeshObject

import bpy


class BooleanOperation(Enum):
    INTERSECT = 'INTERSECT'
    UNION = 'UNION'
    DIFFERENCE = 'DIFFERENCE'


class BooleanSolver(Enum):
    FAST = 'FAST'
    EXACT = 'EXACT'


def boolean(*mesh_objects: MeshObject, op=BooleanOperation.UNION, solver=BooleanSolver.EXACT):
    """Apply a boolean operation to two or more mesh objects.
    NOTE: Applies IN PLACE to the first mesh object. If you want to keep the old object, you need to make a copy."""
    # Add a boolean modifier to the active object
    assert len(mesh_objects) >= 2
    self = mesh_objects[0]
    others = mesh_objects[1:]
    bool_mod = self.obj.modifiers.new("Boolean", type="BOOLEAN")

    # Set the union object to the added modifier
    assert all([o.obj is not None for o in others])
    if len(others) == 1:
        bool_mod.object = others[0].obj
    else:
        bool_objs = bpy.data.collections.new("Boolean Objects")
        for o in others:
            bool_objs.objects.link(o.obj)
        bool_mod.object = bool_objs

    # Set the modifier operation to union
    bool_mod.operation = op.value

    bool_mod.solver = solver.value

    # Enable the modifier
    bool_mod.show_viewport = True
    bool_mod.show_render = True

    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

    self.update_vertices_faces_from_obj()
    return self
