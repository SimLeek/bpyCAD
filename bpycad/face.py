from mathutils import Vector


def polygon(points):
    # create a new vertex for each point
    vertices = []
    for point in points:
        vertex = Vector(point)
        vertices.append(vertex)

    # create a new face using the vertices
    face = tuple(range(len(points)))

    return face