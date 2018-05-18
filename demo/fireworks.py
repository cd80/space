from space.particle import Particle
from space.random import *
from space.constant import *
from application import Application

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from timing import TimingData

timing = TimingData()
timing.init()
timing.update()


class Firework(Particle, object):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.type = 0
        self.age = 0

    def update(self, duration):
        self.integrate(duration)
        self.age -= duration
        return self.age < 0 or self.position.y < 0


class FireworkRule:
    def __init__(self):
        self.type = 0
        self.min_age = 0
        self.max_age = 0
        self.min_velocity = 0
        self.max_velocity = 0
        self.damping = 0
        self.payload_count = 0
        self.payloads = []

    def init(self, payload_count):
        self.payload_count = payload_count
        self.payloads = [Payload() for _ in range(0, self.payload_count)]

    def create(self, parent=None, x=None, y=None):
        """
         original prototype in book is create(Firework *firework, Firework *parent)
         but because python doesn't support call-by-reference
         i made this to return a new firework
        """
        firework = Firework()
        firework.type = self.type
        firework.age = random_real(self.min_age, self.max_age)

        vel = Vector3()
        if parent is not None:
            firework.set_position(parent.get_position())
            vel += parent.get_velocity()
        else:
            start = Vector3()
            if x is not None:
                print x,
                start.x = x / (glutGet(GLUT_WINDOW_WIDTH) / 10.0) - 5
                print start.x
            else:
                x = random_int(3) - 1
                start.x = 5.0 * x
                print start.x

            firework.set_position(start)

        vel += random_vector(self.min_velocity, self.max_velocity)
        firework.set_velocity(vel)

        firework.set_mass(1)
        firework.set_damping(self.damping)
        firework.set_acceleration(CONSTANT_GRAVITY)
        firework.clear_accumulator()

        return firework

    def set_parameters(self, firework_type, min_age, max_age, min_velocity, max_velocity, damping):
        self.type = firework_type
        self.min_age = min_age
        self.max_age = max_age
        self.min_velocity = min_velocity
        self.max_velocity = max_velocity
        self.damping = damping


class Payload:
    def __init__(self):
        self.type = 0
        self.count = 0

    def set(self, firework_type, count):
        self.type = firework_type
        self.count = count


class FireworksDemo(Application, object):
    def __init__(self, next_firework=0):
        super(self.__class__, self).__init__()
        self.max_fireworks = 1024
        self.fireworks = [Firework() for _ in range(0, self.max_fireworks)]
        self.next_firework = next_firework
        self.rule_count = 9
        self.rules = [FireworkRule() for _ in range(0, self.rule_count)]
        self.mouse_x = 0
        self.mouse_y = 0

        for firework in self.fireworks:
            firework.type = 0

        self.init_firework_rules()

    def init_graphics(self):
        Application().init_graphics()

        glClearColor(0.0, 0.0, 0.1, 1.0)

    def get_title(self):
        return "Space > Fireworks Demo"

    def update(self):
        timing.update()
        duration = timing.get().lastFrameDuration * 0.001
        if duration <= 0.0:
            return

        for firework in self.fireworks:
            if firework.type <= 0:
                continue
            if firework.update(duration):
                rule = self.rules[firework.type-1]
                firework.type = 0

                for i in range(0, rule.payload_count):
                    payload = rule.payloads[i]
                    self.create(payload.type, firework, payload.count)
        Application().update()

    def display(self):
        size = 0.1
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0.0, 4.0, 10.0,  0.0, 4.0, 0.0,  0.0, 1.0, 0.0)

        glBegin(GL_QUADS)

        for firework in self.fireworks:
            if not firework.type:
                continue
            if firework.type == 1:
                glColor3f(1, 0, 0)
            elif firework.type == 2:
                glColor3f(1, 0.5, 0)
            elif firework.type == 3:
                glColor3f(1, 1, 0)
            elif firework.type == 4:
                glColor3f(0, 1, 0)
            elif firework.type == 5:
                glColor3f(0, 1, 1)
            elif firework.type == 6:
                glColor3f(0.4, 0.4, 1)
            elif firework.type == 7:
                glColor3f(1, 0, 1)
            elif firework.type == 8:
                glColor3f(1, 1, 1)
            elif firework.type == 9:
                glColor3f(1, 0.5, 0.5)

            pos = firework.get_position()
            glVertex3f(pos.x - size, pos.y - size, pos.z)
            glVertex3f(pos.x + size, pos.y - size, pos.z)
            glVertex3f(pos.x + size, pos.y + size, pos.z)
            glVertex3f(pos.x - size, pos.y + size, pos.z)

            glVertex3f(pos.x - size, -pos.y - size, pos.z)
            glVertex3f(pos.x + size, -pos.y - size, pos.z)
            glVertex3f(pos.x + size, -pos.y + size, pos.z)
            glVertex3f(pos.x - size, -pos.y + size, pos.z)
        glEnd()

    def key(self, key, x, y):
        self.mouse_x = x
        self.mouse_y = y
        key = int(key)
        if key == 1:
            self.create(1, None, 1)
        elif key == 2:
            self.create(2, None, 1)
        elif key == 3:
            self.create(3, None, 1)
        elif key == 4:
            self.create(4, None, 1)
        elif key == 5:
            self.create(5, None, 1)
        elif key == 6:
            self.create(6, None, 1)
        elif key == 7:
            self.create(7, None, 1)
        elif key == 8:
            self.create(8, None, 1)
        elif key == 9:
            self.create(9, None, 1)

    def create(self, firework_type, parent, number=0):
        """
        original prototype was
         1. void create(unsigned type, const Firework *parent=NULL);
         2. void create(unsigned type, unsigned number, const Firework *parent);
        """
        if number == 0:
            rule = self.rules[firework_type-1]
            self.fireworks[self.next_firework] = rule.create(parent, self.mouse_x)
            self.next_firework = (self.next_firework + 1) % self.max_fireworks
        else:
            for i in range(0, number):
                self.create(firework_type, parent)

    def init_firework_rules(self):
        self.rules[0].init(2)
        self.rules[0].set_parameters(
            1,  # type
            0.5, 1.4,  # age range
            Vector3(-5, 25, -5),  # min velocity
            Vector3(5, 28, 5),  # max velocity
            0.1  # damping
        )
        self.rules[0].payloads[0].set(3, 5)
        self.rules[0].payloads[0].set(5, 5)

        self.rules[1].init(1)
        self.rules[1].set_parameters(
            2,  # type
            0.5, 1.0,  # age range
            Vector3(-5, 10, -5),  # min velocity
            Vector3(5, 20, 5),  # max velocity
            0.8  # damping
        )
        self.rules[1].payloads[0].set(4, 2)

        self.rules[2].init(0)
        self.rules[2].set_parameters(
            3,  # type
            0.5, 1.5,  # age range
            Vector3(-5, -5, -5),  # min velocity
            Vector3(5, 5, 5),  # max velocity
            0.1  # damping
        )

        self.rules[3].init(0)
        self.rules[3].set_parameters(
            4,  # type
            0.25, 0.5,  # age range
            Vector3(-20, 5, -5),  # min velocity
            Vector3(20, 5, 5),  # max velocity
            0.2  # damping
        )

        self.rules[4].init(1)
        self.rules[4].set_parameters(
            5,  # type
            0.5, 1.0,  # age range
            Vector3(-20, 2, -5),  # min velocity
            Vector3(20, 18, 5),  # max velocity
            0.01  # damping
        )
        self.rules[4].payloads[0].set(3, 5)

        self.rules[5].init(0)
        self.rules[5].set_parameters(
            6,  # type
            3, 5,  # age range
            Vector3(-5, 5, -5),  # min velocity
            Vector3(5, 10, 5),  # max velocity
            0.95  # damping
        )

        self.rules[6].init(1)
        self.rules[6].set_parameters(
            7,  # type
            4, 5,  # age range
            Vector3(-5, 50, -5),  # min velocity
            Vector3(5, 60, 5),  # max velocity
            0.01  # damping
        )
        self.rules[6].payloads[0].set(8, 10)

        self.rules[7].init(0)
        self.rules[7].set_parameters(
            8,  # type
            0.25, 0.5,  # age range
            Vector3(-1, -1, -1),  # min velocity
            Vector3(1, 1, 1),  # max velocity
            0.01  # damping
        )

        self.rules[8].init(0)
        self.rules[8].set_parameters(
            9,  # type
            3, 5,  # age range
            Vector3(-15, 10, -5),  # min velocity
            Vector3(15, 15, 5),  # max velocity
            0.95  # damping
        )


def get_application():
    return FireworksDemo()
