# -*- coding: utf8 -*-
import numpy
from space import vector
import sys
class Particle():
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

        self.clearAccumulator()

    def setMass(self, mass):
        assert(mass != 0)
        self.inverseMass = 1.0/mass

    def getMass(self):
        if self.inverseMass == 0:
            return sys.float_info.max
        else:
            return 1.0/self.inverseMass

    def setInverseMass(self, inverseMass):
        self.inverseMass = inverseMass

    def getInverseMass(self):
        return self.inverseMass

    def hasFiniteMass(self):
        return self.inverseMass >= 0.0

    def setDamping(self, damping):
        self.damping = damping

    def getDamping(self):
        return self.damping

    def setPosition(self, x, y=0, z=0):
        if isinstance(x, vector.Vector3):
            self.position = x
        else:
            self.position.x = x
            self.position.y = y
            self.position.z = z

    def getPosition(self):
        return self.position

    def setVelocity(self, x, y=0, z=0):
        if isinstance(x, vector.Vector3):
            self.velocity = x
        else:
            self.velocity.x = x
            self.velocity.y = y
            self.velocity.z = z

    def getVelocity(self):
        return self.velocity

    def setAcceleration(self, x, y=0, z=0):
        if isinstance(x, vector.Vector3):
            self.acceleration = x
        else:
            self.acceleration.x = x
            self.acceleration.y = y
            self.acceleration.z = z

    def getAcceleration(self):
        return self.acceleration

    def clearAccumulator(self):
        self.forceAccum.clear()

    def addForce(self, force):
        self.forceAccum += force