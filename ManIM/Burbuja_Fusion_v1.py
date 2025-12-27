# Fusión de burbujas 3D con cámara orbital
from manim import *
import numpy as np

class BurbujaFusion3D:
    def __init__(self, posicion, velocidad, radio, masa, color):
        self.posicion = np.array(posicion, dtype=float)
        self.velocidad = np.array(velocidad, dtype=float)
        self.radio = radio
        self.masa = masa
        self.color = color
        self.fusionada = False
        self.otra_burbuja = None

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

    def actualizar_posicion(self, dt):
        """Actualiza posición"""
        self.posicion += self.velocidad * dt

        # Si está fusionada, acercarse gradualmente (incrustación)
        if self.fusionada and self.otra_burbuja:
            delta = self.otra_burbuja.posicion - self.posicion
            distancia = np.linalg.norm(delta)
            if distancia > 0:
                # Acercarse gradualmente
                velocidad_incrustacion = 0.15
                direccion = delta / distancia
                self.posicion += direccion * velocidad_incrustacion * dt
                self.otra_burbuja.posicion -= direccion * velocidad_incrustacion * dt


class FusionBurbujas3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = BLACK

        # Configurar cámara inicial
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        # Crear burbujas 3D
        b1 = BurbujaFusion3D([-2.5, 0, 0], [0.5, 0, 0], 1.2, 1.0, BLUE)
        b2 = BurbujaFusion3D([2.5, 0, 0], [-0.5, 0, 0], 1.2, 1.0, PINK)

        # Crear esferas visuales
        esfera1 = Sphere(radius=b1.radio, resolution=(20, 20))
        esfera1.set_color(b1.color)
        esfera1.set_opacity(0.7)
        esfera1.move_to(b1.posicion)

        esfera2 = Sphere(radius=b2.radio, resolution=(20, 20))
        esfera2.set_color(b2.color)
        esfera2.set_opacity(0.7)
        esfera2.move_to(b2.posicion)

        self.add(esfera1, esfera2)

        dt = 0.05
        t = 0
        fusionadas = False
        tiempo_fusion = 0

        while t < 7:
            b1.actualizar_posicion(dt)
            b2.actualizar_posicion(dt)

            # Detectar contacto
            distancia = np.linalg.norm(b1.posicion - b2.posicion)

            if not fusionadas and distancia <= (b1.radio + b2.radio):
                b1.fusionar_con(b2)
                fusionadas = True

            # ROTAR CÁMARA durante la fusión
            if fusionadas:
                tiempo_fusion += dt
                # Rotar cámara alrededor del punto de contacto
                velocidad_rotacion = 0.5  # radianes/segundo

                # Calcular nueva orientación de cámara
                theta_actual = 30 * DEGREES + velocidad_rotacion * tiempo_fusion

                self.move_camera(
                    phi=70 * DEGREES,
                    theta=theta_actual,
                    run_time=dt,
                    rate_func=linear
                )

            # Actualizar posiciones de esferas
            esfera1.move_to(b1.posicion)
            esfera2.move_to(b2.posicion)

            self.wait(dt)
            t += dt

        self.wait(1)
