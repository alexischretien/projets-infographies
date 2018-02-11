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
        raise NotImplemented

    def __eq__(self, other):
        r"""
        Returns True if and only if two points are equal

        >>> Point3D(1,2,3) == Point3D(1,2,3)
        True
        >>> Point3D(2,1,3) == Point3D(1,2,3)
        False
        """
        raise NotImplemented

    def __sub__(self, other):
        r"""
        Returns the vector going from other to self.

        >>> Point3D(1,4,3)- Point3D(2,1,0)
        Vector3D(-1,3,3)
        """
        raise NotImplemented

    def distance(self, other):
        r"""
        Returns the distance between self and other.

        >>> is_close(Point3D(2,0,1).distance(Point3D(1,4,8)), 8.124)
        True
        """
        raise NotImplemented

class Vector3D(object):

    def __init__(self, x, y, z):
        r"""
        Creates an instance of 3D vector.

        >>> u = Vector3D(1,-2,3)
        """
        raise NotImplemented

    def __repr__(self):
        r"""
        Returns a string representation of self.

        >>> Vector3D(-2,3,5)
        Vector3D(-2,3,5)
        """
        raise NotImplemented

    def __eq__(self, other):
        r"""
        Returns True if and only if two vectors are equal.

        >>> Vector3D(1,2,3) == Vector3D(1,2,3)
        True
        >>> Vector3D(1,2,3) == Vector3D(4,5,6)
        False
        """
        raise NotImplemented

    def __add__(self, other):
        r"""
        Adds two 3D vectors.

        >>> Vector3D(1,2,3) + Vector3D(4,5,6)
        Vector3D(5,7,9)
        """
        raise NotImplemented

    def __sub__(self, other):
        r"""
        Substracts two 3D vectors.

        >>> Vector3D(1,2,3) - Vector3D(4,5,6)
        Vector3D(-3,-3,-3)
        """
        raise NotImplemented

    def __rmul__(self, scalar):
        r"""
        >>> 2 * Vector3D(1,2,3)
        Vector3D(2,4,6)
        """
        raise NotImplemented

    def __neg__(self):
        r"""
        Returns the additive inverse of self.

        >>> -Vector3D(1,2,3) == Vector3D(-1,-2,-3)
        True
        >>> v = Vector3D(1,-2,4)
        >>> v + (-v) == Vector3D.zero()
        True
        """
        raise NotImplemented

    @staticmethod
    def zero():
        r"""
        Returns the null 3D vector.

        >>> Vector3D.zero() == Vector3D(0,0,0)
        True
        """
        raise NotImplemented

    def square_norm(self):
        r"""
        Returns the square of the norm of self.

        >>> is_close(Vector3D(0,1,0).square_norm(), 1.0)
        True
        >>> is_close(Vector3D(1,1,0).square_norm(), 2.0)
        True
        """
        raise NotImplemented

    def norm(self):
        r"""
        Returns the norm of self.

        >>> is_close(Vector3D(0,1,0).norm(), 1.0)
        True
        >>> is_close(Vector3D(1,1,0).norm(), 1.4142)
        True
        """
        raise NotImplemented

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
        raise NotImplemented

    def dot_product(self, other):
        r"""
        Returns the dot product between self and other.

        >>> is_close(Vector3D(1,2,3).dot_product(Vector3D(4,5,6)), 32.0)
        True
        >>> is_close(Vector3D(1,-2,4).dot_product(Vector3D(2,-1,-1)), 0.0)
        True
        """
        raise NotImplemented

    def cross_product(self, other):
        r"""
        Returns the cross product of self with other.

        See https://en.wikipedia.org/wiki/Cross_product for more details.

        >>> Vector3D(1,0,0).cross_product(Vector3D(0,1,0))
        Vector3D(0,0,1)
        >>> Vector3D(1,0,0).cross_product(Vector3D(1,0,0)) == Vector3D.zero()
        True
        """
        raise NotImplemented
                        
    def project(self, other):
        r"""
        Returns the 3D vector obtained by projecting self onto other.

        See https://en.wikipedia.org/wiki/Vector_projection for more details.

        >>> Vector3D(1,1,0).project(Vector3D(1,0,0)) == Vector3D(1,0,0)
        True
        >>> is_close(Vector3D(1,-1,1).project(Vector3D(1,2,3)).norm(), 0.5345)
        True
        """
        raise NotImplemented

    def reflect(self, normal):
        r"""
        Returns the 3D vector obtained by reflecting self with respect to
        normal.

        >>> Vector3D(1,-1,0).reflect(Vector3D(-1,0,0)) == Vector3D(-1,-1,0)
        True
        >>> Vector3D(1,-1,-2).reflect(Vector3D(0,0,1))
        Vector3D(1.0,-1.0,2.0)
        """
        raise NotImplemented
