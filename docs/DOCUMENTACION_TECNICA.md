# Documentación técnica

## Arquitectura

Todo el juego está en `main.py` y sigue este flujo:

1. **Inicialización**: Pygame, ventana, reloj y carga de sonidos desde `assets/`.
2. **Estado global**: `puntuacion`, `movimientos` y `seleccionado`.
3. **Bucle principal** (`main()`, 30 FPS): eventos de ratón → intercambio → validación → resolución → dibujado.

## Representación del tablero

El tablero es una lista de listas de 7x7. Cada celda guarda la clave de una fruta (`'fresa'`, `'uva'`, `'naranja'`, `'manzana'`, `'sandia'`) o `None` cuando está vacía temporalmente.

## Funciones principales

| Función | Descripción |
|---------|-------------|
| `crear_tablero()` | Genera el tablero evitando 3 en raya iniciales, excluyendo del azar la fruta que formaría la línea. |
| `buscar_coincidencias(tablero)` | Devuelve un `set` de posiciones `(fila, columna)` con 3 o más frutas iguales alineadas. |
| `aplicar_gravedad_y_rellenar(tablero)` | Por columna, baja las frutas a los huecos y rellena los espacios superiores al azar. |
| `resolver_tablero(tablero)` | Bucle: eliminar → gravedad → buscar de nuevo; suma 10 puntos por fruta y reproduce `coin.wav`. |
| `dibujar_fruta(superficie, tipo, centro)` | Dibuja cada fruta con primitivas de Pygame. |
| `dibujar_juego(tablero)` | Dibuja encabezado, cuadrícula, selección y pantalla final. |
| `main()` | Gestiona eventos, intercambios y sonidos. |

## Reglas del juego

- Solo se pueden intercambiar casillas **adyacentes** (distancia de Manhattan = 1).
- Si el intercambio no genera combinación, se revierte y **no gasta movimiento**.
- Si genera combinación, se descuenta 1 movimiento y se resuelven las cascadas.
- Al llegar a 0 movimientos se bloquea la entrada y se muestra la pantalla final.

## Cómo añadir una nueva fruta

1. Agrega una entrada en `TIPOS_CULTIVOS`.
2. Añade un bloque `elif tipo == 'nueva':` en `dibujar_fruta()`.
3. `CLAVES_CULTIVOS` se actualiza automáticamente.

## Limitaciones conocidas

- No hay animaciones de caída ni de intercambio.
- No se detecta cuando el tablero queda sin movimientos posibles.
- No hay opción de reiniciar sin cerrar el juego.
- La fuente `comicsansms` depende del sistema; si no existe, Pygame usa una fuente por defecto.
