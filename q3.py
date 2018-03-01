"""
UQAM - Winter 2018 - INF5017 - Group 20 - q3.py

This module allows the user to display on standard output the content of a
wavefront (.obj) file associated with a sphere or torus. Content may be 
redirected to a file using a pipe.

    $ python q3.py [<OPTION> sphere [R] [U] [V] | tore [RMAJ] [RMIN] [U] [V]]

    R      The radius of a sphere.
    RMAJ   The major radius of a torus.
    RMIN   The minor radius of a torus.
    U      The number of longitudes.
    V      The number of latitudes.

author : Alexis Chretien (CHRA25049209) 
date : February 28th, 2018
"""
import sys
from math import sin, cos, pi
from q1 import Point3D, Vector3D

ERR_NB_PARAMS = "Error : invalid number of parameters."
ERR_INVALID_OBJECT = "Error : \"{}\" is not a valid object. " \
                   + "The available options are \"sphere\" and \"tore\"."
ERR_NB_PARAMS_OBJECT = "Error : the specification of a {} requires {} integers."
ERR_PARAM_TYPE = "Error : the object's parameters need to be integers " \
               + "strictly greater than 0." 

class Vertice(object):
    """ Class containing the informations on a vertice.

    Attributes: 
        point (Point3D): The location of the vertice.
        normal (Vector3D): The vertice's normal vector.
        number (int): the vertice's id. 
    """
    def __init__(self, point, normal, number):
        """ Creates an instance of vertice.
        """
        self.point = point
        self.normal = normal
        self.number = number

class Face(object):
    """ Class containing the informations on a face.

    Attributes:
        vertices (list of vertices): The vertices associated with the face.
    """
    def __init__(self, vertices):
        """ Creates an instance of face.
        """
        self.vertices = vertices
    
    def __repr__(self):
        """ Returns a string representation of self.
        """
        s = "f"
        for v in self.vertices:
            s += " {0}//{0}".format(v.number)
        s += "\n"

        return s

class Obj(object):
    """ Parent class to "Sphere" and "Tore"
    
    Attributes:
        radius (float): The object's radius.
        center (Point3D): The object's center.
        nbLon (int): The number of longitudes.
        nbLat (int): The number of latitudes.
        vertices (list of vertices): The object's vertices.
        faces (list of faces): The object's faces.
    """
    def __init__(self, radius, nbLon, nbLat):
        """ Creates an instance of Obj.
        """
        self.radius = radius
        self.center = Point3D(0.0, 0.0, 0.0)
        self.nbLon = nbLon
        self.nbLat = nbLat
        self.vertices = []
        self.faces = []
    
    def calculateCyclicVertices(self, u_domain, v_domain):
        """ Calculates the object's cyclic vertices and fills self.vertices
        accordingly.

        Finds all vertices if self is a torus. In the case of a sphere,
        all vertices minus the poles are found. 

        A specialized method defined in sphere class' body can be used to find the
        remaining vertices.

        Args:
            u_domain (float): The u domain's end, in radians (should be pi for 
                              a sphere, 2*pi for a torus).
            v_domain (float): The v domain's end, in radians (should be 2*pi 
                              in both cases).
        """
        du = u_domain/self.nbLat
        dv = v_domain/self.nbLon
        u = du/2
        noVertice = 1
         
        while (u < u_domain):
            v = dv/2

            while (v < v_domain):
                point = self.getPoint(u, v)
 
                normal = point - self.center
                self.vertices.append( Vertice( point, normal, noVertice ) )
                noVertice += 1
                v += dv
            u += du
    
    def calculateQuadFaces(self):
        """ Calculates the objects rectangular faces and fills self.faces
        accordingly.

        Finds all faces if self is a torus. In the case of a sphere, all 
        faces minus the triangular faces converging at the poles are found. 

        A specialized method defined in sphere class' body can be used to find 
        the remaining faces.

        precondition:
            self.calculateCyclicVertices must have been called prior. 
        """
        for index in range(0, self.nbQuadFaces):
            
            i = [index, index + 1, 0, index + self.nbLon]
            faceVertices = []

            if (i[1] % self.nbLon != 0):
                i[2] = i[1] + self.nbLon
            # If we have completed a cycle around the radius. Wrapping up. 
            else:
                i[2] = i[1]
                i[1] -= self.nbLon
            
            for j in range(0, 4):
                # Condition can only ever pass for a tore. Links up the 
                # first and last vertice cycles togheter.
                if (i[j]  >= self.nbVertices):
                    i[j] -= self.nbVertices
                
                faceVertices.append( self.vertices[ i[j] ] )

            self.faces.append( Face(faceVertices) )

    def __repr__(self):
        """ Return a string representation of self.
        """
        s = ""
        for v in self.vertices:
            s += "v {} {} {}\n".format(v.point.x, v.point.y, v.point.z)

        for v in self.vertices:
            s += "vn {} {} {}\n".format(v.normal.x, v.normal.y, v.normal.z)

        for f in self.faces:
            s += f.__repr__()

        return s.rstrip("\n")


class Sphere(Obj):
    """ Child class of Obj, representing a sphere

    Attributes:
        nbVertices: The sphere's number of vertices
        nbQuadFaces: The sphere's number of rectangular faces.
        nbTriFaces: The sphere's number of triangular faces. 
    """
    def __init__(self, radius, nbLon, nbLat):
        """ Creates an instance of sphere
        """
        Obj.__init__(self, radius, nbLon, nbLat)
        self.nbVertices = nbLon * nbLat + 2
        self.nbQuadFaces = nbLon * (nbLat - 1)
        self.nbTriFaces = 2 * nbLon

        self.calculateCyclicVertices(pi, 2*pi)
        self.calculateQuadFaces()
        self.calculatePoles()

    def calculatePoles(self):
        """ Finds the vertices and faces related to the two poles. 

        Finds the pole vertices and the faces associated with them.

        Precondition:
            self.calculateCyclicVertices and self.calculateQuadFaces
            must have been called prior, in that order.
        """
        p1 = self.getPoint(0, 0)
        p2 = self.getPoint(pi, 2*pi)
    
        pole1 = Vertice(p1, p1 - self.center, self.nbVertices - 1)
        pole2 = Vertice(p2, p2 - self.center, self.nbVertices)
        
        begin1 = 0
        begin2 = self.nbVertices - self.nbLon - 2
        end1 = self.nbLon
        end2 = begin2 + self.nbLon
        
        # Getting the two cycles of vertices to form tri faces with the poles
        vertCycle1 = self.vertices[ begin1 : end1 ]
        vertCycle1.append( self.vertices[ begin1 ] )

        vertCycle2 = self.vertices[ begin2 : end2 ] 
        vertCycle2.append( self.vertices[ begin2 ] )
         
        # Creating the tri faces assosicated with each pole
        for i in range(0, self.nbLon):
            self.faces.append( Face([pole1, vertCycle1[i], vertCycle1[i+1]]) )
            self.faces.append( Face([pole2, vertCycle2[i], vertCycle2[i+1]]) )
        
        # Saving up the pole vertices   
        self.vertices.extend([pole1, pole2])

    def getPoint(self, u, v):
        """ Finds a point on self's surface using u, v coordinates. 

        Args:
            u (float): The u coordinate, in radians.
            v (float): The v coordinate, in radians.
        """
        return Point3D(self.radius * sin(u) * cos(v), \
                       self.radius * sin(u) * sin(v), \
                       self.radius * cos(u));

class Tore(Obj):
           
    def __init__(self, radius, minorRadius, nbLon, nbLat):
        """ Creates an instance of a torus.

        Attributes:
            minorRadius (float): The torus' minor radius
            nbVertices (int): The number of vertices.
            nbQuadFaces (int): The number of rectangular faces.
        """
        Obj.__init__(self, radius, nbLon, nbLat)
        self.minorRadius = minorRadius 
        self.nbVertices = nbLon * nbLat
        self.nbQuadFaces = nbLon * nbLat

        self.calculateCyclicVertices(2*pi, 2*pi)
        self.calculateQuadFaces()
        
    def getPoint(self, u, v):
        """ Finds a point on self's surface using u, v coordinates.

        Args:
            u (float): The u coordinate, in radians.
            v (float): The v coordinate, in randians.
        """
        return Point3D((self.radius + self.minorRadius*cos(u))*cos(v),\
                       (self.radius + self.minorRadius*cos(u))*sin(v),\
                        self.minorRadius*sin(u))

def getObject():
    """ Validates the argv parameters. 

    Returns a tore or sphere object if the arguments are valid.
    """
    nbArgs = len(sys.argv)
   
    # validating argv params
    if (nbArgs < 2):
        print(ERR_NB_PARAMS)
        sys.exit(0)
  
    type = sys.argv[1]

    if (type != "sphere" and type != "tore"):
        print(ERR_INVALID_OBJECT.format(sys.argv[1]))
        sys.exit(0)

    elif (type == "sphere" and nbArgs != 5):
        print(ERR_NB_PARAMS_OBJECT.format("sphere", 3))
        sys.exit(0)       

    elif (type == "tore" and nbArgs != 6):
        print(ERR_NB_PARAMS_OBJECT.format("tore", 4))
        sys.exit(0)

    else:
        params = [int(s) for s in sys.argv if s.isdigit() and int(s) > 0]

        if (nbArgs - len(params) != 2):
            print(ERR_PARAM_TYPE)
            sys.exit(0)

    # instanciating the object
    if (type == "sphere"):
        object = Sphere(params[0], params[1], params[2])
    else:
        object = Tore(params[0], params[1], params[2], params[3])

    return object

"""Main
"""
object = getObject()
print object
