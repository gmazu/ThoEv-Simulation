# main.py - Con branas que dejan estela
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
uniform float u_phase; // 0-2: branas, 2-5: mandala
out vec4 FragColor;

vec3 palette(float t) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.263, 0.416, 0.557);
    return a + b * cos(6.28318 * (c * t + d));
}

// Línea vertical con estela difuminada
float branaLine(vec2 uv, float xPos) {
    // Distancia horizontal a la línea
    float distX = abs(uv.x - xPos);
    
    // Estela exponencial (igual que el mandala)
    float glow = exp(-distX * 15.0);
    
    // Ancho vertical suave
    float fadeY = smoothstep(1.5, 0.0, abs(uv.y));
    
    return glow * fadeY;
}

void main() {
    vec2 uv = vPos * 13.0;
    uv.x *= u_resolution.x / u_resolution.y;
    vec2 uv0 = uv;
    
    vec3 finalColor = vec3(0.0);
    
    // FASE 1 y 2: Branas avanzando (0-2 segundos)
    if (u_phase < 2.0) {
        float progress = u_phase / 2.0;
        
        // Posiciones de las branas
        float leftPos = -3.0 + (progress * 3.0);  // Desde -3 hacia 0
        float rightPos = 3.0 - (progress * 3.0);   // Desde +3 hacia 0
        
        // Branas con estela
        float leftBrana = branaLine(uv, leftPos);
        float rightBrana = branaLine(uv, rightPos);
        
        // Colores diferentes
        vec3 leftColor = vec3(0.3, 0.7, 1.0);   // Azul
        vec3 rightColor = vec3(1.0, 0.5, 0.2);  // Naranja
        
        finalColor = leftBrana * leftColor + rightBrana * rightColor;
        
    } 
    // FASE 3: Mandala (después de 2 segundos)
    else {
        float mandalaTime = u_phase - 2.0;
        
        for (float i = 0.0; i < 4.0; i++) {
            uv = fract(uv * 1.5) - 0.5;
            
            float d = length(uv) * exp(-length(uv0));
            
            vec3 col = palette(length(uv0) + i * 0.4 + mandalaTime * 0.4);
            
            d = sin(d * 8.0 + mandalaTime) / 8.0;
            d = abs(d);
            
            d = pow(0.01 / d, 1.2);
            
            finalColor += col * d;
        }
        
        // Fade in del mandala
        float fadeIn = smoothstep(0.0, 0.5, mandalaTime);
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
            
            if t > 8.0:  # 8 segundos total
                break
            
            glClearColor(0, 0, 0, 1)
            glClear(GL_COLOR_BUFFER_BIT)
            
            glUseProgram(self.shader)
            glUniform1f(glGetUniformLocation(self.shader, "u_time"), t)
            glUniform2f(glGetUniformLocation(self.shader, "u_resolution"), RESOLUTION[0], RESOLUTION[1])
            glUniform1f(glGetUniformLocation(self.shader, "u_phase"), t)
            
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            time.sleep(1.0/FPS)
        
        glfw.terminate()

if __name__ == "__main__":
    Intro().run()
