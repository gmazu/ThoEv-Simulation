# Fusión de burbujas 3D con cámara orbital TEMPORIZADA
# v8: Ondas expansivas adicionales (tipo piedra al lago)
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
        b2 = BurbujaFusion3D([2.5, 0, 0], [-0.5, 0, 0], 1.2, 1.0, RED_C)  # Rojo suave

        # Crear esferas visuales MÁS SUTILES
        esfera1 = Sphere(radius=b1.radio, resolution=(20, 20))
        esfera1.set_color(b1.color)
        esfera1.set_fill(b1.color, opacity=0.10)  # Más sutil
        esfera1.set_stroke(b1.color, width=2, opacity=0.35)  # Borde más sutil
        esfera1.move_to(b1.posicion)

        esfera2 = Sphere(radius=b2.radio, resolution=(20, 20))
        esfera2.set_color(b2.color)
        esfera2.set_fill(b2.color, opacity=0.10)  # Más sutil
        esfera2.set_stroke(b2.color, width=2, opacity=0.35)  # Borde más sutil
        esfera2.move_to(b2.posicion)

        self.add(esfera1, esfera2)

        # ═══════════════════════════════════════════════════════════════
        # PARÁMETROS DE ONDAS EXPANSIVAS - AJUSTA AQUÍ
        # ═══════════════════════════════════════════════════════════════
        # Onda 1 (principal)
        velocidad_onda1 = 0.6  # Velocidad de crecimiento
        stroke_width_onda1 = 5  # Grosor del borde (para efecto 3D)
        opacidad_max_onda1 = 0.9  # Opacidad máxima

        # Onda 2 (secundaria)
        velocidad_onda2 = 0.4  # Más lenta que onda 1
        stroke_width_onda2 = 4  # Grosor del borde
        opacidad_max_onda2 = 0.6  # Más atenuada que onda 1
        # ═══════════════════════════════════════════════════════════════

        # Círculo de intersección (ONDA 1)
        circulo_interseccion = Circle(radius=0.01, color=PURPLE)
        circulo_interseccion.set_fill(PURPLE, opacity=0.5)
        circulo_interseccion.set_stroke(PURPLE_A, width=stroke_width_onda1, opacity=opacidad_max_onda1)

        # ONDA 2 (aparece cuando onda 1 llega a la mitad)
        onda2 = Circle(radius=0.01, color=PURPLE)
        onda2.set_fill(PURPLE, opacity=0.3)
        onda2.set_stroke(PURPLE_A, width=stroke_width_onda2, opacity=opacidad_max_onda2)
        onda2_activa = False
        onda2_tiempo = 0
        radio_onda2 = 0

        dt = 0.05
        t = 0
        fusionadas = False
        tiempo_fusion = 0
        radio_interseccion = 0

        # CONTROL DE FASES
        fase_rotacion = "sin_contacto"
        theta_inicial = 30 * DEGREES
        theta_final = 30 * DEGREES + PI

        # Opacidades iniciales de las esferas (para la desaparición)
        opacidad_fill_inicial = 0.10
        opacidad_stroke_inicial = 0.35
        duracion_desaparicion = 1.0

        while t < 8:
            # PASO 1: Actualizar física de burbujas
            b1.actualizar_posicion(dt)
            b2.actualizar_posicion(dt)

            # PASO 2: Sincronizar esferas visuales
            esfera1.move_to(b1.posicion)
            esfera2.move_to(b2.posicion)

            # Detectar contacto
            distancia = np.linalg.norm(b1.posicion - b2.posicion)

            if not fusionadas and distancia <= (b1.radio + b2.radio):
                b1.fusionar_con(b2)
                fusionadas = True
                fase_rotacion = "expansion"
                self.add(circulo_interseccion)

            # PASO 3: Actualizar ondas expansivas
            if fusionadas:
                # Radio máximo para las ondas
                radio_maximo = b1.radio * 0.8

                # ═══════════════════════════════════════════════════════════════
                # ONDA 1 (Principal)
                # ═══════════════════════════════════════════════════════════════
                radio_interseccion = min(tiempo_fusion * velocidad_onda1, radio_maximo)

                # Calcular opacidad decreciente para onda 1
                progreso_onda1 = radio_interseccion / radio_maximo if radio_maximo > 0 else 0
                opacidad_onda1 = opacidad_max_onda1 * (1 - progreso_onda1)

                # Centro EXACTO entre las esferas
                centro = (b1.posicion + b2.posicion) / 2

                # Vector NORMAL
                delta = b2.posicion - b1.posicion
                distancia_centros = np.linalg.norm(delta)

                if distancia_centros > 0.001:
                    normal = delta / distancia_centros
                else:
                    normal = np.array([1, 0, 0])

                # Crear círculo NUEVO orientado correctamente (ONDA 1)
                nuevo_circulo = Circle(radius=radio_interseccion, color=PURPLE)
                nuevo_circulo.set_fill(PURPLE, opacity=0.3)
                nuevo_circulo.set_stroke(PURPLE_A, width=stroke_width_onda1, opacity=opacidad_onda1)

                # Orientar el círculo perpendicular al vector normal
                eje_z = np.array([0, 0, 1])
                cross = np.cross(eje_z, normal)
                cross_norm = np.linalg.norm(cross)

                if cross_norm > 0.001:
                    eje_rotacion = cross / cross_norm
                    dot_product = np.clip(np.dot(eje_z, normal), -1.0, 1.0)
                    angulo = np.arccos(dot_product)
                    nuevo_circulo.rotate(angulo, axis=eje_rotacion)
                elif np.dot(eje_z, normal) < 0:
                    nuevo_circulo.rotate(PI, axis=RIGHT)

                nuevo_circulo.move_to(centro)
                circulo_interseccion.become(nuevo_circulo)

                # ═══════════════════════════════════════════════════════════════
                # ONDA 2 (Secundaria) - Aparece cuando onda 1 llega a la mitad
                # ═══════════════════════════════════════════════════════════════
                if not onda2_activa and progreso_onda1 >= 0.5:
                    onda2_activa = True
                    self.add(onda2)

                if onda2_activa:
                    # Crecer onda 2 más lenta
                    radio_onda2 = min(onda2_tiempo * velocidad_onda2, radio_maximo)

                    # Calcular opacidad decreciente para onda 2
                    progreso_onda2 = radio_onda2 / radio_maximo if radio_maximo > 0 else 0
                    opacidad_onda2 = opacidad_max_onda2 * (1 - progreso_onda2)

                    # Crear círculo NUEVO para onda 2
                    nuevo_onda2 = Circle(radius=radio_onda2, color=PURPLE)
                    nuevo_onda2.set_fill(PURPLE, opacity=0.2)
                    nuevo_onda2.set_stroke(PURPLE_A, width=stroke_width_onda2, opacity=opacidad_onda2)

                    # Orientar igual que onda 1
                    if cross_norm > 0.001:
                        nuevo_onda2.rotate(angulo, axis=eje_rotacion)
                    elif np.dot(eje_z, normal) < 0:
                        nuevo_onda2.rotate(PI, axis=RIGHT)

                    nuevo_onda2.move_to(centro)
                    onda2.become(nuevo_onda2)

                    onda2_tiempo += dt

                # ═══════════════════════════════════════════════════════════════

                # FASE 1: EXPANSIÓN (0-2 segundos)
                if fase_rotacion == "expansion":
                    if tiempo_fusion >= 2.0:
                        fase_rotacion = "rotando"

                # FASE 2: ROTACIÓN (1 segundo)
                elif fase_rotacion == "rotando":
                    tiempo_rotacion = tiempo_fusion - 2.0
                    if tiempo_rotacion <= 1.0:
                        progreso = tiempo_rotacion / 1.0
                        theta_actual = theta_inicial + (theta_final - theta_inicial) * progreso
                        self.set_camera_orientation(phi=70 * DEGREES, theta=theta_actual)
                    else:
                        fase_rotacion = "desaparecer_esferas"

                # FASE 3: DESAPARECER ESFERAS (1 segundo)
                elif fase_rotacion == "desaparecer_esferas":
                    tiempo_desaparicion = tiempo_fusion - 3.0
                    if tiempo_desaparicion <= duracion_desaparicion:
                        progreso = tiempo_desaparicion / duracion_desaparicion
                        opacidad_fill_actual = opacidad_fill_inicial * (1 - progreso)
                        opacidad_stroke_actual = opacidad_stroke_inicial * (1 - progreso)

                        esfera1.set_fill(b1.color, opacity=opacidad_fill_actual)
                        esfera1.set_stroke(b1.color, width=2, opacity=opacidad_stroke_actual)

                        esfera2.set_fill(b2.color, opacity=opacidad_fill_actual)
                        esfera2.set_stroke(b2.color, width=2, opacity=opacidad_stroke_actual)
                    else:
                        fase_rotacion = "terminado"

                # FASE 4: TERMINADO
                elif fase_rotacion == "terminado":
                    break

                tiempo_fusion += dt

            self.wait(dt)
            t += dt

        self.wait(0.5)
