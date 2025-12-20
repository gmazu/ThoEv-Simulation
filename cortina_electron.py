# cortina_electron.py - Gas de electrones azul con estela
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import time
import json

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

void main() {
    vec2 uv = vPos;
    uv.x *= u_resolution.x / u_resolution.y;
    
    float t = u_time * 0.5;
    
    // CORTINA CURVA (derecha → izquierda)
    float duration = 3.0;
    float aspectRatio = u_resolution.x / u_resolution.y;
    
    // Invertido: empieza desde la derecha
    float curtainPos = aspectRatio - (u_time / duration) * (aspectRatio * 2.0);
    
    // Aplicar curvatura (invertida para ir de derecha a izquierda)
    float curtainCurved = curtainPos - u_curvature * uv.y * uv.y;
    
    // Distancia desde la posición de la cortina
    float distFromCurtain = uv.x - curtainCurved;
    
    // ANILLO NEÓN (franja brillante en el borde)
    float ring = exp(-abs(distFromCurtain) * 20.0); // Anillo delgado
    float ringGlow = exp(-abs(distFromCurtain) * 5.0); // Glow amplio
    
    // ESTELA (solo detrás de la cortina - lado derecho)
    float trail = 0.0;
    if (distFromCurtain > 0.0) { // Lado derecho de la cortina
        trail = exp(-distFromCurtain * 2.0); // Desvanecimiento gradual
        trail *= exp(-abs(uv.y) * 0.5); // Fade vertical
    }
    
    // Color azul neón
    vec3 blueNeon = vec3(0.3, 0.7, 1.0);
    vec3 blueGlow = vec3(0.5, 0.8, 1.0);
    
    // Combinar anillo + estela
    vec3 finalColor = ring * blueNeon * 2.0 +      // Anillo brillante
                      ringGlow * blueGlow * 0.8 +   // Glow del anillo
                      trail * blueNeon * 0.3;       // Estela azul
    
    FragColor = vec4(finalColor, 1.0);
}
"""

class CortinaElectron:
    def __init__(self):
        glfw.init()
        self.window = glfw.create_window(RESOLUTION[0], RESOLUTION[1], "Gas de Electrones", None, None)
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
            glUniform1f(glGetUniformLocation(self.shader, "u_curvature"), CONFIG['branas']['curvature_right'])
            
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            time.sleep(1.0/FPS)
        
        glfw.terminate()

if __name__ == "__main__":
    CortinaElectron().run()
