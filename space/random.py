import numpy
from space.vector import Vector3


def random_real(real_min, real_max):
    return numpy.random.uniform(real_min, real_max, size=1)[0]


def random_int(int_max):
    return numpy.random.randint(int_max)


def random_vector(vector_min, vector_max):
    return Vector3(
        random_real(vector_min.x, vector_max.x),
        random_real(vector_min.y, vector_max.y),
        random_real(vector_min.z, vector_max.z)
    )
