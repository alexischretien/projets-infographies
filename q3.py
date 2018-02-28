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
date : February 27th, 2018
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
        vertices (list of vertices): The vertices associated to the face.
    """
    def __init__(self, vertices):
        """ Creates an instance of face.
        """
        self.vertices = vertices
    
    def __repr__(self):
        """ Returns a string representation of self
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
        nbVertices (int): The number of vertices.
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
        self.nbVertices = nbLon*nbLat
        self.vertices = []
        self.faces = []
    
    def calculateGeometry(self, u_domain, v_domain):
        """ Calculates the object's geometries and fills self.vertices and
        self.faces accordingly.

        Finds all vertices and faces if self is a torus. In the case of a sphere,
        all vertices and faces minus the ones associated to the two poles are found.
        A specialized method defined sphere's class body can be used to find the
        remaining geometries.

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
                p1 = self.getPoint(u, v)
                p2 = self.getPoint(u+du, v)
                p3 = self.getPoint(u+du, v+dv)
                p4 = self.getPoint(u, v+dv)

                normal = p1 - self.center
                v1 = Vertice(p1, normal, noVertice)
                self.vertices.append(v1)
                self.addQuadFace( [p1, p2, p3, p4], noVertice )

                noVertice += 1
                v += dv
            u += du
    
    def addQuadFace(self, points, noVertice):
        """ Creates the rectangular face associated with the 4 points in arguments.

        The method has to deduce the number id for the last three vertices
        by using the first's.

        Args:
            points (list of 4 Point3D): The location of the four vertices making
                                        up the rectangular face.
            noVertice (int): The number id of the vertice defined by points[0]. 
        """
        # To avoid adding faces for the last cycle of vertices for a sphere
        if (noVertice <= self.nbVertices - self.nbLon or isinstance(self, Tore)):
            verts = []
            noVertices = [noVertice, \
                          noVertice + 1, \
                          noVertice + self.nbLon + 1, \
                          noVertice + self.nbLon]
 
            # If we have completed a cycle around the radius. Wrapping up 
            if (noVertice % self.nbLon == 0):
                noVertices[2] = noVertice + 1
                noVertices[1] = noVertices[2] - self.nbLon
                                 
            for i in range (0, 4):
                # Only applicable for a tore. Links up beginning
                # and end vertices to the same faces
                if(noVertices[i] > self.nbVertices):
                    noVertices[i] -= self.nbVertices

                normal = points[i] - self.center
                verts.append( Vertice(points[i], normal, noVertices[i]) )

            face = Face(verts)
            self.faces.append(face)

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
    """
    def __init__(self, radius, nbLon, nbLat):
        """ Creates an instance of sphere
        """
        Obj.__init__(self, radius, nbLon, nbLat)
        self.calculateGeometry(pi, 2*pi)
        self.calculatePoles()

    def calculatePoles(self):
        """ Finds the remaining geometries, assuming "self.calculateGeometry" has
        been called prior. 

        Finds the pole vertices and the faces associated with them.
        """
        p1 = self.getPoint(0, 0)
        p2 = self.getPoint(pi, 2*pi)
    
        pole1 = Vertice(p1, p1 - self.center, self.nbVertices + 1)
        pole2 = Vertice(p2, p2 - self.center, self.nbVertices + 2)
        
        begin1 = 0
        begin2 = self.nbVertices - self.nbLon
        end1 = self.nbLon
        end2 = self.nbVertices

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
        self.nbVertices += 2

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
        """
        Obj.__init__(self, radius, nbLon, nbLat)
        self.minorRadius = minorRadius      
        self.calculateGeometry(2*pi, 2*pi)
        
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
    error = False

    # validating argv params
    if (nbArgs < 2):
        print(ERR_NB_PARAMS)
        error = True
    
    type = sys.argv[1]

    if (type != "sphere" and type != "tore"):
        print(ERR_INVALID_OBJECT.format(sys.argv[1]))
        error = True

    elif (type == "sphere" and nbArgs != 5):
        print(ERR_NB_PARAMS_OBJECT.format("sphere", 3))
        error = True       

    elif (type == "tore" and nbArgs != 6):
        print(ERR_NB_PARAMS_OBJECT.format("tore", 4))
        error = True

    else:
        params = [int(s) for s in sys.argv if s.isdigit() and int(s) > 0]

        if (nbArgs - len(params) != 2):
            print(ERR_PARAM_TYPE)
            error = True

    if (error):
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
