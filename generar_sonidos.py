"""Genera los efectos de sonido simples (start.wav, coin.wav, win.wav) en la carpeta assets/.
Solo usa la librería estándar de Python. Ejecuta: python generar_sonidos.py
"""
import math
import struct
import wave
from pathlib import Path

TASA = 44100
CARPETA = Path(__file__).resolve().parent / "assets"


def tono(frecuencia, duracion, volumen=0.4):
    n = int(TASA * duracion)
    muestras = []
    for i in range(n):
        envolvente = min(1.0, i / (TASA * 0.01)) * max(0.0, 1 - i / n)
        valor = math.sin(2 * math.pi * frecuencia * i / TASA) * volumen * envolvente
        muestras.append(int(valor * 32767))
    return muestras


def guardar(nombre, notas):
    muestras = []
    for frecuencia, duracion in notas:
        muestras += tono(frecuencia, duracion)
    CARPETA.mkdir(exist_ok=True)
    with wave.open(str(CARPETA / nombre), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(TASA)
        w.writeframes(b"".join(struct.pack("<h", m) for m in muestras))


if __name__ == "__main__":
    guardar("start.wav", [(523, 0.12), (659, 0.12), (784, 0.2)])
    guardar("coin.wav", [(988, 0.07), (1319, 0.18)])
    guardar("win.wav", [(523, 0.15), (659, 0.15), (784, 0.15), (1047, 0.35)])
    print("Sonidos generados en", CARPETA)
