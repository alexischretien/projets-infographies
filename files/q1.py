from math import sqrt

def is_close(a, b, error=0.001):
    r"""
    Returns True if two floating numbers are "almost" equal.

    Since there floating number can yield rounding errors, this is sufficient
    for testing purposes.

    >>> is_close(1.0, 1.01)
    False
    >>> is_close(1.0, 1.0001)
    True
    """
    return abs(a - b) < error

class Point3D(object):

    def __init__(self, x, y, z):
        r"""
        Creates an instance of 3D vector.

        >>> p = Point3D(4,-2,1)
        """
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        r"""
        Returns True if and only if two points are equal

        >>> Point3D(1,2,3) == Point3D(1,2,3)
        True
        >>> Point3D(2,1,3) == Point3D(1,2,3)
        False
        """
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __sub__(self, other):
        r"""
        Returns the vector going from other to self.

        >>> Point3D(1,4,3)- Point3D(2,1,0)
        Vector3D(-1,3,3)
        """
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z

        return Vector3D(dx, dy, dz)

    def distance(self, other):
        r"""
        Returns the distance between self and other.

        >>> is_close(Point3D(2,0,1).distance(Point3D(1,4,8)), 8.124)
        True
        """
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z

        return sqrt(dx*dx + dy*dy + dz*dz)

class Vector3D(object):

    def __init__(self, x, y, z):
        r"""
        Creates an instance of 3D vector.

        >>> u = Vector3D(1,-2,3)
        """
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        r"""
        Returns a string representation of self.

        >>> Vector3D(-2,3,5)
        Vector3D(-2,3,5)
        """
        return 'Vector3D({},{},{})'.format(self.x, self.y, self.z)

    def __eq__(self, other):
        r"""
        Returns True if and only if two vectors are equal.

        >>> Vector3D(1,2,3) == Vector3D(1,2,3)
        True
        >>> Vector3D(1,2,3) == Vector3D(4,5,6)
        False
        """
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        r"""
        Adds two 3D vectors.

        >>> Vector3D(1,2,3) + Vector3D(4,5,6)
        Vector3D(5,7,9)
        """
        ax = self.x + other.x
        ay = self.y + other.y
        az = self.z + other.z

        return Vector3D(ax, ay, az)

    def __sub__(self, other):
        r"""
        Substracts two 3D vectors.

        >>> Vector3D(1,2,3) - Vector3D(4,5,6)
        Vector3D(-3,-3,-3)
        """
        sx = self.x - other.x
        sy = self.y - other.y
        sz = self.z - other.z
        
        return Vector3D(sx, sy, sz)

    def __rmul__(self, scalar):
        r"""
        >>> 2 * Vector3D(1,2,3)
        Vector3D(2,4,6)
        """
        rx = self.x * scalar
        ry = self.y * scalar
        rz = self.z * scalar

        return Vector3D(rx, ry, rz)

    def __neg__(self):
        r"""
        Returns the additive inverse of self.

        >>> -Vector3D(1,2,3) == Vector3D(-1,-2,-3)
        True
        >>> v = Vector3D(1,-2,4)
        >>> v + (-v) == Vector3D.zero()
        True
        """
        nx = -1 * self.x
        ny = -1 * self.y
        nz = -1 * self.z

        return Vector3D(nx, ny, nz)

    @staticmethod
    def zero():
        r"""
        Returns the null 3D vector.

        >>> Vector3D.zero() == Vector3D(0,0,0)
        True
        """
        return Vector3D(0,0,0)

    def square_norm(self):
        r"""
        Returns the square of the norm of self.

        >>> is_close(Vector3D(0,1,0).square_norm(), 1.0)
        True
        >>> is_close(Vector3D(1,1,0).square_norm(), 2.0)
        True
        """
        return self.x * self.x + self.y * self.y + self.z * self.z

    def norm(self):
        r"""
        Returns the norm of self.

        >>> is_close(Vector3D(0,1,0).norm(), 1.0)
        True
        >>> is_close(Vector3D(1,1,0).norm(), 1.4142)
        True
        """

        return sqrt(self.square_norm())

    def normalize(self):
        r"""
        Normalizes self.

        Given a vector `v`, its associated normalized vector is the unit vector
        having the same direction.

        >>> u = Vector3D(1,1,1)
        >>> u.normalize()
        >>> is_close(u.norm(), 1.0)
        True
        """
        norm = self.norm()
        self.x = self.x / norm
        self.y = self.y / norm
        self.z = self.z / norm

    def dot_product(self, other):
        r"""
        Returns the dot product between self and other.

        >>> is_close(Vector3D(1,2,3).dot_product(Vector3D(4,5,6)), 32.0)
        True
        >>> is_close(Vector3D(1,-2,4).dot_product(Vector3D(2,-1,-1)), 0.0)
        True
        """
    
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other):
        r"""
        Returns the cross product of self with other.

        See https://en.wikipedia.org/wiki/Cross_product for more details.

        >>> Vector3D(1,0,0).cross_product(Vector3D(0,1,0))
        Vector3D(0,0,1)
        >>> Vector3D(1,0,0).cross_product(Vector3D(1,0,0)) == Vector3D.zero()
        True
        """
        cx = self.y * other.z - self.z * other.y
        cy = self.z * other.x - self.x * other.z
        cz = self.x * other.y - self.y * other.x

        return Vector3D(cx, cy, cz)
                        
    def project(self, other):
        r"""
        Returns the 3D vector obtained by projecting self onto other.

        See https://en.wikipedia.org/wiki/Vector_projection for more details.

        >>> Vector3D(1,1,0).project(Vector3D(1,0,0)) == Vector3D(1,0,0)
        True
        >>> is_close(Vector3D(1,-1,1).project(Vector3D(1,2,3)).norm(), 0.5345)
        True
        """
        other.normalize()
        plength = self.dot_product(other)
  
        return plength * other

    def reflect(self, normal):
        r"""
        Returns the 3D vector obtained by reflecting self with respect to
        normal.

        >>> Vector3D(1,-1,0).reflect(Vector3D(-1,0,0)) == Vector3D(-1,-1,0)
        True
        >>> Vector3D(1,-1,-2).reflect(Vector3D(0,0,1))
        Vector3D(1.0,-1.0,2.0)
        """
        vm = self.project(normal)
        return self - 2*vm
