from OpenGL.GL import *
import glfw
from PIL import Image
import numpy

# Гравитация
G = 9.81
# Начальная скорость куба
INITIAL_CUBE_VELOCITY = 0
# Диапазон высот куба
CUBE_HEIGHT_RANGE = (0, 3000)

# Инициализация параметров
cube_velocity = INITIAL_CUBE_VELOCITY
cube_height = CUBE_HEIGHT_RANGE[1]
theta = 0

rot = 0
scale = 1
is_texturing_enabled = True


def normalize(x, x_range, normalization_range):
    a, b = normalization_range
    x_min, x_max = x_range
    return (b - a) * ((x - x_min) / (x_max - x_min)) + a


def program():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Lab8", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    setup()

    while not glfw.window_should_close(window):
        prepare()
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()


def key_callback(window, key, scancode, action, mods):
    global rot, scale, is_texturing_enabled

    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            rot -= 3
        if key == glfw.KEY_LEFT:
            rot += 3
        if key == glfw.KEY_UP:
            scale += 0.1
        if key == glfw.KEY_DOWN:
            scale -= 0.1
        if key == glfw.KEY_C:
            is_texturing_enabled = not is_texturing_enabled
            if is_texturing_enabled:
                enable_texturing()
            else:
                disable_texturing()


def enable_texturing():
    global is_texturing_enabled
    if is_texturing_enabled:
        glEnable(GL_TEXTURE_2D)


def disable_texturing():
    global is_texturing_enabled
    if is_texturing_enabled:
        glDisable(GL_TEXTURE_2D)


def setup():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-0.1, 0.1, -0.1, 0.1, 0.2, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)

    load_texture()

    vertex_shader = """
    varying vec3 n;
    varying vec3 v;
    varying vec2 uv;
    void main()
    {   
        uv = gl_MultiTexCoord0.xy;
        v = vec3(gl_ModelViewMatrix * gl_Vertex);
        n = normalize(gl_NormalMatrix * gl_Normal);
        gl_TexCoord[0] = gl_TextureMatrix[0]  * gl_MultiTexCoord0;
        gl_Position = ftransform();
    }
    """

    fragment_shader = """
    varying vec3 n;
    varying vec3 v; 
    uniform sampler2D tex;
    void main ()  
    {  
        vec3 L = normalize(gl_LightSource[0].position.xyz - v);   
        vec3 E = normalize(-v);
        vec3 R = normalize(-reflect(L,n));  
        //calculate Ambient Term:  
        vec4 Iamb = gl_FrontLightProduct[0].ambient;    
        //calculate Diffuse Term:  
        vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(n,L), 0.0);
        Idiff = clamp(Idiff, 0.0, 1.0);     
        // calculate Specular Term:
        vec4 Ispec = gl_LightSource[0].specular 
                        * pow(max(dot(R,E),0.0),0.3);
        Ispec = clamp(Ispec, 0.0, 1.0); 
        vec4 texColor = texture2D(tex, gl_TexCoord[0].st);
        gl_FragColor = (Idiff + Iamb + Ispec) * texColor;
    }
    """

    program = glCreateProgram()
    vertex = create_shader(GL_VERTEX_SHADER, vertex_shader)
    fragment = create_shader(GL_FRAGMENT_SHADER, fragment_shader)
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)
    glUseProgram(program)


def load_texture():
    img = Image.open("light.bmp")
    img_data = numpy.array(list(img.getdata()), numpy.int8)

    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)


def prepare():
    glClearColor(0.5, 0.5, 0.5, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def display():
    global CUBE_HEIGHT_RANGE, cube_velocity, cube_height, theta, rot, scale
    glPushMatrix()  # Сохраняем текущую матрицу преобразований
    glRotatef(-60, 1, 0, 0)  # Вращение сцены
    glRotatef(33, 0, 0, 1)  # Вращение сцены
    glTranslatef(2, 3, -2.5)  # Перемещение сцены

    glRotatef(rot, 0, 0, 1)  # Вращение куба
    glScalef(scale, scale, scale)  # Масштабирование куба

    glPushMatrix()  # Сохраняем текущую матрицу преобразований

    # Физика движения куба
    if cube_height - cube_velocity > CUBE_HEIGHT_RANGE[0]:
        cube_height -= cube_velocity
        if cube_velocity < 0 and cube_velocity + G > 0:
            cube_velocity = 0
        else:
            cube_velocity += G
    else:
        cube_height = CUBE_HEIGHT_RANGE[0]
        cube_velocity = -cube_velocity

    glRotatef(45, 0, 0, 1)  # Вращение куба
    glTranslatef(0, 0, normalize(cube_height, CUBE_HEIGHT_RANGE, (0.5, 1)))  # Перемещение куба по высоте
    glScalef(0.1, 0.1, 0.1)  # Масштабирование куба

    draw_cube()  # Отрисовка куба
    disable_texturing()  # Отключаем текстуру после отрисовки куба

    glPopMatrix()  # Восстанавливаем предыдущую матрицу преобразований

    # Отрисовка света
    glPushMatrix() 
    disable_texturing()   # Отключаем текстуру перед отрисовкой света
    glRotatef(45, 0, 1, 0)  # Вращение света
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 1, 0))  # Позиционирование света

    glTranslatef(0, 0, 2)  # Перемещение света
    glScalef(0.2, 0.2, 0.2)  # Масштабирование света
    glColor3f(1, 1, 1)  # Установка цвета света
    glPopMatrix()  # Восстанавливаем предыдущую матрицу преобразований

    glPopMatrix()  # Восстанавливаем предыдущую матрицу преобразований

    theta += 0.9  # Увеличение угла вращения для анимации


def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader


def draw_cube():
    enable_texturing()
    glBegin(GL_QUADS)

    glNormal3f(1.0, 0.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1, 1, 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1, -1, 1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1, -1, -1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1, 1, -1)

    glNormal3f(0.0, 0.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1, 1, -1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1, -1, -1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1, -1, -1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1, 1, -1)

    glNormal3f(-1.0, 0.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1, 1, -1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1, -1, -1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1, -1, 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1, 1, 1)

    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1, 1, 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1, -1, 1)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1, -1, 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1, 1, 1)

    glNormal3f(0.0, 1.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1, 1, -1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1, 1, 1)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1, 1, 1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1, 1, -1)

    glNormal3f(0.0, -1.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1, -1, 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1, -1, -1)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1, -1, -1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1, -1, 1)

    glEnd()
    disable_texturing()


def draw_plane():
    # Отключаем текстуру перед отрисовкой плоскости
    disable_texturing() 
    verticies = (
        -1, -1, 0,
        1, -1, 0,
        1, 1, 0,
        -1, 1, 0
    )

    normals = (
        0, 1, 0,
        0, 1, 0,
        0, 1, 0,
        0, 1, 0
    )

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, verticies)
    glNormalPointer(GL_FLOAT, 0, normals)
    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    # Включаем текстуру снова, если она была включена
    if is_texturing_enabled:
        enable_texturing() 


program()
