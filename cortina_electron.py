# cortina_electron.py - Gas de electrones con shader mercurio adaptado
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

float bumpFunc(vec2 p, float t) {
    return length(W(p, t)) * 0.7071;
}

void main() {
    vec2 uv = vPos;
    uv.x *= u_resolution.x / u_resolution.y;
    
    float t = u_time * 0.5;
    
    // BUMP MAPPING (más suave para gas)
    vec2 eps = vec2(4.0 / u_resolution.y, 0.0);
    
    float f = bumpFunc(uv, t);
    float fx = bumpFunc(uv - eps.xy, t);
    float fy = bumpFunc(uv - eps.yx, t);
    
    const float bumpFactor = 0.03; // Más suave que mercurio (era 0.05)
    
    fx = (fx - f) / eps.x;
    fy = (fy - f) / eps.x;
    
    vec3 sn = normalize(vec3(0.0, 0.0, -1.0) + vec3(fx, fy, 0.0) * bumpFactor);
    
    // LIGHTING (más difusa para gas)
    vec3 sp = vec3(uv, 0.0);
    vec3 rd = normalize(vec3(uv, 1.0));
    vec3 lp = vec3(cos(u_time) * 0.5, sin(u_time) * 0.2, -1.0);
    
    vec3 ld = lp - sp;
    float lDist = max(length(ld), 0.0001);
    ld /= lDist;
    
    float atten = 1.0 / (1.0 + lDist * lDist * 0.25); // Más atenuación
    atten *= f * 0.8 + 0.2;
    
    // Diffuse (más suave)
    float diff = max(dot(sn, ld), 0.0);
    diff = pow(diff, 2.0) * 0.5 + pow(diff, 4.0) * 0.5; // Menos intenso
    
    // Specular (muy reducido para gas)
    float spec = pow(max(dot(reflect(-ld, sn), -rd), 0.0), 8.0) * 0.3;
    
    // Color azul neón gaseoso
    vec3 gasBlue = vec3(0.3, 0.7, 1.0);
    vec3 texCol = gasBlue * (f * 0.4 + 0.6); // Más uniforme
    
    // Color final más difuso
    vec3 col = (texCol * (diff * vec3(0.9, 0.95, 1.0) * 1.5 + 0.5) + 
                vec3(0.5, 0.8, 1.0) * spec * 0.5) * atten;
    
    // Glow azul ambiental
    float glow = pow(f, 2.0) * 0.3;
    col += vec3(0.3, 0.6, 0.9) * glow;
    
    // CORTINA CURVA (derecha → izquierda)
    float duration = 3.0;
    float aspectRatio = u_resolution.x / u_resolution.y;
    
    float curtainPos = aspectRatio - (u_time / duration) * (aspectRatio * 2.0);
    float curtainCurved = curtainPos - u_curvature * uv.y * uv.y;
    
    // Máscara invertida - lo que está a la derecha queda visible (gas revelado)
    float visible = smoothstep(curtainCurved - 0.1, curtainCurved + 0.1, uv.x);
    
    vec3 finalColor = col * visible;
    
    FragColor = vec4(sqrt(clamp(finalColor, 0.0, 1.0)), 1.0);
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