# Simulación de Fusión de Burbujas

Simulación física de colisión y fusión de burbujas con conservación de momentum.

## 📁 Archivos

### `Burbuja_Fusion.py` - Versión 2D
Simulación en 2D donde dos burbujas colisionan y se incrustan.

**Características:**
- Vista 2D (círculos)
- Física de colisión elástica
- Conservación de momentum
- Las burbujas se acercan gradualmente (incrustación)
- Sin rotación de cámara

**Ejecutar:**
```bash
manim -pql Burbuja_Fusion.py FusionBurbujas
```

---

### `Burbuja_Fusion_v1.py` - Versión 3D con Cámara Orbital ⭐
Simulación en 3D donde dos esferas colisionan mientras la cámara rota para ver la juntura desde todos los ángulos.

**Características:**
- Vista 3D (esferas)
- Física de colisión elástica
- Conservación de momentum
- Las esferas se incrustan gradualmente
- **Cámara orbital** que rota durante la colisión para ver la zona de contacto

**Ejecutar:**
```bash
manim -pql Burbuja_Fusion_v1.py FusionBurbujas3D
```

**Parámetros ajustables (línea 91):**
- `velocidad_rotacion = 0.5` - Velocidad de rotación de cámara (rad/s)

---

## 🎯 Diferencias Principales

| Característica | Burbuja_Fusion.py | Burbuja_Fusion_v1.py |
|---------------|-------------------|----------------------|
| Dimensión | 2D | 3D |
| Geometría | Círculos | Esferas |
| Cámara | Estática | Orbital (rota) |
| Vista de juntura | Frontal | Todos los ángulos |

---

## ⚙️ Física Implementada

Ambas versiones incluyen:

1. **Colisión elástica:**
   - Conservación de momentum: `p_total = m₁v₁ + m₂v₂`
   - Impulso de colisión calculado con coeficiente de restitución

2. **Incrustación gradual:**
   - Velocidad: `0.15` unidades/segundo
   - Las burbujas se acercan continuamente después del contacto

3. **Momentum conservado:**
   - Velocidad final = promedio ponderado por masa
   - Las burbujas avanzan juntas después de fusionarse

---

## 🎨 Parámetros de las Burbujas

```python
# Posiciones iniciales
Burbuja 1: [-2.5, 0, 0]  (izquierda)
Burbuja 2: [2.5, 0, 0]   (derecha)

# Velocidades iniciales
Burbuja 1: [0.5, 0, 0]   (→ derecha)
Burbuja 2: [-0.5, 0, 0]  (← izquierda)

# Radio: 1.2
# Masa: 1.0
```

---

## 📝 Calidad de Renderizado

- `-pql` = Baja calidad (rápido, para pruebas)
- `-pqm` = Calidad media
- `-pqh` = Alta calidad (lento, para video final)

---

**Autor:** Claude Code
**Fecha:** 2025-12-27
