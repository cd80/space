from space import *
import logging
logging.basicConfig()
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import *
from OpenGLContext.context import Context
from OpenGLContext.events import glutevents
from OpenGLContext import contextdefinition

class Application():
    def __init__(self):
        self.width = 0
        self.height = 0

    def initGraphics(self):
        glClearColor(0.9, 0.95, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        self.setView()

    def setView(self):
        if self.height <= 0.0:
            self.height = 1
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, self.width/self.height, 1.0, 500.0)
        glMatrixMode(GL_MODELVIEW)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_LINES)
        glVertex2i(1, 1)
        glVertex2i(639, 319)
        glEnd()

    def getTitle(self):
        return "Space demo"

    def deinit(self):
        pass

    def update(self):
        glutPostRedisplay()

    def key(self, key):
        pass

    def resize(self, width, height):
        if height <= 0:
            height = 1

        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        self.setView()

    def mouse(self, button, state, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def renderText(self, x, y, text, font=0):
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, -1.0, 1.0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        if font == 0:
            font = GLUT_BITMAP_HELVETICA_10

        glRasterPos2f(x, y)
        for i in text:
            if i == '\n':
                y -= 12.0
                glRasterPos2f(x, y)
            glutBitmapCharacter(font, ord(i))

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST)
"""
https://github.com/idmillington/cyclone-physics/blob/master/src/demos/app.h
class MassAggregateApplication():
    def __init__(self, particleCount):
        world = particleCount * 10
        particleArray = list(particleCount)

        for i in range(0, particleCount):
            wo
            world.getParticles().push_back(particleArray + i)


        groundContactGenerator.init(&world.getParticles())
        world.getContactGenerators().push_back(&groundContactGenerator)


MassAggregateApplication.~MassAggregateApplication()
    delete[] particleArray


def initGraphics(self):
    # Call the superclass
    Application.initGraphics()


def display(self):
    # Clear the view port and set the camera direction
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0.0, 3.5, 8.0,  0.0, 3.5, 0.0,  0.0, 1.0, 0.0)

    glColor3f(0,0,0)

    cyclone.ParticleWorld.Particles &particles = world.getParticles()
    for (p = particles.begin()
        p != particles.end()
        p++)
        cyclone.Particle *particle = *p
         cyclone.Vector3 &pos = particle.getPosition()
        glPushMatrix()
        glTranslatef(pos.x, pos.y, pos.z)
        glutSolidSphere(0.1f, 20, 10)
        glPopMatrix()



def update(self):
    # Clear accumulators
    world.startFrame()

    # Find the duration of the last frame in seconds
    duration = (float)TimingData.get().lastFrameDuration * 0.001f
    if (duration <= 0.0f) return

    # Run the simulation
    world.runPhysics(duration)

    Application.update()

"""

"""
class RigidBodyApplication():
    def __init__(self)
    theta(0.0f),
    phi(15.0f),
    resolver(maxContacts*8),

    renderDebugInfo(False),
    pauseSimulation(True),
    autoPauseSimulation(False)
    cData.contactArray = contacts


def update(self):
    # Find the duration of the last frame in seconds
    duration = (float)TimingData.get().lastFrameDuration * 0.001f
    if (duration <= 0.0f) return
    elif (duration > 0.05f) duration = 0.05f

    # Exit immediately if we aren't running the simulation
    if pauseSimulation:
        Application.update()
        return

    elif autoPauseSimulation:
        pauseSimulation = True
        autoPauseSimulation = False


    # Update the objects
    updateObjects(duration)

    # Perform the contact generation
    generateContacts()

    # Resolve detected contacts
    resolver.resolveContacts(
        cData.contactArray,
        cData.contactCount,
        duration
        )

    Application.update()


def display(self):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(18.0f, 0, 0,  0, 0, 0,  0, 1.0f, 0)
    glRotatef(-phi, 0, 0, 1)
    glRotatef(theta, 0, 1, 0)
    glTranslatef(0, -5.0f, 0)


def drawDebug(self):
    if (not renderDebugInfo) return

    # Recalculate the contacts, they are current (in case we're
    # paused, example).
    generateContacts()

    # Render the contacts, required
    glBegin(GL_LINES)
    for (i = 0; i < cData.contactCount; i++)
        # Interbody contacts are in green, contacts are red.
        if contacts[i].body[1]:            glColor3f(0,1,0)
        } else:
            glColor3f(1,0,0)


        vec = contacts[i].contactPoint
        glVertex3f(vec.x, vec.y, vec.z)

        vec += contacts[i].contactNormal
        glVertex3f(vec.x, vec.y, vec.z)


    glEnd()


def mouse(self, button, state, x, y):
    # Set the position
    last_x = x
    last_y = y


def mouseDrag(self, x, y):
    # Update the camera
    theta += (x - last_x)*0.25f
    phi += (y - last_y)*0.25f

    # Keep it in bounds
    if (phi < -20.0f) phi = -20.0f
    elif (phi > 80.0f) phi = 80.0f

    # Remember the position
    last_x = x
    last_y = y


def key(self, char key):
    switch(key)
    case 'R': case 'r':
        # Reset the simulation
        reset()
        return

    case 'C': case 'c':
        # Toggle rendering of contacts
        renderDebugInfo = not renderDebugInfo
        return

    case 'P': case 'p':
        # Toggle running the simulation
        pauseSimulation = not pauseSimulation
        return

    case ' ':
        # Advance one frame
        autoPauseSimulation = True
        pauseSimulation = False


    Application.key(key)
"""

