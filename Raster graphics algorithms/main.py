#  ЛКМ - добавить новую вершину
#  ПКМ - замкнуть многоугольник
#  R - заливка
#  F - постфильтрация
#  C - очистить окно
#  Esc - закрыть окно

#  Задача:
#       - реализовать вывод многоугольника на экран
#       - реализовать алгоритм растровой развертки многоугольника
#         (построчное сканирование многоугольника со списком активных ребер)
#       - реализовать алгоритм фильтрации (постфильтрация с равномерным усреднением области 3*3)
#       - растеризацию производить в специально выделенном для этого буфере в памяти с
#         последующим копированием результата в буфер кадра OpenGL
#       - предусмотреть возможность изменения размеров окна
#       - предусмотреть интерактивный ввод исходных данных для алгоритмов

import glfw
from OpenGL.GL import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Edge:
    def __init__(self, p1, p2):
        if p1.y < p2.y:
            self.start = p1
            self.end = p2
        else:
            self.start = p2
            self.end = p1
        if self.start.y == self.end.y:
            self.dx = 0
        else:
            self.dx = (self.end.x - self.start.x) / (self.end.y - self.start.y)
        self.x_i = self.end.x


window_width = 640
window_height = 640
line_points = []
polygon_points = []
buf_size = window_width * window_height * 3
buffer = []
closed = 0
filling = 0
filtration = 0
color = [1, 1, 1]


def main():
    if not glfw.init():
        return
    window = glfw.create_window(window_width, window_height, "Lab4", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glfw.set_mouse_button_callback(window, mouse_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_window_size_callback(window, window_size_callback)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    for i in range(buf_size):
        buffer.append(0.0)

    while not glfw.window_should_close(window):
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()


def clear_buffer():
    buffer.clear()
    for i in range(buf_size):
        buffer.append(0.0)


def display():
    clear_buffer()
    draw_polygon(polygon_points)
    glDrawPixels(window_width, window_height, GL_RGB, GL_FLOAT, (GLfloat * buf_size)(*buffer))


def draw_polygon(points):
    n = len(points)
    if n == 1:
        set_pixel(points[0].x, points[0].y, color)
    elif n > 1:
        for i in range(n - 1):
            draw_line(points[i].x, points[i].y, points[i + 1].x, points[i + 1].y)
        if closed:
            draw_line(points[n - 1].x, points[n - 1].y, points[0].x, points[0].y)
        if filling:
            rasterization(polygon_points)
        if filtration:
            postfiltration()


# равномерное усреднение области 3*3
def postfiltration():
    global buffer
    for y in range(window_height):
        for x in range(window_width):
            r, g, b, count = 0, 0, 0, 0
            for i in range(x - 1, x + 2, 1):
                if 0 < i < window_width:
                    for j in range(y - 1, y + 2, 1):
                        if 0 < j < window_height:
                            count += 1
                            index = 3 * (i + window_width * j)
                            r += buffer[index]
                            g += buffer[index + 1]
                            b += buffer[index + 2]
            index = 3 * (x + window_width * y)
            buffer[index] = r / count
            buffer[index + 1] = g / count
            buffer[index + 2] = b / count


# построчное сканирование со списком активных ребер
def rasterization(points):
    global color
    edges = []
    y_max = 0
    y_min = points[0].y
    for i in range(len(points)):
        edges.append(Edge(points[i], points[(i + 1) % len(points)]))
        if edges[i].end.y > y_max:
            y_max = edges[i].end.y
        if edges[i].start.y < y_min:
            y_min = edges[i].start.y
    y_cur = y_max
    active_edges = []
    while y_cur >= y_min:
        for edge in reversed(active_edges):
            if edge.start.y >= y_cur:
                active_edges.remove(edge)
        for edge in edges:
            if edge.end.y == y_cur:
                if edge.start.y == edge.end.y:
                    draw_line(edge.start.x, edge.start.y, edge.end.x, edge.end.y)
                else:
                    active_edges.append(edge)
        intersections = []
        for edge in active_edges:
            intersections.append(edge.x_i)
            edge.x_i -= edge.dx
        intersections.sort()
        for i in range(0, len(intersections) - 1, 2):
            x = intersections[i]
            while x <= intersections[i + 1]:
                set_pixel(x, y_cur)
                x += 1
        y_cur -= 1


# целочисленный алгоритм Брезенхема
def draw_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        set_pixel(x1, y1)
        return
    s_x, s_y = 1, 1
    if dx < 0:
        dx = -dx
        s_x = -1
    if dy < 0:
        dy = -dy
        s_y = -1
    x = x1
    y = y1
    set_pixel(x, y)
    if dx > dy:
        e = -dx
        de = 2 * dy
        i = dx
        while i > 0:
            x += s_x
            e += de
            if e >= 0:
                y += s_y
                e -= 2 * dx
            set_pixel(x, y)
            i -= 1
    else:
        e = -dy
        de = 2 * dx
        i = dy
        while i:
            y += s_y
            e += de
            if e >= 0:
                x += s_x
                e -= 2 * dy
            set_pixel(x, y)
            i -= 1


def set_pixel(x, y, c=color):
    i = 3 * (int(x) + window_width * int(y))
    buffer[i] = c[0]
    buffer[i + 1] = c[1]
    buffer[i + 2] = c[2]


def mouse_callback(window, button, action, mods):
    global polygon_points, closed, filling
    pos = glfw.get_cursor_pos(window)
    if action == glfw.PRESS:
        if button == glfw.MOUSE_BUTTON_RIGHT:
            if filling:
                filling = 0
            closed += 1
            closed %= 2
        if button == glfw.MOUSE_BUTTON_LEFT:
            x = pos[0]
            y = window_height - pos[1]
            polygon_points.append(Point(x, y))


def window_size_callback(window, width, height):
    global window_width, window_height, buf_size, buffer, polygon_points
    window_width = width
    window_height = height
    glViewport(0, 0, width, height)
    buf_size = width * height * 3
    buffer.clear()
    for i in range(buf_size):
        buffer.append(0.0)
    polygon_points.clear()


def key_callback(window, key, scancode, action, mode):
    global polygon_points, closed, filling, filtration
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, 1)
        elif key == glfw.KEY_C:
            polygon_points = []
            closed = 0
            filling = 0
            filtration = 0
            clear_buffer()
        elif key == glfw.KEY_R:
            filling += 1
            filling %= 2
            closed = 1
        elif key == glfw.KEY_F:
            filtration += 1
            filtration %= 2


main()
