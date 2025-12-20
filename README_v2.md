# ThöEv - Introducción Cosmológica
## Colisión de Branas y Nacimiento del Universo

### Estructura del Proyecto
```
intro_thoev/
│
├── README.md              # Este archivo
├── config.py              # Parámetros configurables
├── main.py                # Ejecutable principal
│
└── shaders/
    ├── brane.vert         # Vertex shader (geometría branas)
    └── brane.frag         # Fragment shader (color y efectos)
```

### Instalación

**Requisitos:**
- Python 3.8+
- pip

**Dependencias:**
```bash
pip install PyOpenGL PyOpenGL_accelerate glfw numpy
```

### Ejecución
```bash
python main.py
```

### Controles

- **ESC**: Cerrar ventana
- **ESPACIO**: Pausar/Reanudar (próxima versión)
- **R**: Reiniciar animación (próxima versión)

### Parámetros Configurables (config.py)
```python
RESOLUTION = (1280, 720)  # Cambiar a (1920, 1080) o (3840, 2160)
FPS = 60                   # 24, 30 o 60
DURATION = 60              # Segundos totales

BRANE_COLOR_LEFT = (R, G, B, A)   # Color brana izquierda
BRANE_COLOR_RIGHT = (R, G, B, A)  # Color brana derecha

BREATH_RATE = 0.5          # Velocidad respiración
WAVE_SPEED = 1.0           # Velocidad ondulación
COLLISION_TIME = 8.0       # Segundo de contacto
```

### Fases de Animación

1. **Fase 1 (0-8s)**: Branas avanzan, respirando y ondulando
2. **Fase 2 (8-12s)**: Colisión y compresión tipo burbujas
3. **Fase 3 (12-14s)**: Flash de luz blanca
4. **Fase 4 (14-24s)**: Mandala fractal + tetraedro + ThoEv
5. **Fase 5 (24-45s)**: Zoom out revelando esferas
6. **Fase 6 (45-60s)**: Multiverso + logo permanente

### Estado Actual

✅ Configuración base
✅ Branas avanzando con respiración
🔄 Colisión tipo burbujas (en desarrollo)
⏳ Mandala fractal
⏳ Zoom out multiverso
⏳ Logo ThoEv permanente

### Troubleshooting

**Error: "No module named 'OpenGL'"**
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

**Error: "Failed to initialize GLFW"**
- Windows: Instalar Visual C++ Redistributable
- Linux: `sudo apt-get install libglfw3`
- Mac: `brew install glfw`

**Pantalla negra**
- Verificar que carpeta `shaders/` existe
- Verificar que archivos `.vert` y `.frag` están presentes

**Muy lento**
- Reducir FPS a 30 en config.py
- Reducir resolución a (854, 480)

### Créditos

Teoría: eCEL (Engranaje de Carga Eléctrica Liberada)
Concepto: Colisión de universos protón-electrón
Desarrollo: Guille + Claude
