# La mansión del doctor Chiflado

Una mini aventura gráfica al estilo de las de los años 80 (Maniac Mansion, Monkey Island…), **hecha íntegramente por IA** (Claude, de Anthropic) a partir de las ideas de **Ugo García**.

Todo el juego está en un solo archivo HTML: gráficos pixel art dibujados por código, música chiptune y efectos sintetizados en el navegador, sin imágenes ni sonidos externos.

## Cómo jugar

1. Descarga `aventura.html` y ábrelo en el navegador (doble clic). No hace falta instalar nada.
2. Haz clic en la portada para activar el sonido y empezar.
3. Elige un verbo abajo y luego haz clic en un objeto o personaje.
   - Clic en el suelo: andar. Doble clic: llegar al instante.
   - Clic derecho: MIRAR.
   - **ESC**: saltar escenas. **M**: silenciar.

Tito ha apostado diez euros a que en la mansión no hay fantasmas… y la puerta se ha cerrado a su espalda. Encuentra la salida, conoce a Paco el cocinero, a Firulais y a los ensayos de la gala del piso de arriba, y consigue todos los puntos de disparate que puedas.

## Archivos del repositorio

| Archivo | Qué es |
|---|---|
| `aventura.html` | El juego completo, listo para jugar (motor + aventura integrada). |
| `aventura.json` | La aventura en formato JSON: habitaciones, objetos, diálogos, música… |
| `motor.html` | El motor del juego sin aventura (plantilla con el hueco `/*GAME_JSON*/`). |
| `gen.py`, `audio.py`, `story2.py` … `story6.py` | Scripts de Python que generan `aventura.json` por capas. |
| `aventura_v1.json` | Base de partida que usa `gen.py`. |
| `sokoban.py`, `search.py` | Utilidades para comprobar que el puzle de las estanterías tiene solución. |
| `fmt.py`, `build.py` | Formateo del JSON e inserción en `motor.html` para crear `aventura.html`. |
| `README.md` | Esta guía. |

### Regenerar el juego

```bash
python3 gen.py && python3 audio.py && python3 story2.py && python3 story3.py \
  && python3 story4.py && python3 story5.py && python3 story6.py && python3 build.py
```

(`gen.py` parte de `aventura_v1.json`.)

---

# Guía para crear aventuras en JSON


`aventura.html` es el motor. El juego completo (habitaciones, dibujos, objetos, verbos, puzzles e historia) está en un JSON.

## Cómo cargar tu JSON

- **Botón CARGAR JSON** (o arrastrar el `.json` a la ventana): carga tu aventura al momento. Es la forma más cómoda mientras escribes.
- **Integrado**: pega el JSON dentro de `<script type="application/json" id="game-data">` en `aventura.html`. Así queda un único archivo para compartir.
- **Por URL** (solo si lo sirves con un servidor web): `aventura.html?juego=mi_aventura.json`.

Pulsa **D** durante la partida para ver el modo depuración:

- zona andable (cian)
- obstáculos (rojo)
- zonas clicables (amarillo)
- puntos a los que camina el personaje (verde)
- coordenadas del ratón

Si algo del JSON está mal (una habitación que no existe, un objeto mal escrito…), el validador lo avisa abajo a la izquierda.

## Estructura general

```json
{
  "title": "Mi aventura",
  "palette": { "madera": "#6a3412" },
  "verbs": [ {"id":"MIRAR","label":"MIRAR"}, {"id":"USAR","label":"USAR","prep":"CON"}, ... ],
  "defaultVerb": "IR A",
  "lookVerb": "MIRAR",
  "rightClickVerb": "MIRAR",
  "defaults": { "COGER": ["No puedo coger eso.", "Mejor no."], "*": "No puedo hacer eso." },
  "player": { "sprite": "chaval", "speed": 40, "textColor": "#ffe25a", "colors": {...} },
  "start": { "room": "salon", "entry": "inicio" },
  "intro": [ ...comandos... ],
  "flags": [], "inventory": [],
  "items": { ... },
  "scripts": { ... },
  "prefabs": { ... },
  "sprites": { ... },
  "images": { "fondo1": "fondo.png" },
  "audio": { "master":0.9, "music":0.32, "sfx":0.75 },
  "music": { ... }, "sounds": { ... }, "voices": { ... }, "sfx": { "pickup":"coger" },
  "rooms": { "salon": {...}, "sotano": {...} }
}
```

- **Verbos con `prep`** (USAR … CON …, DAR … A …) piden un segundo objeto. Si el primero tiene su propio `"USAR"`, se ejecuta directamente sin pedir otro.
- **`defaults`** son las respuestas cuando un objeto no define ese verbo. Si pones una lista, elige una al azar. Para MIRAR usa antes el campo `desc` del objeto, si lo tiene.
- **`player.colors`** acepta estas claves: `hair`, `hairD`, `skin`, `skinD`, `jacket`, `jacketD`, `shirt`, `belt`, `jeans`, `jeansD`, `shoes`, `shoesD`, `eyes`.

## Habitaciones

```json
"sotano": {
  "width": 320,
  "walk": [10, 104, 310, 141],
  "storm": false,
  "ambient": "#7482c0",
  "lights": [ {"x":107, "y":40, "r":72, "color":"255,190,110", "a":0.45, "flicker":0.07} ],
  "vignette": 0.5,
  "zones": [ {"id":"perro_guarda", "rect":[328,0,480,144], "if":"!perro_distraido", "onEnter":{"run":"perro_ladra"}} ],
  "timers": [ {"every":[14,26], "first":6, "if":"!murcielago_fuera", "script":"vuelo_murcielago"} ],
  "entries": { "escalera": {"x":34, "y":114, "face":"front"} },
  "onEnter": [ ...comandos... ],
  "background": [ ...comandos de dibujo... ],
  "objects": [ ... ]
}
```

- **`width`**: si es mayor que 320, la pantalla hace scroll.
- **`walk`**: rectángulo del suelo por el que se puede andar. El personaje rodea los obstáculos de los objetos buscando la ruta más corta.
- **`storm`**: con `true` hay relámpagos de vez en cuando.
- **`entries`**: puntos de llegada desde otras habitaciones.
- **`ambient`**: color que tiñe toda la escena (se multiplica), por ejemplo un azul de luz de luna.
- **`lights`**: luces que se suman encima del tono ambiente, con posición (`x`, `y`), radio (`r`), color, intensidad (`a`) y parpadeo (`flicker`). Con estas dos propiedades se consigue la iluminación de estilo moderno de la cocina y el patio.
- **`vignette`**: oscurece los bordes de la pantalla (de 0 a 1).
- **`zones`**: zonas de proximidad. Cuando el protagonista entra en el rectángulo `rect` (y se cumple `if`), se ejecuta `onEnter`; al salir, `onExit`. La acción que estuviera haciendo se interrumpe. Así funciona el perro que sale de la caseta cuando te acercas.
- **`background`** en una zona: `"background": true` ejecuta la acción sin interrumpir al jugador (la tele que se enciende sola).
- **`timers`**: eventos en segundo plano. Cada `every` segundos (un número o un rango `[min, max]` al azar) se ejecuta `script` (o `run`) sin bloquear al jugador. `first` es la primera espera. Así aparece el murciélago de vez en cuando.

## Objetos

```json
{
  "id": "mesa", "name": "MESA DE BILLAR",
  "x": 0, "y": 0,
  "box": [x, y, ancho, alto],
  "walkTo": [x, y], "face": "right",
  "obstacle": [x0, y0, x1, y1],
  "z": 134,
  "layer": "back | sort | front",
  "state": "quieta",
  "hidden": false,
  "when": "condición",
  "hotspot": "condición",
  "parent": "otro_objeto",
  "desc": "Texto por defecto para MIRAR",
  "noWalk": true,
  "autoFlip": true, "facing": "left", "pivot": 0,
  "textColor": "#c0c8ff",
  "draw": [ ...dibujo base, siempre visible... ],
  "states": {
    "quieta": { "draw": [...] },
    "movida": { "draw": [...], "name": "...", "box": [...], "verbs": {...} }
  },
  "verbs": {
    "MIRAR": "Texto",
    "EMPUJAR": [ ...comandos... ],
    "USAR:llave": [ ... ],
    "IR A": [ ... ],
    "*": "Respuesta a cualquier otro verbo"
  }
}
```

Qué hace cada campo:

- **`x`, `y`**: desplazan todo el objeto (dibujo, caja, obstáculo…).
- **`box`**: zona clicable.
- **`walkTo`** y **`face`**: adónde camina el personaje antes de actuar y hacia dónde mira después.
- **`obstacle`**: huella en el suelo que no se puede pisar.
- **`z`**: profundidad. El personaje se dibuja detrás si su `y` es menor que `z`.
- **`layer`**: `back` por defecto; `sort` si tiene `z` u `obstacle`.
- **`state`**: estado inicial.
- **`hidden`**: oculto hasta que un comando `show` lo muestre.
- **`when`**: solo existe (se dibuja y se puede clicar) si se cumple la condición.
- **`hotspot`**: `false` hace el objeto no clicable; una condición lo hace clicable solo cuando se cumple.
- **`parent`**: se mueve junto con su objeto padre.
- **`textColor`**: color de sus frases cuando habla.
- **`noWalk`**: el personaje no camina hasta el objeto antes de actuar (útil para cosas que vuelan o están en el techo).
- **`autoFlip`** y **`facing`**: al moverse con `moveTo` o `path`, el objeto se da la vuelta solo según la dirección. `facing` indica hacia dónde mira su dibujo original (`left` o `right`); `pivot` es el eje x del espejo.
- **`states`**: cada estado puede cambiar el dibujo, el nombre, la caja o los verbos.

Otras reglas:

- **Clics solapados**: si hay objetos uno encima de otro, gana el que se dibuja delante.
- **Nombre y caja**: un objeto sin `name` o sin `box` no se puede clicar (útil para decorados o efectos).
- **Salidas**: una puerta de salida es un objeto con verbo `"IR A"` que hace `goto`.

## Inventario (`items`)

```json
"llave": { "name": "LLAVE", "desc": "Una llave oxidada.", "verbs": { "USAR:cofre": [ ... ] } }
```

Las combinaciones se buscan en los dos sentidos. Para USAR LLAVE CON COFRE se busca primero `"USAR:cofre"` en la llave y después `"USAR:llave"` en el cofre.

**Importante**: los ids de inventario no pueden coincidir con los de los objetos de las habitaciones. Por ejemplo, el taco de la mesa es `taco_mesa` y el del inventario es `taco`.

## Comandos (acciones)

Una acción puede ser un texto (el personaje lo dice), un comando o una lista de ambos.

| Comando | Qué hace |
|---|---|
| `"Texto"` o `{"say":"Texto", "who":"armadura", "color":"#fff"}` | Hablar (por defecto el protagonista) |
| `{"walk":[x,y], "face":"back"}` o `{"walk":"id_objeto"}` | Caminar (con búsqueda de ruta) |
| `{"face":"left"}` | Girarse (`left`, `right`, `front`, `back`) |
| `{"wait":0.5}` | Esperar segundos |
| `{"set":"flag"}` / `{"unset":"flag"}` | Activar o desactivar una variable |
| `{"state":["id","estado"]}` | Cambiar el estado de un objeto |
| `{"show":"id"}` / `{"hide":"id"}` | Mostrar u ocultar objetos (acepta listas) |
| `{"pickup":"item"}` / `{"drop":"item"}` | Añadir o quitar del inventario |
| `{"move":["id",dx,dy,segundos], "withPlayer":true}` | Mover un objeto animado; con `withPlayer`, el protagonista lo acompaña (empujar) |
| `{"place":["id",dx,dy]}` | Colocar un objeto con un desplazamiento fijo |
| `{"moveTo":["id",x,y,segundos]}` | Mover un objeto hasta una posición de la habitación |
| `{"path":["id",[[x,y],[x,y],...],velocidad], "bob":3, "arc":30}` | Recorrer una ruta de puntos a esa velocidad (píxeles/segundo). `bob` añade un vaivén vertical (vuelo); `arc`, una parábola (lanzamiento) |
| `{"placeAt":["id","player",dx,dy]}` | Colocar un objeto junto al protagonista (o junto a otro objeto) |
| `{"flip":["id",true]}` | Voltear un objeto |
| `{"walk":[x,y], "speed":95}` | Caminar a otra velocidad (por ejemplo, huir corriendo) |
| `{"wait":[2,5]}` | Esperar un tiempo al azar entre 2 y 5 segundos |
| `{"async":[...], "name":"hilo"}` | Ejecutar acciones en paralelo sin bloquear al jugador |
| `{"stop":"hilo"}` | Cancelar un hilo en paralelo por su nombre |
| `{"goto":"habitacion", "entry":"entrada"}` | Cambiar de habitación (con fundido) |
| `{"player":[x,y], "face":"front"}` | Teletransportar al protagonista |
| `{"if":"cond", "then":..., "else":...}` | Condicional |
| `{"once":"clave", "do":..., "else":...}` | Solo la primera vez |
| `{"random":[acción1, acción2]}` | Una al azar |
| `{"run":"nombre_script"}` | Ejecutar un script de `scripts` |
| `{"card":"TEXTO", "time":3}` | Cartel a pantalla completa |
| `{"banner":"¡¡¡WOW!!!", "sub":"texto", "style":"super", "time":2.5, "sound":"wow"}` | Rótulo gigante animado: `super` (arcoíris que bota, con estrellas) o `title` (dorado, para títulos). Se cierra con un clic |
| `{"score":["id",25]}` | Suma puntos una sola vez por `id`. La puntuación máxima se calcula sola sumando todos los `score` del juego |
| `{"clock":"start"}` / `{"clock":"stop"}` | Arranca o detiene el cronómetro; el tiempo final aparece en la pantalla de fin |
| `{"hidePlayer":true}` / `{"showPlayer":true}` | Oculta o muestra al protagonista (por ejemplo, al entrar por una puerta) |
| `{"flash":true}` | Lanza un relámpago (y su trueno, si la habitación tiene `stormSound`) |
| `{"say":"...", "voice":"cocinera", "color":"#ff9ad0"}` | Frase con otra voz y color (una voz que viene de otro sitio) |
| `{"path":[...], "rel":true}` | Ruta relativa a la posición actual del objeto |
| `{"end":"TEXTO FINAL"}` | Fin de la partida: muestra el texto, el tiempo, los puntos y el rango |

## Condiciones

- `"flag"`: la variable está activa. `"!flag"`: no lo está.
- `"has:llave"`: la llave está en el inventario.
- `"state:mesa=movida"`: la mesa está en el estado `movida`.
- `"visible:id"`, `"hidden:id"`, `"room:sotano"`.
- Combinar: `"a && b"`, `"a || b"`, una lista `[...]` (todas), `{"any":[...]}` o `{"not":...}`.

**Ejemplo del puzzle de la mesa**: no se puede empujar hasta quitar el freno.

```json
"EMPUJAR": {"if": "!freno_quitado",
  "then": "No se mueve. Tiene un freno en la pata.",
  "else": [ {"move":["mesa",100,0,2], "withPlayer":true}, {"state":["mesa","movida"]}, {"set":"mesa_movida"} ]}
```

## Comandos de dibujo

Las coordenadas están en píxeles de la habitación (en un objeto se suman sus `x` e `y`). Los colores pueden ser `#rrggbb`, `rgba(...)` o `$nombre` de la paleta.

Cuando cambias de estado un objeto (`state`), sus animaciones empiezan desde el primer fotograma.

**Básicos**

| Comando | Qué dibuja |
|---|---|
| `["rect",x,y,w,h,color]` | Rectángulo |
| `["pix",x,y,color]` | Un píxel |
| `["line",x0,y0,x1,y1,color]` | Línea |
| `["poly",[[x,y],...],color]` | Polígono relleno |
| `["circle",cx,cy,r,color]` | Círculo relleno |
| `["pixels",x,y,["..XX..",".XooX."],{"X":"#fff","o":"#000"}]` | Pixel art con caracteres (`.` es transparente) |
| `["text",x,y,"TEXTO",color]` | Texto |
| `["image","id",x,y]` o `["image","id",x,y,w,h]` | Una imagen PNG declarada en `images` |
| `["sprite","nombre","animación",x,y,volteado]` | Un sprite animado de `sprites` |
| `["ellipse",cx,cy,rx,ry,color]` / `["ring",cx,cy,r,color,grosor]` | Elipse rellena / anillo |

**Agrupar y reutilizar**

| Comando | Qué hace |
|---|---|
| `["at",dx,dy,[...]]` | Desplaza un grupo de comandos |
| `["repeat",n,dx,dy,[...]]` | Repite un grupo n veces |
| `["use","prefab",dx,dy]` | Reutiliza un dibujo definido en `prefabs` |

**Texturas**

| Comando | Qué dibuja |
|---|---|
| `["wallpaper",x,y,w,h,base,raya,motivo]` | Papel pintado |
| `["planks",x,y,w,h,fugaX,c1,c2,junta,veta,sombra]` | Suelo de tablones en perspectiva |
| `["checker",x,y,w,h,fugaX,c1,c2,tamaño,filas]` | Baldosas en perspectiva |
| `["stones",x,y,w,h,c1,c2,mortero,semilla]` | Muro de piedra |
| `["bricks",x,y,w,h,ladrillo,mortero,ancho,alto]` | Ladrillos |
| `["dither",x,y,w,h,c1,c2]` | Degradado tramado |
| `["books",x,y,w,h,[colores],semilla]` | Fila de libros |
| `["rug",x0,x1,y0,y1,apertura,base,borde,interior,moteado]` | Alfombra en perspectiva |
| `["grad",x,y,w,h,[color1,color2,...],horizontal]` | Degradado suave (cielos, paredes) |
| `["speckle",x,y,w,h,color,densidad,semilla]` | Motas sueltas para dar textura |
| `["tiles",x,y,w,h,anchoCelda,altoCelda,c1,c2,junta]` | Azulejos |
| `["moon",x,y,radio]` | Luna con halo |
| `["hills",x,y,w,h,color,semilla,rugosidad]` | Silueta de colinas o arboleda |
| `["tree",x,base,alto,colorTronco,[oscuro,medio,claro],semilla]` | Árbol con copa sombreada |
| `["grass",x,y,w,h,[colores],cantidad,semilla]` | Briznas de hierba |

**Animados**

| Comando | Qué dibuja |
|---|---|
| `["fire",x,base,w,alto]` | Fuego |
| `["light",x,y,r,"r,g,b",intensidad,parpadeo]` | Luz que se suma después del tono ambiente (por ejemplo, la de la nevera al abrirla) |
| `["stars",x,y,w,h,cantidad,semilla]` | Estrellas que titilan |
| `["clouds",x,y,w,h,cantidad,color,colorBorde,velocidad,semilla]` | Nubes que se desplazan |
| `["fireflies",x,y,w,h,cantidad]` | Luciérnagas |
| `["moths",x,y,radio,cantidad]` | Polillas alrededor de una luz |
| `["steam",x,y,alto]` | Vapor de una olla |
| `["drip",x,y,caída,periodo]` | Gota de un grifo |
| `["swing",px,py,largo,amplitud,periodo,colorCuerda,colorRueda,radio]` | Columpio de neumático |
| `["flame",x,y,ancho]` | Llama de vela |
| `["noise",x,y,w,h]` | Nieve de televisión |
| `["roll",x,y,w,h]` | Barra que recorre la pantalla |
| `["glow",x,y,w,h,"r,g,b",alfa,oscilación,velocidad]` | Resplandor que parpadea |
| `["pendulum",px,py,largo,amplitud,periodo,colorVara,colorBola,tamaño]` | Péndulo |
| `["nightview",x,y,w,h]` | Cielo nocturno con luna y estrellas; con `storm`, relámpagos |
| `["eyes",x,y,separación]` | Ojos que siguen al protagonista |
| `["blink",periodo,fracción,[...]]` | Enciende y apaga un grupo |
| `["frames",fps,[[...],[...]]]` | Animación por fotogramas |
| `["if","condición",[...],[...]]` | Dibuja un grupo u otro según una condición |

Los fondos (`background`) se dibujan una sola vez y se guardan en memoria; las partes animadas se repintan en cada fotograma.

## Sprites animados

Los personajes y animales animados se definen una vez en `sprites` y se dibujan con `["sprite", ...]`:

```json
"sprites": {
  "perro": {
    "palette": {"B":"#b87a3e", "L":"#f0c888", "k":"#111"},
    "anims": {
      "quieto": {"fps":3,  "frames":[ ["..BB..", ".BkBL."], ["..BB..", ".BkBL."] ]},
      "corre":  {"fps":12, "frames":[ ... ]},
      "sale":   {"fps":8,  "loop":false, "frames":[ ... ]}
    }
  }
}
```

Cada fotograma es pixel art con caracteres, como en `pixels`. Con `"loop": false` la animación se reproduce una vez y se queda en el último fotograma.

Lo normal es que cada estado del objeto muestre una animación distinta:

```json
{"id":"perro", "x":398, "y":122, "state":"dentro",
 "states": {
   "quieto": {"draw":[["sprite","perro","quieto",-11,-12]]},
   "corre":  {"obstacle":null, "draw":[["sprite","perro","corre",-11,-12]]}
 }}
```

Un estado puede anular el obstáculo con `"obstacle": null`, por ejemplo mientras el perro corre.

## Ejemplo: el perro guardián

1. Una zona delante de la caseta ejecuta el script `perro_ladra` si no se cumple `perro_distraido`.
2. `perro_ladra` saca al perro (`moveTo` con la animación `corre`), lo pone a ladrar (`say` con `"who":"perro"`) y hace retroceder al protagonista (`walk` con `speed`).
3. Después lanza un hilo en paralelo (`async`) llamado `perro_vuelve`, que tras unos segundos devuelve al perro a la caseta.
4. DAR SALCHICHAS A PERRO:
   - cancela ese hilo (`stop`);
   - lanza la salchicha con `path` y `arc`;
   - hace correr al perro con `path`;
   - activa `perro_distraido`, así que la zona deja de dispararse y ya se puede coger la llave.

## Ejemplo: el murciélago

1. Un `timer` del salón lanza `vuelo_murcielago` cada 14–26 segundos.
2. El script coloca al murciélago fuera de pantalla (`place`) y lo muestra.
3. Vuela con `path` y `bob` hasta una lámpara, donde pasa al estado `colgado` durante un rato al azar (`"wait":[5,9]`).
4. Después se va volando y se oculta.

Con `random` elige cada vez una de cuatro rutas y lámparas distintas.

## Escenas cinemáticas, puntuación y atajos

- **Escenas sin interfaz**: una habitación con `"noUI": true` oculta los verbos y el inventario. El jugador no puede interactuar, solo pasar las frases con un clic o saltarse la escena entera con **ESC** (que la acelera hasta que termina). La intro y el final del juego usan la habitación `exterior`.
- **Inicio**: `start` apunta a la escena de entrada, e `intro` contiene sus acciones. La última acción es `{"clock":"start"}`.
- **Puntuación**:

```json
"scoring": { "timeLabel":"TIEMPO", "pointsLabel":"PUNTOS DE DISPARATE",
  "ranks": [[100,"¡MAESTRO DEL DISPARATE!"], [60,"¡Nada mal!"], [25,"Aventurero serio."], [0,"¿Has venido a trabajar?"]] }
```

  Los rangos se leen de arriba abajo, y se muestra el primero cuyo mínimo alcances. En el juego hay seis disparates que dan puntos, 100 en total:

| Disparate | Cómo se consigue | Puntos |
|---|---|---|
| Carambola mágica | USAR TACO CON MESA DE BILLAR | 25 |
| Home run | USAR TACO CON MURCIÉLAGO | 30 |
| Canal de madrugada | Encender la tele y USARLA | 15 |
| Cocido apagado | APAGAR la cocina de gas | 10 |
| Vuelta al mundo | USAR el globo terráqueo | 10 |
| Regalo a la armadura | DAR FOTO A ARMADURA | 10 |

- **Doble clic**: si haces doble clic mientras el personaje camina hacia un sitio, llega al instante. Si ibas hacia un objeto, la acción se ejecuta enseguida.
- **Temporizadores con nombre**: `"name":"vuelo_murci"` en un temporizador permite cortarlo con `{"stop":"vuelo_murci"}`, como hace el golpe al murciélago.
- **Fuegos artificiales**: `["fireworks",x,y,w,h,cantidad]` es una primitiva de dibujo animada (la del final).

## Rejilla tipo Sokoban (estanterías que se empujan)

Una habitación puede tener una rejilla de celdas en el suelo. Los objetos con `cell` ocupan una celda, y los que además tienen `"pushable": true` se pueden empujar una celda cada vez:

```json
"grid": {"x0":0, "y0":98, "cw":32, "ch":14, "cols":10, "rows":3,
         "pushSound":"arrastre_corto", "pushTime":0.45, "resetEntry":"pasillo", "blocked":[[0,2]]},
"objects": [
  {"id":"est_poesia", "name":"ESTANTERÍA", "cell":[4,0], "pushable":true,
   "box":[-14,-30,28,31], "obstacle":[-14,-12,14,-1], "draw":[...],
   "verbs": {"EMPUJAR": {"push":"est_poesia", "ok":[], "fail":"No se mueve. Hay algo detrás."}}},
  {"id":"busto", "cell":[2,0], "obstacle":[-14,-12,14,-1], ...}
]
```

- **Rejilla**: `x0`/`y0` es la esquina superior izquierda, `cw`/`ch` el tamaño de cada celda y `cols`/`rows` el número de columnas y filas. `blocked` marca celdas fijas sin objeto.
- **Coordenadas del dibujo**: el origen de un objeto con `cell` es el centro inferior de su celda, así que `draw`, `box` y `obstacle` se escriben relativos a ese punto.
- **Empujar**: con el verbo EMPUJAR (`pushVerb`), el protagonista se coloca solo en el lado libre más cercano de la estantería y la empuja hacia el lado contrario, avanzando con ella. Si quieres empujar en otra dirección, colócate antes en ese lado.
- **`{"push":"id", "ok":..., "fail":...}`**: intenta el empujón y ejecuta `ok` o `fail` según salga bien o no (fuera de la rejilla u ocupado = falla).
- **`{"gridReset": true}`**: devuelve todas las piezas a su sitio, para no quedarse atascado. En la biblioteca lo hace la campanilla.
- **Destinos inalcanzables**: si algo está encerrado, el personaje se acerca todo lo posible y dice el texto de `"unreachable"`. Así se nota que la sección Z está bloqueada.

Para diseñar tu propio puzzle, conviene comprobar que tiene solución. La del juego se resuelve en 6 empujes.

## Sonido y música

Todo el audio se sintetiza en el navegador en tiempo real, así que no hace falta ningún archivo de audio. Por la política de los navegadores, el sonido arranca con el primer clic o la primera tecla. La tecla **M** (o el botón SONIDO) lo silencia, y el navegador recuerda esa elección.

### Música (`music`)

Estilo tracker: cada pista es una cadena de notas.

```json
"music": {
  "mansion": { "bpm":126, "loop":true, "tracks":[
    {"wave":"triangle", "vol":0.5, "len":2, "gate":0.55, "notes":"D2 A2 F2 A2 | A#1 F2 D2 F2"},
    {"wave":"pulse25", "vol":0.14, "vibrato":[6,0.006], "notes":"D4 - F4 - A4:4 G#4 A4"},
    {"wave":"drums", "vol":0.3, "len":1, "notes":"k - h - s - h - k - h k s - h h"}
  ]}
}
```

- **Notas**:
  - `D4`, `A#3` o `Bb3` son notas; `-` es un silencio.
  - `:n` indica la duración en semicorcheas (`A4:4` es una negra). Sin `:n`, cada nota dura lo que diga `len` en la pista (2 = corchea).
  - `|` es solo un separador visual.
- **Ondas**: `square`, `pulse25`, `pulse12`, `triangle`, `sawtooth`, `sine`.
- **Batería**: la onda `drums` usa `k` (bombo), `s` (caja), `h` (charles) y `o` (charles abierto).
- **Filtro**: `filter` (`["lowpass", 1500, 1.5]`) suaviza una pista; por ejemplo, el «saxo» de sierra del pasillo.
- **Otros campos de una pista**: `gate` (qué parte de la nota suena, para el staccato), `vibrato` ([velocidad, profundidad]), `decay`, `attack` y `slide`.
- **Longitudes**: cada pista se repite con su propia longitud, así que puedes combinar un bajo de 8 compases con una melodía de 16.
- **En una habitación**: `"music":"mansion"` la hace sonar al entrar; si la siguiente habitación usa la misma, no se corta.
- **Desde un guion**: `{"music":"victoria"}` cambia de tema y `{"music":null}` la para. Con `"loop": false`, el tema suena una sola vez (como la sintonía final).

### Efectos (`sounds`)

Cada efecto es una o varias capas sintetizadas:

```json
"ladrido": {"range":400, "layers":[
  {"wave":"sawtooth", "freq":520, "freqEnd":210, "dur":0.16, "vol":0.8, "filter":["bandpass",900,null,1.5], "repeat":2, "gap":0.28},
  {"wave":"noise", "dur":0.12, "vol":0.22, "filter":["bandpass",1500,null,1], "repeat":2, "gap":0.28}
]}
```

- **`wave`**: cualquiera de las de la música o `noise` (ruido, para truenos, estática, pasos…).
- **Tono**: `freq` o `note` para el tono; `freqEnd` para deslizarlo.
- **Tiempo y volumen**: `dur`, `vol`, `attack`, `sustain` y `delay`.
- **Filtro**: `filter` es `[tipo, frecuencia, frecuenciaFinal, Q]`, con tipo `lowpass`, `highpass` o `bandpass`.
- **Modulación y repetición**: `vibrato` ([velocidad, profundidad en Hz]) y `repeat` + `gap`.
- **`range`**: distancia en píxeles a la que deja de oírse.

Formas de hacerlo sonar:

- **En un guion**: `{"sound":"ladrido", "at":"perro"}`. `at` puede ser un objeto o una x de la habitación; el volumen y el lado (izquierda/derecha) dependen de dónde está el protagonista.
- **Emisores en objetos**: `"sound": {"name":"tictac", "every":2}` en un objeto, o en uno de sus estados, lo hace sonar solo cada cierto tiempo mientras esté visible. Así suenan el reloj, la chimenea, la tele encendida, el aleteo del murciélago, los ronquidos del perro o el grifo.
- **Varios sonidos al azar**: `name` puede ser una lista (`["muelles","risitas","suspiro"]`) y cada vez suena uno.
- **Ambiente de la habitación**: `"sounds": [{"name":"grillo", "every":[0.7,2], "at":320}]`.
- **Truenos**: `"stormSound":"trueno"` en una habitación con tormenta suena justo después de cada relámpago.
- **Al coger objetos**: `"sfx": {"pickup":"coger"}` es la sintonía que suena al recoger algo.
- **Zonas silenciosas**: una zona con `"background": true` ejecuta su acción sin interrumpir al jugador. Por ejemplo, la tele que se enciende sola cuando te acercas.

### Voces "bla bla bla"

Mientras un personaje habla suenan sílabas sin sentido, sintetizadas con un filtro de formante:

```json
"voices": {
  "player":   {"pitch":230, "wave":"sawtooth", "formant":1.1, "vol":0.42, "rate":0.11},
  "metalica": {"pitch":82,  "wave":"square",   "formant":0.7, "rate":0.15}
}
```

- **Campos**: `pitch` es el tono, `formant` el timbre (más alto suena más agudo o nasal) y `rate` los segundos entre sílabas.
- **Protagonista**: usa `"player": {"voice":"player"}`.
- **Objetos que hablan**: usan `"voice":"metalica"` o `"voice": false` para ninguna voz (el perro ladra con un efecto de sonido).

## Protagonista personalizado (opcional)

En lugar de `"sprite":"chaval"` puedes definir tus propios fotogramas en pixel art:

```json
"sprite": { "w":12, "h":24, "anchor":[6,24], "palette":{"X":"#fff","o":"#000"},
  "right": [ [..fotograma quieto..], [..paso 1..], [..paso 2..] ],
  "front": [ ... ], "back": [ ... ] }
```

- El fotograma 0 es el personaje quieto; el resto forma el ciclo de andar.
- Si no defines `left`, se usa `right` en espejo.

## Animaciones del protagonista (`pose`)

Al usar un verbo, el protagonista hace un gesto antes de ejecutar la acción.

- `verbPoses` (raíz del JSON): gesto por defecto de cada verbo, p. ej. `{"ABRIR":"reach","EMPUJAR":"push","GOLPEAR":"knock","DAR":"give"}`.
- En un objeto: `"pose":"reach_up"` (sustituye al del verbo), `"pose":{"COGER":"reach_low"}` (solo para ese verbo) o `"pose":false` (sin gesto).
- En un item del inventario: `"pose":"taco"`, que se usa al hacer USAR o DAR con ese objeto.
- Comando dentro de un script: `{"pose":"taco","time":0.9,"wait":true}`.

Gestos disponibles: `reach`, `reach_low`, `reach_up`, `give`, `push`, `knock`, `whistle` y `taco` (levanta el taco y lo balancea).

## Conversaciones tipo SCUMM (`dialogs`)

Se definen en la raíz del JSON y se abren con el comando `{"dialog":"paco"}`:

```json
"dialogs": {
  "paco": [
    {"text":"Rosita dice que subas.", "if":"recado_rosita", "exit":true, "do":[{"run":"cocinero_se_va"}]},
    {"text":"¿Quién eres tú?", "once":true, "do":[{"say":"Soy Paco.", "who":"cocinero"}]},
    {"text":"Nada, me voy.", "exit":true}
  ]
}
```

Cada opción admite estos campos:

- `text`: la frase, que dice el protagonista al elegirla.
- `if`: la opción solo aparece si se cumple la condición.
- `once`: la opción desaparece después de usarla.
- `do`: los comandos que se ejecutan al elegirla.
- `exit`: cierra la conversación.
- `next`: salta a otro diálogo.
- `silent`: el protagonista no dice la frase.

Se muestran como mucho 6 opciones y la última se mantiene siempre visible.

## Foto del objeto al MIRAR (`icon`)

Un item puede llevar `"icon":[ ...comandos de dibujo... ]` en un lienzo de 40x28. Al MIRAR o LEER ese item aparece un panel arriba a la derecha con el dibujo ampliado y su nombre. El panel se cierra solo al cabo de un rato o con un clic.

## Otros detalles

- `talkDraw` (en un objeto): lo que se dibuja mientras ese personaje habla, por ejemplo la animación con la boca moviéndose.
- `ui.speechBackdrop`: opacidad (de 0 a 1, por defecto 0.45) de la caja oscura detrás de los textos, para que se lean en fondos claros.
- Reloj de pulsera: el hueco de la derecha del interfaz muestra un reloj digital de estilo CASIO con el tiempo transcurrido (MM:SS) y los puntos (PTS). Arranca con el comando `clock`.
- Sonido: el audio se activa con la primera interacción (clic o tecla), como exigen los navegadores. En las escenas sin interfaz parpadea un aviso hasta que se active.

## Pantalla de título (`titleScreen`)

Se muestra antes de la intro y espera a que el jugador haga clic (o pulse Intro o Espacio). Ese clic activa el sonido, así que la intro ya suena desde el principio. Si no la pones, el juego empieza directamente con la intro.

```json
"titleScreen": {
  "title": ["LA MANSIÓN DEL", "DOCTOR CHIFLADO"],
  "sub": "UNA AVENTURA GRÁFICA COMO LAS DE LOS 80",
  "howtoTitle": "CÓMO SE JUEGA",
  "howto": ["1. ELIGE UN VERBO...", "2. LUEGO HAZ CLIC..."],
  "warn": ["¡ATENCIÓN! ESTE JUEGO TIENE MÚSICA Y RUIDOS.", "..."],
  "prompt": "HAZ CLIC PARA ACTIVAR EL SONIDO Y EMPEZAR"
}
```

Caben unos 48 caracteres por línea en `howto` y unos 46 en `warn`. La pantalla solo aparece la primera vez; al volver a jugar se salta.

## Créditos finales (`credits`)

Después de la pantalla de puntuación (a los 9 segundos o con un clic) suben los créditos como en el cine. Con un clic se aceleran y, al terminar, otro clic empieza una partida nueva.

```json
"creditsMusic": "titulo",
"creditsSpeed": 16,
"credits": [
  {"t": "LA MANSIÓN DEL"},
  {"h": "TU PARTIDA"}, "TIEMPO: {TIEMPO}", "PUNTOS: {PUNTOS} DE {MAX}", {"c": "{RANGO}", "color": "#ff9ad0"},
  {"gap": 20},
  {"h": "UNA IDEA DE"}, {"n": "UGO GARCIA"},
  {"t": "FIN"}
]
```

Tipos de entrada:

- Texto suelto: una línea normal.
- `h`: un encabezado en color.
- `c`: una línea con el color que indiques en `color`.
- `t`: un título grande dorado.
- `n`: un nombre grande de colores.
- `gap`: un espacio en píxeles.

`{TIEMPO}`, `{PUNTOS}`, `{MAX}` y `{RANGO}` se sustituyen por los datos de la partida. En esta aventura, `story5.py` cuenta las líneas de código y los objetos cada vez que se regenera el JSON.

## Versión (`version`)

`"version": "v0.15"` en la raíz del JSON se muestra en pequeño en la esquina inferior derecha de la portada y de las escenas. Sirve para saber si estás viendo la última versión. En esta aventura se cambia en `story6.py` (constante `VERSION`) y sube en 1 con cada iteración.
