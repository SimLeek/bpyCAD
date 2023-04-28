import bpy
from mathutils import Matrix
import bmesh
import numpy as np

class MeshObject:
    def __init__(self, mesh_name, object_name):
        self.mesh_name = mesh_name
        self.obj_name = object_name
        self.mesh = bpy.data.meshes.new(name=mesh_name)
        self.obj = None
        self.vertices = []
        self.faces = []

    def obj_from_mesh(self):
        self.obj = bpy.data.objects.new(self.obj_name, self.mesh)
        bpy.context.scene.collection.objects.link(self.obj)

    @classmethod
    def from_existing_object(cls, obj):
        mesh_name = obj.data.name
        object_name = obj.name
        mesh = obj.data

        new_mesh_object = cls(mesh_name, object_name)
        new_mesh_object.mesh = mesh
        new_mesh_object.obj = obj
        new_mesh_object.update_vertices_faces_from_obj()

        return new_mesh_object

    def update_vertices_faces_from_obj(self):
        assert self.obj is not None
        mesh_data = self.obj.data
        self.vertices = [v.co for v in mesh_data.vertices]
        self.faces = [f.vertices for f in mesh_data.polygons]

    def update_vertices_faces_from_mesh(self):
        assert self.mesh is not None
        mesh_data = self.mesh
        self.vertices = [v.co for v in mesh_data.vertices]
        self.faces = [f.vertices for f in mesh_data.polygons]

    def update_mesh(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.update_internal_mesh()

    def update_internal_mesh(self):
        del self.mesh
        self.mesh = bpy.data.meshes.new(name=self.mesh_name)
        self.mesh.from_pydata(np.asarray(self.vertices).tolist(), [], self.faces)
        self.mesh.update()

    def get_mesh_vertices_faces(self):
        if not self.vertices or not self.faces:
            mesh_data = self.obj.data
            self.vertices = [v.co for v in mesh_data.vertices]
            self.faces = [f.vertices for f in mesh_data.polygons]
            matrix = self.obj.matrix_world
            self.vertices = [matrix @ v for v in self.vertices]
        return self.vertices, self.faces

    def convert_to_triangles(self):
        # Create a new mesh object
        mesh_data = bpy.data.meshes.new(name="temp_mesh")

        # Initialize a bmesh and add vertices and faces
        bm = bmesh.new()
        for vertex in self.vertices:
            bm.verts.new(vertex)
        bm.verts.ensure_lookup_table()
        for face in self.faces:
            bm.faces.new([bm.verts[index] for index in face])
        bm.faces.ensure_lookup_table()

        # Triangulate the faces
        bmesh.ops.triangulate(bm, faces=bm.faces)

        # Retrieve the updated vertices and faces
        bm.to_mesh(mesh_data)
        mesh_data.update()
        vertices = [list(v.co[:]) for v in mesh_data.vertices]
        faces = [list(f.vertices[:]) for f in mesh_data.polygons]

        # Cleanup
        bm.free()
        bpy.data.meshes.remove(mesh_data)

        self.vertices = vertices
        self.faces = faces

    def sweep_once(self, vertices2):
        v1_len = len(self.vertices) - len(vertices2)
        v2_len = len(vertices2)
        self.vertices = np.vstack([self.vertices, vertices2])
        for i in range(v2_len - 1):
            self.faces.append([v1_len + i, v1_len + i + 1, v1_len + v2_len + i])
            self.faces.append([v1_len + i + 1, v1_len + v2_len + i + 1, v1_len + v2_len + i])
        self.faces.append([v1_len + v2_len - 1, v1_len, v1_len + v2_len + v2_len - 1])
        self.faces.append([v1_len, v1_len + v2_len, v1_len + v2_len + v2_len - 1])
        # self.update_internal_mesh()




