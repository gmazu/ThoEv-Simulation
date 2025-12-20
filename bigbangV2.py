# bigbangV2.py - Colision entre branas (proton + electron sin cambios)
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

vec2 velocityField(vec2 p, float t) {
    vec2 mainFlow = vec2(-1.0, 0.0);
    vec2 wave = vec2(
        sin(p.y * 3.0 + t * 2.0) * 0.3,
        cos(p.x * 2.0 + t * 1.5) * 0.2
    );
    vec2 vortex = curl(p * 1.5, t) * 0.4;
    return mainFlow + wave + vortex;
}

float warpTime(float tRaw, float duration) {
    float tHit = duration * 0.5;
    float window1 = 1.0;
    float window2 = 0.5;
    float releaseWindow = 0.05;
    float factor1 = 0.5;
    float factor2 = 0.25;

    float t0 = max(0.0, tHit - window1);
    float t1 = max(t0, tHit - window2);
    float t2 = max(t1, tHit - releaseWindow);

    if (tRaw <= t0) {
        return tRaw;
    }
    if (tRaw < t1) {
        return t0 + (tRaw - t0) * factor1;
    }
    if (tRaw < t2) {
        return t0 + (t1 - t0) * factor1 + (tRaw - t1) * factor2;
    }
    if (tRaw < tHit) {
        return t0 + (t1 - t0) * factor1
            + (t2 - t1) * factor2
            + (tRaw - t2);
    }

    float saved = (t1 - t0) * (1.0 - factor1) + (t2 - t1) * (1.0 - factor2);
    return tRaw - saved;
}

void main() {
    vec2 uv = vPos;
    float aspect = u_resolution.x / u_resolution.y;
    uv.x *= aspect;

    float duration = 20.0;
    float timeForMotion = warpTime(u_time, duration);
    float t = timeForMotion * 0.5;

    float curtainPosProton = -aspect + (timeForMotion / duration) * (aspect * 2.0);
    float curtainCurvedProton = curtainPosProton + u_curvature_left * uv.y * uv.y;
    float protonMask = 1.0 - smoothstep(curtainCurvedProton - 0.1, curtainCurvedProton + 0.1, uv.x);
    vec2 uvProton = vec2(uv.x - curtainCurvedProton, uv.y);

    float curtainPosElectron = aspect - (timeForMotion / duration) * (aspect * 2.0);
    float curtainCurvedElectron = curtainPosElectron - u_curvature_right * uv.y * uv.y;
    float electronMask = smoothstep(curtainCurvedElectron - 0.1, curtainCurvedElectron + 0.1, uv.x);
    vec2 uvElectron = vec2(uv.x - curtainCurvedElectron, uv.y);

    // PROTON (brana_proton.py)
    vec2 eps = vec2(4.0 / u_resolution.y, 0.0);
    float f = bumpFunc(uvProton, t);
    float fx = bumpFunc(uvProton - eps.xy, t);
    float fy = bumpFunc(uvProton - eps.yx, t);

    const float bumpFactor = 0.05;
    fx = (fx - f) / eps.x;
    fy = (fy - f) / eps.x;

    vec3 sn = normalize(vec3(0.0, 0.0, -1.0) + vec3(fx, fy, 0.0) * bumpFactor);
    vec3 sp = vec3(uv, 0.0);
    vec3 rd = normalize(vec3(uv, 1.0));
    vec3 lp = vec3(cos(timeForMotion) * 0.5, sin(timeForMotion) * 0.2, -1.0);

    vec3 ld = lp - sp;
    float lDist = max(length(ld), 0.0001);
    ld /= lDist;

    float atten = 1.0 / (1.0 + lDist * lDist * 0.15);
    atten *= f * 0.9 + 0.1;

    float diff = max(dot(sn, ld), 0.0);
    diff = pow(diff, 4.0) * 0.66 + pow(diff, 8.0) * 0.34;

    float spec = pow(max(dot(reflect(-ld, sn), -rd), 0.0), 12.0);

    vec3 mercuryBase = vec3(0.8, 0.85, 0.9);
    vec3 texCol = mercuryBase * (f * 0.5 + 0.5);
    vec3 protonCol = (texCol * (diff * vec3(1.0, 0.97, 0.92) * 2.0 + 0.5) +
                      vec3(1.0, 0.9, 0.8) * spec * 2.0) * atten;

    float ref = max(dot(reflect(rd, sn), vec3(1.0)), 0.0);
    protonCol += protonCol * pow(ref, 4.0) * vec3(0.4, 0.5, 0.6) * 2.0;

    // ELECTRON (brana_electron.py)
    vec2 flow = velocityField(uvElectron, t);
    vec2 uvAdvected = uvElectron;
    float dt = 0.05;
    for (int i = 0; i < 3; i++) {
        vec2 vel = velocityField(uvAdvected, t - float(i) * dt);
        uvAdvected -= vel * dt;
    }

    vec2 distortion = curl(uvAdvected * 2.0, t) * 0.25;
    vec2 uvFinal = uvAdvected + distortion;

    float turbulence = fbm(uvFinal * 3.0 + t * 0.3);
    float density = turbulence * 0.6 + 0.3;

    float vortex = length(curl(uvFinal * 4.0, t)) * 1.5;
    vortex = smoothstep(0.2, 0.7, vortex);

    float distToCurtain = abs(uv.x - curtainCurvedElectron);
    float edgeTurbulence = 0.0;
    if (distToCurtain < 0.3) {
        float edgeNoise = fbm(uvElectron * 8.0 + t * 3.0);
        edgeTurbulence = edgeNoise * (1.0 - distToCurtain / 0.3) * 0.5;
        vec2 edgeCurl = curl(uvElectron * 10.0, t * 2.0);
        edgeTurbulence += length(edgeCurl) * 0.3;
    }

    vec3 gasBlue = vec3(0.3, 0.7, 1.0);
    vec3 glowBlue = vec3(0.5, 0.85, 1.0);
    vec3 edgeBlue = vec3(0.7, 0.9, 1.0);

    vec3 electronCol = mix(gasBlue, glowBlue, turbulence);
    electronCol *= density;
    electronCol += vec3(0.4, 0.8, 1.0) * vortex * 0.4;
    electronCol += edgeBlue * edgeTurbulence * 0.8;

    float atmosphericGlow = fbm(uvFinal * 1.5 + t * 0.2) * 0.3;
    electronCol += gasBlue * atmosphericGlow * 0.15;

    vec3 col = protonCol * protonMask + electronCol * electronMask;
    col *= max(protonMask, electronMask);

    FragColor = vec4(sqrt(clamp(col, 0.0, 1.0)), 1.0);
}
"""


class BigBangV2:
    def __init__(self, render_video=False):
        glfw.init()
        self.window = glfw.create_window(
            RESOLUTION[0], RESOLUTION[1], "BigBangV2", None, None
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
        duration = 12.0
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
    BigBangV2(render_video=render_video).run()
