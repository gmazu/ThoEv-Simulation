# Fusión de burbujas 3D con cámara orbital TEMPORIZADA
# v17.1.1: Título handwriting + datos reales ThöEv-RğB
from manim import *
import numpy as np
import random

# ═══════════════════════════════════════════════════════════════
# DATOS REALES ThöEv-RğB
# ═══════════════════════════════════════════════════════════════
# Sistema de unidades: 1 UO = 46.5 Gly = Radio universo observable

R_PROTOCOSMOS = 1.16          # Radio cada protocosmos en UO (54 Gly)
PENETRACION_ACTUAL = 0.88     # Penetración actual en UO (41 Gly)
VELOCIDAD_COLISION = 6        # Velocidad en unidades de c (6c)
ARCO_INTERSECCION = 1.77      # Arco total intersección en UO (82 Gly)
RESTANTE_COLISION = 0.28      # Restante por colisionar en UO (13 Gly)

# Distancias calculadas
DISTANCIA_INICIAL = R_PROTOCOSMOS * 3      # 3.48 UO
DISTANCIA_CONTACTO = R_PROTOCOSMOS * 2     # 2.32 UO
DISTANCIA_ACTUAL = DISTANCIA_CONTACTO - PENETRACION_ACTUAL  # 1.44 UO

# Escala visual para Manim
ESCALA_MANIM = 1.0  # Ajustar si las esferas son muy grandes/pequeñas

# ═══════════════════════════════════════════════════════════════


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

        # ═══════════════════════════════════════════════════════════════
        # TÍTULO HANDWRITING + VERSIÓN
        # ═══════════════════════════════════════════════════════════════

        # Título principal con estilo handwriting (CENTRADO SOLO)
        titulo = Text(
            "ThöEv-RğB",
            font="serif",
            font_size=72,
            color=WHITE,
            slant=ITALIC
        )
        titulo.to_edge(UP, buff=0.5)

        # Versión (pegada al título, alineada al piso)
        version = Text(
            "v131n",
            font="monospace",
            font_size=20,
            color=GRAY_C
        )
        version.next_to(titulo, RIGHT, buff=0.2).align_to(titulo, DOWN)

        # Subtítulo (más pequeño)
        subtitulo = Text(
            "Colisión → Big Freeze",
            font="serif",
            font_size=30,
            color=GRAY_B
        )
        subtitulo.next_to(titulo, DOWN, buff=0.3)

        # Animación secuencial: título → versión → subtítulo
        # (cada uno se agrega como fixed_in_frame ANTES de animarlo)

        # 1. Título
        self.add_fixed_in_frame_mobjects(titulo)
        self.play(Write(titulo), run_time=2)

        # 2. Versión
        self.add_fixed_in_frame_mobjects(version)
        self.play(FadeIn(version), run_time=0.5)

        # 3. Subtítulo
        self.add_fixed_in_frame_mobjects(subtitulo)
        self.play(FadeIn(subtitulo, shift=UP * 0.2), run_time=1)

        self.wait(1)

        # ═══════════════════════════════════════════════════════════════
        # SIMULACIÓN 3D
        # ═══════════════════════════════════════════════════════════════

        # Configurar cámara 3D
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        # Usar datos reales escalados
        radio_visual = R_PROTOCOSMOS * ESCALA_MANIM

        # Crear burbujas 3D con datos reales
        b1 = BurbujaFusion3D([-2.5, 0, 0], [0.5, 0, 0], radio_visual, 1.0, BLUE)
        b2 = BurbujaFusion3D([2.5, 0, 0], [-0.5, 0, 0], radio_visual, 1.0, RED_C)

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
        # CONFIGURACIÓN DE GALAXIAS EN ESPACIOS VACÍOS - AJUSTA AQUÍ
        # ═══════════════════════════════════════════════════════════════
        tamano_nucleo = 0.02  # Núcleo sutil
        tamano_halo = 0.05  # Halo sutil
        radio_zona_galaxias = 0.35  # Radio máximo donde aparecen galaxias
        num_galaxias = 20  # Cantidad de galaxias (distribuidas aleatoriamente)
        velocidad_encendido_base = 6.0  # Base para encendido
        velocidad_apagado_base = 0.8  # Base para apagado
        velocidad_expansion_base = 0.3  # Velocidad de expansión radial
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

        # Crear 4 CONJUNTOS de galaxias (uno por cada onda)
        conjuntos_galaxias = []

        for idx_conjunto in range(num_ondas):
            galaxias = []
            for i in range(num_galaxias):
                # Distribución aleatoria dentro del círculo (espacios vacíos)
                # Usar coordenadas polares aleatorias
                radio_aleatorio = random.uniform(0.1, radio_zona_galaxias)
                angulo_aleatorio = random.uniform(0, 2 * np.pi)

                # Offset en el plano del círculo lila
                offset_glow = np.array([
                    radio_aleatorio * np.cos(angulo_aleatorio),
                    radio_aleatorio * np.sin(angulo_aleatorio),
                    0
                ])

                # Variación aleatoria para cada galaxia
                variacion_encendido = random.uniform(0.7, 1.3)  # ±30%
                variacion_apagado = random.uniform(0.6, 1.4)  # ±40%
                brillo_max = random.uniform(0.5, 1.0)  # 50%-100% brillo
                delay_activacion = random.uniform(0, 0.15)  # Delay aleatorio

                # Dirección radial normalizada para expansión
                direccion_radial = np.array([np.cos(angulo_aleatorio), np.sin(angulo_aleatorio), 0])
                velocidad_expansion = velocidad_expansion_base * random.uniform(0.8, 1.2)

                # Núcleo brillante (tamaño variable)
                tamano_nucleo_var = tamano_nucleo * random.uniform(0.8, 1.2)
                nucleo = Dot(radius=tamano_nucleo_var, color=WHITE)
                nucleo.set_fill(WHITE, opacity=0)

                # Halo/aura alrededor (tamaño variable)
                tamano_halo_var = tamano_halo * random.uniform(0.8, 1.2)
                halo = Circle(radius=tamano_halo_var, color=WHITE)
                halo.set_fill(WHITE, opacity=0)
                halo.set_stroke(WHITE, width=1, opacity=0)

                # Estado de esta galaxia
                galaxias.append({
                    'nucleo': nucleo,
                    'halo': halo,
                    'offset': offset_glow,
                    'radio': radio_aleatorio,  # Radio específico de esta galaxia
                    'opacidad': 0,
                    'estado': 'inactivo',
                    'agregado': False,
                    'velocidad_encendido': velocidad_encendido_base * variacion_encendido,
                    'velocidad_apagado': velocidad_apagado_base * variacion_apagado,
                    'brillo_max': brillo_max,
                    'delay_activacion': delay_activacion,
                    'tiempo_desde_onda': 0,
                    'direccion_radial': direccion_radial,  # Dirección de expansión
                    'velocidad_expansion': velocidad_expansion  # Velocidad de expansión
                })

            # Agregar este conjunto a la lista de conjuntos
            conjuntos_galaxias.append(galaxias)

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

                # === 4 CONJUNTOS DE GALAXIAS (uno por onda) ===
                # Procesar cada onda y su conjunto de galaxias correspondiente
                for idx_onda, onda in enumerate(ondas):
                    if onda['activa']:
                        radio_onda = onda['radio']
                        galaxias_actuales = conjuntos_galaxias[idx_onda]

                        # BORRAR conjunto de 2 ondas atrás (máximo 2 conjuntos visibles)
                        if idx_onda >= 2 and onda['tiempo'] < dt * 2:  # Recién activada
                            galaxias_2_atras = conjuntos_galaxias[idx_onda - 2]
                            for gal_ant in galaxias_2_atras:
                                if gal_ant['agregado']:
                                    self.remove(gal_ant['nucleo'], gal_ant['halo'])
                                    gal_ant['agregado'] = False
                                    gal_ant['estado'] = 'apagado'

                        # Actualizar cada galaxia de este conjunto
                        for galaxia in galaxias_actuales:
                            # Activar galaxia cuando la onda pasa por SU radio específico + delay
                            if galaxia['estado'] == 'inactivo' and radio_onda >= galaxia['radio']:
                                galaxia['tiempo_desde_onda'] += dt

                                # Activar después del delay
                                if galaxia['tiempo_desde_onda'] >= galaxia['delay_activacion']:
                                    galaxia['estado'] = 'encendiendo'

                                    # Agregar a escena
                                    if not galaxia['agregado']:
                                        self.add(galaxia['halo'], galaxia['nucleo'])
                                        galaxia['agregado'] = True

                            # Actualizar opacidad según estado (con velocidades variables)
                            if galaxia['estado'] == 'encendiendo':
                                # Encender con velocidad variable
                                galaxia['opacidad'] = min(galaxia['brillo_max'],
                                                         galaxia['opacidad'] + galaxia['velocidad_encendido'] * dt)

                                if galaxia['opacidad'] >= galaxia['brillo_max']:
                                    galaxia['estado'] = 'apagando'

                            elif galaxia['estado'] == 'apagando':
                                # Apagar con velocidad variable
                                galaxia['opacidad'] = max(0, galaxia['opacidad'] - galaxia['velocidad_apagado'] * dt)

                                if galaxia['opacidad'] <= 0:
                                    galaxia['estado'] = 'apagado'

                            # === EXPANSIÓN RADIAL ===
                            # Mover galaxia hacia afuera si está activa (encendiendo o apagando)
                            if galaxia['estado'] in ['encendiendo', 'apagando']:
                                # Actualizar offset (mover radialmente hacia afuera)
                                galaxia['offset'] += galaxia['direccion_radial'] * galaxia['velocidad_expansion'] * dt

                            # === ACTUALIZAR POSICIÓN DE LA GALAXIA ===
                            if galaxia['agregado']:
                                # ROTAR el offset para que esté en el plano del círculo lila
                                offset_local = galaxia['offset']

                                # Rotar el offset usando la misma transformación que el círculo lila
                                if cross_norm > 0.001:
                                    eje_rotacion = cross / cross_norm
                                    dot_product = np.clip(np.dot(eje_z, normal), -1.0, 1.0)
                                    angulo_rotacion = np.arccos(dot_product)

                                    # Aplicar rotación de Rodrigues al offset
                                    k = eje_rotacion
                                    v = offset_local
                                    cos_a = np.cos(angulo_rotacion)
                                    sin_a = np.sin(angulo_rotacion)
                                    offset_rotado = v * cos_a + np.cross(k, v) * sin_a + k * np.dot(k, v) * (1 - cos_a)
                                elif np.dot(eje_z, normal) < 0:
                                    # Rotación de 180° alrededor del eje X
                                    offset_rotado = np.array([offset_local[0], -offset_local[1], -offset_local[2]])
                                else:
                                    # Sin rotación
                                    offset_rotado = offset_local

                                # Posición fija en el plano del círculo lila (SIN movimiento ondulatorio)
                                posicion_glow = centro + offset_rotado

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
                                galaxia['halo'].become(nuevo_halo)

                                # Posicionar núcleo
                                galaxia['nucleo'].move_to(posicion_glow)

                                # Aplicar opacidad a la galaxia (SUTIL)
                                # Núcleo: opacidad variable
                                galaxia['nucleo'].set_fill(WHITE, opacity=galaxia['opacidad'])

                                # Halo: muy sutil
                                opacidad_halo = galaxia['opacidad'] * 0.3
                                galaxia['halo'].set_fill(WHITE, opacity=opacidad_halo)
                                galaxia['halo'].set_stroke(WHITE, width=1, opacity=opacidad_halo * 0.5)

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
                        # Eliminar TODOS los conjuntos de galaxias
                        for conjunto in conjuntos_galaxias:
                            for galaxia in conjunto:
                                if galaxia['agregado']:
                                    self.remove(galaxia['nucleo'], galaxia['halo'])
                                    galaxia['agregado'] = False

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

        # Fade out de la versión al final
        self.play(FadeOut(version), run_time=1)
        self.wait(1)
