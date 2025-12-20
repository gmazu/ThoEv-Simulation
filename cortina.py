# cortina.py - Cortina curva configurable
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import time
import json

# Cargar config compartido
with open('config/config.json', 'r') as f:
    CONFIG = json.load(f)

RESOLUTION = tuple(CONFIG['render']['resolution'])
FPS = CONFIG['render']['fps']

VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec2 aPos;
out vec2 vPos;
void main() {
    vPos = aPos;
    gl_Position = vec4(aPos, 0.0, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec2 vPos;
uniform float u_time;
uniform vec2 u_resolution;
uniform float u_curvature;
out vec4 FragColor;

vec2 W(vec2 p, float t) {
    p = (p + 3.0) * 4.0;
    
    for (int i = 0; i < 3; i++) {
        p += cos(p.yx * 3.0 + vec2(t, 1.57)) / 3.0;
        p += sin(p.yx + t + vec2(1.57, 0.0)) / 2.0;
        p *= 1.3;
    }
    
    p += fract(sin(p + vec2(13, 7)) * 5e5) * 0.03 - 0.015;
    return mod(p, 2.0) - 1.0;
}

vec3 palette(float t) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.0, 0.33, 0.67);
    return a + b * cos(6.28318 * (c * t + d));
}

void main() {
    vec2 uv = vPos;
    uv.x *= u_resolution.x / u_resolution.y;
    
    float t = u_time * 0.5;
    
    // EL OCÉANO COMPLETO
    vec2 warped = W(uv * 0.3, t);
    float d = length(warped);
    
    d = sin(d * 8.0 + t) / 8.0;
    d = abs(d);
    d = 0.02 / d;
    
    vec3 col = palette(length(uv) + t * 0.3);
    vec3 pattern = col * d;
    
    // CORTINA CURVA que TAPA
    float duration = 3.0;
    float aspectRatio = u_resolution.x / u_resolution.y;
    
    // Posición base de la cortina
    float curtainPos = -aspectRatio + (u_time / duration) * (aspectRatio * 2.0);
    
    // Aplicar curvatura parabólica (como brana)
    float curtainCurved = curtainPos - u_curvature * uv.y * uv.y;
    
    // Máscara INVERTIDA con curvatura
    float visible = 1.0 - smoothstep(curtainCurved - 0.1, curtainCurved + 0.1, uv.x);
    
    vec3 finalColor = pattern * visible;
    
    FragColor = vec4(finalColor, 1.0);
}
"""

class Cortina:
    def __init__(self):
        glfw.init()
        self.window = glfw.create_window(RESOLUTION[0], RESOLUTION[1], "Cortina Curva", None, None)
        glfw.make_context_current(self.window)
        
        glViewport(0, 0, RESOLUTION[0], RESOLUTION[1])
        
        self.shader = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        )
        
        vertices = np.array([-1,-1, -1,1, 1,1, 1,-1], dtype=np.float32)
        
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        self.start = time.time()
    
    def run(self):
        while not glfw.window_should_close(self.window):
            t = time.time() - self.start
            
            if t > 6.0:
                break
            
            glClearColor(0, 0, 0, 1)
            glClear(GL_COLOR_BUFFER_BIT)
            
            glUseProgram(self.shader)
            glUniform1f(glGetUniformLocation(self.shader, "u_time"), t)
            glUniform2f(glGetUniformLocation(self.shader, "u_resolution"), RESOLUTION[0], RESOLUTION[1])
            # Usa curvatura del config (negativa para curvar hacia afuera como brana izquierda)
            glUniform1f(glGetUniformLocation(self.shader, "u_curvature"), CONFIG['branas']['curvature_right'])
            
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            time.sleep(1.0/FPS)
        
        glfw.terminate()

if __name__ == "__main__":
    Cortina().run()