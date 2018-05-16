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
import ballistic
from timing import *
from application import *
import sys
import pygame
from pygame.locals import *
def createWindow(title):
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640, 320)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(title)

def update():
    app.update()

def display():
    app.display()

    glFlush()
    glutSwapBuffers()

def mouse(button, state, x, y):
    app.mouse(button, state, x, y)

def reshape(width, height):
    app.resize(width, height)

def keyboard(key, x, y):
    app.key(key)

def motion(x, y):
    app.mouseDrag(x, y)

if __name__ == '__main__':

    glutInit(sys.argv)

    app = ballistic.getApplication()
    createWindow(app.getTitle())

    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display)
    glutIdleFunc(update)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)

    app.initGraphics()
    glutMainLoop()

    app.deinit()
