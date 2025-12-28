# Fusión de burbujas 3D con cámara orbital TEMPORIZADA
# v7: Después de rotación, las esferas desaparecen y queda solo el círculo lila
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

        # Círculo de intersección - MÁS SÓLIDO Y BRILLANTE para que resalte
        circulo_interseccion = Circle(radius=0.01, color=PURPLE)
        circulo_interseccion.set_fill(PURPLE, opacity=0.8)  # Más sólido
        circulo_interseccion.set_stroke(PURPLE_A, width=3, opacity=0.9)  # Más brillante

        dt = 0.05
        t = 0
        fusionadas = False
        tiempo_fusion = 0
        radio_interseccion = 0

        # CONTROL DE FASES
        fase_rotacion = "sin_contacto"  # Estados: "sin_contacto", "expansion", "rotando", "desaparecer_esferas", "terminado"
        theta_inicial = 30 * DEGREES
        theta_final = 30 * DEGREES + PI  # Rotar 180 grados

        # Opacidades iniciales de las esferas (para la desaparición)
        opacidad_fill_inicial = 0.10
        opacidad_stroke_inicial = 0.35
        duracion_desaparicion = 1.0  # Duración de la desaparición en segundos

        while t < 8:
            # PASO 1: Actualizar física de burbujas
            b1.actualizar_posicion(dt)
            b2.actualizar_posicion(dt)

            # PASO 2: Sincronizar esferas visuales con posiciones físicas INMEDIATAMENTE
            esfera1.move_to(b1.posicion)
            esfera2.move_to(b2.posicion)

            # Detectar contacto
            distancia = np.linalg.norm(b1.posicion - b2.posicion)

            if not fusionadas and distancia <= (b1.radio + b2.radio):
                b1.fusionar_con(b2)
                fusionadas = True
                fase_rotacion = "expansion"  # Iniciar fase de expansión
                # Agregar círculo de intersección
                self.add(circulo_interseccion)

            # PASO 3: Actualizar círculo de intersección EN CADA FRAME (100% sincronizado)
            if fusionadas:
                # Crecer el círculo de intersección
                velocidad_crecimiento = 0.6
                radio_interseccion = min(tiempo_fusion * velocidad_crecimiento, b1.radio * 0.8)

                # ═══════════════════════════════════════════════════════════════
                # SINCRONIZACIÓN COMPLETA DEL CÍRCULO LILA
                # ═══════════════════════════════════════════════════════════════

                # Centro EXACTO entre las esferas (usando posiciones YA actualizadas)
                centro = (b1.posicion + b2.posicion) / 2

                # Vector NORMAL (perpendicular al círculo) - dirección entre centros
                delta = b2.posicion - b1.posicion
                distancia_centros = np.linalg.norm(delta)

                if distancia_centros > 0.001:  # Evitar división por cero
                    normal = delta / distancia_centros
                else:
                    normal = np.array([1, 0, 0])  # Default si están muy cerca

                # Crear círculo NUEVO orientado correctamente
                # El círculo debe estar en un plano perpendicular a 'normal'

                # 1. Crear círculo base en plano XY
                nuevo_circulo = Circle(radius=radio_interseccion, color=PURPLE)
                nuevo_circulo.set_fill(PURPLE, opacity=0.8)
                nuevo_circulo.set_stroke(PURPLE_A, width=3, opacity=0.9)

                # 2. Orientar el círculo perpendicular al vector normal
                # Usar el eje Z como referencia inicial
                eje_z = np.array([0, 0, 1])

                # Calcular el ángulo y eje de rotación necesarios
                # para rotar de Z hacia 'normal'
                cross = np.cross(eje_z, normal)
                cross_norm = np.linalg.norm(cross)

                if cross_norm > 0.001:  # Si no son paralelos
                    # Eje de rotación (normalizado)
                    eje_rotacion = cross / cross_norm

                    # Ángulo de rotación
                    dot_product = np.clip(np.dot(eje_z, normal), -1.0, 1.0)
                    angulo = np.arccos(dot_product)

                    # Aplicar rotación única y limpia
                    nuevo_circulo.rotate(angulo, axis=eje_rotacion)
                elif np.dot(eje_z, normal) < 0:
                    # Si son antiparalelos, rotar 180 grados
                    nuevo_circulo.rotate(PI, axis=RIGHT)

                # 3. Mover al centro exacto
                nuevo_circulo.move_to(centro)

                # 4. REEMPLAZAR el círculo viejo con el nuevo (sincronización total)
                circulo_interseccion.become(nuevo_circulo)

                # ═══════════════════════════════════════════════════════════════

                # FASE 1: EXPANSIÓN (0-2 segundos) - SIN ROTACIÓN
                if fase_rotacion == "expansion":
                    if tiempo_fusion >= 2.0:
                        fase_rotacion = "rotando"

                # FASE 2: ROTACIÓN (1 segundo)
                elif fase_rotacion == "rotando":
                    tiempo_rotacion = tiempo_fusion - 2.0
                    if tiempo_rotacion <= 1.0:
                        # Interpolar suavemente la rotación
                        progreso = tiempo_rotacion / 1.0
                        theta_actual = theta_inicial + (theta_final - theta_inicial) * progreso
                        self.set_camera_orientation(phi=70 * DEGREES, theta=theta_actual)
                    else:
                        fase_rotacion = "desaparecer_esferas"

                # FASE 3: DESAPARECER ESFERAS (1 segundo)
                elif fase_rotacion == "desaparecer_esferas":
                    tiempo_desaparicion = tiempo_fusion - 3.0  # Empieza en t=3 (después de expansion + rotacion)
                    if tiempo_desaparicion <= duracion_desaparicion:
                        # Interpolar opacidad de las esferas hacia 0
                        progreso = tiempo_desaparicion / duracion_desaparicion
                        opacidad_fill_actual = opacidad_fill_inicial * (1 - progreso)
                        opacidad_stroke_actual = opacidad_stroke_inicial * (1 - progreso)

                        # Actualizar opacidad de las esferas
                        esfera1.set_fill(b1.color, opacity=opacidad_fill_actual)
                        esfera1.set_stroke(b1.color, width=2, opacity=opacidad_stroke_actual)

                        esfera2.set_fill(b2.color, opacity=opacidad_fill_actual)
                        esfera2.set_stroke(b2.color, width=2, opacity=opacidad_stroke_actual)
                    else:
                        fase_rotacion = "terminado"

                # FASE 4: TERMINADO - Salir inmediatamente
                elif fase_rotacion == "terminado":
                    break

                tiempo_fusion += dt

            self.wait(dt)
            t += dt

        self.wait(0.5)
