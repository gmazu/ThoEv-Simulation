# branas.py - Con curvatura configurable
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

uniform float u_collision_time;
uniform float u_brana_scale;
uniform float u_brana_speed;
uniform float u_brana_width;
uniform float u_brana_core;
uniform float u_brana_curvature;
uniform vec3 u_brana_left_color;
uniform vec3 u_brana_right_color;

uniform float u_proton_size;
uniform float u_proton_density;
uniform vec3 u_proton_color;
uniform float u_electron_size;
uniform float u_electron_density;
uniform vec3 u_electron_color;
uniform float u_particle_grid;
uniform float u_particle_brightness;

uniform float u_trail_decay;
uniform float u_trail_intensity;

uniform float u_mandala_scale;
uniform float u_mandala_iterations;
uniform float u_mandala_speed;
uniform float u_mandala_fade;

uniform vec3 u_palette_a;
uniform vec3 u_palette_b;
uniform vec3 u_palette_c;
uniform vec3 u_palette_d;

uniform float u_contrast;

out vec4 FragColor;

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

vec3 palette(float t) {
    return u_palette_a + u_palette_b * cos(6.28318 * (u_palette_c * t + u_palette_d));
}

float circle(vec2 p, float r) {
    return length(p) - r;
}

float particles(vec2 uv, float seed, float size, float density) {
    vec2 gridPos = floor(uv * u_particle_grid);
    float particleHash = hash(gridPos + seed);
    
    if (particleHash > density) return 0.0;
    
    vec2 localPos = fract(uv * u_particle_grid) - 0.5;
    float dist = circle(localPos, size);
    
    float glow = smoothstep(0.1, 0.0, dist);
    glow += 0.5 / (abs(dist) * 50.0 + 1.0);
    
    return glow * (particleHash - density) * u_particle_brightness;
}

float branaCurve(vec2 uv, float xPos) {
    // Curvatura parabólica desde config
    float xCurved = xPos + u_brana_curvature * uv.y * uv.y;
    
    float distX = abs(uv.x - xCurved);
    float core = smoothstep(u_brana_core, 0.0, distX);
    float glow = exp(-distX * u_brana_width);
    float fadeY = smoothstep(2.0, 0.0, abs(uv.y));
    return (core * 0.7 + glow * 0.3) * fadeY;
}

float branaTrail(vec2 uv, float xPos, float direction) {
    float behind = (uv.x - xPos) * direction;
    if (behind < 0.0) return 0.0;
    float trail = exp(-behind * u_trail_decay) * exp(-abs(uv.y) * 0.6);
    return trail * u_trail_intensity;
}

void main() {
    vec2 uv = vPos;
    uv.x *= u_resolution.x / u_resolution.y;
    
    vec3 finalColor = vec3(0.0);
    
    if (u_time < u_collision_time) {
        vec2 uvBranas = uv * u_brana_scale;
        
        float progress = u_time / u_collision_time;
        float leftPos = -u_brana_speed + (progress * u_brana_speed);
        float rightPos = u_brana_speed - (progress * u_brana_speed);
        
        float leftBrana = branaCurve(uvBranas, leftPos);
        float rightBrana = branaCurve(uvBranas, rightPos);
        float leftTrail = branaTrail(uvBranas, leftPos, -1.0);
        float rightTrail = branaTrail(uvBranas, rightPos, 1.0);
        
        vec2 uvLeft = uvBranas - vec2(leftPos, 0.0);
        vec2 uvRight = uvBranas - vec2(rightPos, 0.0);
        
        float protones = particles(uvLeft, 1.0, u_proton_size, u_proton_density) * leftBrana;
        float electrones = particles(uvRight, 2.0, u_electron_size, u_electron_density) * rightBrana;
        
        finalColor = (leftBrana + leftTrail) * u_brana_left_color + 
                     (rightBrana + rightTrail) * u_brana_right_color +
                     protones * u_proton_color +
                     electrones * u_electron_color;
    }
    else {
        vec2 uvMandala = uv * u_mandala_scale;
        vec2 uv0 = uvMandala;
        
        float t = u_time - u_collision_time;
        
        for (float i = 0.0; i < u_mandala_iterations; i++) {
            uvMandala = fract(uvMandala * 1.5) - 0.5;
            float d = length(uvMandala) * exp(-length(uv0));
            vec3 col = palette(length(uv0) + i * 0.4 + t * u_mandala_speed);
            d = sin(d * 8.0 + t) / 8.0;
            d = abs(d);
            d = pow(0.01 / d, 1.2);
            finalColor += col * d;
        }
        
        float fadeIn = smoothstep(0.0, u_mandala_fade, t);
        finalColor *= fadeIn;
        finalColor = pow(finalColor, vec3(u_contrast));
    }
    
    FragColor = vec4(finalColor, 1.0);
}
"""

class Intro:
    def __init__(self):
        glfw.init()
        self.window = glfw.create_window(RESOLUTION[0], RESOLUTION[1], "ThöEv", None, None)
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
    
    def set_uniforms(self, t):
        glUseProgram(self.shader)
        
        glUniform1f(glGetUniformLocation(self.shader, "u_time"), t)
        glUniform2f(glGetUniformLocation(self.shader, "u_resolution"), RESOLUTION[0], RESOLUTION[1])
        
        glUniform1f(glGetUniformLocation(self.shader, "u_collision_time"), CONFIG['timing']['collision_time'])
        
        glUniform1f(glGetUniformLocation(self.shader, "u_brana_scale"), CONFIG['branas']['scale'])
        glUniform1f(glGetUniformLocation(self.shader, "u_brana_speed"), CONFIG['branas']['speed'])
        glUniform1f(glGetUniformLocation(self.shader, "u_brana_width"), CONFIG['branas']['width'])
        glUniform1f(glGetUniformLocation(self.shader, "u_brana_core"), CONFIG['branas']['core'])
        glUniform1f(glGetUniformLocation(self.shader, "u_brana_curvature"), CONFIG['branas']['curvature'])
        glUniform3f(glGetUniformLocation(self.shader, "u_brana_left_color"), *CONFIG['branas']['left_color'])
        glUniform3f(glGetUniformLocation(self.shader, "u_brana_right_color"), *CONFIG['branas']['right_color'])
        
        glUniform1f(glGetUniformLocation(self.shader, "u_proton_size"), CONFIG['particles']['proton_size'])
        glUniform1f(glGetUniformLocation(self.shader, "u_proton_density"), CONFIG['particles']['proton_density'])
        glUniform3f(glGetUniformLocation(self.shader, "u_proton_color"), *CONFIG['particles']['proton_color'])
        glUniform1f(glGetUniformLocation(self.shader, "u_electron_size"), CONFIG['particles']['electron_size'])
        glUniform1f(glGetUniformLocation(self.shader, "u_electron_density"), CONFIG['particles']['electron_density'])
        glUniform3f(glGetUniformLocation(self.shader, "u_electron_color"), *CONFIG['particles']['electron_color'])
        glUniform1f(glGetUniformLocation(self.shader, "u_particle_grid"), CONFIG['particles']['grid_density'])
        glUniform1f(glGetUniformLocation(self.shader, "u_particle_brightness"), CONFIG['particles']['brightness'])
        
        glUniform1f(glGetUniformLocation(self.shader, "u_trail_decay"), CONFIG['trail']['decay'])
        glUniform1f(glGetUniformLocation(self.shader, "u_trail_intensity"), CONFIG['trail']['intensity'])
        
        glUniform1f(glGetUniformLocation(self.shader, "u_mandala_scale"), CONFIG['mandala']['scale'])
        glUniform1f(glGetUniformLocation(self.shader, "u_mandala_iterations"), CONFIG['mandala']['iterations'])
        glUniform1f(glGetUniformLocation(self.shader, "u_mandala_speed"), CONFIG['mandala']['speed'])
        glUniform1f(glGetUniformLocation(self.shader, "u_mandala_fade"), CONFIG['mandala']['fade_in'])
        
        glUniform3f(glGetUniformLocation(self.shader, "u_palette_a"), *CONFIG['palette']['a'])
        glUniform3f(glGetUniformLocation(self.shader, "u_palette_b"), *CONFIG['palette']['b'])
        glUniform3f(glGetUniformLocation(self.shader, "u_palette_c"), *CONFIG['palette']['c'])
        glUniform3f(glGetUniformLocation(self.shader, "u_palette_d"), *CONFIG['palette']['d'])
        
        glUniform1f(glGetUniformLocation(self.shader, "u_contrast"), CONFIG['post']['contrast'])
    
    def run(self):
        while not glfw.window_should_close(self.window):
            t = time.time() - self.start
            
            if t > CONFIG['render']['duration']:
                break
            
            glClearColor(0, 0, 0, 1)
            glClear(GL_COLOR_BUFFER_BIT)
            
            self.set_uniforms(t)
            
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            time.sleep(1.0/FPS)
        
        glfw.terminate()

if __name__ == "__main__":
    Intro().run()