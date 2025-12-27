# burbuja_paso1.py
# Solo paso 1: Círculo con outline blanco

from manim import *

class BurbujaPaso1(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Paso 1: Círculo con outline blanco
        circulo = Circle(radius=2.5, color=WHITE)
        circulo.set_stroke(WHITE, width=5)
        circulo.set_fill(opacity=0)  # Transparente

        # Paso 2: Franjas con efecto tiza (con espacio desde el borde)
        # Lado izquierdo - más adentro para dejar espacio transparente
        # Capa difuminada general
        franja1_blur = Arc(radius=2.5 * 0.88, start_angle=60 * DEGREES, angle=100 * DEGREES)
        franja1_blur.set_stroke(BLUE, width=20, opacity=0.15)
        # Difuminado extra en punta izquierda
        franja1_punta1 = Arc(radius=2.5 * 0.88, start_angle=60 * DEGREES, angle=15 * DEGREES)
        franja1_punta1.set_stroke(BLUE, width=30, opacity=0.08)
        # Difuminado extra en punta derecha
        franja1_punta2 = Arc(radius=2.5 * 0.88, start_angle=145 * DEGREES, angle=15 * DEGREES)
        franja1_punta2.set_stroke(BLUE, width=30, opacity=0.08)
        # Línea principal
        franja1_main = Arc(radius=2.5 * 0.88, start_angle=60 * DEGREES, angle=100 * DEGREES)
        franja1_main.set_stroke(BLUE, width=3, opacity=0.4)

        franja1 = VGroup(franja1_punta1, franja1_punta2, franja1_blur, franja1_main)

        # franja2
        franja2_blur = Arc(radius=2.5 * 0.86, start_angle=70 * DEGREES, angle=80 * DEGREES)
        franja2_blur.set_stroke(PURPLE, width=18, opacity=0.12)
        franja2_p1 = Arc(radius=2.5 * 0.86, start_angle=70 * DEGREES, angle=12 * DEGREES)
        franja2_p1.set_stroke(PURPLE, width=25, opacity=0.07)
        franja2_p2 = Arc(radius=2.5 * 0.86, start_angle=138 * DEGREES, angle=12 * DEGREES)
        franja2_p2.set_stroke(PURPLE, width=25, opacity=0.07)
        franja2_main = Arc(radius=2.5 * 0.86, start_angle=70 * DEGREES, angle=80 * DEGREES)
        franja2_main.set_stroke(PURPLE, width=3, opacity=0.4)
        franja2 = VGroup(franja2_p1, franja2_p2, franja2_blur, franja2_main)

        # franja3
        franja3_blur = Arc(radius=2.5 * 0.84, start_angle=80 * DEGREES, angle=60 * DEGREES)
        franja3_blur.set_stroke(PINK, width=16, opacity=0.1)
        franja3_p1 = Arc(radius=2.5 * 0.84, start_angle=80 * DEGREES, angle=10 * DEGREES)
        franja3_p1.set_stroke(PINK, width=22, opacity=0.06)
        franja3_p2 = Arc(radius=2.5 * 0.84, start_angle=130 * DEGREES, angle=10 * DEGREES)
        franja3_p2.set_stroke(PINK, width=22, opacity=0.06)
        franja3_main = Arc(radius=2.5 * 0.84, start_angle=80 * DEGREES, angle=60 * DEGREES)
        franja3_main.set_stroke(PINK, width=3, opacity=0.4)
        franja3 = VGroup(franja3_p1, franja3_p2, franja3_blur, franja3_main)

        # Lado derecho - franja4
        franja4_blur = Arc(radius=2.5 * 0.88, start_angle=-60 * DEGREES, angle=80 * DEGREES)
        franja4_blur.set_stroke(TEAL, width=18, opacity=0.12)
        franja4_p1 = Arc(radius=2.5 * 0.88, start_angle=-60 * DEGREES, angle=12 * DEGREES)
        franja4_p1.set_stroke(TEAL, width=25, opacity=0.07)
        franja4_p2 = Arc(radius=2.5 * 0.88, start_angle=8 * DEGREES, angle=12 * DEGREES)
        franja4_p2.set_stroke(TEAL, width=25, opacity=0.07)
        franja4_main = Arc(radius=2.5 * 0.88, start_angle=-60 * DEGREES, angle=80 * DEGREES)
        franja4_main.set_stroke(TEAL, width=3, opacity=0.4)
        franja4 = VGroup(franja4_p1, franja4_p2, franja4_blur, franja4_main)

        # franja5
        franja5_blur = Arc(radius=2.5 * 0.86, start_angle=-50 * DEGREES, angle=60 * DEGREES)
        franja5_blur.set_stroke(BLUE, width=16, opacity=0.1)
        franja5_p1 = Arc(radius=2.5 * 0.86, start_angle=-50 * DEGREES, angle=10 * DEGREES)
        franja5_p1.set_stroke(BLUE, width=22, opacity=0.06)
        franja5_p2 = Arc(radius=2.5 * 0.86, start_angle=0 * DEGREES, angle=10 * DEGREES)
        franja5_p2.set_stroke(BLUE, width=22, opacity=0.06)
        franja5_main = Arc(radius=2.5 * 0.86, start_angle=-50 * DEGREES, angle=60 * DEGREES)
        franja5_main.set_stroke(BLUE, width=3, opacity=0.4)
        franja5 = VGroup(franja5_p1, franja5_p2, franja5_blur, franja5_main)

        # Parte superior - franja6
        franja6_blur = Arc(radius=2.5 * 0.87, start_angle=170 * DEGREES, angle=50 * DEGREES)
        franja6_blur.set_stroke(PURPLE, width=17, opacity=0.11)
        franja6_p1 = Arc(radius=2.5 * 0.87, start_angle=170 * DEGREES, angle=10 * DEGREES)
        franja6_p1.set_stroke(PURPLE, width=24, opacity=0.065)
        franja6_p2 = Arc(radius=2.5 * 0.87, start_angle=210 * DEGREES, angle=10 * DEGREES)
        franja6_p2.set_stroke(PURPLE, width=24, opacity=0.065)
        franja6_main = Arc(radius=2.5 * 0.87, start_angle=170 * DEGREES, angle=50 * DEGREES)
        franja6_main.set_stroke(PURPLE, width=3, opacity=0.4)
        franja6 = VGroup(franja6_p1, franja6_p2, franja6_blur, franja6_main)

        # Paso 3: Con efecto tiza en puntas - incluyendo blancas
        # capa_izq1
        c1_blur = Arc(radius=2.5 * 0.90, start_angle=85 * DEGREES, angle=55 * DEGREES)
        c1_blur.set_stroke(BLUE, width=24, opacity=0.08)
        c1_p1 = Arc(radius=2.5 * 0.90, start_angle=85 * DEGREES, angle=10 * DEGREES)
        c1_p1.set_stroke(BLUE, width=32, opacity=0.05)
        c1_p2 = Arc(radius=2.5 * 0.90, start_angle=130 * DEGREES, angle=10 * DEGREES)
        c1_p2.set_stroke(BLUE, width=32, opacity=0.05)
        c1_main = Arc(radius=2.5 * 0.90, start_angle=85 * DEGREES, angle=55 * DEGREES)
        c1_main.set_stroke(BLUE, width=3, opacity=0.4)
        capa_izq1 = VGroup(c1_p1, c1_p2, c1_blur, c1_main)

        # capa_izq2
        c2_blur = Arc(radius=2.5 * 0.88, start_angle=90 * DEGREES, angle=50 * DEGREES)
        c2_blur.set_stroke(PURPLE, width=20, opacity=0.07)
        c2_p1 = Arc(radius=2.5 * 0.88, start_angle=90 * DEGREES, angle=10 * DEGREES)
        c2_p1.set_stroke(PURPLE, width=28, opacity=0.04)
        c2_p2 = Arc(radius=2.5 * 0.88, start_angle=130 * DEGREES, angle=10 * DEGREES)
        c2_p2.set_stroke(PURPLE, width=28, opacity=0.04)
        c2_main = Arc(radius=2.5 * 0.88, start_angle=90 * DEGREES, angle=50 * DEGREES)
        c2_main.set_stroke(PURPLE, width=3, opacity=0.4)
        capa_izq2 = VGroup(c2_p1, c2_p2, c2_blur, c2_main)

        # capa_izq3 BLANCA
        c3_blur = Arc(radius=2.5 * 0.86, start_angle=95 * DEGREES, angle=45 * DEGREES)
        c3_blur.set_stroke(WHITE, width=18, opacity=0.06)
        c3_p1 = Arc(radius=2.5 * 0.86, start_angle=95 * DEGREES, angle=10 * DEGREES)
        c3_p1.set_stroke(WHITE, width=25, opacity=0.04)
        c3_p2 = Arc(radius=2.5 * 0.86, start_angle=130 * DEGREES, angle=10 * DEGREES)
        c3_p2.set_stroke(WHITE, width=25, opacity=0.04)
        c3_main = Arc(radius=2.5 * 0.86, start_angle=95 * DEGREES, angle=45 * DEGREES)
        c3_main.set_stroke(WHITE, width=3, opacity=0.4)
        capa_izq3 = VGroup(c3_p1, c3_p2, c3_blur, c3_main)

        # blanco1
        b1_blur = Arc(radius=2.5 * 0.84, start_angle=100 * DEGREES, angle=40 * DEGREES)
        b1_blur.set_stroke(WHITE, width=16, opacity=0.05)
        b1_p1 = Arc(radius=2.5 * 0.84, start_angle=100 * DEGREES, angle=8 * DEGREES)
        b1_p1.set_stroke(WHITE, width=22, opacity=0.03)
        b1_p2 = Arc(radius=2.5 * 0.84, start_angle=132 * DEGREES, angle=8 * DEGREES)
        b1_p2.set_stroke(WHITE, width=22, opacity=0.03)
        b1_main = Arc(radius=2.5 * 0.84, start_angle=100 * DEGREES, angle=40 * DEGREES)
        b1_main.set_stroke(WHITE, width=3, opacity=0.4)
        blanco1 = VGroup(b1_p1, b1_p2, b1_blur, b1_main)

        # blanco2
        b2_blur = Arc(radius=2.5 * 0.82, start_angle=105 * DEGREES, angle=35 * DEGREES)
        b2_blur.set_stroke(WHITE, width=14, opacity=0.04)
        b2_p1 = Arc(radius=2.5 * 0.82, start_angle=105 * DEGREES, angle=8 * DEGREES)
        b2_p1.set_stroke(WHITE, width=20, opacity=0.025)
        b2_p2 = Arc(radius=2.5 * 0.82, start_angle=132 * DEGREES, angle=8 * DEGREES)
        b2_p2.set_stroke(WHITE, width=20, opacity=0.025)
        b2_main = Arc(radius=2.5 * 0.82, start_angle=105 * DEGREES, angle=35 * DEGREES)
        b2_main.set_stroke(WHITE, width=3, opacity=0.4)
        blanco2 = VGroup(b2_p1, b2_p2, b2_blur, b2_main)

        # linea_separada BLANCA MÁS VISIBLE
        ls_blur = Arc(radius=2.5 * 0.75, start_angle=110 * DEGREES, angle=25 * DEGREES)
        ls_blur.set_stroke(WHITE, width=14, opacity=0.15)
        ls_p1 = Arc(radius=2.5 * 0.75, start_angle=110 * DEGREES, angle=6 * DEGREES)
        ls_p1.set_stroke(WHITE, width=20, opacity=0.1)
        ls_p2 = Arc(radius=2.5 * 0.75, start_angle=129 * DEGREES, angle=6 * DEGREES)
        ls_p2.set_stroke(WHITE, width=20, opacity=0.1)
        ls_main = Arc(radius=2.5 * 0.75, start_angle=110 * DEGREES, angle=25 * DEGREES)
        ls_main.set_stroke(WHITE, width=4, opacity=0.7)  # Más visible
        linea_separada = VGroup(ls_p1, ls_p2, ls_blur, ls_main)

        # capa_der
        cd_blur = Arc(radius=2.5 * 0.88, start_angle=-45 * DEGREES, angle=40 * DEGREES)
        cd_blur.set_stroke(TEAL, width=18, opacity=0.05)
        cd_p1 = Arc(radius=2.5 * 0.88, start_angle=-45 * DEGREES, angle=8 * DEGREES)
        cd_p1.set_stroke(TEAL, width=25, opacity=0.03)
        cd_p2 = Arc(radius=2.5 * 0.88, start_angle=-13 * DEGREES, angle=8 * DEGREES)
        cd_p2.set_stroke(TEAL, width=25, opacity=0.03)
        cd_main = Arc(radius=2.5 * 0.88, start_angle=-45 * DEGREES, angle=40 * DEGREES)
        cd_main.set_stroke(TEAL, width=3, opacity=0.4)
        capa_der = VGroup(cd_p1, cd_p2, cd_blur, cd_main)

        # Paso 4: Reflejos curvos (siguiendo la forma de la burbuja)
        # Reflejo 1 - abajo izquierda (múltiples arcos formando ventana curva)
        ref1_top = Arc(radius=1.8, start_angle=200 * DEGREES, angle=30 * DEGREES)
        ref1_top.set_stroke(WHITE, width=0).set_fill(WHITE, opacity=0.85)
        ref1_bot = Arc(radius=1.5, start_angle=200 * DEGREES, angle=30 * DEGREES)
        ref1_bot.set_stroke(WHITE, width=0).set_fill(WHITE, opacity=0.85)
        ref1_left = Line(ref1_top.get_start(), ref1_bot.get_start())
        ref1_left.set_stroke(WHITE, width=0)
        ref1_right = Line(ref1_top.get_end(), ref1_bot.get_end())
        ref1_right.set_stroke(WHITE, width=0)
        reflejo1 = VMobject()
        reflejo1.set_points_as_corners([
            ref1_top.get_start(),
            *ref1_top.get_all_points()[::3],
            ref1_top.get_end(),
            ref1_bot.get_end(),
            *ref1_bot.get_all_points()[::-3],
            ref1_bot.get_start()
        ])
        reflejo1.set_fill(WHITE, opacity=0.85)
        reflejo1.set_stroke(WHITE, width=0)

        # Reflejo 2 - arriba izquierda (más pequeño, curvo)
        ref2_arco1 = Arc(radius=2.2, start_angle=110 * DEGREES, angle=25 * DEGREES)
        ref2_arco2 = Arc(radius=2.0, start_angle=110 * DEGREES, angle=25 * DEGREES)
        reflejo2 = VMobject()
        reflejo2.set_points_as_corners([
            ref2_arco1.get_start(),
            *ref2_arco1.get_all_points()[::3],
            ref2_arco1.get_end(),
            ref2_arco2.get_end(),
            *ref2_arco2.get_all_points()[::-3],
            ref2_arco2.get_start()
        ])
        reflejo2.set_fill(WHITE, opacity=0.75)
        reflejo2.set_stroke(WHITE, width=0)

        # Reflejo 3 - pequeño, derecha
        ref3_arco1 = Arc(radius=2.3, start_angle=40 * DEGREES, angle=15 * DEGREES)
        ref3_arco2 = Arc(radius=2.15, start_angle=40 * DEGREES, angle=15 * DEGREES)
        reflejo3 = VMobject()
        reflejo3.set_points_as_corners([
            ref3_arco1.get_start(),
            *ref3_arco1.get_all_points()[::3],
            ref3_arco1.get_end(),
            ref3_arco2.get_end(),
            *ref3_arco2.get_all_points()[::-3],
            ref3_arco2.get_start()
        ])
        reflejo3.set_fill(WHITE, opacity=0.7)
        reflejo3.set_stroke(WHITE, width=0)

        # Destello en punta - separado siguiendo la curva de la burbuja
        # Más abajo y más separado del reflejo grande
        destello = Polygon(
            [-0.8, -1.6, 0],   # arriba izquierda
            [-0.6, -1.7, 0],   # arriba derecha
            [-0.65, -1.95, 0], # punta principal abajo
            [-0.9, -1.85, 0],  # lado izquierdo
            color=WHITE
        )
        destello.set_fill(WHITE, opacity=0.8)
        destello.set_stroke(WHITE, width=0)

        self.play(Create(circulo), run_time=1.5)
        self.play(
            Create(franja1), Create(franja2), Create(franja3),
            Create(franja4), Create(franja5), Create(franja6),
            run_time=2
        )
        self.play(
            Create(capa_izq1), Create(capa_izq2), Create(capa_izq3),
            Create(blanco1), Create(blanco2), Create(linea_separada),
            Create(capa_der),
            run_time=1.5
        )
        # Paso 4: Reflejos y destello
        self.play(
            FadeIn(reflejo1), FadeIn(reflejo2), FadeIn(reflejo3),
            FadeIn(destello),
            run_time=1
        )
        self.wait(2)
