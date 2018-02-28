"""
UQAM - Winter 2018 - INF5071 - Group 20 - q2.py

This module allows the user generate a simple scene made of a certain number of
boxes and circles specified in a json file. The user may also specify a filename
to generate the image of the scene. If a filename has given, the user may also 
specify the properties of light ray. The trajectory of this light ray will be
traced on the image.

    $ python q2.py [<OPTINAL> FILE [<OPTINAL> [OX],[OY],[DX],[DY],[I]]]

    FILE    Relative path of the image file to be produced.
    OX      X coordinate of the light ray's origin point.
    OY      Y coordinate of the light ray's origin point.
    DX      X coordiante of the light ray's direction vector.
    DY      Y coordinate of the light ray's direction vector.
    I       Intensity of the light ray (number of rebounces).
 
author : Alexis Chretien (CHRA25049209)
date : February 26th, 2018
"""

import json
import os
import sys
from PIL import Image, ImageDraw, ImageColor
from q1 import Point3D, Vector3D
from math import sqrt

ERR_INVALID_FILENAME = "Error : invalid filename"
ERR_LIGHT_RAY_PARAMS = "Error : invalid number of parameters for light ray object"
ERR_INVALID_JSON = "Error : invalid object(s) in json file. The scene " \
                 + "only allows circles and boxes"
ERR_NB_PARAMS = "Error : the program takes at least one argument"

class Scene(object):
    """ Class containing the informations on a scene and the objects it contains.
    
    Attributes:
        width (float): The width of the scene.
        height (float): The height of the scene.
        center (Point3D): The center of the scene.
        objects (list of Box, Circle): The objects present in the scene.
        lightRay (Ray, None): The light ray, if present in the scene. 
    """
    def __init__(self, jsonData, lightRay):
        """ Creates an instance of scene.

        Attributes:
            jsonData (dict): The json data containing the information of the scene
                             to be instanciated.
            lightRay (Ray, None): The initial light ray, if present in the scene.
        """
        self.width = jsonData.get('width')
        self.height = jsonData.get('height')
        self.center = Point3D(self.width/2, self.height/2, 0)
        self.objects = [ Box(self.center, self.width, self.height) ]
        self.lightRay = lightRay

        for o in jsonData.get('objects'):          
            type = o.get('type')  
            c = o.get('center')
            center = Point3D(c[0], c[1], 0) 

            if type == "circle":
                radius = o.get('radius')
                self.objects.append( Circle(center, radius) )
            elif type == "box":
                width  = o.get('width')
                height = o.get('height')
                self.objects.append( Box(center, width, height) )

    def drawScene(self):
        """ Draws the scene and saves the results to an image.

        Produces an image with the dimensions of the scene. The boxes and
        circles are drawn in black. If present, the light ray's trajectory 
        is drawn in orange.
        """         
        image = Image.new('RGB', (self.width, self.height), (255,255,255))
        draw  = ImageDraw.Draw(image)

        for o in self.objects:
            o.drawObject(draw)

        # If a light ray was specified
        while(self.lightRay != None and self.lightRay.intensity >= 0):            
            minDistance = float('inf')
            nextLightRay = None

            for o in self.objects:                    
                lightRay = o.reflectedRay(self.lightRay)

                if (lightRay != None):
                    distance = lightRay.origin.distance(self.lightRay.origin)
                    if (distance < minDistance): 
                        minDistance = distance
                        nextLightRay = lightRay                
                
            if (nextLightRay != None):        
                draw.line( (self.lightRay.origin.x, self.lightRay.origin.y, \
                            nextLightRay.origin.x, nextLightRay.origin.y), \
                            fill= "orange" )
            self.lightRay = nextLightRay
        image.save(sys.argv[2])

    def __repr__(self):
        """ Returns a string representation of self.
        """
        s = "Scene of dimensions {} x {}\n".format(self.width, self.height) \
            + "Containing {} objects:".format(len(self.objects))

        for o in self.objects[1:len(self.objects)]:
            s += "\n- " + o.__repr__()
            
        return s
        
class Circle(object):
    """ Class containing the informations of the a circle.

    Attributes:
        center (Point3D): The center of the circle.
        radius (float):   The radius of the circle.
    """
    def __init__(self, center, radius):
        """ Creates an instance of circle.
        """
        self.center = center
        self.radius = radius

    def drawObject(self, draw):
        """ Draws self to an image using the draw attribute.

        Args:
            draw (ImageDraw): The "drawer". Must already have an active image.
        """
        r = self.radius  
        x1 = self.center.x - r
        y1 = self.center.y - r
        x2 = self.center.x + r
        y2 = self.center.y + r
        draw.ellipse((x1, y1, x2, y2), outline=(0,0,0))
        
    def __repr__(self):
        """ Returns a string representation of self.
        """
        return "A circle of radius {}, centered in ({},{})" \
            .format(self.radius, self.center.x, self.center.y)

    def reflectedRay(self, lightRay):
        """ Returns the light ray reflected on self and originating
        from "lightRay", if exists. 

        Args:
            lightRay (Ray): The originating light ray

        Returns:
            Ray, None: The reflected light ray, if exists. "None" otherwise. 
        """
        distance = lightRay.origin - self.center

        a = lightRay.direction.square_norm()
        b = 2 * lightRay.direction.dot_product(distance)
        c = distance.square_norm() - self.radius ** 2
        d = b**2 - 4*a*c
        s = 1

        # no intersection
        if (d < 0):
            return None
        
        t1 = (-b - sqrt(b**2 - 4*a*c))/(2*a)
        t2 = (-b + sqrt(b**2 - 4*a*c))/(2*a)

        # no intersection
        if (t1 < 0.001 and t2 < 0.001):
            return None
        # two intersection, taking the closest one to lightRay's origin
        elif (t1 > 0.001 and t2 > 0.001):
            t = min([t1, t2])
        # one intersection, the one with a positive t value
        else:
            t = max([t1, t2])

        origin = Point3D(lightRay.origin.x + lightRay.direction.x*t,
                         lightRay.origin.y + lightRay.direction.y*t,
                         lightRay.origin.z + lightRay.direction.z*t)
        normal = origin - self.center
        direction = lightRay.direction.reflect(normal)

        return Ray(origin, direction, lightRay.intensity - 1)
    
class Box(object):
    """ Class containing the information on a box.

    Attributes:
        center (Point3D): The center of the box.
        width (float):    The width of the box.
        height (float):   The height of the box.
        lineSegments (list of LineSegments): The list of the four line segments
                                             making up the box.
    """    
    def __init__(self, center, width, height):
        """ Creates a box
        """
        self.center = center
        self.width = width
        self.height = height
      
        p1 = Point3D(center.x - width/2, center.y - height/2, 0)
        p2 = Point3D(center.x + width/2, center.y - height/2, 0)
        p3 = Point3D(center.x + width/2, center.y + height/2, 0)
        p4 = Point3D(center.x - width/2, center.y + height/2, 0)

        self.lineSegments = [LineSegment(p1, p2), \
                             LineSegment(p2, p3), \
                             LineSegment(p3, p4), \
                             LineSegment(p4, p1)]

    def drawObject(self, draw):
        """ Draws self to an image using the draw attribute.

        Args:
            draw (ImageDraw): The "drawer". Must already have an active image.
        """    
        p1 = self.lineSegments[0].p1
        p2 = self.lineSegments[2].p1

        draw.rectangle((p1.x, p1.y, p2.x, p2.y), outline=(0,0,0))

    def reflectedRay(self, lightRay):
        """ Returns the light ray reflected on self and originating
        from "lightRay", if exists. 

        Args:
            lightRay (Ray): The originating light ray

        Returns:
            Ray, None: The reflected light ray, if exists. "None" otherwise. 

        """
        reflectedRay = None
        minPoint = None
        minDistance = float('inf')

        # find the closest point of intersection between the ray and the box (if any).
        # Requires verifying each of the 4 segments.
        for seg in self.lineSegments:
            point = seg.intersection(lightRay)

            if(isinstance(point, Point3D)):
                distance = point.distance(lightRay.origin)

                if (distance < minDistance and distance != 0):
                    minPoint = point
                    minDistance = distance
                    dx = seg.p2.x - seg.p1.x
                    dy = seg.p2.y - seg.p1.y
                    normal = Vector3D(-dy, dx, 0)
  
        if (minPoint != None):
            direction =  lightRay.direction.reflect(normal) 
            reflectedRay = Ray(minPoint, direction, lightRay.intensity - 1)

 
        return reflectedRay
            
       
    def __repr__(self):
        """ Returns the string representation of self.
        """
        return "A box of width {} and height {}, centered in ({},{})" \
            .format(self.width, self.height, self.center.x, self.center.y)

class LineSegment(object):
    """ Class containing the informations of a line segment.

    Attributes:
        p1 (Point3D): The point at the start of the line segment.
        p2 (Point3D): The point at the end of the line segment.
    """
    def __init__(self, p1, p2):
        """ Creates a line segment.
        """
        self.p1 = p1
        self.p2 = p2

    def intersection(self, ray):
        """ Returns the intersection between self and line ray "ray", if exists.

        Args:  
            ray (Ray): The ray that may intersect with self.
     
        Returns:
            Point3D, None: The point of the intersection, if that point is unique. 
                           "None" if the intersection doesn't exist or isn't a single
                           point. 
        """
        # Step 1 : find the intersection point of the infinite lines associated
        # with segment line "self" and line ray "ray" 
        line1 = Line(self.p1, Vector3D(self.p2.x - self.p1.x, self.p2.y - self.p1.y, 0))
        line2 = Line(ray.origin, ray.direction)

        point = line1.intersection(line2)

        if (isinstance(point, Point3D) == False or point == ray.origin):
            return None
        
        # step 2 : Verify that the point is both inside the line segment "self" and
        # the line ray "ray"

        # For both axis, find min and max for line segment
        if (self.p1.x < self.p2.x):
            minSegX = self.p1.x
            maxSegX = self.p2.x
        else:
            minSegX = self.p2.x
            maxSegX = self.p1.x

        if (self.p1.y < self.p2.y):
            minSegY = self.p1.y
            maxSegY = self.p2.y
        else:
            minSegY = self.p2.y
            maxSegY = self.p1.y
        
        # For both axis, find min and max for line ray
        if (ray.direction.x > 0):
            minRayX = ray.origin.x
            maxRayX = float('inf')
        elif (ray.direction.x < 0):
            minRayX = -float('inf')
            maxRayX = ray.origin.x
        else:
            minRayX = ray.origin.x
            maxRayX = minRayX
        
        if (ray.direction.y > 0):
            minRayY = ray.origin.y
            maxRayY = float('inf')
        elif (ray.direction.y < 0):
            minRayY = -float('inf')
            maxRayY = ray.origin.y
        else:               
            minRayY = ray.origin.y
            maxRayY = minRayY
            
        if (minSegX <= point.x and point.x <= maxSegX and \
                minRayX <= point.x and point.x <= maxRayX and \
                minSegY <= point.y and point.y <= maxSegY and \
                minRayY <= point.y and point.y <= maxRayY):
            return point

        else:
            return None

 
class Ray(object):
    """ Class containing the informations of a line ray.

    Attributes:
        origin (Point3D): The origin of the ray.
        direction (Vector3D): The direction vector of the ray.
        intensity (int): The number of time the ray can rebounce.
    """
    def __init__(self, origin, direction, intensity):
        """ Creates a line ray
        """
        self.origin = origin
        self.direction = direction
        self.intensity = intensity   

    def __repr__(self):
        """ Returns a string representation of self.
        """
        return "A ray of intensity {}, oriented at {}, {}, centered in ({},{})" \
                    .format(self.intensity, self.direction.x, self.direction.y, \
                            self.origin.x, self.origin.y) 
       
class Line(object):
    """ Class containing the informations of an infinite line.

    Attributes:
        point (Point3D): a point along the line.
        direction (Vector3D): The direction of the line.
    """
    def __init__(self, point, direction):
        """ Creates an instance of line.
        """
        self.point = point
        self.direction = direction

    def intersection(self, line):
        """ Returns the intersection between self and another line.
        
        Args:
            line (Line): The line that may intersect with self. 

        Returns:
            Point3D, Line, None: The result of the intersection, which may be empty,
                                 a single point or the entire line. 
        """
        nullVector = Vector3D.zero()

        if(self.direction == nullVector or line.direction == nullVector):
            # No intersection
            return None

        p1 = self.point
        p2 = line.point

        # choosing another point p2 to represent "line" if p1 == p2
        if (p1 == p2):
            p2 = Point3D(p2.x + line.direction.x, p2.y + line.direction.y, p2.z + line.direction.z)

        if (line.contains(p1)):
            if (self.contains(p2)):
                # line and self represent the same line
                return self
            else:
                # Unique point
                return p1
        elif (self.contains(p2)):
            # Unique point
            return p2
        else:
            s = 1
            u = line.point - self.point
            v = line.direction.cross_product(u)
            w = line.direction.cross_product(self.direction)

            # Since we are in 2D, the z component for all point is 0, which means
            # that the result of any cross-product is a vector with both x and y = 0.
            # We only need to verify the z component.
            if (v.z == 0 or w.z == 0):
                # No intersection
                return None

            elif ( (v.z > 0 and w.z < 0) or \
                   (v.z < 0 and w.z > 0) ): 
                s = -s

            d = s * v.norm() / w.norm()

            px = p1.x + d * self.direction.x
            py = p1.y + d * self.direction.y
            pz = p1.z + d * self.direction.z
         
            return Point3D(px, py, pz)  
                 
                 
    def contains(self, point):
        """ Verifies if self contains a given point.

        Args:
            point (Point3D): The point to verify.
    
        Returns:
            bool: True if self contains "point", false otherwise.
        """
        p1 = self.point
        p2 = Point3D(p1.x + self.direction.x, p1.y + self.direction.y, 0)
         
        p1p0 = point - p1
        p1p2 = point - p2

        return (p1p0.cross_product(p1p2) == Vector3D.zero())
            
    
def loadScene():
    """ Returns the scene using data (json file path, light ray parameters) 
    specified in argv.
    
    Returns:
        Scene: The loaded scene. 
    """
    # Opening Json file
    cwd = os.path.dirname(os.path.realpath(__file__))
    sceneFile = cwd + "/" + sys.argv[1]

    try:
        jsonData = json.loads(open(sceneFile).read())
    except:
        print(ERR_INVALID_FILENAME)
        sys.exit(0)
          
    lightRay = None

    # creating Ray object if the parameters were specified
    if (len(sys.argv) > 3):
        params = [float(s) for s in sys.argv[3].split(",")]
        if (len(params) != 5):
            print(ERR_LIGHT_RAY_PARAMS)
            sys.exit(0)

        origin = Point3D(params[0], params[1], 0)
        direction = Vector3D(params[2], params[3], 0)
        intensity = params[4]
        lightRay = Ray(origin, direction, intensity)

    # creating scene object
    try:
       scene = Scene(jsonData, lightRay)
    except: 
        print(ERR_INVALID_JSON)
        sys.exit(0)

    return scene
                      
""" Main
"""
nbArgs = len(sys.argv)

if (nbArgs < 2):
    print(ERR_NB_PARAMS)
    sys.exit(0)

scene = loadScene()
print scene

if (nbArgs > 2):
    scene.drawScene()
        
