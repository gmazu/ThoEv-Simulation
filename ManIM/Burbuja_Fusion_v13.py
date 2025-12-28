# Fusión de burbujas 3D con cámara orbital TEMPORIZADA
# v13: Glow de prueba con efecto boya (sube/baja con las ondas)
from manim import *
import numpy as np
import random

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
        b2 = BurbujaFusion3D([2.5, 0, 0], [-0.5, 0, 0], 1.2, 1.0, RED_C)

        # Crear esferas visuales MÁS SUTILES
        esfera1 = Sphere(radius=b1.radio, resolution=(20, 20))
        esfera1.set_color(b1.color)
        esfera1.set_fill(b1.color, opacity=0.10)
        esfera1.set_stroke(b1.color, width=2, opacity=0.35)
        esfera1.move_to(b1.posicion)

        esfera2 = Sphere(radius=b2.radio, resolution=(20, 20))
        esfera2.set_color(b2.color)
        esfera2.set_fill(b2.color, opacity=0.10)
        esfera2.set_stroke(b2.color, width=2, opacity=0.35)
        esfera2.move_to(b2.posicion)

        self.add(esfera1, esfera2)

        # ═══════════════════════════════════════════════════════════════
        # CONFIGURACIÓN DE ONDAS EXPANSIVAS - AJUSTA AQUÍ
        # ═══════════════════════════════════════════════════════════════
        num_ondas = 4

        velocidad_base = 0.6
        factor_velocidad = 0.7
        opacidad_base = 0.9
        factor_opacidad = 0.75
        stroke_width_base = 6
        factor_stroke = 0.85
        umbral_activacion = 0.5

        # ═══════════════════════════════════════════════════════════════
        # CONFIGURACIÓN DE LUCIÉRNAGAS - AJUSTA AQUÍ
        # ═══════════════════════════════════════════════════════════════
        # PRUEBA: Solo 1 luciérnaga con efecto glow
        tamano_nucleo = 0.03  # Núcleo brillante
        tamano_halo = 0.08  # Halo/aura alrededor
        radio_prueba = 0.25  # Radio donde aparece (más cerca del centro)
        velocidad_encendido = 8.0  # Qué tan rápido se enciende
        velocidad_apagado = 0.8  # Qué tan lento se apaga (más lento para durar más)
        # ═══════════════════════════════════════════════════════════════

        # Crear sistema de ondas
        ondas = []
        for i in range(num_ondas):
            velocidad = velocidad_base * (factor_velocidad ** i)
            opacidad_max = opacidad_base * (factor_opacidad ** i)
            stroke_width = max(2, int(stroke_width_base * (factor_stroke ** i)))

            circulo = Circle(radius=0.01, color=PURPLE)
            circulo.set_fill(PURPLE, opacity=opacidad_max * 0.3)
            circulo.set_stroke(PURPLE_A, width=stroke_width, opacity=opacidad_max)

            ondas.append({
                'circulo': circulo,
                'velocidad': velocidad,
                'opacidad_max': opacidad_max,
                'stroke_width': stroke_width,
                'radio': 0,
                'tiempo': 0,
                'activa': (i == 0),
                'agregada': False
            })

        # Radio máximo para las ondas
        radio_maximo = b1.radio * 0.8

        # Crear UNA luciérnaga de prueba con efecto glow
        # Núcleo brillante
        nucleo = Dot(radius=tamano_nucleo, color=WHITE)
        nucleo.set_fill(WHITE, opacity=0)

        # Halo/aura alrededor
        halo = Circle(radius=tamano_halo, color=WHITE)
        halo.set_fill(WHITE, opacity=0)
        halo.set_stroke(WHITE, width=1, opacity=0)

        # Offset en el plano del círculo lila (posición fija para prueba)
        offset_glow = np.array([radio_prueba, 0, 0])

        # Estado del glow
        glow_estado = {
            'nucleo': nucleo,
            'halo': halo,
            'offset': offset_glow,
            'opacidad': 0,
            'estado': 'inactivo',  # Estados: inactivo, encendiendo, apagando
            'agregado': False,
            'desplazamiento_boya': 0  # Desplazamiento vertical (como boya)
        }

        dt = 0.05
        t = 0
        fusionadas = False
        tiempo_fusion = 0

        # CONTROL DE FASES
        fase_rotacion = "sin_contacto"
        theta_inicial = 30 * DEGREES
        theta_final = 30 * DEGREES + PI

        # Opacidades iniciales de las esferas
        opacidad_fill_inicial = 0.10
        opacidad_stroke_inicial = 0.35
        duracion_desaparicion = 1.0

        while t < 20:
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

            # PASO 3: Actualizar ondas y chispazos
            if fusionadas:
                centro = (b1.posicion + b2.posicion) / 2
                delta = b2.posicion - b1.posicion
                distancia_centros = np.linalg.norm(delta)

                if distancia_centros > 0.001:
                    normal = delta / distancia_centros
                else:
                    normal = np.array([1, 0, 0])

                # Calcular rotación
                eje_z = np.array([0, 0, 1])
                cross = np.cross(eje_z, normal)
                cross_norm = np.linalg.norm(cross)

                # === ONDAS ===
                for i, onda in enumerate(ondas):
                    if onda['activa']:
                        if not onda['agregada']:
                            self.add(onda['circulo'])
                            onda['agregada'] = True

                        # Crecer onda
                        onda['radio'] = min(onda['tiempo'] * onda['velocidad'], radio_maximo)
                        progreso = onda['radio'] / radio_maximo if radio_maximo > 0 else 0
                        opacidad_actual = onda['opacidad_max'] * (1 - progreso)

                        # Crear círculo
                        nuevo_circulo = Circle(radius=onda['radio'], color=PURPLE)
                        nuevo_circulo.set_fill(PURPLE, opacity=opacidad_actual * 0.3)
                        nuevo_circulo.set_stroke(PURPLE_A, width=onda['stroke_width'], opacity=opacidad_actual)

                        # Orientar círculo
                        if cross_norm > 0.001:
                            eje_rotacion = cross / cross_norm
                            dot_product = np.clip(np.dot(eje_z, normal), -1.0, 1.0)
                            angulo = np.arccos(dot_product)
                            nuevo_circulo.rotate(angulo, axis=eje_rotacion)
                        elif np.dot(eje_z, normal) < 0:
                            nuevo_circulo.rotate(PI, axis=RIGHT)

                        nuevo_circulo.move_to(centro)
                        onda['circulo'].become(nuevo_circulo)

                        onda['tiempo'] += dt

                        # Activar siguiente onda
                        if i < len(ondas) - 1 and not ondas[i + 1]['activa']:
                            if progreso >= umbral_activacion:
                                ondas[i + 1]['activa'] = True

                # === GLOW DE PRUEBA (comportamiento de boya) ===
                if ondas[0]['activa']:  # Solo con la primera onda
                    radio_onda_1 = ondas[0]['radio']

                    # Activar glow cuando la onda pasa por su radio
                    if glow_estado['estado'] == 'inactivo' and radio_onda_1 >= radio_prueba:
                        glow_estado['estado'] = 'encendiendo'

                        # Agregar a escena
                        if not glow_estado['agregado']:
                            self.add(glow_estado['halo'], glow_estado['nucleo'])
                            glow_estado['agregado'] = True

                    # Actualizar opacidad según estado
                    if glow_estado['estado'] == 'encendiendo':
                        # Encender rápido
                        glow_estado['opacidad'] = min(1.0, glow_estado['opacidad'] + velocidad_encendido * dt)

                        if glow_estado['opacidad'] >= 1.0:
                            glow_estado['estado'] = 'apagando'

                    elif glow_estado['estado'] == 'apagando':
                        # Apagar lento
                        glow_estado['opacidad'] = max(0, glow_estado['opacidad'] - velocidad_apagado * dt)

                        if glow_estado['opacidad'] <= 0:
                            glow_estado['estado'] = 'apagado'

                    # === EFECTO BOYA: Calcular desplazamiento por ondas ===
                    desplazamiento_total = 0
                    amplitud_boya = 0.15  # Qué tan alto/bajo sube la boya
                    ancho_onda = 0.2  # Ancho de influencia de cada onda

                    for onda in ondas:
                        if onda['activa']:
                            # Distancia entre el radio de la onda y el radio del glow
                            distancia_onda = abs(onda['radio'] - radio_prueba)

                            # Si la onda está cerca del glow, contribuye al desplazamiento
                            if distancia_onda < ancho_onda:
                                # Factor que decrece con la distancia (gaussiana simplificada)
                                factor = np.cos((distancia_onda / ancho_onda) * PI / 2) ** 2
                                desplazamiento_total += amplitud_boya * factor

                    glow_estado['desplazamiento_boya'] = desplazamiento_total

                    # === ACTUALIZAR POSICIÓN DEL GLOW ===
                    if glow_estado['agregado']:
                        # Posición base en el plano del círculo lila
                        posicion_base = centro + offset_glow

                        # Desplazamiento perpendicular al plano (dirección del normal)
                        posicion_glow = posicion_base + normal * glow_estado['desplazamiento_boya']

                        # Orientar el halo según el plano del círculo lila
                        nuevo_halo = Circle(radius=tamano_halo, color=WHITE)
                        nuevo_halo.set_fill(WHITE, opacity=0)
                        nuevo_halo.set_stroke(WHITE, width=1, opacity=0)

                        # Aplicar la misma rotación que el círculo lila
                        if cross_norm > 0.001:
                            eje_rotacion = cross / cross_norm
                            dot_product = np.clip(np.dot(eje_z, normal), -1.0, 1.0)
                            angulo = np.arccos(dot_product)
                            nuevo_halo.rotate(angulo, axis=eje_rotacion)
                        elif np.dot(eje_z, normal) < 0:
                            nuevo_halo.rotate(PI, axis=RIGHT)

                        nuevo_halo.move_to(posicion_glow)
                        glow_estado['halo'].become(nuevo_halo)

                        # Posicionar núcleo
                        glow_estado['nucleo'].move_to(posicion_glow)

                        # Aplicar opacidad al glow
                        # Núcleo: opacidad completa
                        glow_estado['nucleo'].set_fill(WHITE, opacity=glow_estado['opacidad'])

                        # Halo: opacidad reducida (más sutil)
                        opacidad_halo = glow_estado['opacidad'] * 0.3
                        glow_estado['halo'].set_fill(WHITE, opacity=opacidad_halo)
                        glow_estado['halo'].set_stroke(WHITE, width=1, opacity=opacidad_halo)

                # FASES DE ANIMACIÓN
                if fase_rotacion == "expansion":
                    if tiempo_fusion >= 2.0:
                        fase_rotacion = "rotando"

                elif fase_rotacion == "rotando":
                    tiempo_rotacion = tiempo_fusion - 2.0
                    if tiempo_rotacion <= 1.0:
                        progreso = tiempo_rotacion / 1.0
                        theta_actual = theta_inicial + (theta_final - theta_inicial) * progreso
                        self.set_camera_orientation(phi=70 * DEGREES, theta=theta_actual)
                    else:
                        fase_rotacion = "desaparecer_esferas"

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
                        # Eliminar glow de prueba
                        if glow_estado['agregado']:
                            self.remove(glow_estado['nucleo'], glow_estado['halo'])
                            glow_estado['agregado'] = False

                        fase_rotacion = "solo_ondas"

                elif fase_rotacion == "solo_ondas":
                    # Esperar a que la última onda se disuelva
                    ultima_onda = ondas[-1]
                    if ultima_onda['activa'] and ultima_onda['radio'] >= radio_maximo * 0.99:
                        fase_rotacion = "terminado"

                elif fase_rotacion == "terminado":
                    break

                tiempo_fusion += dt

            self.wait(dt)
            t += dt

        self.wait(1)
