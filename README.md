# Configuración ThöEv - Guía de Parámetros

Este documento explica cada parámetro en `config.json` con ejemplos y resultados esperados.

---

## 📺 RENDER

### `resolution`
**Qué hace:** Define el tamaño de la ventana en píxeles [ancho, alto]

**Ejemplos:**
- `[1280, 720]` → HD (rápido, baja calidad)
- `[1920, 1080]` → Full HD (estándar, buena calidad)
- `[2560, 1440]` → 2K (alta calidad, más lento)
- `[3840, 2160]` → 4K (máxima calidad, muy lento)

**Resultado:** Ventanas más grandes permiten ver más detalles en partículas y mandala.

---

### `fps`
**Qué hace:** Frames por segundo (cuadros que se renderizan cada segundo)

**Ejemplos:**
- `24` → Estilo cinematográfico
- `30` → Estándar (balance velocidad/calidad)
- `60` → Muy suave (requiere GPU potente)

**Resultado:** FPS mayor = animación más fluida pero consume más recursos.

---

### `duration`
**Qué hace:** Duración total de la animación en segundos

**Ejemplos:**
- `5.0` → Intro rápida
- `10.0` → Duración estándar
- `20.0` → Intro extendida

**Resultado:** Controla cuánto tiempo corre antes de cerrar automáticamente.

---

## ⏱️ TIMING

### `collision_time`
**Qué hace:** Segundo exacto cuando las branas colisionan y aparece el mandala

**Ejemplos:**
- `1.0` → Colisión rápida
- `2.0` → Estándar (2 segundos para ver branas avanzar)
- `4.0` → Colisión lenta (más tiempo viendo branas)

**Resultado:** Controla el timing narrativo entre fase de branas y fase de mandala.

---

## 🌊 BRANAS

### `scale`
**Qué hace:** Escala espacial de las branas. **Menor = más grande en pantalla**

**Ejemplos:**
- `0.3` → Branas muy grandes (ocupan casi toda pantalla)
- `0.5` → Branas grandes
- `1.0` → Tamaño estándar
- `2.0` → Branas pequeñas

**Resultado:** Controla zoom in/out de las branas.

---

### `speed`
**Qué hace:** Distancia total que recorren las branas antes de colisionar

**Ejemplos:**
- `2.0` → Avanzan poco (empiezan cerca del centro)
- `3.0` → Estándar
- `5.0` → Avanzan mucho (empiezan lejos)

**Resultado:** Mayor valor = branas empiezan más lejos y viajan más distancia.

---

### `width`
**Qué hace:** Ancho del glow de las branas. **Menor = más ancha**

**Ejemplos:**
- `2.0` → Branas muy anchas y difusas
- `3.0` → Estándar
- `5.0` → Branas delgadas y definidas

**Resultado:** Controla qué tan gruesas/delgadas se ven las branas.

---

### `core`
**Qué hace:** Tamaño del núcleo sólido brillante de cada brana

**Ejemplos:**
- `0.1` → Núcleo pequeño, más glow
- `0.15` → Estándar
- `0.3` → Núcleo grande, menos glow

**Resultado:** Balance entre parte sólida y parte difuminada de la brana.

---

### `curvature`
**Qué hace:** Controla la curvatura parabólica de las branas. **0 = perfectamente rectas, mayor = más curvas**

**Física eCEL:** Branas perfectamente paralelas generarían colisión simultánea en toda su superficie. La curvatura sutil hace que colisionen primero en el centro (punto de contacto inicial) y luego se propague hacia arriba y abajo, como una "mecha de dinamita".

**Ejemplos:**
- `0.0` → Branas perfectamente rectas (NO físico en eCEL)
- `0.1` → Curvatura muy sutil (imperceptible a simple vista)
- `0.3` → Estándar (curvatura suave y realista)
- `0.5` → Curvatura notable
- `1.0` → Muy curva (exagerado)

**Resultado:** La curvatura determina cómo se propaga el contacto entre branas. Valores sutiles (0.1-0.3) crean el efecto de "universos buscándose" mientras mantienen apariencia casi paralela que engaña visualmente.

**Recomendado:** 0.1 para máximo realismo científico, 0.3 para visualización artística.

---

### `left_color` / `right_color`
**Qué hace:** Color RGB de cada brana [rojo, verde, azul]. Valores de 0.0 a 1.0

**Ejemplos:**
- `[0.3, 0.7, 1.0]` → Azul cian (brana izquierda estándar)
- `[1.0, 0.5, 0.2]` → Naranja (brana derecha estándar)
- `[1.0, 0.0, 1.0]` → Magenta
- `[0.0, 1.0, 0.5]` → Verde agua

**Resultado:** Define apariencia visual de cada universo-brana.

---

## ⚛️ PARTICLES (Protones y Electrones)

### `proton_size` / `electron_size`
**Qué hace:** Tamaño de cada partícula brillante

**Ejemplos:**
- `0.01` → Partículas muy pequeñas (puntos)
- `0.02` → Protones estándar
- `0.015` → Electrones estándar (más pequeños que protones)
- `0.05` → Partículas grandes (como burbujas)

**Resultado:** Controla escala visual de protones y electrones.

---

### `proton_density` / `electron_density`
**Qué hace:** Qué tan probable es que aparezca una partícula. **Mayor = menos partículas**

**Rango:** 0.0 (todas) a 1.0 (ninguna)

**Ejemplos:**
- `0.70` → Muchas partículas (muy denso)
- `0.85` → Protones estándar
- `0.88` → Electrones estándar (menos que protones)
- `0.95` → Pocas partículas (disperso)

**Resultado:** Controla cantidad de partículas visibles en cada brana.

---

### `proton_color` / `electron_color`
**Qué hace:** Color RGB de las partículas [rojo, verde, azul]

**Ejemplos:**
- `[0.5, 0.8, 1.0]` → Azul brillante (protones estándar)
- `[1.0, 0.3, 0.2]` → Rojo brillante (electrones estándar)
- `[1.0, 1.0, 1.0]` → Blanco (neutral)

**Resultado:** Color de las "perlas" brillantes dentro de cada brana.

---

### `grid_density`
**Qué hace:** Densidad de la cuadrícula donde se generan partículas

**Ejemplos:**
- `10.0` → Grid grueso (partículas más separadas)
- `15.0` → Estándar
- `25.0` → Grid fino (partículas más juntas)

**Resultado:** Afecta distribución espacial de partículas.

---

### `brightness`
**Qué hace:** Multiplicador de brillo de todas las partículas

**Ejemplos:**
- `2.0` → Partículas tenues
- `5.0` → Estándar
- `10.0` → Partículas muy brillantes (efecto neón)

**Resultado:** Intensidad del glow de protones y electrones.

---

## 💫 TRAIL (Estela)

### `decay`
**Qué hace:** Velocidad de desvanecimiento de la estela. **Mayor = desaparece más rápido**

**Ejemplos:**
- `0.5` → Estela larga y persistente
- `0.8` → Estándar
- `1.5` → Estela corta (desaparece rápido)

**Resultado:** Longitud visual de la cola que dejan las branas.

---

### `intensity`
**Qué hace:** Brillo de la estela (0.0 = invisible, 1.0 = igual que brana)

**Ejemplos:**
- `0.2` → Estela muy tenue
- `0.4` → Estándar
- `0.8` → Estela casi tan brillante como brana

**Resultado:** Qué tan visible es la estela detrás de cada brana.

---

## 🌀 MANDALA (Bigbang)

### `scale`
**Qué hace:** Escala espacial del mandala. **Menor = más grande en pantalla**

**Ejemplos:**
- `1.0` → Mandala muy grande (llena pantalla)
- `1.5` → Grande
- `3.0` → Estándar
- `5.0` → Pequeño (se ven más repeticiones fractales)

**Resultado:** Zoom in/out del patrón fractal.

---

### `iterations`
**Qué hace:** Número de capas fractales superpuestas

**Rango:** 1 a 10 (4-8 recomendado)

**Ejemplos:**
- `3` → Patrón simple (rápido)
- `6` → Estándar (balance complejidad/velocidad)
- `8` → Muy complejo (puede ir lento)

**Resultado:** Más iteraciones = patrón más detallado y denso, pero más lento.

---

### `speed`
**Qué hace:** Velocidad de animación del mandala

**Ejemplos:**
- `0.2` → Muy lento (meditativo)
- `0.4` → Estándar
- `0.8` → Rápido (enérgico)

**Resultado:** Qué tan rápido late y rota el mandala.

---

### `fade_in`
**Qué hace:** Duración del fade in del mandala después de la colisión (en segundos)

**Ejemplos:**
- `0.3` → Aparece súbitamente
- `0.8` → Estándar (transición suave)
- `2.0` → Aparece muy lentamente

**Resultado:** Controla suavidad de la transición branas → mandala.

---

## 🎨 PALETTE (Paleta de Colores del Mandala)

### `a`, `b`, `c`, `d`
**Qué hace:** Parámetros de la función coseno para generar paleta de colores dinámica

**Valores estándar:** (basados en Íñigo Quílez)
```json
"a": [0.5, 0.5, 0.5],
"b": [0.5, 0.5, 0.5],
"c": [1.0, 1.0, 1.0],
"d": [0.263, 0.416, 0.557]
```

**Ejemplos de paletas:**

**Paleta fuego:**
```json
"a": [0.5, 0.5, 0.5],
"b": [0.5, 0.5, 0.5],
"c": [1.0, 1.0, 0.5],
"d": [0.8, 0.9, 0.3]
```

**Paleta oceánica:**
```json
"d": [0.0, 0.15, 0.20]
```

**Resultado:** Define la gama de colores que aparecen en el mandala mientras anima.

**Referencia:** https://iquilezles.org/articles/palettes/

---

## 🎬 POST (Post-procesado)

### `contrast`
**Qué hace:** Ajuste final de contraste. Menor = más contraste

**Ejemplos:**
- `0.7` → Alto contraste (negros profundos)
- `0.9` → Estándar
- `1.1` → Bajo contraste (más suave)

**Resultado:** Ajuste estético final de la imagen.

---

## 💡 Tips de Configuración

**Para intro rápida e impactante:**
```json
"collision_time": 1.0,
"mandala": { "iterations": 4, "speed": 0.6 }
```

**Para intro contemplativa:**
```json
"collision_time": 4.0,
"mandala": { "speed": 0.2, "fade_in": 2.0 }
```

**Para máxima calidad (renderizado offline):**
```json
"render": { "resolution": [3840, 2160], "fps": 60 },
"mandala": { "iterations": 8 }
```

**Para pruebas rápidas:**
```json
"render": { "resolution": [1280, 720], "fps": 24 },
"mandala": { "iterations": 3 }
```

**Para branas casi imperceptiblemente curvas (engañar científicos):**
```json
"branas": { "curvature": 0.1 }
```

---

## 🔄 Workflow Recomendado

1. Ajusta `resolution` y `fps` según tu hardware
2. Ajusta `collision_time` para timing narrativo
3. Modifica `scale` de branas y mandala para composición visual
4. Ajusta `curvature` para física eCEL (0.1-0.3 recomendado)
5. Ajusta `particles` para densidad deseada de protones/electrones
6. Personaliza `palette` para colores únicos
7. Fine-tune `speed`, `brightness`, `contrast` al gusto

**Guarda múltiples versiones de config.json para diferentes propósitos (web, presentación, render final, etc.)**

---

## 📊 Física Representada

**Teoría eCEL:**
- Branas = Universos de cargas (protones vs electrones)
- Curvatura = Permite contacto secuencial (mecha de dinamita)
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
- [ ] Propagación de mandalas (efecto mecha)
- [ ] Singularidad con god rays
- [ ] Zoom out revelando multiverso
- [ ] Logo ThöEv persistente
- [ ] Panel web para edición en tiempo real
- [ ] Integración con Manim para videos educativos

---

**Versión:** 1.1  
**Última actualización:** Diciembre 2024