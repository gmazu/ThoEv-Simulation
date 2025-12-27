# Fusión de burbujas con interface plana
from manim import *
import numpy as np

NUM_PUNTOS = 100

class BurbujaFusion:
    def __init__(self, posicion, velocidad, radio, masa, color):
        self.posicion = np.array(posicion, dtype=float)
        self.velocidad = np.array(velocidad, dtype=float)
        self.radio = radio
        self.masa = masa
        self.color = color
        self.fusionada = False
        self.otra_burbuja = None
        self.interface_plana = None
        self.radio_puente = 0.0  # Radio del círculo de fusión (empieza en 0)
        self.tiempo_fusion = 0.0  # Tiempo desde que empezó la fusión

    def fusionar_con(self, otra):
        """Fusiona esta burbuja con otra"""
        if self.fusionada:
            return

        # Conservar momentum
        vel_total = (self.masa * self.velocidad + otra.masa * otra.velocidad) / (self.masa + otra.masa)
        self.velocidad = vel_total
        otra.velocidad = vel_total

        # Marcar como fusionadas
        self.fusionada = True
        otra.fusionada = True
        self.otra_burbuja = otra
        otra.otra_burbuja = self

        # Calcular puntos de interface plana
        self.calcular_interface()

    def calcular_interface(self):
        """Calcula la línea de interface plana entre las burbujas"""
        if not self.fusionada or not self.otra_burbuja:
            return

        # Vector entre centros
        delta = self.otra_burbuja.posicion - self.posicion
        distancia = np.linalg.norm(delta)

        if distancia == 0:
            return

        # Normal (dirección de la interface)
        normal = delta / distancia

        # Punto medio ajustado (interface se forma aquí)
        # La interface está entre las dos burbujas
        punto_medio = (self.posicion + self.otra_burbuja.posicion) / 2

        # Calcular altura de la interface (ancho del plano)
        # Usando teorema de Pitágoras para encontrar el ancho
        d = distancia / 2
        if d < self.radio:
            altura = 2 * np.sqrt(self.radio**2 - d**2)
        else:
            altura = 0

        self.interface_plana = {
            'centro': punto_medio,
            'normal': normal,
            'altura': altura,
            'distancia': distancia
        }

    def actualizar_posicion(self, dt):
        """Actualiza posición"""
        self.posicion += self.velocidad * dt

        # Si está fusionada, actualizar interface y crecer el puente
        if self.fusionada and self.otra_burbuja:
            self.tiempo_fusion += dt

            # El puente crece gradualmente (velocidad ajustable)
            velocidad_crecimiento = 0.8  # Radio/segundo
            self.radio_puente = min(self.tiempo_fusion * velocidad_crecimiento, self.radio)

            # Las burbujas se acercan gradualmente (se incrustan)
            delta = self.otra_burbuja.posicion - self.posicion
            distancia = np.linalg.norm(delta)
            if distancia > 0:
                # Acercarse un poco más cada frame
                velocidad_incrustacion = 0.15
                direccion = delta / distancia
                self.posicion += direccion * velocidad_incrustacion * dt
                self.otra_burbuja.posicion -= direccion * velocidad_incrustacion * dt

            self.calcular_interface()

    def get_puntos_circulo_con_plano(self):
        """Retorna puntos del círculo, con cara plana si está fusionada"""
        puntos = []
        angulos = np.linspace(0, 2*PI, NUM_PUNTOS, endpoint=False)

        if not self.fusionada or not self.interface_plana:
            # Círculo normal
            for angulo in angulos:
                x = self.posicion[0] + self.radio * np.cos(angulo)
                y = self.posicion[1] + self.radio * np.sin(angulo)
                puntos.append([x, y, 0])
        else:
            # Círculo con cara plana
            normal = self.interface_plana['normal']
            centro_interface = self.interface_plana['centro']

            for angulo in angulos:
                # Punto en círculo completo
                dir_x = np.cos(angulo)
                dir_y = np.sin(angulo)
                direccion = np.array([dir_x, dir_y, 0])

                # Punto en el círculo
                punto_circulo = self.posicion + self.radio * direccion

                # Verificar si este punto está del lado de la interface
                # (debe ser cortado por el plano)
                vec_a_interface = centro_interface - self.posicion
                proyeccion = np.dot(direccion[:2], vec_a_interface[:2])

                if proyeccion > 0:
                    # Este punto está hacia la otra burbuja, cortarlo
                    # Proyectar sobre el plano de interface
                    dist_a_plano = np.dot(punto_circulo[:2] - centro_interface[:2], normal[:2])

                    if dist_a_plano > 0:
                        # Mover el punto al plano
                        punto_circulo[:2] -= dist_a_plano * normal[:2]

                puntos.append(punto_circulo.tolist())

        return puntos


class FusionBurbujas(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Crear burbujas
        b1 = BurbujaFusion([-3, 0, 0], [0.6, 0, 0], 1.5, 1.0, BLUE)
        b2 = BurbujaFusion([3, 0, 0], [-0.6, 0, 0], 1.5, 1.0, PINK)

        v1 = self.crear_visual(b1)
        v2 = self.crear_visual(b2)
        interface_visual = None

        self.add(v1, v2)

        dt = 0.03
        t = 0
        fusionadas = False

        while t < 7:
            b1.actualizar_posicion(dt)
            b2.actualizar_posicion(dt)

            # Detectar contacto
            distancia = np.linalg.norm(b1.posicion - b2.posicion)

            if not fusionadas and distancia <= (b1.radio + b2.radio):
                b1.fusionar_con(b2)
                fusionadas = True

            # Actualizar visuales
            self.actualizar_visual(v1, b1)
            self.actualizar_visual(v2, b2)

            self.wait(dt)
            t += dt

        self.wait(0.5)

    def crear_visual(self, b):
        puntos = b.get_puntos_circulo_con_plano()
        p = Polygon(*puntos, color=b.color)
        p.set_stroke(b.color, width=3)
        p.set_fill(b.color, opacity=0.25)
        return VGroup(p)

    def crear_interface_visual(self, b):
        """Crea zona de impacto brillante con corona"""
        if not b.interface_plana:
            return VGroup()

        centro = b.interface_plana['centro']

        # Zona brillante central (amarillo/blanco)
        nucleo = Circle(radius=0.1, color=WHITE)
        nucleo.move_to(centro)
        nucleo.set_fill(YELLOW, opacity=0.9)
        nucleo.set_stroke(WHITE, width=2)

        # Corona naranja alrededor
        corona = Circle(radius=0.2, color=ORANGE)
        corona.move_to(centro)
        corona.set_fill(ORANGE, opacity=0.5)
        corona.set_stroke(ORANGE, width=1)

        # Anillo exterior difuso
        anillo = Circle(radius=0.3, color=RED)
        anillo.move_to(centro)
        anillo.set_fill(opacity=0)
        anillo.set_stroke(ORANGE, width=3, opacity=0.4)

        return VGroup(anillo, corona, nucleo)

    def actualizar_visual(self, visual, b):
        nuevos = b.get_puntos_circulo_con_plano()
        visual[0].set_points_as_corners([*nuevos, nuevos[0]])

    def actualizar_interface_visual(self, interface, b):
        """Actualiza zona de impacto - crece y sigue la juntura"""
        if not b.interface_plana:
            return

        centro = b.interface_plana['centro']
        factor = b.radio_puente

        # Actualizar anillo exterior (más grande)
        anillo = interface[0]
        anillo.become(
            Circle(radius=factor * 1.5, color=ORANGE)
            .move_to(centro)
            .set_fill(opacity=0)
            .set_stroke(ORANGE, width=4, opacity=0.3)
        )

        # Actualizar corona media
        corona = interface[1]
        corona.become(
            Circle(radius=factor * 1.0, color=ORANGE)
            .move_to(centro)
            .set_fill(ORANGE, opacity=0.4)
            .set_stroke(YELLOW, width=2, opacity=0.6)
        )

        # Actualizar núcleo brillante
        nucleo = interface[2]
        nucleo.become(
            Circle(radius=factor * 0.6, color=YELLOW)
            .move_to(centro)
            .set_fill(YELLOW, opacity=0.8)
            .set_stroke(WHITE, width=3)
        )
