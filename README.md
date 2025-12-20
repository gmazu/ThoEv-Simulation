# ThöEv - Introducción Cosmológica
## Colisión de Branas y Nacimiento del Universo

Visualización shader en tiempo real del origen del universo según la teoría eCEL (Engranaje de Carga Eléctrica Liberada).

---

## 📁 Estructura del Proyecto
```
intro_thoev/
│
├── README.md              # Este archivo
├── branas.py              # Ejecutable principal
│
└── config/
    └── config.json        # Configuración completa (API REST ready)
```

---

## 🚀 Instalación

**Requisitos:**
- Python 3.8+
- pip

**Dependencias:**
```bash
pip install PyOpenGL PyOpenGL_accelerate glfw numpy
```

---

## ▶️ Ejecución
```bash
python3 branas.py
```

---

## ⚙️ Configuración

Todos los parámetros están en `config/config.json`. Modifica valores y ejecuta de nuevo (sin tocar código).

### Estructura JSON
```json
{
  "render": {
    "resolution": [1280, 720],    // Resolución ventana
    "fps": 30,                     // Frames por segundo
    "duration": 10.0               // Duración total (segundos)
  },
  "timing": {
    "collision_time": 2.0          // Segundo de colisión
  },
  "branas": {
    "scale": 1.0,                  // Escala espacial
    "speed": 3.0,                  // Velocidad avance
    "width": 3.0,                  // Ancho glow (menor = más ancha)
    "core": 0.15,                  // Tamaño núcleo sólido
    "left_color": [0.3, 0.7, 1.0], // RGB brana izquierda
    "right_color": [1.0, 0.5, 0.2] // RGB brana derecha
  },
  "particles": {
    "proton_size": 0.02,           // Tamaño protones
    "proton_density": 0.85,        // Densidad (0-1, mayor = menos)
    "proton_color": [0.5, 0.8, 1.0],
    "electron_size": 0.015,        // Tamaño electrones
    "electron_density": 0.88,
    "electron_color": [1.0, 0.3, 0.2],
    "grid_density": 15.0,          // Densidad grid partículas
    "brightness": 5.0              // Multiplicador brillo
  },
  "trail": {
    "decay": 0.8,                  // Velocidad desvanecimiento
    "intensity": 0.4               // Brillo estela
  },
  "mandala": {
    "scale": 3.0,                  // Escala espacial
    "iterations": 6,               // Capas fractales (4-8)
    "speed": 0.4,                  // Velocidad animación
    "fade_in": 0.8                 // Duración fade in
  },
  "palette": {                     // Paleta coseno (colores mandala)
    "a": [0.5, 0.5, 0.5],
    "b": [0.5, 0.5, 0.5],
    "c": [1.0, 1.0, 1.0],
    "d": [0.263, 0.416, 0.557]
  },
  "post": {
    "contrast": 0.9                // Contraste final (0.8-1.2)
  }
}
```

---

## 🎬 Fases de Animación

1. **Fase 1 (0-2s)**: Branas avanzan con partículas brillantes
   - Brana izquierda: Protones azules (universo de protones)
   - Brana derecha: Electrones rojos (universo de electrones)
   - Estela difuminada exponencial

2. **Fase 2 (2s)**: Colisión en el centro

3. **Fase 3 (2-10s)**: Mandala fractal (bigbang)
   - 6 iteraciones fractales con glow neón
   - Paleta de colores dinámica
   - Fade in suave

---

## 🎨 Técnicas Shader Utilizadas

- **SDFs (Signed Distance Fields)** para geometría precisa
- **Funciones de hash** para partículas procedurales
- **Glow exponencial** para estelas y neón
- **Fractales iterativos** con `fract()`
- **Paleta coseno** (Íñigo Quílez) para colores dinámicos
- **Smoothstep** para transiciones suaves
- **Post-procesado** con `pow()` para contraste

---

## 🌐 API REST Ready

El archivo `config.json` está diseñado para ser consumido/modificado por API REST:
```bash
# Ejemplo: Modificar desde API
curl -X PUT http://tu-api.com/config \
  -H "Content-Type: application/json" \
  -d @config/config.json
```

---

## 🔧 Parámetros Recomendados

**Para branas más visibles:**
```json
"branas": {
  "width": 2.0,
  "core": 0.2
}
```

**Para más partículas:**
```json
"particles": {
  "proton_density": 0.80,
  "electron_density": 0.82,
  "brightness": 8.0
}
```

**Para mandala más lento:**
```json
"mandala": {
  "speed": 0.2
}
```

**Para resolución 4K:**
```json
"render": {
  "resolution": [3840, 2160]
}
```

---

## 🐛 Troubleshooting

**Error: "No module named 'OpenGL'"**
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

**Error: "config/config.json not found"**
- Verifica que la carpeta `config/` existe
- Verifica que ejecutas desde la carpeta raíz del proyecto

**Pantalla negra**
- Verifica que GPU soporta OpenGL 3.3+
- Prueba reducir `mandala.iterations` a 4

**Muy lento**
```json
"render": {
  "fps": 24,
  "resolution": [854, 480]
},
"mandala": {
  "iterations": 4
}
```

---

## 📊 Física Representada

**Teoría eCEL:**
- Branas = Universos de cargas (protones vs electrones)
- Colisión = Origen de nuestro universo
- Mandala = Patrón de interferencia cuántica
- Partículas = Cargas acopladas en retícula

---

## 🎓 Créditos

- **Teoría**: eCEL (Engranaje de Carga Eléctrica Liberada)
- **Concepto**: Colisión de universos protón-electrón
- **Técnicas shader**: Tutorial de Arte con Shaders (GLSL)
- **Desarrollo**: Guille + Claude
- **Paleta coseno**: Íñigo Quílez

---

## 📝 Licencia

Proyecto educativo/artístico. Código libre para experimentación.

---

## 🔮 Próximos Pasos

- [ ] Exportación a video MP4
- [ ] Zoom out revelando multiverso
- [ ] Logo ThöEv persistente
- [ ] Panel web para edición en tiempo real
- [ ] Integración con Manim para videos educativos

---

**Versión:** 1.0  
**Última actualización:** Diciembre 2024