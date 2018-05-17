import numpy
from space.vector import Vector3
def random_real(min, max):
    return numpy.random.uniform(min, max, size=1)[0]

def random_int(max):
    return numpy.random.randint(max)

def random_vector(min, max):
    return Vector3(
        random_real(min.x, max.x),
        random_real(min.y, max.y),
        random_real(min.z, max.z)
    )