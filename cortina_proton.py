# cortina_proton.py - Océano de mercurio metálico
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import time
import json
import ctypes
from render_utils import VideoRenderer, parse_render_args

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

// Bump function para superficie
float bumpFunc(vec2 p, float t) {
    return length(W(p, t)) * 0.7071;
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
    
    // BUMP MAPPING
    vec2 eps = vec2(4.0 / u_resolution.y, 0.0);
    
    float f = bumpFunc(uv, t);
    float fx = bumpFunc(uv - eps.xy, t);
    float fy = bumpFunc(uv - eps.yx, t);
    
    const float bumpFactor = 0.05;
    
    fx = (fx - f) / eps.x;
    fy = (fy - f) / eps.x;
    
    // Normal perturbada
    vec3 sn = normalize(vec3(0.0, 0.0, -1.0) + vec3(fx, fy, 0.0) * bumpFactor);
    
    // LIGHTING
    vec3 sp = vec3(uv, 0.0);
    vec3 rd = normalize(vec3(uv, 1.0));
    vec3 lp = vec3(cos(u_time) * 0.5, sin(u_time) * 0.2, -1.0);
    
    vec3 ld = lp - sp;
    float lDist = max(length(ld), 0.0001);
    ld /= lDist;
    
    float atten = 1.0 / (1.0 + lDist * lDist * 0.15);
    atten *= f * 0.9 + 0.1;
    
    // Diffuse
    float diff = max(dot(sn, ld), 0.0);
    diff = pow(diff, 4.0) * 0.66 + pow(diff, 8.0) * 0.34;
    
    // Specular
    float spec = pow(max(dot(reflect(-ld, sn), -rd), 0.0), 12.0);
    
    // Color mercurio metálico
    vec3 mercuryBase = vec3(0.8, 0.85, 0.9); // Plateado
    vec3 texCol = mercuryBase * (f * 0.5 + 0.5);
    
    // Color final con iluminación
    vec3 col = (texCol * (diff * vec3(1.0, 0.97, 0.92) * 2.0 + 0.5) + 
                vec3(1.0, 0.9, 0.8) * spec * 2.0) * atten;
    
    // Reflexión ambiental
    float ref = max(dot(reflect(rd, sn), vec3(1.0)), 0.0);
    col += col * pow(ref, 4.0) * vec3(0.4, 0.5, 0.6) * 2.0;
    
    // CORTINA CURVA
    float duration = 3.0;
    float aspectRatio = u_resolution.x / u_resolution.y;
    
    float curtainPos = -aspectRatio + (u_time / duration) * (aspectRatio * 2.0);
    float curtainCurved = curtainPos + u_curvature * uv.y * uv.y;
    
    float visible = 1.0 - smoothstep(curtainCurved - 0.1, curtainCurved + 0.1, uv.x);
    
    vec3 finalColor = col * visible;
    
    FragColor = vec4(sqrt(clamp(finalColor, 0.0, 1.0)), 1.0);
}
"""

class Cortina:
    def __init__(self, render_video=False):
        glfw.init()
        self.window = glfw.create_window(RESOLUTION[0], RESOLUTION[1], "Mercurio Líquido", None, None)
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

        # Video renderer
        self.renderer = VideoRenderer(RESOLUTION[0], RESOLUTION[1], FPS, "cortina_mercurio.mp4")
        if render_video:
            self.renderer.enable()
    
    def run(self):
        duration = 3.0
        frame_time = 1.0 / FPS

        if self.renderer.enabled:
            # Renderizado controlado por frames para video
            total_frames = int(duration * FPS)
            for frame in range(total_frames):
                if glfw.window_should_close(self.window):
                    break

                t = frame * frame_time

                glClearColor(0, 0, 0, 1)
                glClear(GL_COLOR_BUFFER_BIT)

                glUseProgram(self.shader)
                glUniform1f(glGetUniformLocation(self.shader, "u_time"), t)
                glUniform2f(glGetUniformLocation(self.shader, "u_resolution"), RESOLUTION[0], RESOLUTION[1])
                glUniform1f(glGetUniformLocation(self.shader, "u_curvature"), CONFIG['branas']['curvature_left'])

                glBindVertexArray(self.vao)
                glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

                self.renderer.capture_frame()

                glfw.swap_buffers(self.window)
                glfw.poll_events()

            self.renderer.generate_video()
        else:
            # Demo en tiempo real
            while not glfw.window_should_close(self.window):
                t = time.time() - self.start

                if t > duration:
                    break

                glClearColor(0, 0, 0, 1)
                glClear(GL_COLOR_BUFFER_BIT)

                glUseProgram(self.shader)
                glUniform1f(glGetUniformLocation(self.shader, "u_time"), t)
                glUniform2f(glGetUniformLocation(self.shader, "u_resolution"), RESOLUTION[0], RESOLUTION[1])
                glUniform1f(glGetUniformLocation(self.shader, "u_curvature"), CONFIG['branas']['curvature_left'])

                glBindVertexArray(self.vao)
                glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

                glfw.swap_buffers(self.window)
                glfw.poll_events()
                time.sleep(frame_time)

        glfw.terminate()

if __name__ == "__main__":
    render_video = parse_render_args()
    Cortina(render_video=render_video).run()
