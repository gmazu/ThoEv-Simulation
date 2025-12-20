# main.py - Un solo mandala central
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import time

RESOLUTION = (1280, 720)
FPS = 30

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
uniform float u_phase;
out vec4 FragColor;

vec3 palette(float t) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.0, 0.33, 0.67);
    return a + b * cos(6.28318 * (c * t + d));
}

void main() {
    vec2 uv = (vPos * 2.0 - vec2(1.0)) * vec2(u_resolution.x / u_resolution.y, 1.0);
    vec2 uv0 = uv;
    vec3 finalColor = vec3(0.0);
    
    // Solo 1 mandala central
    for (float i = 0.0; i < 3.0; i++) {
        float d = length(uv);
        
        vec3 col = palette(length(uv0) + i * 0.4 + u_time * 0.4);
        
        d = sin(d * 8.0 + u_time) / 8.0;
        d = abs(d);
        
        d = 0.02 / d;
        
        finalColor += col * d;
        
        // Rotar para siguiente capa
        float angle = u_time * 0.5 + i;
        mat2 rot = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
        uv = rot * uv * 1.3;
    }
    
    finalColor *= u_phase;
    
    FragColor = vec4(finalColor, 1.0);
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
            
            if t > 5.0:
                break
            
            glClearColor(0, 0, 0, 1)
            glClear(GL_COLOR_BUFFER_BIT)
            
            phase = min(t / 2.0, 1.0)
            
            glUseProgram(self.shader)
            glUniform1f(glGetUniformLocation(self.shader, "u_time"), t)
            glUniform2f(glGetUniformLocation(self.shader, "u_resolution"), RESOLUTION[0], RESOLUTION[1])
            glUniform1f(glGetUniformLocation(self.shader, "u_phase"), phase)
            
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            time.sleep(1.0/FPS)
        
        glfw.terminate()

if __name__ == "__main__":
    Intro().run()
