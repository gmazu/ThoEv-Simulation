# Cosmos – Animaciones Manim

Guía breve para ejecutar las escenas relacionadas con el pitch ThoEv.

## Prerrequisitos
- Python 3.9+ y Manim Community con soporte OpenGL (`pip install manim`).
- Backend OpenGL disponible (en algunos sistemas necesitas `ffmpeg` y drivers/mesa actualizados).

## Archivos clave
- `tho_ev_scene.py`: escena principal que sigue el pitch (branas, flash, mandala, zoom out) sin depender de OpenGL.

## Ejecución rápida
```bash
# Escena principal con calidad alta y previsualización
manim -pqh tho_ev_scene.py ThoEvScene
```
Opciones útiles:
- `-pql` para preview más rápida (baja calidad).
- `-s` para renderizar un solo frame (útil al ajustar estilos).

## Notas de uso
- Este sketch usa renderer Cairo (sin shaders), por lo que no requiere OpenGL.
- Ajusta parámetros visuales en `tho_ev_scene.py`: colores de las capas de glow, tiempos de animación, posiciones de las branas/universos y velocidad de los pulsos del texto.
