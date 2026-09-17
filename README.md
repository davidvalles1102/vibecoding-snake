# Snake — Vibecoding Guiado

Mini-juego 2D de Snake hecho en Python con `tkinter` (solo librería estándar,
no requiere instalar nada extra). Proyecto para la actividad individual
**"Vibecoding Guiado: Desarrollo de una Aplicación o Mini-Juego con IA como
Copiloto"**.

**Repositorio:** https://github.com/davidvalles1102/vibecoding-snake

## 1. Descripción y objetivo

El objetivo del juego es controlar una serpiente con las flechas del teclado,
comer la comida (círculo rojo) para crecer y sumar puntos, evitando chocar
contra las paredes o contra el propio cuerpo. La dificultad aumenta con el
puntaje: la serpiente se mueve cada vez más rápido.

**Controles**

| Tecla       | Acción                              |
|-------------|--------------------------------------|
| Flechas     | Mover la serpiente                   |
| `P`         | Pausar / reanudar                    |
| `R`         | Reiniciar (solo tras "Game Over")    |

## 2. Cómo ejecutarlo

Requiere Python 3.8+ (se desarrolló y probó con Python 3.14). `tkinter` viene
incluido en las instalaciones oficiales de Python para Windows y macOS; en
Linux puede requerir `sudo apt install python3-tk`.

```bash
python snake.py          # ejecutar el juego
python test_snake.py     # ejecutar las pruebas automáticas de la lógica
```

## 3. Evidencia de vibecoding (prompts usados)

El desarrollo se hizo en 3 rondas de prompts a la IA (Claude), cada una
construyendo sobre el resultado de la anterior:

**Prompt 1 — versión base**
> "Ayúdame a crear un mini-juego de Snake en Python usando tkinter (sin
> librerías externas), con movimiento por flechas, comida, crecimiento de la
> serpiente, choque contra pared/uno mismo, y reinicio con la tecla R."

*Por qué este prompt:* se pidió primero una base mínima jugable (bucle del
juego, dibujo en el canvas, detección de colisiones) para validar que la
mecánica central funcionara antes de complicar el código con reglas
adicionales.

**Prompt 2 — refinamiento de jugabilidad**
> "El juego ya funciona, pero es muy fácil y se puede revertir de golpe.
> Agrégale que la velocidad aumente conforme se come comida, evita que se
> pueda girar 180° sobre el propio cuello, agrega una pantalla de inicio con
> instrucciones y una pausa con la tecla P."

*Por qué se refinó:* al jugar la versión 1 (ver sección de validación) se
notó que perder por girar en dirección contraria se sentía como un error del
juego y no como una decisión del jugador, y que el juego nunca se ponía más
difícil. Este prompt fue más específico que el primero porque ya se conocía
exactamente qué comportamiento faltaba.

**Prompt 3 — necesidad de pruebas**
> "Necesito pruebas automáticas de la lógica (colisiones, dirección, aparición
> de comida) que no dependan de abrir la ventana gráfica, para poder validar
> el código sin tener que jugar manualmente cada vez."

*Por qué se pidió esto:* jugar manualmente no cubre de forma confiable ni
repetible casos límite (por ejemplo, que la comida nunca aparezca encima de
la propia serpiente). Se pidió separar la lógica pura (funciones sin
`tkinter`) del código gráfico para poder probarla con `assert` normales.

## 4. Iteración y mejora (antes / después)

| Aspecto | Versión 1 | Versión 2 (mejorada) |
|---|---|---|
| Velocidad | Fija (150 ms siempre) | Aumenta con el puntaje (`speed_for_score`), con un límite mínimo para que siga siendo jugable |
| Cambio de dirección | Inmediato, sin validar | Se valida con `is_reversal()`: no se permite girar 180° sobre el propio cuello |
| Pantallas | Solo "Game Over" | Se agregó pantalla de inicio con instrucciones y pantalla de pausa |
| Pausa | No existía | Tecla `P` |

El impacto es visible jugando: en la v1 era común "perder sin razón aparente"
al presionar la flecha opuesta por reflejo; en la v2 esa entrada simplemente
se ignora, y el juego se siente progresivamente más retador en vez de tener
una dificultad plana.

## 5. Validación del resultado

Se usaron cuatro formas de validar el código, de menor a mayor nivel:

1. **Compilación**: `python -m py_compile snake.py` — detecta errores de
   sintaxis antes de ejecutar.
2. **Arranque en vivo (smoke test)**: se lanzó `python snake.py` y se
   confirmó que el proceso siguiera corriendo unos segundos sin lanzar
   excepciones (ventana y bucle `after()` funcionando).
3. **Pruebas automáticas de lógica** (`test_snake.py`, sin abrir ventana):
   6/6 pruebas pasaron, cubriendo movimiento (`next_head`), colisión con
   pared (`hits_wall`), colisión con el propio cuerpo (`hits_self`),
   prevención de reversión (`is_reversal`), incremento de velocidad con
   límite (`speed_for_score`) y que la comida nunca aparezca sobre la
   serpiente (`random_food_position`).
4. **Prueba manual jugando**: se verificó a mano que la serpiente crece al
   comer, el puntaje sube, aparece "Game Over" al chocar, `R` reinicia y `P`
   pausa correctamente.

**Error identificado y corregido:** en la v1, si se presionaba la tecla de
dirección opuesta a la actual (ej. ir a la derecha y presionar izquierda), la
serpiente se movía directo sobre su segundo segmento y perdía al instante —
un bug clásico de los juegos tipo Snake. Se corrigió agregando
`is_reversal()`, que ignora ese input en vez de aplicarlo.

**Limitaciones conocidas** (no corregidas, quedan como alcance futuro):
- El puntaje más alto no se guarda entre partidas (no hay persistencia en
  archivo).
- El tamaño de la ventana es fijo (no es responsive).
- Solo se puede jugar con teclado (no hay soporte táctil ni de mouse).

## 6. Reflexión final

*(Sección personal — se deja redactada como punto de partida; se recomienda
ajustarla con la propia experiencia antes de entregar.)*

Usar Claude como copiloto de programación permitió llegar rápido a una
primera versión jugable y enfocar el tiempo en pulir la *sensación* del
juego (velocidad progresiva, evitar la reversión injusta) en vez de pelear
con la sintaxis de `tkinter` desde cero. La principal ventaja del vibecoding
fue poder iterar en lenguaje natural describiendo *comportamientos* ("se
siente muy fácil", "pierde sin razón aparente") y dejar que Claude los
tradujera a cambios de código concretos. El límite más claro es que Claude
no puede *sentir* si el juego es divertido ni detectar por sí solo bugs de
experiencia de usuario (como el de la reversión) — eso solo apareció al
jugarlo manualmente, lo que confirma que el criterio humano sigue siendo
necesario para validar, no solo para pedir.

Partes del código que comprendo bien: el bucle principal del juego con
`root.after()`, la detección de colisiones (`hits_wall`, `hits_self`), y por
qué separar la lógica pura de la parte gráfica hace posible probarla con
`assert` sin abrir ninguna ventana.

Partes que necesito reforzar: el manejo de eventos de teclado de `tkinter`
(`bind("<Key>", ...)`) y cómo funciona exactamente la cola de eventos frente
a `after()` para asegurarme de que no se pueda dar más de una vuelta por
"tick" del juego.

## Estructura del proyecto

```
vibecoding-snake/
├── snake.py        # el juego
├── test_snake.py   # pruebas automáticas de la lógica (sin ventana gráfica)
└── README.md        # este documento
```
