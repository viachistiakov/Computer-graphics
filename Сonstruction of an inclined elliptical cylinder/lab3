import pygame
from pygame.locals import *
from OpenGL.GL import *
import math
from OpenGL.GLU import *

vertices = []
edges = []
radius_a = 0.5  # большая полуось эллипса
radius_b = 0.3  # малая полуось эллипса
height = 1.0
slices = 50

def create_cylinder():
    for i in range(slices):
        angle = 2 * i * 3.14 / slices
        x = radius_a * math.cos(angle)
        y = radius_b * math.sin(angle)
        z1 = height / 2.0
        z2 = -height / 2.0
        vertices.append((x, y, z1))
        vertices.append((x, y, z2))
        edges.append((2*i, 2*i+1))
        edges.append(((2*i+2) % (2*slices), (2*i+4) % (2*slices)))
        edges.append(((2*i+1) % (2*slices), (2*i+3) % (2*slices)))

def draw_cylinder():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    create_cylinder()

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glRotatef(1, 1, 1, 1)
        draw_cylinder()
        pygame.display.flip()
        pygame.time.wait(10)
main()
