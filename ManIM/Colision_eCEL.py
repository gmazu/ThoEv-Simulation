# colision_universos_v1.py
# ThöEv-RğB - Colisión de Universos
# Version: 1.0
# Tags: colision, universos, protones, electrones, origen
# Timeline: 0-45 segundos
# Event Log:
#   - 0-10s: Dos universos acercándose
#   - 10-20s: Momento de colisión
#   - 20-35s: Formación estructura inicial
#   - 35-45s: Título final

from manim import *
import numpy as np

class ColisionUniversos(ThreeDScene):
    def construct(self):
        # Configuración
        self.camera.background_color = BLACK

        # Configurar cámara 3D
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        
        # ESCENA 1: Dos universos separados (0-10s)
        self.escena_1_universos_separados()
        
        # ESCENA 2: Aceleración y colisión (10-20s)
        self.escena_2_colision()
        
        # ESCENA 3: Formación estructura (20-35s)
        self.escena_3_formacion()
        
        # ESCENA 4: Título final (35-45s)
        self.escena_4_titulo()
    
    def escena_1_universos_separados(self):
        """0-10s: Dos burbujas de jabón acercándose"""
        
        # Universo de protones (izquierda, rojo/naranja)
        universo_protones = self.crear_burbuja(
            center=LEFT * 4,
            radius=1.5,
            color=RED,
            num_particulas=50
        )
        
        # Universo de electrones (derecha, azul/violeta)
        universo_electrones = self.crear_burbuja(
            center=RIGHT * 4,
            radius=1.5,
            color=BLUE,
            num_particulas=50
        )
        
        # Mostrar burbujas
        self.play(
            FadeIn(universo_protones["burbuja"]),
            FadeIn(universo_electrones["burbuja"]),
            *[FadeIn(p) for p in universo_protones["particulas"]],
            *[FadeIn(p) for p in universo_electrones["particulas"]],
            run_time=2
        )
        
        # Movimiento lento acercándose
        self.play(
            universo_protones["grupo"].animate.shift(RIGHT * 2),
            universo_electrones["grupo"].animate.shift(LEFT * 2),
            run_time=8,
            rate_func=smooth
        )
        
        self.universo_protones = universo_protones
        self.universo_electrones = universo_electrones
    
    def escena_2_colision(self):
        """10-20s: Momento de colisión con deformación y ondas"""

        # Aceleración final
        self.play(
            self.universo_protones["grupo"].animate.shift(RIGHT * 1.5),
            self.universo_electrones["grupo"].animate.shift(LEFT * 1.5),
            run_time=3,
            rate_func=rush_into
        )

        # Deformación de burbujas al contacto (efecto newtoniano)
        burbuja_p = self.universo_protones["burbuja"]
        burbuja_e = self.universo_electrones["burbuja"]

        # Deformar burbujas hacia adentro en el punto de contacto
        self.play(
            burbuja_p.animate.stretch(0.7, 0),  # comprimir en X
            burbuja_e.animate.stretch(0.7, 0),
            run_time=0.3
        )

        # Ondas expansivas desde el punto de colisión
        self.crear_ondas_expansivas(num_ondas=5, duracion=2)

        # Recuperar forma mientras se fusionan
        self.play(
            burbuja_p.animate.stretch(1/0.7, 0).set_opacity(0.2),
            burbuja_e.animate.stretch(1/0.7, 0).set_opacity(0.2),
            run_time=0.5
        )

        # Flash de colisión (esfera 3D)
        flash = Sphere(radius=3, resolution=(20, 20))
        flash.set_color(WHITE)
        flash.set_opacity(0.8)
        self.add(flash)
        self.play(
            flash.animate.scale(0.1).set_opacity(0),
            run_time=0.5
        )
        self.remove(flash)

        # Explosión de partículas
        self.explosion_particulas()

        self.wait(1)
    
    def escena_3_formacion(self):
        """20-35s: Formación estructura inicial"""
        
        # Todas las partículas comienzan a organizarse
        # (Simplificado: formación circular inicial)
        
        todas_particulas = (
            self.universo_protones["particulas"] + 
            self.universo_electrones["particulas"]
        )
        
        # Organizar en patrón inicial (grid básico)
        organizacion = VGroup()
        for i, particula in enumerate(todas_particulas):
            angulo = i * (2 * PI / len(todas_particulas))
            nueva_pos = np.array([
                2 * np.cos(angulo),
                2 * np.sin(angulo),
                0
            ])
            organizacion.add(particula)
        
        self.play(
            *[p.animate.move_to(
                np.array([
                    2 * np.cos(i * 2 * PI / len(todas_particulas)),
                    2 * np.sin(i * 2 * PI / len(todas_particulas)),
                    0
                ])
            ) for i, p in enumerate(todas_particulas)],
            run_time=10,
            rate_func=smooth
        )
        
        self.wait(2)
    
    def escena_4_titulo(self):
        """35-45s: Título final"""
        
        # Fade out partículas
        self.play(
            *[FadeOut(p) for p in self.universo_protones["particulas"]],
            *[FadeOut(p) for p in self.universo_electrones["particulas"]],
            FadeOut(self.universo_protones["burbuja"]),
            FadeOut(self.universo_electrones["burbuja"]),
            run_time=2
        )
        
        # Título principal
        titulo = Text("ThöEv (●)●)•( RğB", font_size=60)
        subtitulo = Text("Theory of Everything", font_size=36)
        formula = MathTex("E = Mc^3", font_size=48)
        
        titulo.to_edge(UP, buff=1)
        subtitulo.next_to(titulo, DOWN, buff=0.5)
        formula.next_to(subtitulo, DOWN, buff=0.8)
        
        self.play(
            Write(titulo),
            run_time=2
        )
        self.play(
            FadeIn(subtitulo),
            run_time=1.5
        )
        self.play(
            Write(formula),
            run_time=2
        )
        
        self.wait(3)
    
    def crear_burbuja(self, center, radius, color, num_particulas):
        """Crea una burbuja 3D con partículas dentro"""

        # Burbuja (esfera 3D transparente con efecto jabón)
        burbuja = Sphere(
            radius=radius,
            resolution=(30, 30)
        ).move_to(center)

        # Aplicar colores con gradiente tipo burbuja de jabón
        burbuja.set_color(color)
        burbuja.set_opacity(0.3)
        burbuja.set_stroke(color=color, width=1)
        burbuja.set_sheen_direction(UL)
        burbuja.set_sheen(0.5)

        # Partículas dentro distribuidas en 3D
        particulas = []
        for _ in range(num_particulas):
            # Posición aleatoria dentro de la esfera usando coordenadas esféricas
            r = radius * np.cbrt(np.random.random())  # cbrt para distribución uniforme en volumen
            theta = 2 * PI * np.random.random()  # ángulo azimutal
            phi = np.arccos(2 * np.random.random() - 1)  # ángulo polar

            pos = center + np.array([
                r * np.sin(phi) * np.cos(theta),
                r * np.sin(phi) * np.sin(theta),
                r * np.cos(phi)
            ])

            particula = Sphere(
                radius=0.04,
                resolution=(8, 8)
            ).move_to(pos)
            particula.set_color(color)
            particula.set_sheen(0.8)
            particulas.append(particula)

        grupo = VGroup(burbuja, *particulas)

        return {
            "burbuja": burbuja,
            "particulas": particulas,
            "grupo": grupo
        }
    
    def explosion_particulas(self):
        """Efecto de explosión en el momento de colisión"""
        
        todas_particulas = (
            self.universo_protones["particulas"] + 
            self.universo_electrones["particulas"]
        )
        
        # Expandir radialmente desde centro
        self.play(
            *[p.animate.shift(
                (p.get_center() - ORIGIN) * 0.5
            ) for p in todas_particulas],
            run_time=2,
            rate_func=rush_from
        )

    def crear_ondas_expansivas(self, num_ondas=5, duracion=2):
        """Crea ondas expansivas desde el punto de colisión"""

        ondas = []
        delay_entre_ondas = duracion / num_ondas

        for i in range(num_ondas):
            # Crear esfera de onda
            onda = Sphere(radius=0.5, resolution=(20, 20))
            onda.set_color(WHITE)
            onda.set_stroke(width=2)
            onda.set_fill(opacity=0)
            onda.set_stroke(opacity=0.8 - i * 0.15)  # cada onda más tenue
            ondas.append(onda)

        # Animar ondas secuencialmente
        animaciones = []
        for i, onda in enumerate(ondas):
            self.add(onda)
            # Cada onda aparece con un pequeño delay
            self.play(
                onda.animate.scale(6).set_stroke(opacity=0),
                run_time=duracion * 0.8,
                rate_func=linear
            )
            self.remove(onda)

            # Esperar antes de la siguiente onda si no es la última
            if i < len(ondas) - 1:
                self.wait(delay_entre_ondas * 0.3)
