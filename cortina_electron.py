# cortina_electron.py - Gas con flujo y turbulencia en borde
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

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    
    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));
    
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

float fbm(vec2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    
    for (int i = 0; i < 5; i++) {
        value += amplitude * noise(p * frequency);
        frequency *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}

vec2 curl(vec2 p, float t) {
    float eps = 0.1;
    float n1 = fbm(p + vec2(0.0, eps) + t * 0.1);
    float n2 = fbm(p + vec2(0.0, -eps) + t * 0.1);
    float n3 = fbm(p + vec2(eps, 0.0) + t * 0.1);
    float n4 = fbm(p + vec2(-eps, 0.0) + t * 0.1);
    
    float dx = (n1 - n2) / (2.0 * eps);
    float dy = (n3 - n4) / (2.0 * eps);
    
    return vec2(dy, -dx);
}

// Campo de velocidad del flujo
vec2 velocityField(vec2 p, float t) {
    // Flujo principal de derecha a izquierda
    vec2 mainFlow = vec2(-1.0, 0.0);
    
    // Perturbaciones sinusoidales
    vec2 wave = vec2(
        sin(p.y * 3.0 + t * 2.0) * 0.3,
        cos(p.x * 2.0 + t * 1.5) * 0.2
    );
    
    // Remolinos locales
    vec2 vortex = curl(p * 1.5, t) * 0.4;
    
    return mainFlow + wave + vortex;
}

void main() {
    vec2 uv = vPos;
    uv.x *= u_resolution.x / u_resolution.y;
    
    float t = u_time * 0.5;
    
    // ADVECCIÓN - el gas sigue el flujo
    vec2 flow = velocityField(uv, t);
    vec2 uvAdvected = uv;
    
    // Integrar flujo hacia atrás en el tiempo (backtracing)
    float dt = 0.05;
    for (int i = 0; i < 3; i++) {
        vec2 vel = velocityField(uvAdvected, t - float(i) * dt);
        uvAdvected -= vel * dt;
    }
    
    // Distorsión por curl
    vec2 distortion = curl(uvAdvected * 2.0, t) * 0.25;
    vec2 uvFinal = uvAdvected + distortion;
    
    // Turbulencia base
    float turbulence = fbm(uvFinal * 3.0 + t * 0.3);
    
    // Densidad del gas
    float density = turbulence * 0.6 + 0.3;
    
    // Remolinos visibles
    float vortex = length(curl(uvFinal * 4.0, t)) * 1.5;
    vortex = smoothstep(0.2, 0.7, vortex);
    
    // CORTINA CURVA
    float duration = 3.0;
    float aspectRatio = u_resolution.x / u_resolution.y;
    
    float curtainPos = aspectRatio - (u_time / duration) * (aspectRatio * 2.0);
    float curtainCurved = curtainPos - u_curvature * uv.y * uv.y;
    
    // Distancia al borde de la cortina
    float distToCurtain = abs(uv.x - curtainCurved);
    
    // TURBULENCIA EXTRA EN EL BORDE (inercia/fricción)
    float edgeTurbulence = 0.0;
    if (distToCurtain < 0.3) {
        // Turbulencia intensa cerca del borde
        float edgeNoise = fbm(uv * 8.0 + t * 3.0);
        edgeTurbulence = edgeNoise * (1.0 - distToCurtain / 0.3) * 0.5;
        
        // Vórtices en el borde
        vec2 edgeCurl = curl(uv * 10.0, t * 2.0);
        edgeTurbulence += length(edgeCurl) * 0.3;
    }
    
    // Color base
    vec3 gasBlue = vec3(0.3, 0.7, 1.0);
    vec3 glowBlue = vec3(0.5, 0.85, 1.0);
    vec3 edgeBlue = vec3(0.7, 0.9, 1.0);
    
    // Mezclar colores
    vec3 col = mix(gasBlue, glowBlue, turbulence);
    col *= density;
    
    // Vórtices brillan
    col += vec3(0.4, 0.8, 1.0) * vortex * 0.4;
    
    // Turbulencia en borde (más brillante)
    col += edgeBlue * edgeTurbulence * 0.8;
    
    // Glow atmosférico
    float atmosphericGlow = fbm(uvFinal * 1.5 + t * 0.2) * 0.3;
    col += gasBlue * atmosphericGlow * 0.15;
    
    // Máscara
    float visible = smoothstep(curtainCurved - 0.1, curtainCurved + 0.1, uv.x);
    
    vec3 finalColor = col * visible;
    
    FragColor = vec4(finalColor, 1.0);
}
"""

class CortinaElectron:
    def __init__(self):
        glfw.init()
        self.window = glfw.create_window(RESOLUTION[0], RESOLUTION[1], "Electronos - Gas en Flujo", None, None)
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