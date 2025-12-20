# main.py - ThöEv completo mejorado
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

// Hash para partículas
float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

// Paleta mejorada
vec3 palette(float t) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.263, 0.416, 0.557);
    return a + b * cos(6.28318 * (c * t + d));
}

// SDF círculo para partículas
float circle(vec2 p, float r) {
    return length(p) - r;
}

// Partículas brillantes (protones o electrones)
float particles(vec2 uv, float seed, float size, float density) {
    vec2 gridPos = floor(uv * 15.0);
    float particleHash = hash(gridPos + seed);
    
    if (particleHash > density) return 0.0;
    
    vec2 localPos = fract(uv * 15.0) - 0.5;
    float dist = circle(localPos, size);
    
    // Glow neón
    float glow = smoothstep(0.1, 0.0, dist);
    glow += 0.5 / (abs(dist) * 50.0 + 1.0);
    
    return glow * (particleHash - density) * 5.0;
}

// Brana con SDF mejorado
float branaLine(vec2 uv, float xPos) {
    float distX = abs(uv.x - xPos);
    
    // SDF con smoothstep para bordes definidos
    float core = smoothstep(0.15, 0.0, distX);
    float glow = exp(-distX * 3.0);
    
    float fadeY = smoothstep(2.0, 0.0, abs(uv.y));
    
    return (core * 0.7 + glow * 0.3) * fadeY;
}

// Estela mejorada
float branaTrail(vec2 uv, float xPos, float direction) {
    float behind = (uv.x - xPos) * direction;
    if (behind < 0.0) return 0.0;
    
    float trail = exp(-behind * 0.8) * exp(-abs(uv.y) * 0.6);
    return trail * 0.4;
}

void main() {
    vec3 finalColor = vec3(0.0);
    
    // FASE 1: Branas con partículas (0-2 segundos)
    if (u_time < 2.0) {
        vec2 uvBranas = vPos * 1.0;
        uvBranas.x *= u_resolution.x / u_resolution.y;
        
        float progress = u_time / 2.0;
        float leftPos = -3.0 + (progress * 3.0);
        float rightPos = 3.0 - (progress * 3.0);
        
        // Branas base
        float leftBrana = branaLine(uvBranas, leftPos);
        float rightBrana = branaLine(uvBranas, rightPos);
        float leftTrail = branaTrail(uvBranas, leftPos, -1.0);
        float rightTrail = branaTrail(uvBranas, rightPos, 1.0);
        
        // Partículas dentro de branas
        vec2 uvLeft = uvBranas - vec2(leftPos, 0.0);
        vec2 uvRight = uvBranas - vec2(rightPos, 0.0);
        
        // Protones azules en brana izquierda (pequeños)
        float protones = particles(uvLeft, 1.0, 0.02, 0.85) * leftBrana;
        
        // Electrones rojos en brana derecha (más pequeños)
        float electrones = particles(uvRight, 2.0, 0.015, 0.88) * rightBrana;
        
        vec3 leftColor = vec3(0.3, 0.7, 1.0);
        vec3 rightColor = vec3(1.0, 0.5, 0.2);
        
        // Color partículas
        vec3 protonColor = vec3(0.5, 0.8, 1.0);
        vec3 electronColor = vec3(1.0, 0.3, 0.2);
        
        finalColor = (leftBrana + leftTrail) * leftColor + 
                     (rightBrana + rightTrail) * rightColor +
                     protones * protonColor +
                     electrones * electronColor;
    }
    // FASE 2: Bigbang mejorado (después de 2 segundos)
    else {
        vec2 uv = vPos * 3.0;
        uv.x *= u_resolution.x / u_resolution.y;
        vec2 uv0 = uv;
        
        float t = u_time - 2.0;
        
        // 6 iteraciones fractales (era 4)
        for (float i = 0.0; i < 6.0; i++) {
            uv = fract(uv * 1.5) - 0.5;
            
            float d = length(uv) * exp(-length(uv0));
            
            vec3 col = palette(length(uv0) + i * 0.4 + t * 0.4);
            
            d = sin(d * 8.0 + t) / 8.0;
            d = abs(d);
            
            // Neón intenso
            d = pow(0.01 / d, 1.2);
            
            finalColor += col * d;
        }
        
        // Transición suave
        float fadeIn = smoothstep(0.0, 0.8, t);
        finalColor *= fadeIn;
        
        // Contraste final
        finalColor = pow(finalColor, vec3(0.9));
    }
    
    FragColor = vec4(finalColor, 1.0);
}
"""

class Intro:
    def __init__(self):
        glfw.init()
        self.window = glfw.create_window(RESOLUTION[0], RESOLUTION[1], "ThöEv - Completo", None, None)
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
            
            if t > 10.0:
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
