import glfw
from OpenGL.GL import *
from math import *
import random
import time


def color_change():
    return [
        random.uniform(0, 1),
        random.uniform(0, 1),
        random.uniform(0, 1),
        1
    ]


angleX = 0.0
angleY = 0.0
angleZ = 0.0
scale = 1
size = 0.5
color = color_change()

tetta = pi / 5.1045
phi = pi / 4

l = None

newMatrix = [
    cos(tetta), -cos(phi) * sin(tetta), sin(tetta) * sin(phi), 0,
    -sin(tetta), -cos(phi) * cos(tetta), -sin(phi) * cos(tetta), 0,
    0, sin(tetta), cos(phi), 0,
    0, 0, 0, 1
]


def main():
    global l
    if not glfw.init():
        return
    window = glfw.create_window(700, 750, "Lab2", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    l = compile_list()
    while not glfw.window_should_close(window):
        start = time.time()
        display(window)
        end = time.time()
        print(end - start)
    glfw.destroy_window(window)
    glfw.terminate()


def key_callback(window, key, scancode, action, mods):
    global angleZ, angleX, angleY, scale, color
    if (action == glfw.REPEAT or action == glfw.PRESS):
        if key == glfw.KEY_RIGHT:
            angleZ -= 2
        if key == glfw.KEY_LEFT:
            angleZ += 2
        if key == glfw.KEY_A:
            angleX += 2
        if key == glfw.KEY_D:
            angleX -= 2
        if key == glfw.KEY_W:
            angleY += 2
        if key == glfw.KEY_S:
            angleY -= 2
        if key == glfw.KEY_F:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if key == glfw.KEY_B:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        if key == glfw.KEY_EQUAL:
            scale = scale * 1.05
        if key == glfw.KEY_MINUS:
            scale = scale * 0.95
        if key == glfw.KEY_C:
            color = color_change()


def compile_list():
    prism_list = glGenLists(1)
    glNewList(prism_list, GL_COMPILE)
    draw_cube_optimized()
    glEndList()
    return prism_list


verticies = [
    -1, -1, -1,
    -1, -1, 1,
    -1, 1, 1,
    1, 1, -1,
    -1, -1, -1,
    -1, 1, -1,
    1, -1, 1,
    -1, -1, -1,
    1, -1, -1,
    1, 1, -1,
    1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, 1, 1,
    -1, 1, -1,
    1, -1, 1,
    -1, -1, 1,
    -1, -1, -1,
    -1, 1, 1,
    -1, -1, 1,
    1, -1, 1,
    1, 1, 1,
    1, -1, -1,
    1, 1, -1,
    1, -1, -1,
    1, 1, 1,
    1, -1, 1,
    1, 1, 1,
    1, 1, -1,
    -1, 1, -1,
    1, 1, 1,
    -1, 1, -1,
    -1, 1, 1,
    1, 1, 1,
    -1, 1, 1,
    1, -1, 1
]


def draw_cube_optimized():
    global verticies, color
    glColor3f(*color[:3])  # Передаем только первые три элемента списка color
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, verticies)
    glDrawArrays(GL_TRIANGLES, 0, 36)
    glDisableClientState(GL_VERTEX_ARRAY)


def draw_cube():
    # Левая грань
    glBegin(GL_POLYGON)
    glColor3f(*color)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, -1, 1)
    glEnd()

    # Правая грань
    glBegin(GL_POLYGON)
    glColor3f(*color)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)
    glEnd()

    # Нижняя грань
    glBegin(GL_POLYGON)
    glColor3f(*color)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)
    glEnd()

    # Верхняя грань
    glBegin(GL_POLYGON)
    glColor3f(*color)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(1, 1, -1)
    glEnd()

    # Задняя грань
    glBegin(GL_POLYGON)
    glColor3f(*color)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glEnd()

    # Передняя грань
    glBegin(GL_POLYGON)
    glColor3f(*color)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)
    glVertex3f(1, 1, 1)
    glVertex3f(-1, 1, 1)
    glEnd()


def display(window):
    global color, l
    glEnable(GL_CULL_FACE)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMultMatrixd(newMatrix)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glRotatef(angleX, 1.0, 0.0, 0.0)
    glRotatef(angleY, 0.0, 1.0, 0.0)
    glRotatef(angleZ, 0.0, 0.0, 1.0)
    glScale(scale, scale, scale)

    # Двигающийся куб
    glPushMatrix()
    glScalef(0.5, 0.5, 0.5)
    glColor3f(1, 0, 1)
    glCallList(l)
    glPopMatrix()

    glfw.swap_buffers(window)
    glfw.poll_events()



if __name__ == '__main__':
    main()