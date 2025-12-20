"""
ThoEv Pitch – Cairo renderer version (sin OpenGL/shaders).
Ejecuta con: manim -pqh tho_ev_scene.py ThoEvScene
"""

import math
from manim import (
    BLUE,
    GREEN,
    RED,
    WHITE,
    BLACK,
    ORIGIN,
    Scene,
    Circle,
    FadeIn,
    FadeOut,
    LaggedStart,
    MathTex,
    DOWN,
    PI,
    RIGHT,
    Rectangle,
    Text,
    VGroup,
    ValueTracker,
    config,
)
from numpy import array


class ThoEvScene(Scene):
    def construct(self):
        # Fondo animado con capas de glow para simular nebulosa.
        background = VGroup()
        glow_layers = []
        for radius, color, opacity in [
            (8, "#0b1024", 0.55),
            (6, "#13234a", 0.45),
            (5, "#1c326b", 0.35),
        ]:
            glow = Circle(
                radius=radius,
                fill_color=color,
                fill_opacity=opacity,
                stroke_width=0,
            )
            glow_layers.append(glow)
        background.add(*glow_layers)

        pulse = ValueTracker(0)

        def pulse_glow(mob, dt):
            pulse.increment_value(dt)
            scale = 1 + 0.03 * math.sin(1.2 * pulse.get_value())
            for layer in glow_layers:
                layer.scale(scale, about_point=ORIGIN)

        background.add_updater(pulse_glow)
        self.add(background)

        # Dos branas que entran desde los lados.
        brane_left = Rectangle(height=6, width=8, fill_opacity=0.7, stroke_width=0, color=RED)
        brane_left.shift(5 * [-1, 0, 0])

        brane_right = Rectangle(height=6, width=8, fill_opacity=0.7, stroke_width=0, color=BLUE)
        brane_right.shift(5 * [1, 0, 0])

        self.play(FadeIn(brane_left, shift=(1.5, 0, 0)), FadeIn(brane_right, shift=(-1.5, 0, 0)))
        self.play(
            brane_left.animate.shift(array([4.5, 0, 0])),
            brane_right.animate.shift(array([-4.5, 0, 0])),
            run_time=3,
        )

        # Compresión y flash.
        flash_overlay = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=WHITE,
            fill_opacity=0.0,
            stroke_width=0,
        )
        self.add(flash_overlay)
        self.play(flash_overlay.animate.set_fill(opacity=0.6), run_time=0.4)
        self.play(flash_overlay.animate.set_fill(opacity=0), run_time=0.6)

        # Mandala + tetraedro sugerido.
        rings = VGroup(
            Circle(radius=0.8, color=RED, stroke_width=3),
            Circle(radius=1.0, color=GREEN, stroke_width=3),
            Circle(radius=1.2, color=BLUE, stroke_width=3),
        )
        spokes = VGroup(
            *[Rectangle(height=1.2, width=0.04, color=WHITE, fill_opacity=0.7).rotate(i * PI / 6) for i in range(12)]
        )
        tetra = MathTex(r"\triangle").scale(1.5).set_color(WHITE)
        mandala = VGroup(rings, spokes, tetra).scale(0.9)

        self.play(LaggedStart(*[FadeIn(r) for r in rings], lag_ratio=0.2), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(s) for s in spokes], lag_ratio=0.05), FadeIn(tetra), run_time=1.0)

        # Capas de color y TOEF pulsante.
        layer_red = Rectangle(width=4, height=0.8, fill_color=RED, fill_opacity=0.35, stroke_width=0).shift(
            0.5 * [-1, -1.0, 0]
        )
        layer_green = Rectangle(width=4, height=0.8, fill_color=GREEN, fill_opacity=0.35, stroke_width=0)
        layer_blue = Rectangle(width=4, height=0.8, fill_color=BLUE, fill_opacity=0.35, stroke_width=0).shift(
            0.5 * [1, 1.0, 0]
        )

        toef = Text("TOEF", font_size=72, weight="BOLD", color=WHITE)
        toef_group = VGroup(layer_red, layer_green, layer_blue, toef)

        nucleus = toef[1] if len(toef) > 1 else toef
        toef_pulse = ValueTracker(0.0)
        nucleus_template = nucleus.copy()

        def pulse_o(mob, dt):
            toef_pulse.increment_value(dt)
            scale = 1 + 0.06 * math.sin(2 * toef_pulse.get_value())
            mob.become(nucleus_template.copy().scale(scale).move_to(nucleus_template.get_center()))

        nucleus.add_updater(pulse_o)

        self.play(FadeIn(layer_red), FadeIn(layer_green), FadeIn(layer_blue), FadeIn(toef), run_time=1.2)
        self.wait(1.0)
        self.play(FadeOut(toef_group), FadeOut(mandala), run_time=1.0)
        nucleus.clear_updaters()

        # Zoom out y gas de universos.
        universes = VGroup(
            *[
                Circle(radius=0.3, color=WHITE, fill_opacity=0.05).shift(pos)
                for pos in [
                    array([3.5, 2.5, 0]),
                    array([-3.0, 1.8, 0]),
                    array([2.2, -2.1, 0]),
                    array([-2.7, -2.5, 0]),
                    array([0.8, 3.0, 0]),
                    array([-0.5, -3.2, 0]),
                    array([3.8, -0.4, 0]),
                    array([-3.8, 0.6, 0]),
                ]
            ]
        )

        self.play(self.camera.frame.animate.scale(2.5), FadeIn(universes, run_time=1.5))
        self.wait(1.0)
        self.play(self.camera.frame.animate.scale(0.4), run_time=1.5)

        # Símbolo persistente.
        symbol = Text("TOEF", font_size=36, color=WHITE).to_corner(DOWN + RIGHT)
        symbol_pulse = ValueTracker(0.0)
        symbol_template = symbol.copy()

        def symbol_updater(mob, dt):
            symbol_pulse.increment_value(dt)
            scale = 1 + 0.03 * math.sin(3 * symbol_pulse.get_value())
            mob.become(symbol_template.copy().scale(scale).move_to(symbol_template.get_center()))

        symbol.add_updater(symbol_updater)
        self.add(symbol)
        self.wait(1.2)
