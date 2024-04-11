import trimesh
import pyrender
from .mesh_object import MeshObject
import vtk
import numpy as np
#from numpy import random

def display_mesh(mo: MeshObject):
    scene = pyrender.Scene()

    def add_mesh(m):
        m.convert_to_triangles()
        mesh = trimesh.Trimesh(vertices=m.vertices, faces=m.faces).apply_transform(np.asarray(m.obj.matrix_world))

        mesh = pyrender.Mesh.from_trimesh(mesh)
        scene.add(mesh)

    if isinstance(mo, (list, tuple)):
        for momesh in mo:
            momesh.update_vertices_faces_from_obj()
            add_mesh(momesh)
    else:
        mo.update_vertices_faces_from_mesh()
        add_mesh(mo)

    pyrender.Viewer(scene, all_wireframe=True, cull_faces=True)



class VtkPointCloud:

    def __init__(self, zMin=-10.0, zMax=10.0, maxNumPoints=1e6):
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()
        self.clearPoints()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        # mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)

    def addPoint(self, point, color):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.rgb3.InsertNextValue(color[0])
            self.rgb3.InsertNextValue(color[1])
            self.rgb3.InsertNextValue(color[2])
            # self.vtkDepth.InsertNextValue(color[3])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)
        else:
            r = np.random.randint(0, self.maxNumPoints)
            self.vtkPoints.SetPoint(r, point[:])
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.rgb3.Modified()

    def clearPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.rgb3 = vtk.vtkUnsignedCharArray()
        self.rgb3.SetNumberOfComponents(3)
        self.rgb3.SetName("Colors")
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.rgb3)
        self.vtkPolyData.GetPointData().SetActiveScalars('Colors')


def _rand_test():
    pointCloud = VtkPointCloud()
    for k in range(10000):
        point = 20 * (np.random.rand(3) - 0.5)
        color = (255 * np.random.rand(3)).astype(np.uint8)
        # color[2]=0
        # color[1] = 0
        pointCloud.addPoint(point, color)


def list_of_lists_to_point_cloud(lol,
                                 col1=np.asarray([[0,0,0],[0,0,255]]),
                                 col2=np.asarray([[255,0,0],[255,255,0]])):
    pointCloud = VtkPointCloud()
    color = np.zeros(3, dtype=np.uint8)
    lm = len(lol)
    colors = []
    for li, l in enumerate(lol):
        color1 = (col1[1] * li / lm + col1[0]*(1-li/lm)).astype(np.uint8)
        pm = len(l)
        for pi, p in enumerate(l):
            color2 = (col2[1] * pi / pm + col2[0]*(1-pi/pm)).astype(np.uint8)
            pointCloud.addPoint(p, color1+color2)
            colors.append((color1+color2).copy())
    return pointCloud


def display_point_cloud(pointCloud, bg=(0, 0, 0)):
    renderer = vtk.vtkRenderer()
    renderer.AddActor(pointCloud.vtkActor)
    #renderer.SetBackground(.2, .3, .4)
    renderer.SetBackground(*bg)
    renderer.ResetCamera()

    # Render Window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    # Interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Begin Interaction
    renderWindow.Render()
    renderWindowInteractor.Start()


class VtkVecCloud:

    def __init__(self, maxNumPoints=1e6):
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()
        self.clearPoints()
        mapper = vtk.vtkPolyDataMapper()
        #mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        mapper.SetInputConnection(self.glyph.GetOutputPort())
        # mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)

    def addVector(self, point, vec, color):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.rgb3.InsertNextValue(color[0])
            self.rgb3.InsertNextValue(color[1])
            self.rgb3.InsertNextValue(color[2])
            self.vtk_vectors.InsertNextTuple(vec)
            # self.vtkDepth.InsertNextValue(color[3])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)
        else:
            r = random.randint(0, self.maxNumPoints)
            self.vtkPoints.SetPoint(r, point[:])
            self.vtk_vectors.SetTuple(r, vec[:])
            self.rgb3.SetTuple3(r, color[0], color[1], color[2])
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtk_vectors.Modified()
        self.rgb3.Modified()
        self.glyph.SetInputData(self.vtkPolyData)
        self.vtkPolyData.Modified()
        self.glyph.Modified()

    def clearPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.rgb3 = vtk.vtkUnsignedCharArray()
        self.rgb3.SetNumberOfComponents(3)
        self.rgb3.SetName("Colors")
        # Create a vtkFloatArray object to store the vector orientations
        self.vtk_vectors = vtk.vtkFloatArray()
        self.vtk_vectors.SetNumberOfComponents(3)

        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.GetPointData().SetVectors(self.vtk_vectors)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.rgb3)
        self.vtkPolyData.GetPointData().SetActiveScalars('Colors')

        self.arrow= vtk.vtkArrowSource()

        self.glyph = vtk.vtkGlyph3D()
        self.glyph.SetInputData(self.vtkPolyData)
        self.glyph.SetSourceConnection(self.arrow.GetOutputPort())
        self.glyph.SetVectorModeToUseVector()
        self.glyph.SetScaleModeToScaleByVector()
        self.glyph.SetScaleFactor(1)
        self.glyph.SetColorModeToColorByScalar()
        #self.glyph.SetRange(-1, 1)
        self.glyph.OrientOn()
        self.glyph.Update()
        #self.glyph.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, "Vector")


def render_vec_cloud(vec_cloud, bg=(0, 0, 0)):
    renderer = vtk.vtkRenderer()
    renderer.AddActor(vec_cloud.vtkActor)
    #renderer.SetBackground(.2, .3, .4)
    renderer.SetBackground(*bg)
    renderer.ResetCamera()

    # Render Window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    # Interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Begin Interaction
    renderWindow.Render()
    renderWindowInteractor.Start()