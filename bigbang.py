# bigbang.py - Colision entre branas
import os
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
uniform float u_duration;
uniform vec2 u_resolution;
uniform float u_curvature_left;
uniform float u_curvature_right;
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

vec3 palette(float t) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.263, 0.416, 0.557);
    return a + b * cos(6.28318 * (c * t + d));
}

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

void main() {
    vec2 uv = vPos;
    float aspect = u_resolution.x / u_resolution.y;
    uv.x *= aspect;

    float t = u_time;
    float duration = u_duration;

    float baseProton = -aspect + (t / duration) * (aspect * 2.0);
    float baseElectron = aspect - (t / duration) * (aspect * 2.0);

    float tHit = duration * 0.5;
    float impact = smoothstep(tHit - 1.2, tHit + 1.2, t);
    float impactFade = 1.0 - smoothstep(tHit + 6.0, tHit + 10.0, t);
    impact *= impactFade;

    float protonPos = baseProton - impact * 0.12;
    float electronPos = baseElectron + impact * 0.35;

    float protonCurved = protonPos + u_curvature_left * uv.y * uv.y;
    float electronCurved = electronPos - u_curvature_right * uv.y * uv.y;

    float edge = 0.12;
    float protonMask = 1.0 - smoothstep(protonCurved - edge, protonCurved + edge, uv.x);
    float electronMask = smoothstep(electronCurved - edge, electronCurved + edge, uv.x);

    float contactX = protonCurved;
    float distContact = abs(uv.x - contactX);
    float contactBand = impact * exp(-distContact * 18.0) * (1.0 - abs(uv.y) * 0.7);

    vec2 toContact = vec2(uv.x - contactX, uv.y);
    float scatter = impact * smoothstep(0.45, 0.0, distContact);
    vec2 scatterDir = normalize(toContact + vec2(0.001, 0.0));
    vec2 scatterJitter = vec2(
        fbm(uv * 6.0 + t * 1.2),
        fbm(uv * 6.0 - t * 1.1)
    ) - 0.5;
    vec2 electronUV = uv;
    electronUV += scatterDir * scatter * 0.08;
    electronUV += scatterJitter * scatter * 0.12;
    electronUV.x += impact * 0.12;

    float tMetal = t * 0.5;
    vec2 eps = vec2(4.0 / u_resolution.y, 0.0);
    float f = bumpFunc(uv, tMetal);
    float fx = bumpFunc(uv - eps.xy, tMetal);
    float fy = bumpFunc(uv - eps.yx, tMetal);
    fx = (fx - f) / eps.x;
    fy = (fy - f) / eps.x;
    vec3 sn = normalize(vec3(0.0, 0.0, -1.0) + vec3(fx, fy, 0.0) * 0.05);
    vec3 rd = normalize(vec3(uv, 1.0));
    vec3 lp = vec3(cos(t) * 0.5, sin(t) * 0.2, -1.0);
    vec3 ld = normalize(lp - vec3(uv, 0.0));
    float diff = pow(max(dot(sn, ld), 0.0), 4.0);
    float spec = pow(max(dot(reflect(-ld, sn), -rd), 0.0), 12.0);
    vec3 mercuryBase = vec3(0.8, 0.85, 0.9);
    vec3 protonCol = mercuryBase * (f * 0.5 + 0.5);
    protonCol = protonCol * (diff * vec3(1.0, 0.97, 0.92) * 2.0 + 0.5)
        + vec3(1.0, 0.9, 0.8) * spec * 2.0;

    float turbulence = fbm(electronUV * 3.0 + t * 0.3);
    float density = turbulence * 0.6 + 0.3;
    float vortex = length(curl(electronUV * 4.0, t)) * 1.5;
    vortex = smoothstep(0.2, 0.7, vortex);
    vec3 gasBlue = vec3(0.3, 0.7, 1.0);
    vec3 glowBlue = vec3(0.5, 0.85, 1.0);
    vec3 edgeBlue = vec3(0.7, 0.9, 1.0);
    vec3 electronCol = mix(gasBlue, glowBlue, turbulence);
    electronCol *= density;
    electronCol += vec3(0.4, 0.8, 1.0) * vortex * 0.4;

    float edgeTurbulence = fbm(electronUV * 8.0 + t * 3.0);
    electronCol += edgeBlue * edgeTurbulence * scatter * 0.8;

    vec3 fusedCol = mix(protonCol, electronCol, 0.45);
    fusedCol += vec3(1.0, 0.95, 0.85) * contactBand * 1.8;

    vec3 col = protonCol * protonMask + electronCol * electronMask;
    col = mix(col, fusedCol, contactBand);

    vec2 uvBig = vec2((uv.x - contactX), uv.y) * 10.0;
    vec2 uv0 = uvBig;
    vec3 bigbangCol = vec3(0.0);
    for (float i = 0.0; i < 4.0; i++) {
        uvBig = fract(uvBig * 1.5) - 0.5;
        float d = length(uvBig) * exp(-length(uv0));
        vec3 pal = palette(length(uv0) + i * 0.4 + t * 0.4);
        d = sin(d * 8.0 + t) / 8.0;
        d = abs(d);
        d = pow(0.01 / d, 1.2);
        bigbangCol += pal * d;
    }

    float bigbangMix = smoothstep(0.1, 0.9, impact) * smoothstep(0.15, 0.45, contactBand);
    col = mix(col, bigbangCol, bigbangMix);

    float visible = max(protonMask, electronMask);
    visible = max(visible, bigbangMix);
    col *= visible;

    FragColor = vec4(sqrt(clamp(col, 0.0, 1.0)), 1.0);
}
"""


class BigBang:
    def __init__(self, render_video=False):
        glfw.init()
        self.window = glfw.create_window(
            RESOLUTION[0], RESOLUTION[1], "BigBang", None, None
        )
        glfw.make_context_current(self.window)

        glViewport(0, 0, RESOLUTION[0], RESOLUTION[1])

        self.shader = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER),
        )

        vertices = np.array([-1, -1, -1, 1, 1, 1, 1, -1], dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        self.start = time.time()
        output_name = os.path.splitext(os.path.basename(__file__))[0] + ".mp4"
        self.renderer = VideoRenderer(RESOLUTION[0], RESOLUTION[1], FPS, output_name)
        if render_video:
            self.renderer.enable()

    def run(self):
        duration = float(CONFIG.get('bigbang_duration', 30.0))
        frame_time = 1.0 / FPS

        if self.renderer.enabled:
            total_frames = int(duration * FPS)
            for frame in range(total_frames):
                if glfw.window_should_close(self.window):
                    break

                t = frame * frame_time

                glClearColor(0, 0, 0, 1)
                glClear(GL_COLOR_BUFFER_BIT)

                glUseProgram(self.shader)
                glUniform1f(glGetUniformLocation(self.shader, "u_time"), t)
                glUniform1f(glGetUniformLocation(self.shader, "u_duration"), duration)
                glUniform2f(
                    glGetUniformLocation(self.shader, "u_resolution"),
                    RESOLUTION[0],
                    RESOLUTION[1],
                )
                glUniform1f(
                    glGetUniformLocation(self.shader, "u_curvature_left"),
                    CONFIG['branas']['curvature_left'],
                )
                glUniform1f(
                    glGetUniformLocation(self.shader, "u_curvature_right"),
                    CONFIG['branas']['curvature_right'],
                )

                glBindVertexArray(self.vao)
                glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

                self.renderer.capture_frame()

                glfw.swap_buffers(self.window)
                glfw.poll_events()

            self.renderer.generate_video()
        else:
            while not glfw.window_should_close(self.window):
                t = time.time() - self.start

                if t > duration:
                    break

                glClearColor(0, 0, 0, 1)
                glClear(GL_COLOR_BUFFER_BIT)

                glUseProgram(self.shader)
                glUniform1f(glGetUniformLocation(self.shader, "u_time"), t)
                glUniform1f(glGetUniformLocation(self.shader, "u_duration"), duration)
                glUniform2f(
                    glGetUniformLocation(self.shader, "u_resolution"),
                    RESOLUTION[0],
                    RESOLUTION[1],
                )
                glUniform1f(
                    glGetUniformLocation(self.shader, "u_curvature_left"),
                    CONFIG['branas']['curvature_left'],
                )
                glUniform1f(
                    glGetUniformLocation(self.shader, "u_curvature_right"),
                    CONFIG['branas']['curvature_right'],
                )

                glBindVertexArray(self.vao)
                glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

                glfw.swap_buffers(self.window)
                glfw.poll_events()
                time.sleep(frame_time)

        glfw.terminate()


if __name__ == "__main__":
    render_video = parse_render_args()
    BigBang(render_video=render_video).run()
