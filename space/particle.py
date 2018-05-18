# -*- coding: utf8 -*-
import numpy
from space import vector
import sys


class Particle:
    def __init__(self):
        self.position = vector.Vector3()
        self.velocity = vector.Vector3()
        self.acceleration = vector.Vector3()

        # reduces increased energy caused by precision error of integrator
        self.damping = 0.999

        self.inverseMass = 0
        self.forceAccum = vector.Vector3()

    def integrate(self, duration):
        if self.inverseMass <= 0.0:
            return

        assert(duration > 0.0)
        self.position += self.velocity * duration
        resulting_acc = self.acceleration

        self.velocity += resulting_acc * duration
        self.velocity *= numpy.power(self.damping, duration)

        self.clear_accumulator()

    def set_mass(self, mass):
        assert(mass != 0)
        self.inverseMass = 1.0/mass

    def get_mass(self):
        if self.inverseMass == 0:
            return sys.float_info.max
        else:
            return 1.0/self.inverseMass

    def set_inverse_mass(self, inverse_mass):
        self.inverseMass = inverse_mass

    def get_inverse_mass(self):
        return self.inverseMass

    def has_finite_mass(self):
        return self.inverseMass >= 0.0

    def set_damping(self, damping):
        self.damping = damping

    def get_damping(self):
        return self.damping

    def set_position(self, x, y=0, z=0):
        if isinstance(x, vector.Vector3):
            self.position = x
        else:
            self.position.x = x
            self.position.y = y
            self.position.z = z

    def get_position(self):
        return self.position

    def set_velocity(self, x, y=0, z=0):
        if isinstance(x, vector.Vector3):
            self.velocity = x
        else:
            self.velocity.x = x
            self.velocity.y = y
            self.velocity.z = z

    def get_velocity(self):
        return self.velocity

    def set_acceleration(self, x, y=0, z=0):
        if isinstance(x, vector.Vector3):
            self.acceleration = x
        else:
            self.acceleration.x = x
            self.acceleration.y = y
            self.acceleration.z = z

    def get_acceleration(self):
        return self.acceleration

    def clear_accumulator(self):
        self.forceAccum.clear()

    def add_force(self, force):
        self.forceAccum += force
