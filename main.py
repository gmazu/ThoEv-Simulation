# main.py - Mandala procedural con shader
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import time

RESOLUTION = (1280, 720)
FPS = 60

VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec2 aPos;
out vec2 vPos;
uniform vec2 u_offset;
void main() {
    vPos = aPos;
    gl_Position = vec4(aPos.x + u_offset.x, aPos.y + u_offset.y, 0.0, 1.0);
}
"""

# Shader que genera patrón de onda gravitacional
FRAGMENT_SHADER = """
#version 330 core
in vec2 vPos;
uniform float u_time;
uniform bool u_show_mandala;
uniform vec3 u_color;
out vec4 FragColor;

void main() {
    if (!u_show_mandala) {
        FragColor = vec4(u_color, 1.0);
        return;
    }
    
    // Distancia al centro
    float dist = length(vPos);
    
    // Múltiples ondas concéntricas
    float wave1 = sin(dist * 20.0 - u_time * 2.0);
    float wave2 = sin(dist * 15.0 + u_time * 1.5);
    float wave3 = sin(dist * 25.0 - u_time * 2.5);
    
    // Patrón angular (8 rayos)
    float angle = atan(vPos.y, vPos.x);
    float angular = sin(angle * 4.0) * 0.5 + 0.5;
    
    // Combinar ondas
    float pattern = (wave1 + wave2 + wave3) * 0.333;
    pattern *= angular;
    
    // Aberración cromática (separación RGB)
    float r = sin(dist * 18.0 - u_time * 2.0 + 0.0) * 0.5 + 0.5;
    float g = sin(dist * 20.0 - u_time * 2.0 + 2.0) * 0.5 + 0.5;
    float b = sin(dist * 22.0 - u_time * 2.0 + 4.0) * 0.5 + 0.5;
    
    // Intensidad desde centro
    float glow = 1.0 / (1.0 + dist * dist * 2.0);
    
    vec3 color = vec3(r, g, b) * glow * (pattern * 0.5 + 0.5);
    
    FragColor = vec4(color, 1.0);
}
"""

class Intro:
    def __init__(self):
        glfw.init()
        self.window = glfw.create_window(RESOLUTION[0], RESOLUTION[1], "ThöEv", None, None)
        glfw.make_context_current(self.window)
        
        self.shader = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        )
        
        # Columna
        col_vertices = np.array([
            -0.1, -0.8,
            -0.1,  0.8,
             0.1,  0.8,
             0.1, -0.8
        ], dtype=np.float32)
        
        self.vao_col = glGenVertexArrays(1)
        self.vbo_col = glGenBuffers(1)
        
        glBindVertexArray(self.vao_col)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_col)
        glBufferData(GL_ARRAY_BUFFER, col_vertices.nbytes, col_vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Pantalla completa para mandala
        screen_vertices = np.array([
            -1, -1,
            -1,  1,
             1,  1,
             1, -1
        ], dtype=np.float32)
        
        self.vao_screen = glGenVertexArrays(1)
        self.vbo_screen = glGenBuffers(1)
        
        glBindVertexArray(self.vao_screen)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_screen)
        glBufferData(GL_ARRAY_BUFFER, screen_vertices.nbytes, screen_vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        self.start = time.time()
        self.collision_happened = False
    
    def draw_column(self, x_pos, color):
        glUseProgram(self.shader)
        loc_offset = glGetUniformLocation(self.shader, "u_offset")
        loc_color = glGetUniformLocation(self.shader, "u_color")
        loc_mandala = glGetUniformLocation(self.shader, "u_show_mandala")
        
        glUniform2f(loc_offset, x_pos, 0.0)
        glUniform3f(loc_color, color[0], color[1], color[2])
        glUniform1i(loc_mandala, 0)
        
        glBindVertexArray(self.vao_col)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
    
    def draw_mandala(self, time_val):
        glUseProgram(self.shader)
        loc_time = glGetUniformLocation(self.shader, "u_time")
        loc_mandala = glGetUniformLocation(self.shader, "u_show_mandala")
        loc_offset = glGetUniformLocation(self.shader, "u_offset")
        
        glUniform1f(loc_time, time_val)
        glUniform1i(loc_mandala, 1)
        glUniform2f(loc_offset, 0.0, 0.0)
        
        glBindVertexArray(self.vao_screen)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
    
    def run(self):
        while not glfw.window_should_close(self.window):
            t = time.time() - self.start
            
            glClearColor(0, 0, 0, 1)
            glClear(GL_COLOR_BUFFER_BIT)
            
            pos_left = -1.5 + (t * 0.2)
            pos_right = 1.5 - (t * 0.2)
            
            # Detectar contacto
            if pos_left >= -0.1 and pos_right <= 0.1 and not self.collision_happened:
                self.collision_happened = True
                self.collision_time = t
                print("¡CONTACTO! - Generando mandala...")
            
            if self.collision_happened:
                # Mostrar mandala generado proceduralmente
                time_since = t - self.collision_time
                self.draw_mandala(time_since)
            else:
                # Columnas avanzando
                self.draw_column(pos_left, (0.3, 0.7, 1.0))
                self.draw_column(pos_right, (1.0, 0.4, 0.3))
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            time.sleep(1.0/FPS)
        
        glfw.terminate()

if __name__ == "__main__":
    Intro().run()
