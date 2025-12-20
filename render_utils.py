# render_utils.py - Utilidades para renderizar a video
import os
import subprocess
import tempfile
import shutil
from OpenGL.GL import glReadPixels, GL_RGB, GL_UNSIGNED_BYTE
import numpy as np

class VideoRenderer:
    """Clase para capturar frames y generar video MP4."""

    def __init__(self, width, height, fps, output_name):
        self.width = width
        self.height = height
        self.fps = fps
        self.output_name = output_name
        self.frame_dir = tempfile.mkdtemp(prefix="frames_")
        self.frame_count = 0
        self.enabled = False

    def enable(self):
        """Activa la captura de frames."""
        self.enabled = True
        print(f"Renderizando a: {self.output_name}")
        print(f"Frames temporales en: {self.frame_dir}")

    def capture_frame(self):
        """Captura el frame actual de OpenGL."""
        if not self.enabled:
            return

        # Leer pixels del framebuffer
        pixels = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        image = np.frombuffer(pixels, dtype=np.uint8).reshape(self.height, self.width, 3)

        # Voltear verticalmente (OpenGL tiene origen abajo-izquierda)
        image = np.flipud(image)

        # Guardar como PPM (formato simple, sin dependencias extra)
        frame_path = os.path.join(self.frame_dir, f"frame_{self.frame_count:05d}.ppm")
        with open(frame_path, 'wb') as f:
            f.write(f"P6\n{self.width} {self.height}\n255\n".encode())
            f.write(image.tobytes())

        self.frame_count += 1

        # Mostrar progreso cada 30 frames
        if self.frame_count % 30 == 0:
            print(f"  Frame {self.frame_count}...")

    def generate_video(self):
        """Genera el video MP4 con ffmpeg."""
        if not self.enabled or self.frame_count == 0:
            return

        print(f"\nGenerando video con {self.frame_count} frames...")

        # Comando ffmpeg
        cmd = [
            'ffmpeg',
            '-y',  # Sobrescribir si existe
            '-framerate', str(self.fps),
            '-i', os.path.join(self.frame_dir, 'frame_%05d.ppm'),
            '-c:v', 'libx264',
            '-preset', 'slow',
            '-crf', '18',  # Alta calidad
            '-pix_fmt', 'yuv420p',
            self.output_name
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"Video generado: {self.output_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error generando video: {e.stderr.decode()}")
        finally:
            # Limpiar frames temporales
            shutil.rmtree(self.frame_dir)
            print("Frames temporales eliminados.")

    def cleanup(self):
        """Limpia recursos si no se generó video."""
        if os.path.exists(self.frame_dir):
            shutil.rmtree(self.frame_dir)


def parse_render_args():
    """Parsea argumentos de línea de comandos para renderizado."""
    import sys
    return '--mp4' in sys.argv or '--render' in sys.argv
