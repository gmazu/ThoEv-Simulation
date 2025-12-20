# main.py - Branas con estela → Bigbang
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
out vec4 FragColor;

vec3 palette(float t) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.263, 0.416, 0.557);
    return a + b * cos(6.28318 * (c * t + d));
}

float branaLine(vec2 uv, float xPos) {
    float distX = abs(uv.x - xPos);
    float glow = exp(-distX * 3.0);
    float fadeY = smoothstep(2.0, 0.0, abs(uv.y));
    return glow * fadeY;
}

float branaTrail(vec2 uv, float xPos, float direction) {
    float behind = (uv.x - xPos) * direction;
    if (behind < 0.0) return 0.0;
    float trail = exp(-behind * 0.5) * exp(-abs(uv.y) * 0.5);
    return trail * 0.3;
}

void main() {
    vec3 finalColor = vec3(0.0);
    
    // FASE 1: Branas (0-2 segundos)
    if (u_time < 2.0) {
        vec2 uvBranas = vPos * 1.0;
        uvBranas.x *= u_resolution.x / u_resolution.y;
        
        float progress = u_time / 2.0;
        float leftPos = -3.0 + (progress * 3.0);
        float rightPos = 3.0 - (progress * 3.0);
        
        float leftBrana = branaLine(uvBranas, leftPos);
        float rightBrana = branaLine(uvBranas, rightPos);
        float leftTrail = branaTrail(uvBranas, leftPos, -1.0);
        float rightTrail = branaTrail(uvBranas, rightPos, 1.0);
        
        vec3 leftColor = vec3(0.3, 0.7, 1.0);
        vec3 rightColor = vec3(1.0, 0.5, 0.2);
        
        finalColor = (leftBrana + leftTrail) * leftColor + 
                     (rightBrana + rightTrail) * rightColor;
    }
    // FASE 2: Bigbang (después de 2 segundos)
    else {
        vec2 uv = vPos * 10.0;
        uv.x *= u_resolution.x / u_resolution.y;
        vec2 uv0 = uv;
        
        float t = u_time - 2.0;
        
        for (float i = 0.0; i < 4.0; i++) {
            uv = fract(uv * 1.5) - 0.5;
            float d = length(uv) * exp(-length(uv0));
            vec3 col = palette(length(uv0) + i * 0.4 + t * 0.4);
            d = sin(d * 8.0 + t) / 8.0;
            d = abs(d);
            d = pow(0.01 / d, 1.2);
            finalColor += col * d;
        }
        
        // Fade in del bigbang
        float fadeIn = smoothstep(0.0, 0.5, t);
        finalColor *= fadeIn;
    }
    
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
            
            if t > 8.0:
                break
            
            glClearColor(0, 0, 0, 1)
            glClear(GL_COLOR_BUFFER_BIT)
            
            glUseProgram(self.shader)
            glUniform1f(glGetUniformLocation(self.shader, "u_time"), t)
            glUniform2f(glGetUniformLocation(self.shader, "u_resolution"), RESOLUTION[0], RESOLUTION[1])
            
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            time.sleep(1.0/FPS)
        
        glfw.terminate()

if __name__ == "__main__":
    Intro().run()
