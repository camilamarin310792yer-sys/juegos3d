# 🍓 Farm Heroes Saga - Python Emulator

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-green)
![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow)

Juego de combinar frutas (*match-3*) inspirado en **Farm Heroes Saga**, desarrollado en **Python** con **Pygame**. Intercambia frutas adyacentes para formar líneas de 3 o más, activa reacciones en cadena y consigue la mayor puntuación antes de quedarte sin movimientos.

## ✨ Características

- Tablero de **7 × 7** sin combinaciones iniciales.
- **5 frutas** dibujadas por código (sin imágenes): fresa, uva, naranja, manzana y sandía.
- Combinaciones **horizontales y verticales** de 3 o más.
- **Gravedad, relleno automático y reacciones en cadena**.
- Intercambios inválidos se **deshacen** sin gastar movimiento.
- **Puntuación** y **15 movimientos** por partida.
- **Efectos de sonido** de inicio, cosecha y fin.

## 🎮 Cómo jugar

1. Haz clic en una fruta para seleccionarla.
2. Haz clic en una fruta **adyacente** para intercambiarlas.
3. Si se forma una línea de 3 o más, desaparecen y ganas **10 puntos por fruta**.
4. Si no hay combinación, el intercambio se deshace y no pierdes movimiento.
5. La partida termina al llegar a **0 movimientos**.

## 📋 Requisitos

- Python 3.8 o superior
- Pygame (ver `requirements.txt`)

## 🚀 Instalación y ejecución

```bash
git clone https://github.com/TU_USUARIO/farm-heroes-saga.git
cd farm-heroes-saga

# (Opcional) entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
python main.py
```

> Si falta la carpeta `assets/`, ejecuta `python generar_sonidos.py` para crear los sonidos.

## 📁 Estructura del proyecto

```
farm-heroes-saga/
├── main.py                  # Código principal del juego
├── generar_sonidos.py       # Genera los .wav de la carpeta assets
├── assets/
│   ├── start.wav            # Sonido de inicio
│   ├── coin.wav             # Sonido al cosechar
│   └── win.wav              # Sonido de fin de partida
├── docs/
│   └── DOCUMENTACION_TECNICA.md
├── requirements.txt
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## 📚 Documentación

Consulta la [documentación técnica](docs/DOCUMENTACION_TECNICA.md) para ver la arquitectura, las funciones y cómo añadir nuevas frutas.

## ⚙️ Personalización

```python
COLUMNAS = 7      # Columnas del tablero
FILAS = 7         # Filas del tablero
TAM_CELDA = 70    # Tamaño de cada casilla (px)
movimientos = 15  # Movimientos por partida
```

## 🗺️ Ideas futuras

- Botón de reinicio y menú principal.
- Animaciones de caída e intercambio.
- Objetivos por nivel.
- Detección de tablero sin movimientos.
- Puntuación más alta guardada.

## 🤝 Contribuir

Lee la [guía de contribución](CONTRIBUTING.md).

## 📄 Licencia

Distribuido bajo licencia **MIT**. Ver [LICENSE](LICENSE).

## ⚠️ Aviso

Proyecto educativo y sin fines de lucro, inspirado en *Farm Heroes Saga*. No está afiliado ni respaldado por King ni sus propietarios.
