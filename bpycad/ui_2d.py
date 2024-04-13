import matplotlib.pyplot as plt
from.shapes_2d import Shape2D

def show_2d_point_loop(points, fc='#660000', ec='#660000', pc='#ff8800'):
    # Add arrows to connect the points
    for i in range(len(points) - 1):
        plt.arrow(points[i][0], points[i][1], points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1],
                  length_includes_head=True, head_width=0.3, fc=fc, ec=ec)

    plt.arrow(points[len(points) - 1][0], points[len(points) - 1][1],
              points[0][0] - points[len(points) - 1][0], points[0][1] - points[len(points) - 1][1],
              length_includes_head=True, head_width=0.3, fc=fc, ec=ec)
    plt.scatter([p[0] for p in points], [p[1] for p in points], s=3, c=pc)
    plt.axis('equal')
    plt.show()

def show_2d_point_loops(loops, fc='#660000', ec='#660000', pc='#ff8800'):
    # Add arrows to connect the points
    for points in loops:
        for i in range(len(points) - 1):
            plt.arrow(points[i][0], points[i][1], points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1],
                      length_includes_head=True, head_width=0.3, fc=fc, ec=ec)

        plt.arrow(points[len(points) - 1][0], points[len(points) - 1][1],
                  points[0][0] - points[len(points) - 1][0], points[0][1] - points[len(points) - 1][1],
                  length_includes_head=True, head_width=0.3, fc=fc, ec=ec)
        plt.scatter([p[0] for p in points], [p[1] for p in points], s=3, c=pc)
    plt.axis('equal')
    plt.show()

def show_2d_shape(shape:Shape2D, fc='#660000', ec='#660000', pc='#ff8800'):
    for face in shape.faces:
        # Extract the vertices of the current face
        face_vertices = [shape.vertices[index] for index in face]

        # Plot the arrows for the edges of the face
        for i in range(len(face_vertices)):
            p1 = face_vertices[i]
            p2 = face_vertices[(i + 1) % len(face_vertices)]  # Wrap around to the first vertex for the last edge
            plt.arrow(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1],
                      length_includes_head=True, head_width=0.3, fc=fc, ec=ec)

        # Plot the vertices of the face
        plt.scatter([p[0] for p in face_vertices], [p[1] for p in face_vertices], s=3, c=pc)

    plt.axis('equal')
    plt.show()