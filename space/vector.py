# -*- coding: utf8 -*-
import numpy


class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def invert(self):
        self.x *= -1
        self.y *= -1
        self.z *= -1

    def magnitude(self):
        return numpy.sqrt(self.x**2 + self.y**2 + self.z**2)

    def square_magnitude(self):
        return self.x**2 + self.y**2 + self.z**2

    def normalize(self):
        l = self.magnitude()
        if l > 0:
            self.x *= (1.0 / l)
            self.y *= (1.0 / l)
            self.z *= (1.0 / l)

    """
    Function is removed because it looks better if we just write A * (3*B)
    def addScaledVector(self, v, scale):
        self.x += v.x * scale
        self.y += v.y * scale
        self.z += v.z * scale
    """

    def component_product(self, v):
        assert(type(v) == type(self))
        return Vector3(self.x * v.x, self.y * v.y, self.z * v.z)

    def component_product_update(self, v):
        self.x *= v.x
        self.y *= v.y
        self.z *= v.z
    """
    removed because of the same reason with addScaledVector
    def scalarProduct(self, v):
        pass
    """

    def clear(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def __mul__(self, v):
        if isinstance(v, Vector3):
            # Inner product of the vector, ret : scalar
            return self.x*v.x + self.y*v.y + self.z*v.z
        else:
            #  Scalar multiplication of vector
            return Vector3(self.x*v, self.y*v, self.z*v)

    def __add__(self, v):
        assert(type(v) == type(self))
        return Vector3(self.x+v.x, self.y+v.y, self.z+v.z)

    def __sub__(self, v):
        assert(type(v) == type(self))
        return Vector3(self.x-v.x, self.y-v.y, self.z-v.z)

    def __mod__(self, v):
        # cross product
        return Vector3(self.y*v.z - self.z*v.y, self.z*v.x - self.x*v.z, self.x*v.y - self.y*v.x)

    def __str__(self):
        return "{} {} {}".format(self.x, self.y, self.z)

