import numpy as np
import cv2
from sys import platform
from typing import List
import bisect

default_min_angle = np.pi / 15
default_min_chord = 2
from PIL import ImageFont, ImageDraw, Image

class Shape2D:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces  # loops of vertex indices

def polygon(vertices:np.ndarray):
    assert vertices.shape[1] == 2, "Input numpy array must have shape [n, 2]"
    face = [[i for i in range(vertices.shape[0])]]
    return Shape2D(vertices, face)



def polygons(vertices: List[np.ndarray]):
    unique_vertices = []
    faces = []

    for v in vertices:
        v = np.asarray(v)
        assert v.shape[1] == 2, "Input numpy array must have shape [n, 2]"
        face = []
        for vertex in v:
            unique_vertex_index = bisect.bisect_left(unique_vertices, list(vertex)+[float('inf')])
            if unique_vertex_index < len(unique_vertices) and np.array_equal(unique_vertices[unique_vertex_index][:2],
                                                                             vertex):
                face.append(unique_vertices[unique_vertex_index][2])
            else:
                unique_vertices.insert(unique_vertex_index, list(vertex)+[len(unique_vertices)])
                face.append(len(unique_vertices) - 1)
        faces.append(face)

    unique_vertices.sort(key=lambda x: x[2])
    unique_vertices = np.array(unique_vertices)[:, :2]

    return Shape2D(unique_vertices, faces)

def get_theta_step(radius, min_angle=None, min_chord=None, num_fragments=None):
    if num_fragments is not None:
        return 2 * np.pi / num_fragments
    if min_angle is None:
        min_angle = default_min_angle
    if min_chord is None:
        min_chord = default_min_chord

    chord = 2 * radius * np.sin(min_angle / 2)

    if min_chord > chord:
        return 2 * np.arcsin(min_chord / (2 * radius))
    else:
        return min_angle


def circle(radius, min_angle=None, min_chord=None, num_fragments=None):
    theta_step_len = get_theta_step(radius, min_angle, min_chord, num_fragments)
    num_points = max(int(np.floor(2 * np.pi / theta_step_len)), 3)
    theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return polygon(np.column_stack((x, y)))


def square(s):
    half_s = s / 2
    return polygon(np.array([
        [-half_s, -half_s],
        [half_s, -half_s],
        [half_s, half_s],
        [-half_s, half_s]
    ]))


def rectangle(width, height):
    x = [-width / 2, width / 2, width / 2, -width / 2]
    y = [-height / 2, -height / 2, height / 2, height / 2]
    return polygon(np.column_stack((x, y)))


def is_ccw(points):
    # Use Shoelace formula to determine the orientation of the polygon
    s = 0
    n = len(points)
    for i in range(n):
        j = (i + 1) % n
        s += (points[j][0] - points[i][0]) * (points[j][1] + points[i][1])
    return s > 0


def is_contour_ccw(contour):
    # Use Green's theorem to compute the signed area of the contour
    area = cv2.contourArea(contour)
    if area < 0:
        return True
    else:
        return False


def get_contour_levels(contours, hierarchy):
    levels = [0] * len(contours)
    for i in range(len(hierarchy[0])):
        level = 0
        parent = hierarchy[0][i][3]
        while parent != -1:
            level += 1
            parent = hierarchy[0][parent][3]
        levels[i] = level
    return levels

# todo: cut edges from exteriors to holes, or from holes to other holes, so blender can render hole-free faces
def text(text_str, font=None, size=100):
    # Draw non-ascii text onto image
    # draw = ImageDraw.Draw(pil_image)
    # draw.text((30, 30), text, font=font)

    if font is None:
        if platform == "win32":
            font = "C:\\Windows\\Fonts\\arial.ttf"
        elif platform == "darwin":
            font = "/System/Library/Fonts/Arial.ttf"
        else:
            font = "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"

    font = ImageFont.truetype(font, size)
    img = Image.new('RGB', (1, 1), color='black')
    draw = ImageDraw.Draw(img)
    text_size = draw.textbbox([0,0], text_str, font=font)
    text_size = [text_size[2], text_size[3]]

    pil_image = Image.new('RGB', text_size, color='black')

    draw = ImageDraw.Draw(pil_image)
    draw.text((0, 0), text_str, font=font, fill='white')

    # Convert back to Numpy array and switch back from RGB to BGR
    img = np.asarray(pil_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    img = np.flip(img, axis=0)
    # Threshold the image to obtain a binary image
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    lvls = get_contour_levels(contours, hierarchy)
    # Determine the orientation of each contour and create the corresponding ccw polygon
    ccw_polygons = []
    for contour, lvl in zip(contours, lvls):
        is_ccw = is_contour_ccw(contour)
        if not (is_ccw and lvl % 2 == 0):
            contour = np.flip(contour, axis=0)
        ccw_polygon = [tuple(point[0]) for point in contour.tolist()]
        ccw_polygons.append(ccw_polygon)

    return polygons(ccw_polygons)
