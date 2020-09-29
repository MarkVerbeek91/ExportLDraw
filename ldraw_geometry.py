import mathutils
from .face_info import FaceInfo


class LDrawGeometry:
    def __init__(self):
        self.edge_vertices = []
        self.edges = []
        self.vertices = []
        self.faces = []
        self.face_info = []

    def parse_edge(self, params):
        vert_count = int(params[0])

        vertices = []
        for i in range(vert_count):
            vertex = mathutils.Vector((float(params[i * 3 + 2]), float(params[i * 3 + 3]), float(params[i * 3 + 4])))
            vertices.append(vertex)

        self.edge_vertices.extend(vertices)
        self.edges.append(vert_count)

    def parse_face(self, params):
        vert_count = int(params[0])
        color_code = params[1]

        vertices = []
        for i in range(vert_count):
            vertex = mathutils.Vector((float(params[i * 3 + 2]), float(params[i * 3 + 3]), float(params[i * 3 + 4])))
            vertices.append(vertex)

        # https://wiki.ldraw.org/wiki/LDraw_Files_Requirements#Complex_quadrilaterals
        # https://github.com/TobyLobster/ImportLDraw/pull/65/files#diff-f5a55f4be537f9ace2c9534f1e49c82e
        if vert_count == 4:
            vA = (vertices[1] - vertices[0]).cross(vertices[2] - vertices[0])
            vB = (vertices[2] - vertices[1]).cross(vertices[3] - vertices[1])
            vC = (vertices[3] - vertices[2]).cross(vertices[0] - vertices[2])
            if vA.dot(vB) < 0:
                vertices[2], vertices[3] = vertices[3], vertices[2]
            elif vB.dot(vC) < 0:
                vertices[2], vertices[1] = vertices[1], vertices[2]

        self.vertices.extend(vertices)
        self.faces.append(vert_count)
        self.face_info.append(FaceInfo(color_code))
