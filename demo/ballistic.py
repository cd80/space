# -*- coding: utf8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from space.particle import *
from application import Application
from timing import TimingData
import logging
logging.basicConfig()

UNUSED = 0
PISTOL = 1
ARTILLERY = 2
FIREBALL = 3
LASER = 4
timing = TimingData()
timing.init()
timing.update()


class BallisticDemo(Application, object):
    def __init__(self, current_shot_type=PISTOL):
        super(self.__class__, self).__init__()
        self.width = 0
        self.height = 0
        self.ammoRounds = 16
        self.ammo = [AmmoRound() for _ in range(0, self.ammoRounds)]
        self.currentShotType = current_shot_type

    def get_title(self):
        return "Space > Ballistic Demo"

    def fire(self):
        for shot in self.ammo:
            if shot.type == UNUSED:
                break
        else:
            return
        current_shot_type = self.currentShotType
        if current_shot_type == PISTOL:
            shot.particle.set_mass(2.0)
            shot.particle.set_velocity(0.0, 0.0, 35.0)
            shot.particle.set_acceleration(0.0, -1.0, 0.0)
            shot.particle.set_damping(0.99)

        elif current_shot_type == ARTILLERY:
            shot.particle.set_mass(200.0)
            shot.particle.set_velocity(0.0, 30.0, 40.0)
            shot.particle.set_acceleration(0.0, -20.0, 0.0)
            shot.particle.set_damping(0.99)

        elif current_shot_type == FIREBALL:
            shot.particle.set_mass(1.0)
            shot.particle.set_velocity(0.0, 0.0, 10.0)
            shot.particle.set_acceleration(0.0, 0.6, 0.0)
            shot.particle.set_damping(0.99)

        elif current_shot_type == LASER:
            shot.particle.set_mass(0.1)
            shot.particle.set_velocity(0.0, 0.0, 100.0)
            shot.particle.set_acceleration(0.0, 0.0, 0.0)
            shot.particle.set_damping(0.99)

        shot.particle.set_position(0.0, 1.5, 0.0)
        shot.startTime = timing.get().lastFrameTimeStamp
        shot.type = current_shot_type

        shot.particle.clear_accumulator()

    def update(self):
        timing.update()
        duration = timing.get().lastFrameDuration * 0.001
        if duration <= 0.0:
            return

        for shot in self.ammo:
            if shot.type != UNUSED:
                shot.particle.integrate(duration)

                if shot.particle.get_position().y < 0.0 or \
                   shot.startTime+5000 < timing.get().lastFrameTimeStamp or \
                   shot.particle.get_position().z > 200.0:
                    shot.type = UNUSED
        Application().update()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(-25.0, 8.0, 5.0, 0.0, 5.0, 22.0, 0.0, 1.0, 0.0)

        # Draw a sphere at the firing point, add a shadow projected
        # onto the ground plane.
        glColor3f(0.1, 0.1, 0.1)
        glPushMatrix()
        glTranslatef(0.1, 1.1, 0.1)
        glutSolidSphere(0.1, 5, 5)
        glTranslatef(0.1, -1.1, 0.1)
        glColor3f(0.71, 0.71, 0.71)
        glScalef(1.1, 0.1, 1.1)
        glutSolidSphere(0.1, 5, 5)
        glPopMatrix()

        # Draw some scale lines
        glColor3f(0.71, 0.71, 0.71)
        glBegin(GL_LINES)
        for i in range(0, 200, 10):
            glVertex3f(-5.1, 0.1, i)
            glVertex3f(5.1, 0.1, i)

        glEnd()

        # Render each particle in turn
        for shot in self.ammo:
            if shot.type != UNUSED:
                shot.render()

        # Render the description
        glColor3f(0.1, 0.1, 0.1)
        self.render_text(10.1, 34.1, "Click: Fire\n1-4: Select Ammo")

        # Render the name of the current shot type
        current_shot_type = self.currentShotType
        if current_shot_type == PISTOL:
            self.render_text(10.1, 10.1, "Current Ammo: Pistol")
        elif current_shot_type == ARTILLERY:
            self.render_text(10.1, 10.1, "Current Ammo: Artillery")
        elif current_shot_type == FIREBALL:
            self.render_text(10.1, 10.1, "Current Ammo: Fireball")
        elif current_shot_type == LASER:
            self.render_text(10.1, 10.1, "Current Ammo: Laser")

    def mouse(self, button, state, x, y):
        if state == GLUT_DOWN:
            self.fire()

    def key(self, key, x, y):
        key = int(key)
        if key == 1:
            self.currentShotType = PISTOL
        elif key == 2:
            self.currentShotType = ARTILLERY
        elif key == 3:
            self.currentShotType = FIREBALL
        elif key == 4:
            self.currentShotType = LASER


class AmmoRound:
        def __init__(self):
            self.particle = Particle()
            self.type = UNUSED
            self.startTime = 0

        def render(self):
            position = self.particle.get_position()
            glColor3f(0, 0, 0)
            glPushMatrix()
            glTranslatef(position.x, position.y, position.z)
            glutSolidSphere(0.3, 5, 4)
            glPopMatrix()

            glColor3f(0.75, 0.75, 0.75)
            glPushMatrix()
            glTranslatef(1.0, 0.1, 1.0)
            glutSolidSphere(0.6, 5, 4)
            glPopMatrix()


def get_application():
    return BallisticDemo()
