from demo import fireworks
from OpenGL.GL import *
from OpenGL.GLUT import *
import logging
import sys
logging.basicConfig()


def create_window(title):
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
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
    app.key(key, x, y)


def motion(x, y):
    app.mouse_drag(x, y)

if __name__ == '__main__':

    glutInit(sys.argv)

    app = fireworks.get_application()
    create_window(app.get_title())

    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display)
    glutIdleFunc(update)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)

    app.init_graphics()
    glutMainLoop()

    app.deinit()
