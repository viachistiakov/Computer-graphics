import glfw
from OpenGL.GL import *
from math import *

mode = 0
angle = 0
x = 0.0
y = 0.0


def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Lab2", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


def cube():

    glBegin(GL_POLYGON)
    glColor3f(1.0, 0, 0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(0.5, 0, 0)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(0, 1, 0)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(0.0, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(1, 0.0, 2)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glEnd()


def display(window):
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(640 - 160, 640 - 160, 160, 160)
    glLoadIdentity()
    glClearColor(0, 0, 0, 0)

    rotate_x = [
        1, 0, 0, 0,
        0, cos(x), sin(x), 0,
        0, -sin(x), cos(x), 0,
        0, 0, 0, 1
    ]

    rotate_y = [
        cos(y), 0, -sin(y), 0, 0, 1, 0, 0, sin(y), 0, cos(y), 0, 0, 0, 0, 1
    ]

    mat1 = [1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, -1, 0,
            0, 0, 0, 1]
    mat2 = [0, 0, -1, 0,
            0, 1, 0, 0,
            -1, 0, 0, 0,
            0, 0, 0, 1]
    mat3 = [1, 0, 0, 0,
            0, 0, -1, 0,
            0, -1, 0, 0,
            0, 0, 0, 1]

    if mode == 0:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glPushMatrix()
    # glMultMatrixf(rotate_x)
    # glMultMatrixf(rotate_y)
    cube()
    glRotate(20, 20, 20, 45)

    glPopMatrix()

    glViewport(640 - 3 * 160, 640 - 160, 160, 160)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMultMatrixf(mat1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMultMatrixf(rotate_x)
    glMultMatrixf(rotate_y)
    cube()

    glViewport(640 - 3 * 160, 640 - 3 * 160, 160, 160)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMultMatrixf(mat2)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMultMatrixf(rotate_x)
    glMultMatrixf(rotate_y)
    cube()

    glViewport(640 - 160, 640 - 3 * 160, 160, 160)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMultMatrixf(mat3)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMultMatrixf(rotate_x)
    glMultMatrixf(rotate_y)
    cube()

    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global mode, x, y
    if key == glfw.KEY_RIGHT:
        y += 0.25

    if key == glfw.KEY_LEFT:
        y -= 0.25

    if key == glfw.KEY_UP:
        x += 0.25

    if key == glfw.KEY_DOWN:
        x -= 0.25
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            mode = (mode + 1) % 2


def scroll_callback(window, xoffset, yoffset):
    pass
main()
