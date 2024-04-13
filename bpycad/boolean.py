from enum import Enum
from .mesh_object import MeshObject
from shapely.geometry import Polygon, LinearRing, MultiPolygon
import numpy as np
import shapely
from rtree import index
import bpy
from .shapes_2d import Shape2D, polygon, polygons

class BooleanOperation(Enum):
    INTERSECT = 'INTERSECT'
    UNION = 'UNION'
    DIFFERENCE = 'DIFFERENCE'


class BooleanSolver(Enum):
    FAST = 'FAST'
    EXACT = 'EXACT'

def traverse_edge_graph(edge_graph):
    # Initialize list to store faces
    faces = []

    # Keep track of visited edges
    visited = set()

    # Initialize start vertex
    start_vertex = 0

    # Traverse the edge graph
    while start_vertex < edge_graph.shape[0]:
        # Check if the start vertex has any unvisited neighbors
        if not np.any(edge_graph.row == start_vertex):
            start_vertex += 1
            continue

        # Start a new path from the current start vertex
        current_vertex = start_vertex
        path = [current_vertex]

        # Traverse the path until we return to the start vertex
        while True:
            # Find the indices of edges connected to the current vertex
            edge_indices = np.where(edge_graph.row == current_vertex)[0]

            # Find the index of the first unvisited edge
            next_edge_index = None
            for index in edge_indices:
                edge = (edge_graph.row[index], edge_graph.col[index])
                if edge not in visited:
                    next_edge_index = index
                    break

            # If there is no unvisited edge, break the loop
            if next_edge_index is None:
                break

            # Mark the edge as visited
            visited.add((edge_graph.row[next_edge_index], edge_graph.col[next_edge_index]))

            # Update the current vertex
            current_vertex = edge_graph.col[next_edge_index]
            path.append(current_vertex)

            # If we've reached the start vertex again, record the path as a face
            if current_vertex == start_vertex:
                faces.append(path[:])
                break

    return faces

def split_holes_for_blender(shape_with_holes):
    # Create an R-tree index
    idx = index.Index()

    # Initialize a list to store the actual vertices
    vertices = []

    # Populate the R-tree index with vertices of the outer shape and holes
    # Use a counter to differentiate shapes
    counter = 0
    shape_counter = [0]
    # Add the exterior of shape_with_holes to the R-tree
    for vertex in shape_with_holes.exterior.coords:
        idx.insert(counter, vertex)
        vertices.append(vertex)
        counter += 1

    # Iterate over each hole
    for hole in shape_with_holes.interiors:
        # Add the interior of each hole to the R-tree
        for vertex in hole.coords:
            idx.insert(counter, vertex)
            vertices.append(vertex)
            counter += 1
        shape_counter.append(counter)

    # Initialize lists to store row, col, and data for COO matrix
    rows = []
    cols = []
    data = []

    # Iterate over each shape (outer shape and holes)
    for i in range(len(shape_counter)):
        # Get the shape corresponding to the current index
        if i == 0:
            shape = shape_with_holes.exterior
        else:
            shape = shape_with_holes.interiors[i - 1]

        # Add edges between consecutive vertices within the current shape
        prev_vertex = None
        for vertex_id, vertex in enumerate(vertices):
            true_id = vertex_id + shape_counter[i]
            if prev_vertex is not None:
                rows.extend([prev_vertex, true_id])
                # cols.extend([true_id, prev_vertex])
                data.extend([1])
            prev_vertex = true_id

        # Connect the last vertex to the first vertex to finish the loop for each shape
        if prev_vertex is not None:
            first_vertex = shape_counter[i]
            rows.extend([prev_vertex, first_vertex])
            # cols.extend([first_vertex, prev_vertex])
            data.extend([1])

        # Remove vertices of the current shape from the R-tree
        for j, vertex in enumerate(shape.coords):
            idx.delete(j + shape_counter[i], vertex)

        if len(idx)==0: # no hole case
            continue

        # Find the closest pair of vertices between the current shape and other shapes
        closest_pair = None
        min_distance = float('inf')
        for j, vertex in enumerate(shape.coords):
            j_idx = j+shape_counter[i]
            for other_vertex in idx.nearest(vertex, 1):
                distance = np.linalg.norm(np.asarray(vertex) - np.asarray(vertices[other_vertex]))
                if distance < min_distance:
                    min_distance = distance
                    closest_pair = (i, other_vertex)

        # Add the closest pair of vertices to the list
        if closest_pair is not None:
            vertex, nearest_vertex = closest_pair
            rows.extend([vertex, nearest_vertex])
            cols.extend([nearest_vertex, vertex])
            data.extend([1, 1])

        # Add vertices of the current shape back to the R-tree
        for j, vertex in enumerate(shape.coords):
            idx.insert(j+shape_counter[i], vertex)

    # Create COO matrix
    edge_graph = coo_matrix((data, (rows, cols)), shape=(counter, counter))
    faces = traverse_edge_graph(edge_graph)
    shape_2d = Shape2D(vertices, faces)
    return shape_2d


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
        #bool_objs = bpy.data.collections.new("Boolean Objects")
        #for o in others:
        #    bool_objs.objects.link(o.obj)
        #bool_mod.collection = bool_objs

        # note: consecutive objects must overlap
        other = boolean_3d(*mesh_objects[1:], op=op, solver=solver)
        bool_mod.object = other.obj

    # Set the modifier operation to union
    bool_mod.operation = op.value

    bool_mod.solver = solver.value
    #bool_mod.use_hole_tolerant = True

    # Enable the modifier
    bool_mod.show_viewport = True
    bool_mod.show_render = True

    # Apply the modifier
    bpy.context.view_layer.objects.active = self.obj
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

    self.update_vertices_faces_from_obj()
    return self


def boolean_2d(*np_objs, op=BooleanOperation.UNION, solver=BooleanSolver.EXACT):
    assert len(np_objs) >= 2
    self = np_objs[0]
    others = np_objs[1:]

    self = Polygon(np.append(self, self[0:1, :], axis=0))  # todo: fix

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
        result = split_holes_for_blender(self)
        for f in range(len(result.faces)):
            result.faces[f] = list(reversed(result.faces[f]))
    elif isinstance(self, MultiPolygon):
        result = [split_holes_for_blender(s) for s in self]
        for r in result:
            for f in range(len(r.faces)):
                r.faces[f] = list(reversed(r.faces[f]))
        result_verts = []
        result_faces = []
        v_count = 0
        for r in result:
            result_verts.extend(r.vertices)
            for f in r.faces:
                for fi in range(len(f)):
                    f[fi]+=v_count
            result_faces.extend(r.faces)
        result = Shape2D(
            result_verts,
            result_faces
        )
    # if not Polygon(result).is_ccw:
    #    result = np.flip(result, axis=0)

    return result

def flatten_list(list_in):
    if isinstance(list_in,(list, tuple)):
        for l in list_in:
            for y in flatten_list(l):
                yield y
    else:
        yield list_in

def boolean(*objs, op=BooleanOperation.UNION, solver=BooleanSolver.EXACT):
    objs = [o for o in flatten_list(objs)]
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
