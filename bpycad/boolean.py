from enum import Enum
from .mesh_object import MeshObject
from shapely.geometry import Polygon, LinearRing, MultiPolygon
import numpy as np
import shapely

import bpy


class BooleanOperation(Enum):
    INTERSECT = 'INTERSECT'
    UNION = 'UNION'
    DIFFERENCE = 'DIFFERENCE'


class BooleanSolver(Enum):
    FAST = 'FAST'
    EXACT = 'EXACT'


def boolean_3d(*mesh_objects: MeshObject, op=BooleanOperation.UNION, solver=BooleanSolver.EXACT):
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


def boolean_2d(*np_objs, op=BooleanOperation.UNION, solver=BooleanSolver.EXACT):
    assert len(np_objs) >= 2
    self = np_objs[0]
    others = np_objs[1:]

    self = Polygon(np.append(self, self[0:1, :], axis=0))

    for o in others:
        shapely_poly2 = Polygon(np.append(o, o[0:1, :], axis=0))
        if op == BooleanOperation.UNION:
            self = self.union(shapely_poly2)
        elif op == BooleanOperation.INTERSECT:
            self = self.intersection(shapely_poly2)
        elif op == BooleanOperation.DIFFERENCE:
            self = self.difference(shapely_poly2)
        else:
            raise NotImplementedError

    # Shapely does CW polygons, but blender faces use ccw, so it needs to be reversed.
    # Also, Shapely uses last=first to determine closed loops,
    # and faces don't use repeated vertices, so it needs to be removed
    if isinstance(self, Polygon):
        result = np.flip(np.array(self.exterior.coords), axis=0)[:-1, :]
    elif isinstance(self, MultiPolygon):
        result = [np.flip(np.array(s.exterior.coords), axis=0)[:-1, :] for s in self.geoms]

    # if not Polygon(result).is_ccw:
    #    result = np.flip(result, axis=0)

    return result


def boolean(*objs, op=BooleanOperation.UNION, solver=BooleanSolver.EXACT):
    if isinstance(objs[0], MeshObject):
        return boolean_3d(*objs, op=op, solver=solver)
    else:
        return boolean_2d(*objs, op=op, solver=solver)


def union(*objs, solver=BooleanSolver.EXACT):
    return boolean(*objs, op=BooleanOperation.UNION, solver=solver)


def difference(*objs, solver=BooleanSolver.EXACT):
    return boolean(*objs, op=BooleanOperation.DIFFERENCE, solver=solver)


def intersection(*objs, solver=BooleanSolver.EXACT):
    return boolean(*objs, op=BooleanOperation.INTERSECT, solver=solver)
