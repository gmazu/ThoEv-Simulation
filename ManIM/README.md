README para proyecto completo ThöEv-RğB que incluye:

Documentación teórica (README_v11, ThöEv_v11)
Videos Manim (secuencia completa)
Estructura general del proyecto


ThöEv (●)●)•( RğB - Complete Project
Theory of Everything via Reversed Big Bang
E=Mc³

Estructura del Proyecto
ThöEv-RgB/
├── README.md                          # Este archivo (overview completo)
├── docs/
│   ├── README_v11.md                  # Documentación del proyecto v11
│   └── ThöEv_v11.md                   # Desarrollo teórico v11
├── manim/
│   ├── README_MANIM.md                # Guía específica para videos
│   ├── colision_universos_v1.py       # Video 1: Colisión
│   ├── formacion_ecel_v1.py           # Video 2: Formación red eCEL
│   ├── dualidad_particula_v1.py       # Video 3: Dualidad onda-partícula
│   └── media/                         # Videos renderizados (generados)
├── simulations/
│   └── [código simulaciones futuras]
└── papers/
    └── [drafts papers para publicación]

¿Qué es ThöEv-RğB?
Marco teórico determinista que propone que fenómenos electromagnéticos emergen de interacciones mecánicas en una red discreta de cargas acopladas (red eCEL).
Resuelve 16+ misterios de física fundamental:

Dualidad onda-partícula
Entrelazamiento cuántico
Tiempo
Inercia
Velocidad límite c
Fuerzas nucleares
Estructura atómica
Y más...


Documentación Teórica
README_v11.md
Estado del proyecto, backlog, estrategia de financiamiento, lista de 16 misterios resueltos.
Ubicación: docs/README_v11.md
ThöEv_v11.md
Desarrollo teórico completo v11 con explicaciones detalladas de:

Dualidad onda-partícula (tablero de Galton)
Tiempo (cálculo mental, memoria)
Inercia (ola frontal + vórtice)
Velocidad límite C (viscosidad eCEL)
Entrelazamiento cuántico (correlación origen común)

Ubicación: docs/ThöEv_v11.md

Videos Manim
Secuencia Completa (3 videos)
#ArchivoVideoDuraciónDescripción1colision_universos_v1.pyColisión Universos30-45sUniverso protones vs universo electrones, momento de colisión, formación inicial2formacion_ecel_v1.pyFormación red eCEL30-45sEmergencia red supersimétrica, rendijas naturales, estructura 3D3dualidad_particula_v1.pyDualidad Onda-Partícula2-3minElectrón cayendo por red eCEL, tablero de Galton, campana de Gauss

## Simulaciones de Fusión de Protocosmos

Serie de animaciones 3D que visualizan la colisión y fusión de universos protocósmicos (burbujas) con física realista y efectos de ondas expansivas.

### Versiones Disponibles

**v7** - `Burbuja_Fusion_v7.py`
- Colisión de dos protocosmos (azul y rojo)
- Ajuste gradual con conservación de momento
- Círculo de intersección lila (punto de fusión)
- Cámara orbital con rotación 180°
- Las esferas desaparecen al final, quedando solo el círculo lila

**v8** - `Burbuja_Fusion_v8.py`
- Todo lo de v7 +
- **2 ondas expansivas** tipo "piedra al lago"
- Segunda onda aparece cuando primera llega al 50%
- Cada onda más lenta y atenuada
- Efecto 3D con stroke grueso

**v9** - `Burbuja_Fusion_v9.py` ⭐ **RECOMENDADA**
- Todo lo de v8 +
- **5 ondas expansivas** configurables
- Sistema escalable (fácil agregar/quitar ondas)
- Cada onda sucesivamente más lenta y atenuada
- Las ondas continúan después de que las esferas desaparecen
- Parámetros ajustables:
  - Número de ondas
  - Velocidad y atenuación de cada onda
  - Umbral de activación

### Ejecutar Simulaciones

```bash
# v9 (recomendada) - calidad baja para pruebas
manim -pql Burbuja_Fusion_v9.py FusionBurbujas3D

# v9 - calidad alta (1080p)
manim -pqh Burbuja_Fusion_v9.py FusionBurbujas3D
```

### Parámetros Ajustables (v9)

En `Burbuja_Fusion_v9.py` líneas 79-91:

```python
num_ondas = 5              # Número de ondas (3, 4, 5, 6...)
velocidad_base = 0.6       # Velocidad primera onda
factor_velocidad = 0.7     # Cada onda 30% más lenta
opacidad_base = 0.9        # Opacidad primera onda
factor_opacidad = 0.75     # Cada onda 25% más tenue
stroke_width_base = 6      # Grosor primera onda
umbral_activacion = 0.5    # Cuando activa siguiente (0.5 = 50%)
```
Instalación Dependencias
Instalar Manim:
bashpip install manim --break-system-packages
Instalar LaTeX (opcional, para fórmulas matemáticas):
bash# Ubuntu/Debian
sudo apt-get install texlive texlive-latex-extra texlive-fonts-extra

# macOS
brew install --cask mactex
Si no quieres LaTeX: Usa Text() en lugar de MathTex() en el código.
Ejecutar Videos
Calidad baja (testeo rápido):
bashcd manim/
manim -pql colision_universos_v1.py ColisionUniversos
Calidad alta (1080p, para compartir):
bashmanim -pqh colision_universos_v1.py ColisionUniversos
Renderizar secuencia completa:
bashmanim -pqh colision_universos_v1.py ColisionUniversos
manim -pqh formacion_ecel_v1.py FormacionECEL
manim -pqh dualidad_particula_v1.py DualidadOndaParticula
```

**Videos generados en:**
```
manim/media/videos/[nombre_archivo]/[calidad]/[NombreClase].mp4
Flags Útiles

-p = Play (abre video automáticamente)
-q = Quality:

l = low (480p, rápido)
m = medium (720p)
h = high (1080p)
k = 4K (2160p, lento)


-s = Save last frame (imagen final)
-a = Render all scenes

Ver más opciones:
bashmanim --help

Filosofía del Proyecto
Evolución = Transformación

Feto → Bebé (dolor del nacimiento)
Oruga → Mariposa (muerte necesaria)
Física cuántica → ThöEv-RğB (determinismo visualizable)

Si no duele, no vale la pena.
El miedo es normal. Abrázalo y vuela con tu nueva forma.

Estado Actual - v11.0
Fecha: 27 diciembre 2025
Breakthroughs completados:

✅ Dualidad onda-partícula
✅ Tiempo explicado
✅ Inercia explicada
✅ Velocidad límite C
✅ Entrelazamiento cuántico

Pendientes:

Nombre para red eCEL
Cuantificación C → viscosidad eCEL
Formación tabla periódica
Computadores cuánticos clásicos

Siguiente paso:

Buscar financiamiento institucional
Publicar paper ArXiv (dualidad onda-partícula)
Contactar FQXi + 44 instituciones


Estrategia de Financiamiento
Modelo de Colaboración
NO pedimos "ayuda". VENDEMOS acceso a asesoría.

Publicamos 1 de 16 misterios como prueba concepto
Otros 15 disponibles para investigación institucional
Universidades pagan por:

Asesoría técnica
Acceso marco teórico eCEL
Co-autoría papers


Universidades aportan recursos:

Laboratorios
Supercomputadoras
Estudiantes
Financiamiento



Contactos Target
45 instituciones/físicos:

20 físicos teóricos (ideas no convencionales)
15 institutos investigación
10 fundaciones privadas

Prioridad 1: Foundational Questions Institute (FQXi)

Autor
Guillermo [Apellido]

Electronics & Telecommunications Engineer
Former Teaching Assistant, Physics Dept, Universidad de Santiago de Chile
Skills: OpenGL, Python, Manim, shader programming


Versiones

v11.0 (27 dic 2025): Tiempo, inercia, C, entrelazamiento
v10.0: eCEL = andamiaje de la luz
v7.0: Documentación estructurada GitHub
v5.1: Transición cosmología → materia


Licencia
[Por definir - considerar según estrategia publicación]

Contacto
[Email]
[GitHub]
[LinkedIn]

Agradecimientos
Desarrollo asistido por Claude (Anthropic) en colaboración con el autor.

Última actualización: 27 diciembre 2025
