import pygame
import random
import sys
from pathlib import Path

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
pygame.init()

COLUMNAS = 7
FILAS = 7
TAM_CELDA = 70
MARGEN_X = 50
MARGEN_Y = 100

ANCHO = COLUMNAS * TAM_CELDA + (MARGEN_X * 2)
ALTO = FILAS * TAM_CELDA + MARGEN_Y + 50

pygame.display.set_caption("Farm Heroes Saga - Python Emulator")
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
CARPETA_ASSETS = Path(__file__).resolve().parent / "assets"
sonido_inicio = pygame.mixer.Sound(str(CARPETA_ASSETS / "start.wav"))
sonido_cosecha = pygame.mixer.Sound(str(CARPETA_ASSETS / "coin.wav"))
sonido_fin = pygame.mixer.Sound(str(CARPETA_ASSETS / "win.wav"))

# --- COLORES Y CULTIVOS ---
COLOR_FONDO = (230, 245, 220)
COLOR_TABLERO = (180, 215, 160)
COLOR_TEXTO = (50, 50, 50)

# Representación de las cosechas/frutas de Farm Heroes
TIPOS_CULTIVOS = {
    'fresa': {'color': (235, 50, 50), 'nombre': 'Fresa'},
    'uva': {'color': (145, 75, 190), 'nombre': 'Uvas'},
    'naranja': {'color': (250, 145, 35), 'nombre': 'Naranja'},
    'manzana': {'color': (60, 180, 75), 'nombre': 'Manzana'},
    'sandia': {'color': (225, 70, 90), 'nombre': 'Sandia'}
}
CLAVES_CULTIVOS = list(TIPOS_CULTIVOS.keys())

# --- VARIABLES DEL JUEGO ---
puntuacion = 0
movimientos = 15
seleccionado = None  # (fila, col) de la fruta seleccionada

# --- FUNCIONES DE LÓGICA ---
def crear_tablero():
    """Crea un tablero inicial sin combinaciones previas de 3 en raya."""
    tablero = []
    for f in range(FILAS):
        fila = []
        for c in range(COLUMNAS):
            opciones = list(CLAVES_CULTIVOS)
            # Evitar combinaciones horizontales
            if c >= 2 and fila[c-1] == fila[c-2]:
                if fila[c-1] in opciones:
                    opciones.remove(fila[c-1])
            # Evitar combinaciones verticales
            if f >= 2 and tablero[f-1][c] == tablero[f-2][c]:
                if tablero[f-1][c] in opciones:
                    opciones.remove(tablero[f-1][c])
            fila.append(random.choice(opciones))
        tablero.append(fila)
    return tablero

def buscar_coincidencias(tablero):
    """Encuentra todas las posiciones de cosechas que forman 3 o más en raya."""
    eliminar = set()

    # Horizontales
    for f in range(FILAS):
        for c in range(COLUMNAS - 2):
            if tablero[f][c] and tablero[f][c] == tablero[f][c+1] == tablero[f][c+2]:
                eliminar.add((f, c))
                eliminar.add((f, c+1))
                eliminar.add((f, c+2))

    # Verticales
    for f in range(FILAS - 2):
        for c in range(COLUMNAS):
            if tablero[f][c] and tablero[f+1][c] and tablero[f][c] == tablero[f+1][c] == tablero[f+2][c]:
                eliminar.add((f, c))
                eliminar.add((f+1, c))
                eliminar.add((f+2, c))

    return eliminar

def aplicar_gravedad_y_rellenar(tablero):
    """Hace caer los elementos y llena los huecos vacíos."""
    for c in range(COLUMNAS):
        # Caída de fichas
        for f in range(FILAS - 1, -1, -1):
            if tablero[f][c] is None:
                for f_arriba in range(f - 1, -1, -1):
                    if tablero[f_arriba][c] is not None:
                        tablero[f][c] = tablero[f_arriba][c]
                        tablero[f_arriba][c] = None
                        break
        # Rellenar espacios vacíos arriba
        for f in range(FILAS):
            if tablero[f][c] is None:
                tablero[f][c] = random.choice(CLAVES_CULTIVOS)

def resolver_tablero(tablero):
    """Elimina combinaciones en cadena y suma puntos."""
    global puntuacion
    coincidencias = buscar_coincidencias(tablero)

    while coincidencias:
        puntuacion += len(coincidencias) * 10
        sonido_cosecha.play()
        for f, c in coincidencias:
            tablero[f][c] = None
        aplicar_gravedad_y_rellenar(tablero)
        coincidencias = buscar_coincidencias(tablero)

def dibujar_fruta(superficie, tipo, centro):
    x, y = centro

    if tipo == 'fresa':
        cuerpo = [(x - 19, y - 13), (x - 13, y - 21), (x + 13, y - 21),
                  (x + 19, y - 13), (x + 15, y + 4), (x, y + 23),
                  (x - 15, y + 4)]
        pygame.draw.polygon(superficie, (204, 39, 49), cuerpo)
        pygame.draw.lines(superficie, (255, 112, 108), False, cuerpo, 2)
        for semilla_x, semilla_y in [(-9, -11), (2, -12), (10, -7), (-7, 0),
                                     (4, 1), (-3, 9), (7, 10), (0, 17)]:
            pygame.draw.ellipse(superficie, (255, 226, 142),
                                (x + semilla_x - 1, y + semilla_y - 2, 3, 5))
        pygame.draw.polygon(superficie, (46, 143, 66),
                            [(x - 15, y - 19), (x - 7, y - 27), (x - 2, y - 19),
                             (x + 3, y - 28), (x + 7, y - 19), (x + 16, y - 24),
                             (x + 12, y - 15), (x - 12, y - 15)])
    elif tipo == 'uva':
        for ox, oy in [(-10, -12), (1, -14), (11, -9), (-15, -1), (-4, -2),
                       (7, 1), (-10, 9), (1, 11)]:
            pygame.draw.circle(superficie, (111, 53, 157), (x + ox, y + oy), 8)
            pygame.draw.circle(superficie, (183, 122, 218), (x + ox - 2, y + oy - 3), 2)
        pygame.draw.line(superficie, (100, 75, 44), (x, y - 15), (x + 2, y - 24), 3)
        pygame.draw.ellipse(superficie, (59, 151, 67), (x + 1, y - 27, 15, 8))
    elif tipo == 'naranja':
        pygame.draw.circle(superficie, (218, 106, 25), (x, y + 1), 20)
        pygame.draw.circle(superficie, (255, 157, 42), (x, y), 18)
        pygame.draw.arc(superficie, (255, 204, 103), (x - 13, y - 14, 24, 25), .7, 2.3, 3)
        pygame.draw.circle(superficie, (255, 220, 135), (x - 7, y - 8), 3)
        pygame.draw.line(superficie, (109, 78, 43), (x, y - 17), (x + 2, y - 23), 3)
        pygame.draw.ellipse(superficie, (62, 145, 67), (x + 1, y - 25, 13, 7))
    elif tipo == 'manzana':
        pygame.draw.circle(superficie, (48, 139, 55), (x - 9, y - 1), 14)
        pygame.draw.circle(superficie, (48, 139, 55), (x + 9, y - 1), 14)
        pygame.draw.ellipse(superficie, (48, 139, 55), (x - 16, y - 3, 32, 24))
        pygame.draw.polygon(superficie, (48, 139, 55),
                            [(x - 13, y + 5), (x, y + 23), (x + 13, y + 5)])
        pygame.draw.circle(superficie, (112, 203, 89), (x - 7, y - 8), 4)
        pygame.draw.line(superficie, (99, 66, 38), (x, y - 15), (x + 2, y - 23), 3)
        pygame.draw.ellipse(superficie, (55, 137, 63), (x + 2, y - 24, 13, 7))
    elif tipo == 'sandia':
        corteza = [(x - 23, y - 13), (x + 23, y - 13), (x, y + 22)]
        pulpa = [(x - 17, y - 10), (x + 17, y - 10), (x, y + 15)]
        pygame.draw.polygon(superficie, (42, 137, 64), corteza)
        pygame.draw.polygon(superficie, (245, 235, 166),
                            [(x - 19, y - 12), (x + 19, y - 12), (x, y + 18)])
        pygame.draw.polygon(superficie, (224, 62, 76), pulpa)
        for semilla_x, semilla_y in [(-8, -4), (4, -3), (-3, 4), (8, 1), (1, 10)]:
            pygame.draw.ellipse(superficie, (68, 47, 43),
                                (x + semilla_x - 1, y + semilla_y - 2, 3, 5))

# --- DIBUJADO DE LA INTERFAZ ---
def dibujar_juego(tablero):
    pantalla.fill(COLOR_FONDO)

    # Fuentes
    fuente_titulo = pygame.font.SysFont("comicsansms", 28, bold=True)
    fuente_info = pygame.font.SysFont("comicsansms", 20)

    # Encabezado
    txt_titulo = fuente_titulo.render("FARM HEROES SAGA", True, (30, 100, 30))
    txt_puntos = fuente_info.render(f"Puntos: {puntuacion}", True, COLOR_TEXTO)
    txt_movs = fuente_info.render(f"Movimientos: {movimientos}", True, COLOR_TEXTO)

    pantalla.blit(txt_titulo, (MARGEN_X, 15))
    pantalla.blit(txt_puntos, (MARGEN_X, 60))
    pantalla.blit(txt_movs, (ANCHO - MARGEN_X - 160, 60))

    # Dibujar Cuadrícula
    for f in range(FILAS):
        for c in range(COLUMNAS):
            x = MARGEN_X + c * TAM_CELDA
            y = MARGEN_Y + f * TAM_CELDA

            # Fondo de la celda
            rect_celda = pygame.Rect(x, y, TAM_CELDA - 4, TAM_CELDA - 4)
            pygame.draw.rect(pantalla, COLOR_TABLERO, rect_celda, border_radius=8)

            # Resaltar la selección actual
            if seleccionado == (f, c):
                pygame.draw.rect(pantalla, (255, 255, 255), rect_celda, width=4, border_radius=8)

            # Dibujar Cosecha/Cultivo
            tipo = tablero[f][c]
            if tipo:
                centro_x = x + TAM_CELDA // 2 - 2
                centro_y = y + TAM_CELDA // 2 - 2
                dibujar_fruta(pantalla, tipo, (centro_x, centro_y))

    # Pantalla de Fin del Juego
    if movimientos <= 0:
        s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        pantalla.blit(s, (0, 0))

        txt_fin = fuente_titulo.render("¡FIN DEL JUEGO!", True, (255, 255, 255))
        txt_final_puntos = fuente_info.render(f"Puntuación total: {puntuacion}", True, (255, 255, 255))

        pantalla.blit(txt_fin, (ANCHO // 2 - 120, ALTO // 2 - 40))
        pantalla.blit(txt_final_puntos, (ANCHO // 2 - 110, ALTO // 2 + 10))

    pygame.display.flip()

# --- BUCLE PRINCIPAL DEL JUEGO ---
def main():
    global seleccionado, movimientos

    tablero = crear_tablero()
    sonido_inicio.play()
    corriendo = True
    sonido_fin_reproducido = False

    while corriendo:
        reloj.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN and movimientos > 0:
                mx, my = pygame.mouse.get_pos()

                # Comprobar si el clic ocurrió dentro de la cuadrícula
                if (MARGEN_X <= mx < MARGEN_X + COLUMNAS * TAM_CELDA and
                        MARGEN_Y <= my < MARGEN_Y + FILAS * TAM_CELDA):

                    c = (mx - MARGEN_X) // TAM_CELDA
                    f = (my - MARGEN_Y) // TAM_CELDA

                    if seleccionado is None:
                        seleccionado = (f, c)
                    else:
                        f1, c1 = seleccionado
                        f2, c2 = f, c

                        # Comprobar si son adyacentes (arriba, abajo, izq, der)
                        es_adyacente = (abs(f1 - f2) + abs(c1 - c2)) == 1

                        if es_adyacente:
                            # Intercambiar temporalmente
                            tablero[f1][c1], tablero[f2][c2] = tablero[f2][c2], tablero[f1][c1]

                            # Validar si el intercambio genera match
                            coincidencias = buscar_coincidencias(tablero)
                            if coincidencias:
                                movimientos -= 1
                                resolver_tablero(tablero)
                            else:
                                # Si no hay match, deshacer intercambio
                                tablero[f1][c1], tablero[f2][c2] = tablero[f2][c2], tablero[f1][c1]

                            seleccionado = None
                        else:
                            # Cambiar selección a la nueva casilla
                            seleccionado = (f, c)

        if movimientos <= 0 and not sonido_fin_reproducido:
            sonido_fin.play()
            sonido_fin_reproducido = True

        dibujar_juego(tablero)

if __name__ == "__main__":
    main()
