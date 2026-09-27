# Genera la versión ampliada de aventura.json (cocina, patio, perro, murciélago).
import json, copy

g = json.load(open('aventura_v1.json'))
R = g['rooms']

# ---------------------------------------------------------------- sprites
def grid(w, h): return [['.'] * w for _ in range(h)]
def put(G, x, y, rows):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != '.' and 0 <= y + j < len(G) and 0 <= x + i < len(G[0]):
                G[y + j][x + i] = ch
def fill(G, x0, x1, y, ch):
    for x in range(x0, x1 + 1): G[y][x] = ch
def S(G): return [''.join(r) for r in G]

HEAD = ["...BBBB..", "..BBBBBDD", ".BwkBBDDD", "kLLBBBDDD", "LLLLBBBD.", ".LLLLBB.."]
HEAD_BARK = ["...BBBB..", "..BBBBBDD", ".BwkBBDDD", "kLLBBBDDD", "ttt.BBBD.", "LLLLBBB.."]
HEAD_EAT = ["...BBBB..", "..BBBBBDD", ".BDDBBDDD", "kLLBBBDDD", "LLLLBBBD.", ".LLLLBB.."]

def body(G, tail):
    fill(G, 8, 18, 4, 'B'); fill(G, 9, 17, 4, 'H')
    fill(G, 7, 19, 5, 'B'); fill(G, 6, 19, 6, 'B'); fill(G, 6, 19, 7, 'B')
    fill(G, 6, 19, 8, 'B'); fill(G, 9, 16, 8, 'L')
    G[4][8] = 'r'; G[5][7] = 'r'; G[5][8] = 'r'; G[6][7] = 'r'
    if tail == 'up':
        G[1][19] = 'B'; G[2][18] = 'B'; G[3][17] = 'B'; G[3][18] = 'B'
    else:
        G[1][21] = 'B'; G[2][20] = 'B'; G[3][19] = 'B'; G[3][18] = 'B'

def legs(G, kind):
    if kind == 'stand':
        for x in (6, 9, 15, 18):
            for y in (9, 10): G[y][x] = G[y][x + 1] = 'B'
            G[11][x] = G[11][x + 1] = 'D'
    elif kind == 'run1':
        for x9, x10 in ((5, 4), (10, 11), (14, 13), (19, 20)):
            G[9][x9] = G[9][x9 + 1] = 'B'; G[10][x10] = G[10][x10 + 1] = 'B'; G[11][x10] = G[11][x10 + 1] = 'D'
    elif kind == 'run2':
        for x in (7, 16):
            for y in (9, 10): fill(G, x, x + 2, y, 'B')
            fill(G, x, x + 2, 11, 'D')

def dog(head=HEAD, tail='up', leg='stand', head_dy=0):
    G = grid(22, 12); body(G, tail); legs(G, leg); put(G, 0, head_dy, head); return S(G)

SLEEP = ["......................",
         "......................",
         "......................",
         "......................",
         "......................",
         "......................",
         "...BBBB...............",
         "..BBBBBDDBBBBBBBBB....",
         ".BDDBBDDDBBHHHHHHBBB..",
         "kLLBBBBBBBBBBBBBBBBBBB",
         "LLLLLLBBBLLLLLLLLBBBB.",
         ".DDDD..........DDDD..."]

perro = {
    "palette": {"B": "#b87a3e", "H": "#d8a060", "L": "#f0c888", "D": "#6a4020", "k": "#111111",
                "w": "#ffffff", "r": "#c02828", "t": "#e05a6a"},
    "anims": {
        "quieto": {"fps": 3, "frames": [dog(tail='up'), dog(tail='wag')]},
        "ladra": {"fps": 7, "frames": [dog(HEAD_BARK, 'up'), dog(HEAD, 'wag')]},
        "corre": {"fps": 12, "frames": [dog(tail='wag', leg='run1'), dog(tail='up', leg='run2')]},
        "come": {"fps": 4, "frames": [dog(HEAD_EAT, 'wag', head_dy=3), dog(HEAD_EAT, 'up', head_dy=4)]},
        "duerme": {"fps": 1, "frames": [SLEEP]}
    }
}

murcielago = {
    "palette": {"X": "#3a2a48", "W": "#7a5a90", "e": "#ff5050"},
    "anims": {
        "vuela": {"fps": 12, "frames": [
            ["W.........W", "WW..X.X..WW", ".WWWXXXWWW.", "..WWeXeWW..", "....XXX....", ".....X....."],
            ["....X.X....", "....XXX....", "WWWWeXeWWWW", ".WWWXXXWWW.", "..W.XXX.W..", ".....X....."],
            ["....X.X....", "....XXX....", "...WeXeW...", "..WWXXXWW..", ".WWW.X.WWW.", "WW.......WW"],
            ["....X.X....", "....XXX....", "WWWWeXeWWWW", ".WWWXXXWWW.", "..W.XXX.W..", ".....X....."]]},
        "colgado": {"fps": 1, "frames": [["X...X", ".XXX.", "WXXXW", "WXXXW", "WXXXW", "WeXeW", ".XXX.", "X...X"]]}
    }
}
g['sprites'] = {"perro": perro, "murcielago": murcielago}

ZZZ = ["XXXX", "..X.", ".X..", "XXXX"]

# ---------------------------------------------------------------- items / historia
items = g['items']
del items['llave']
items['llave_patio'] = {"name": "LLAVE PEQUEÑA", "desc": "Una llave pequeña con una etiqueta que pone: PATIO."}
items['llave_porton'] = {"name": "LLAVE GRANDE", "desc": "Una llave enorme y oxidada. ¡La del portón!"}
items['salchichas'] = {"name": "SALCHICHAS", "desc": "Una ristra de salchichas de Frankfurt. Huelen de maravilla.",
                       "verbs": {"COGER": "Ya las tengo.", "USAR": "¿Comérmelas? Mejor las guardo para algo."}}
items['taco']['verbs']['USAR:perro'] = "¿Pegar al perro? ¡Ni hablar! Pobre animal."

g['scripts']['leer_nota'] = [
    "Dice así:",
    "La llave del patio la colgué en la viga del sótano.",
    "La entrada al sótano está bajo la mesa de billar. Quiten el freno antes de moverla.",
    "La llave del portón la tiene Firulais, en su caseta.",
    "P.D.: a Firulais le chiflan las salchichas.",
    "Firmado: el mayordomo."
]
g['intro'][-1] = "Tengo que encontrar la manera de salir de aquí."

# sótano: la llave colgada ahora es la del patio
for o in R['sotano']['objects']:
    if o['id'] == 'llave_colgada':
        o['verbs']['USAR:taco'] = [{"face": "back"}, "¡A ver con el taco...!",
                                   {"move": ["llave_colgada", 0, 84, 0.5]}, {"hide": "llave_colgada"},
                                   {"pickup": "llave_patio"}, "¡Te pillé! Es una llave pequeña. La etiqueta dice: PATIO."]
        o['verbs']['MIRAR'] = "¡Una llave! Cuelga de la viga, muy alta."

# ---------------------------------------------------------------- murciélago en el salón
salon = R['salon']
salon['objects'].append({
    "id": "murcielago", "name": "MURCIÉLAGO", "hidden": True, "layer": "front", "noWalk": True,
    "state": "vuela", "box": [-7, -5, 14, 11],
    "states": {
        "vuela": {"draw": [["sprite", "murcielago", "vuela", -5, -3]]},
        "colgado": {"box": [-4, -1, 9, 11], "draw": [["sprite", "murcielago", "colgado", -2, 0]]}
    },
    "verbs": {
        "MIRAR": {"if": "state:murcielago=colgado", "then": "Un murciélago colgado cabeza abajo. Como yo los lunes.",
                  "else": "¡Un murciélago! Qué mono. Qué asco."},
        "COGER": "Ni loco. Muerde.",
        "HABLAR": ["¿Qué tal, conde?", "...", "No es muy hablador. Mejor."]
    }
})

def vuelo(start, into, perch, out):
    return [{"place": ["murcielago", start[0], start[1]]}, {"state": ["murcielago", "vuela"]}, {"show": "murcielago"},
            {"path": ["murcielago", into + [perch], 75], "bob": 3},
            {"place": ["murcielago", perch[0], perch[1]]},
            {"state": ["murcielago", "colgado"]}, {"wait": [5, 9]},
            {"state": ["murcielago", "vuela"]},
            {"path": ["murcielago", out, 85], "bob": 3}]

g['scripts']['vuelo_murcielago'] = [
    {"set": "murcielago_fuera"},
    {"random": [
        vuelo([-12, 32], [[50, 18], [100, 40]], [130, 24], [[180, 34], [330, 14], [480, 40], [656, 22]]),
        vuelo([656, 26], [[590, 34], [500, 14]], [436, 24], [[380, 38], [240, 16], [90, 40], [-14, 26]]),
        vuelo([656, 44], [[610, 58], [560, 46]], [510, 69], [[545, 40], [600, 22], [656, 30]]),
        vuelo([-12, 20], [[80, 30], [250, 14], [380, 36]], [436, 24], [[520, 20], [656, 36]])
    ]},
    {"hide": "murcielago"},
    {"unset": "murcielago_fuera"}
]
salon['timers'] = [{"every": [14, 26], "first": 6, "if": "!murcielago_fuera", "script": "vuelo_murcielago"}]

# ---------------------------------------------------------------- vestíbulo más ancho con puerta a la cocina
h = R['vestibulo']
old = h['background']
inner = old[3:-2]
h['width'] = 400
h['walk'] = [8, 100, 392, 141]
h['background'] = [
    ["wallpaper", 0, 6, 400, 56, "#1e3a2a", "#24442f", "#8a7a3a"],
    ["repeat", 10, 40, 0, [["use", "moldura", 0, 0], ["use", "arrimadero", 0, 0]]],
    ["checker", 0, 90, 400, 54, 200, "#d8d0c0", "#2a2a34", 18, 6],
    ["at", 80, 0, inner],
    ["rect", 10, 26, 40, 3, "#b08a48"], ["rect", 12, 29, 36, 61, "#3a200c"], ["rect", 16, 32, 28, 58, "#0e0806"],
    ["tiles", 16, 34, 28, 34, 7, 5, "#6a7870", "#62706a", "#3a4640"], ["rect", 16, 32, 28, 2, "#1e4a4a"],
    ["rect", 16, 68, 28, 22, "#3a1a14"], ["rect", 16, 68, 28, 1, "#1a0a08"],
    ["rect", 58, 78, 12, 14, "#5a5a62"], ["rect", 58, 78, 12, 1, "#8a8a92"], ["rect", 60, 80, 1, 11, "#707078"],
    ["line", 61, 78, 57, 58, "#8a2020"], ["rect", 55, 56, 5, 3, "#8a2020"],
    ["line", 66, 78, 70, 60, "#20306a"], ["rect", 68, 58, 5, 3, "#20306a"],
    ["line", 64, 78, 64, 64, "#2a2a2a"], ["rect", 63, 63, 3, 2, "#2a2a2a"],
    ["rect", 0, 0, 2, 144, "#120804"], ["rect", 398, 0, 2, 144, "#120804"]
]
for o in h['objects']:
    o['x'] = o.get('x', 0) + 80
txt = json.dumps(h['objects'], ensure_ascii=False).replace('"walk": [160, 100]', '"walk": [240, 100]')
h['objects'] = json.loads(txt)
h['objects'].insert(0, {"id": "puerta_cocina_v", "name": "PUERTA DE LA COCINA", "box": [10, 26, 40, 64],
                        "walkTo": [30, 104], "face": "back",
                        "verbs": {"MIRAR": "Por ahí se va a la cocina. Huele a guiso.",
                                  "IR A": {"goto": "cocina", "entry": "vestibulo"}}})
h['entries'] = {"salon": {"x": 110, "y": 110, "face": "right"}, "cocina": {"x": 32, "y": 110, "face": "right"}}
for o in h['objects']:
    if o['id'] == 'puerta_principal':
        v = o['verbs']
        v.pop('USAR:llave')
        v['USAR:llave_porton'] = [{"say": "A ver si encaja..."}, {"wait": 0.4}, {"state": ["puerta_principal", "abierta"]},
                                  {"drop": "llave_porton"}, {"set": "puerta_abierta"}, "¡Clac! ¡Se ha abierto!"]
        v['USAR:llave_patio'] = "No encaja. Es demasiado pequeña."
        v['ABRIR'] = {"if": "state:puerta_principal=abierta", "then": "Ya está abierta.",
                      "else": {"if": "has:llave_porton", "then": "Está cerrada con llave. Pero yo tengo una llave grande...",
                               "else": "Está cerrada con llave. Necesito la llave del portón."}}

# ---------------------------------------------------------------- COCINA
cocina = {
    "name": "Cocina",
    "width": 320,
    "walk": [10, 102, 310, 141],
    "ambient": "#8a92bc",
    "vignette": 0.45,
    "lights": [
        {"x": 200, "y": 40, "r": 110, "color": "255,205,130", "a": 0.42, "flicker": 0.03},
        {"x": 168, "y": 36, "r": 46, "color": "120,150,255", "a": 0.22}
    ],
    "entries": {"vestibulo": {"x": 30, "y": 112, "face": "right"}, "patio": {"x": 280, "y": 110, "face": "left"}},
    "onEnter": [{"once": "cocina_primera", "do": "La cocina. Aquí huele a puchero... y a misterio."}],
    "background": [
        ["grad", 0, 0, 320, 56, ["#3e4834", "#56603f", "#646e4a"]],
        ["speckle", 0, 4, 320, 50, "#4a543c", 0.05, 3], ["speckle", 0, 4, 320, 50, "#6c7652", 0.03, 4],
        ["rect", 0, 0, 320, 4, "#2a1a10"], ["rect", 0, 4, 320, 1, "#4a3020"],
        ["rect", 0, 54, 320, 3, "#1e5a5a"], ["rect", 0, 54, 320, 1, "#2e7a7a"],
        ["tiles", 0, 57, 320, 33, 8, 6, "#dfe6da", "#d2dccf", "#9aa89c"],
        ["rect", 0, 90, 320, 3, "#2a1a10"],
        ["checker", 0, 93, 320, 51, 160, "#8e3226", "#d8ccb0", 14, 5],
        ["speckle", 0, 93, 320, 51, "rgba(0,0,0,0.25)", 0.04, 9],
        ["rect", 6, 26, 40, 3, "#6a4a28"], ["rect", 8, 29, 36, 61, "#2a1a10"], ["rect", 12, 32, 28, 58, "#0e0806"],
        ["rect", 12, 32, 28, 40, "#1e3a2a"], ["checker", 12, 72, 28, 18, 26, "#d8d0c0", "#2a2a34", 6, 3],
        ["rect", 84, 28, 48, 2, "#6a6a70"], ["rect", 84, 28, 48, 1, "#9a9aa0"],
        ["line", 92, 30, 92, 34, "#444444"], ["circle", 92, 38, 4, "#3a3a40"], ["circle", 92, 38, 2, "#56565c"],
        ["line", 108, 30, 108, 34, "#444444"], ["circle", 108, 39, 5, "#9a5230"], ["circle", 107, 38, 3, "#b86a40"], ["pix", 106, 36, "#e0a070"],
        ["line", 122, 30, 122, 33, "#444444"], ["rect", 120, 33, 5, 2, "#8a8a94"], ["rect", 121, 35, 3, 8, "#8a8a94"],
        ["rect", 144, 16, 50, 42, "#e8e4d8"], ["rect", 146, 18, 46, 38, "#c8c4b8"],
        ["nightview", 148, 20, 42, 34],
        ["rect", 168, 20, 2, 34, "#e8e4d8"], ["rect", 148, 36, 42, 2, "#e8e4d8"],
        ["rect", 141, 56, 56, 3, "#e8e4d8"], ["rect", 141, 58, 56, 1, "#9a968c"],
        ["tiles", 146, 18, 12, 22, 2, 2, "#c83a3a", "#f0e4e0", "#d86060"], ["tiles", 180, 18, 12, 22, 2, 2, "#c83a3a", "#f0e4e0", "#d86060"],
        ["rect", 144, 16, 50, 3, "#b82a2a"],
        ["rect", 206, 22, 18, 24, "#f0ece0"], ["rect", 206, 22, 18, 5, "#c02828"], ["pix", 214, 21, "#444444"],
        ["repeat", 4, 0, 4, [["rect", 208, 30, 14, 1, "#b0a898"]]], ["rect", 216, 33, 3, 3, "#c02828"],
        ["rect", 228, 40, 28, 2, "#6a4a28"], ["rect", 228, 40, 28, 1, "#8a6a40"],
        ["rect", 230, 32, 5, 8, "#c8a040"], ["rect", 230, 31, 5, 1, "#e0e0e0"], ["rect", 237, 34, 4, 6, "#4a8a4a"], ["rect", 237, 33, 4, 1, "#e0e0e0"],
        ["rect", 243, 30, 6, 10, "#a04040"], ["rect", 243, 29, 6, 1, "#e0e0e0"], ["rect", 251, 33, 4, 7, "#d0d0e8"], ["rect", 251, 32, 4, 1, "#e0e0e0"],
        ["rect", 258, 24, 44, 3, "#6a4a28"], ["rect", 260, 27, 40, 63, "#2a1a10"],
        ["line", 200, 0, 200, 28, "#1a1a1a"], ["poly", [[192, 36], [208, 36], [204, 29], [196, 29]], "#2a6a4a"],
        ["rect", 191, 36, 18, 1, "#1a4a34"], ["rect", 196, 29, 8, 1, "#3a8a64"], ["rect", 197, 37, 6, 2, "#fff4c0"],
        ["rect", 0, 0, 2, 144, "#120804"], ["rect", 318, 0, 2, 144, "#120804"]
    ],
    "objects": [
        {"id": "puerta_cocina_hall", "name": "PUERTA", "box": [8, 26, 38, 64], "walkTo": [26, 106], "face": "back",
         "verbs": {"MIRAR": "Vuelve al vestíbulo.", "IR A": {"goto": "vestibulo", "entry": "cocina"}}},
        {"id": "nevera", "name": "NEVERA", "box": [46, 36, 36, 60], "walkTo": [64, 106], "face": "back", "state": "cerrada",
         "draw": [
             ["rect", 50, 37, 28, 2, "#a8d8c8"], ["rect", 48, 39, 32, 57, "#a8d8c8"], ["rect", 48, 39, 3, 57, "#c8f0e0"],
             ["rect", 77, 39, 3, 57, "#78a898"], ["rect", 48, 62, 32, 1, "#78a898"],
             ["rect", 58, 43, 12, 3, "#c8c8d0"], ["rect", 58, 43, 12, 1, "#f0f0f8"],
             ["rect", 74, 46, 2, 10, "#e8e8f0"], ["rect", 74, 66, 2, 14, "#e8e8f0"], ["rect", 75, 46, 1, 10, "#a8a8b0"],
             ["rect", 50, 96, 4, 2, "#333333"], ["rect", 74, 96, 4, 2, "#333333"]],
         "states": {
             "cerrada": {},
             "abierta": {"draw": [
                 ["rect", 50, 64, 28, 31, "#f4f8f0"], ["rect", 50, 74, 28, 1, "#b8c8c8"], ["rect", 50, 84, 28, 1, "#b8c8c8"],
                 ["rect", 54, 76, 4, 8, "#ffffff"], ["rect", 54, 76, 4, 1, "#3a6ac8"], ["rect", 66, 78, 5, 6, "#d0a030"],
                 ["poly", [[58, 92], [68, 92], [68, 86]], "#f0d040"], ["rect", 71, 88, 4, 4, "#c04040"],
                 ["rect", 40, 63, 8, 34, "#a8d8c8"], ["rect", 40, 63, 1, 34, "#c8f0e0"], ["rect", 41, 70, 6, 1, "#78a898"],
                 ["light", 64, 78, 42, "200,240,255", 0.35]]}
         },
         "verbs": {
             "MIRAR": {"if": "state:nevera=cerrada", "then": "Una nevera de los años 50. Zumba como un avión.", "else": "Leche, queso... lo típico."},
             "ABRIR": {"if": "state:nevera=abierta", "then": "Ya está abierta.",
                       "else": [{"state": ["nevera", "abierta"]}, {"if": "!has:salchichas && !salchichas_usadas", "then": "¡Brrr! Hay unas salchichas.", "else": "¡Brrr!"}]},
             "CERRAR": {"if": "state:nevera=cerrada", "then": "Ya está cerrada.", "else": {"state": ["nevera", "cerrada"]}},
             "COGER": "No me cabe en el bolsillo."
         }},
        {"id": "salchichas_nevera", "name": "SALCHICHAS", "when": "state:nevera=abierta", "box": [53, 64, 24, 9],
         "walkTo": [64, 106], "face": "back",
         "draw": [["rect", 55, 69, 4, 3, "#c06050"], ["rect", 60, 69, 4, 3, "#c06050"], ["rect", 65, 69, 4, 3, "#c06050"], ["rect", 70, 69, 4, 3, "#c06050"],
                  ["rect", 55, 69, 19, 1, "#e08070"], ["pix", 59, 70, "#e0d0b0"], ["pix", 64, 70, "#e0d0b0"], ["pix", 69, 70, "#e0d0b0"]],
         "verbs": {"MIRAR": "Salchichas de Frankfurt. Irresistibles.",
                   "COGER": [{"hide": "salchichas_nevera"}, {"pickup": "salchichas"}, "¡Me las llevo! Nunca se sabe cuándo harán falta unas salchichas."]}},
        {"id": "fogon", "name": "COCINA DE GAS", "box": [86, 44, 42, 52], "walkTo": [106, 106], "face": "back",
         "draw": [
             ["rect", 88, 60, 38, 36, "#e8dcc0"], ["rect", 88, 60, 38, 1, "#fff4dc"], ["rect", 124, 60, 2, 36, "#b8ac90"],
             ["rect", 88, 57, 38, 3, "#2a2a2a"], ["rect", 92, 56, 10, 1, "#111111"], ["rect", 112, 56, 10, 1, "#111111"],
             ["repeat", 4, 7, 0, [["rect", 94, 63, 3, 2, "#3a3a3a"]]],
             ["rect", 92, 70, 30, 20, "#d8ccb0"], ["rect", 96, 74, 22, 10, "#2a2018"],
             ["glow", 96, 74, 22, 10, "255,140,40", 0.2, 0.08, 4], ["rect", 94, 68, 26, 1, "#b0b0b8"],
             ["rect", 90, 96, 4, 2, "#333333"], ["rect", 120, 96, 4, 2, "#333333"],
             ["rect", 98, 47, 16, 9, "#8a8a94"], ["rect", 97, 47, 18, 1, "#b0b0b8"], ["rect", 96, 49, 2, 2, "#6a6a74"],
             ["rect", 114, 49, 2, 2, "#6a6a74"], ["rect", 105, 45, 2, 2, "#3a3a40"], ["rect", 99, 48, 2, 7, "#a8a8b4"],
             ["flame", 99, 57, 12], ["steam", 106, 44, 26]],
         "verbs": {"MIRAR": "Un puchero hierve a fuego lento. Huele a... ¿calcetín?", "ABRIR": "El horno está vacío. Y sucio.",
                   "APAGAR": "Mejor no toco nada. No es mi casa.", "COGER": "Quema.", "USAR": "No tengo hambre. Bueno, un poco."}},
        {"id": "fregadero", "name": "FREGADERO", "box": [132, 60, 68, 36], "walkTo": [168, 106], "face": "back",
         "draw": [
             ["rect", 132, 74, 68, 22, "#8a5a34"], ["rect", 132, 72, 68, 3, "#c8c0b0"], ["rect", 132, 72, 68, 1, "#e8e0d0"],
             ["rect", 136, 79, 28, 15, "#7a4a28"], ["rect", 168, 79, 28, 15, "#7a4a28"], ["rect", 136, 79, 28, 1, "#9a6a40"], ["rect", 168, 79, 28, 1, "#9a6a40"],
             ["rect", 161, 85, 2, 3, "#c8a040"], ["rect", 170, 85, 2, 3, "#c8a040"],
             ["rect", 150, 72, 36, 2, "#8a9098"], ["rect", 166, 62, 2, 10, "#c8c8d0"], ["rect", 166, 62, 8, 2, "#c8c8d0"],
             ["rect", 172, 64, 2, 3, "#c8c8d0"], ["pix", 166, 62, "#ffffff"], ["drip", 173, 67, 5, 1.7],
             ["rect", 139, 67, 9, 5, "#f0f0f0"], ["rect", 139, 67, 9, 1, "#ffffff"], ["rect", 140, 65, 7, 2, "#e0e8f0"]],
         "verbs": {"MIRAR": "Un grifo que gotea. Plic. Plic. Plic.", "USAR": "Me lavo las manos. Así da gusto.",
                   "CERRAR": "Está cerrado. Gotea igual.", "ABRIR": "No tengo sed."}},
        {"id": "ventana_cocina", "name": "VENTANA", "box": [144, 16, 50, 40], "walkTo": [168, 106], "face": "back",
         "verbs": {"MIRAR": "Da al patio trasero. Veo una caseta de perro ahí fuera.", "ABRIR": "Está atascada. Como todo en esta casa."}},
        {"id": "calendario", "name": "CALENDARIO", "box": [206, 21, 18, 25], "walkTo": [215, 106], "face": "back",
         "verbs": {"MIRAR": "Un calendario de 1987. Alguien marcó hoy: BAÑO DE FIRULAIS.", "LEER": "Un calendario de 1987. Alguien marcó hoy: BAÑO DE FIRULAIS.",
                   "COGER": "No me sirve. Estamos en otro año. Creo."}},
        {"id": "puerta_trasera", "name": "PUERTA DEL PATIO", "box": [258, 24, 44, 66], "walkTo": [280, 106], "face": "back", "state": "cerrada",
         "states": {
             "cerrada": {"draw": [
                 ["rect", 262, 29, 36, 61, "#7a4a28"], ["rect", 262, 29, 36, 1, "#9a6a40"],
                 ["rect", 268, 34, 24, 18, "#10182e"], ["rect", 279, 34, 2, 18, "#7a4a28"], ["rect", 268, 42, 24, 2, "#7a4a28"],
                 ["pix", 286, 37, "#f4f0d8"], ["pix", 271, 36, "#8890c0"],
                 ["rect", 267, 58, 26, 26, "#6a3e20"], ["rect", 267, 58, 26, 1, "#9a6a40"],
                 ["rect", 290, 60, 3, 3, "#e0c040"], ["rect", 290, 66, 3, 4, "#8a8a92"], ["pix", 291, 67, "#000000"]]},
             "abierta": {"draw": [
                 ["grad", 262, 29, 36, 44, ["#0b1030", "#26306a", "#4a3a78"]], ["pix", 286, 36, "#f4f0d8"], ["pix", 270, 40, "#ffffff"],
                 ["rect", 262, 64, 36, 9, "#10132e"], ["rect", 262, 73, 36, 17, "#1e3a24"],
                 ["rect", 262, 29, 5, 61, "#7a4a28"], ["rect", 266, 29, 1, 61, "#4a2a14"]]}
         },
         "verbs": {
             "MIRAR": {"if": "state:puerta_trasera=cerrada", "then": "La puerta del patio trasero. Cerrada con llave.", "else": "Da al patio. Hace fresquito."},
             "ABRIR": {"if": "state:puerta_trasera=abierta", "then": "Ya está abierta.",
                       "else": {"if": "has:llave_patio", "then": "Cerrada con llave. ¡Pero tengo una llave que pone PATIO!", "else": "Cerrada con llave. Necesito la llave del patio."}},
             "USAR:llave_patio": [{"say": "Veamos..."}, {"state": ["puerta_trasera", "abierta"]}, {"drop": "llave_patio"}, "¡Clic! Abierta."],
             "USAR:llave_porton": "Esta es demasiado grande.",
             "CERRAR": {"if": "state:puerta_trasera=abierta", "then": "Mejor la dejo abierta, por si acaso.", "else": "Ya está cerrada."},
             "IR A": {"if": "state:puerta_trasera=abierta", "then": {"goto": "patio", "entry": "cocina"}, "else": "Está cerrada con llave."}
         }},
        {"id": "lampara_cocina", "name": "LÁMPARA", "box": [190, 26, 20, 14], "walkTo": [200, 136], "noWalk": True,
         "verbs": {"MIRAR": "Una lámpara de cocina. Zumba como un mosquito.", "APAGAR": "Prefiero ver dónde piso."}},
        {"id": "mesa_cocina", "name": "MESA", "box": [164, 100, 74, 32], "obstacle": [170, 118, 232, 130], "z": 130,
         "walkTo": [200, 137], "face": "back",
         "draw": [
             ["rect", 166, 100, 3, 30, "#6a4428"], ["rect", 166, 100, 3, 1, "#8a6040"], ["rect", 166, 116, 12, 3, "#7a5030"], ["rect", 175, 119, 2, 11, "#5a3a20"],
             ["rect", 233, 100, 3, 30, "#6a4428"], ["rect", 233, 100, 3, 1, "#8a6040"], ["rect", 224, 116, 12, 3, "#7a5030"], ["rect", 225, 119, 2, 11, "#5a3a20"],
             ["tiles", 174, 110, 54, 6, 3, 3, "#e04848", "#f4f0f0", "#e87070"],
             ["tiles", 172, 116, 58, 5, 3, 3, "#c83838", "#e0dcdc", "#d86060"],
             ["rect", 176, 121, 3, 10, "#5a3a20"], ["rect", 223, 121, 3, 10, "#5a3a20"],
             ["rect", 186, 106, 5, 5, "#f0f0f0"], ["rect", 191, 107, 1, 2, "#f0f0f0"], ["rect", 186, 106, 5, 1, "#6a3a1a"],
             ["ellipse", 214, 109, 6, 2, "#e8e0d0"], ["rect", 211, 106, 6, 3, "#c89050"]]},
        {"id": "periodico", "name": "PERIÓDICO", "box": [196, 104, 12, 8], "z": 130.5, "walkTo": [200, 137], "face": "back",
         "draw": [["rect", 197, 107, 10, 3, "#d8d4c8"], ["rect", 197, 107, 10, 1, "#f0ece0"], ["rect", 198, 108, 4, 1, "#6a6a6a"]],
         "verbs": {"MIRAR": {"run": "periodico"}, "LEER": {"run": "periodico"}, "COGER": "No me hace falta. Ya me sé el titular."}}
    ]
}
g['scripts']['periodico'] = ["Titular: EL MAYORDOMO GANA EL CONCURSO MÍSTER BAÑADOR 1987.", "Eso explica la foto."]
R['cocina'] = cocina

# ---------------------------------------------------------------- PATIO
stones = []
for x, y in [(80, 106), (98, 112), (120, 117), (146, 121), (174, 124), (206, 125), (240, 126), (274, 126), (306, 125)]:
    stones += [["ellipse", x, y, 7, 3, "#4a4c58"], ["ellipse", x, y - 1, 6, 2, "#6a6c78"], ["pix", x - 3, y - 2, "#8a8c98"]]

patio = {
    "name": "Patio",
    "width": 480,
    "walk": [8, 104, 472, 141],
    "ambient": "#7482c0",
    "vignette": 0.5,
    "lights": [
        {"x": 107, "y": 40, "r": 72, "color": "255,190,110", "a": 0.45, "flicker": 0.07},
        {"x": 32, "y": 46, "r": 56, "color": "255,200,120", "a": 0.32},
        {"x": 77, "y": 90, "r": 44, "color": "255,190,110", "a": 0.25},
        {"x": 410, "y": 24, "r": 46, "color": "170,190,255", "a": 0.18},
        {"x": 395, "y": 118, "r": 80, "color": "150,170,255", "a": 0.22},
        {"x": 150, "y": 126, "r": 60, "color": "150,170,255", "a": 0.16}
    ],
    "entries": {"cocina": {"x": 78, "y": 112, "face": "front"}},
    "onEnter": [{"once": "patio_primera", "do": ["El patio trasero. Qué noche tan bonita...", "...y qué ronquidos tan raros salen de esa caseta."]}],
    "zones": [{"id": "perro_guarda", "rect": [328, 0, 480, 144], "if": "!perro_distraido", "onEnter": {"run": "perro_ladra"}}],
    "background": [
        ["grad", 0, 0, 480, 92, ["#070b22", "#101a44", "#1f2a62", "#3a3474", "#5e4478"]],
        ["stars", 0, 0, 480, 64, 70, 21],
        ["moon", 410, 24, 9],
        ["clouds", 0, 4, 480, 36, 6, "#1c2454", "#34407a", 2.5, 5],
        ["hills", 0, 58, 480, 34, "#161a40", 7, 0],
        ["hills", 0, 70, 480, 24, "#0c1030", 9, 4],
        ["repeat", 42, 8, 0, [["rect", 150, 70, 5, 24, "#4a3e36"], ["rect", 150, 70, 5, 1, "#6a5e56"], ["pix", 152, 69, "#4a3e36"], ["rect", 154, 70, 1, 24, "#342a24"]]],
        ["rect", 148, 76, 332, 2, "#3a2e26"], ["rect", 148, 88, 332, 2, "#3a2e26"],
        ["grad", 0, 88, 480, 56, ["#16301e", "#224226", "#2e5430"]],
        ["speckle", 0, 90, 480, 54, "#3e6a34", 0.07, 4], ["speckle", 0, 90, 480, 54, "#10261a", 0.08, 5],
        ["grass", 0, 92, 480, 52, ["#3a6030", "#4a7a38", "#284a24", "#5a8a40"], 320, 8],
        *stones,
        ["tree", 250, 98, 86, "#2a1e18", ["#0e2618", "#183a22", "#26522e"], 3],
        ["swing", 272, 46, 42, 0.12, 3.4, "#9a8a64", "#18181c", 6],
        ["bricks", 0, 0, 140, 96, "#4a3030", "#2a1a1a", 12, 5],
        ["speckle", 0, 0, 140, 96, "#5a3a38", 0.04, 12],
        ["rect", 0, 90, 140, 7, "#3a3a3e"], ["rect", 0, 90, 140, 1, "#5a5a60"], ["rect", 136, 0, 4, 97, "#1a1010"],
        ["rect", 14, 28, 36, 32, "#2a1a1a"], ["rect", 16, 30, 32, 28, "#f0c870"], ["rect", 16, 30, 7, 28, "#c89040"],
        ["rect", 41, 30, 7, 28, "#c89040"], ["rect", 31, 30, 2, 28, "#6a4020"], ["rect", 16, 43, 32, 2, "#6a4020"],
        ["rect", 12, 58, 40, 3, "#5a5a60"],
        ["rect", 104, 34, 6, 8, "#2a2a2a"], ["rect", 105, 36, 4, 5, "#ffe8a0"], ["rect", 103, 33, 8, 1, "#1a1a1a"],
        ["line", 107, 26, 107, 33, "#1a1a1a"], ["rect", 104, 26, 8, 1, "#1a1a1a"], ["moths", 107, 38, 11, 3],
        ["fireflies", 150, 64, 320, 56, 10],
        ["rect", 0, 0, 2, 144, "#05060c"], ["rect", 478, 0, 2, 144, "#05060c"]
    ],
    "objects": [
        {"id": "puerta_patio", "name": "PUERTA DE LA COCINA", "box": [58, 38, 38, 58], "walkTo": [77, 107], "face": "back",
         "draw": [["rect", 58, 38, 38, 58, "#2a1a10"], ["rect", 62, 42, 30, 54, "#e0b060"],
                  ["tiles", 62, 46, 30, 26, 6, 5, "#e8d0a0", "#dcc494", "#b89a70"], ["rect", 62, 72, 30, 24, "#a8563a"],
                  ["rect", 62, 42, 30, 4, "#6a5a3a"], ["rect", 62, 42, 6, 54, "#5a3a20"], ["rect", 67, 42, 1, 54, "#3a2410"],
                  ["rect", 56, 96, 42, 3, "#5a5a60"]],
         "verbs": {"MIRAR": "Vuelve a la cocina.", "IR A": {"goto": "cocina", "entry": "patio"}}},
        {"id": "farol", "name": "FAROL", "box": [100, 24, 14, 20], "noWalk": True,
         "verbs": {"MIRAR": "Un farol lleno de polillas. Fiesta de polillas.", "COGER": "Está atornillado a la pared."}},
        {"id": "arbol", "name": "ÁRBOL", "box": [216, 10, 70, 86], "walkTo": [250, 106], "face": "back",
         "verbs": {"MIRAR": "Un roble enorme. Tiene un columpio hecho con un neumático.", "HABLAR": "Hola, árbol. ... Tampoco habla.",
                   "COGER": "Claro. Me lo meto en el bolsillo con la mesa de billar."}},
        {"id": "columpio", "name": "COLUMPIO", "box": [262, 76, 22, 20], "walkTo": [272, 108], "face": "back",
         "verbs": {"MIRAR": "Un columpio de neumático. Se mueve solo. Brrr.", "USAR": "No es momento de columpiarse. Aunque apetece."}},
        {"id": "carretilla", "name": "CARRETILLA", "box": [176, 108, 32, 20], "obstacle": [180, 122, 206, 128], "z": 128,
         "walkTo": [192, 134], "face": "back",
         "draw": [["poly", [[178, 112], [206, 112], [202, 122], [182, 122]], "#6a7078"], ["rect", 178, 112, 28, 1, "#9aa0a8"],
                  ["speckle", 180, 110, 24, 3, "#8a6a2a", 0.5, 3], ["speckle", 180, 110, 24, 3, "#6a8a3a", 0.4, 4],
                  ["line", 206, 116, 214, 112, "#6a4a2a"], ["line", 206, 118, 214, 114, "#6a4a2a"],
                  ["ring", 186, 124, 4, "#1a1a1a", 2], ["rect", 196, 122, 2, 5, "#4a4a50"]],
         "verbs": {"MIRAR": "Una carretilla oxidada llena de hojas.", "EMPUJAR": "Tiene la rueda pinchada. Como todo aquí.", "COGER": "No me cabe en el bolsillo."}},
        {"id": "caseta", "name": "CASETA", "box": [366, 72, 68, 52], "obstacle": [374, 112, 426, 124], "z": 124,
         "walkTo": [318, 126], "face": "right",
         "draw": [
             ["rect", 372, 92, 56, 32, "#9a6a3a"], ["repeat", 9, 6, 0, [["rect", 374, 92, 1, 32, "#7a5028"]]],
             ["rect", 424, 92, 4, 32, "#6a4020"], ["rect", 372, 122, 56, 2, "#4a2c14"],
             ["poly", [[364, 93], [400, 71], [436, 93]], "#8a2a24"], ["line", 364, 93, 400, 71, "#b84a3a"], ["line", 400, 71, 436, 93, "#5a1a14"],
             ["repeat", 3, 0, 6, [["line", 376, 88, 424, 88, "#6a1e1a"]]],
             ["rect", 388, 104, 20, 20, "#0a0806"], ["rect", 390, 102, 16, 2, "#0a0806"], ["rect", 392, 101, 12, 1, "#0a0806"],
             ["rect", 374, 93, 52, 9, "#d8c090"], ["rect", 374, 93, 52, 1, "#f0dcb0"], ["text", 377, 94, "FIRULAIS", "#5a3014"],
             ["line", 408, 116, 416, 126, "#8a8a92"], ["line", 416, 126, 424, 124, "#8a8a92"]],
         "verbs": {
             "MIRAR": {"if": "perro_distraido", "then": "La caseta de Firulais. Ahora está vacía.", "else": "La caseta de un perro. Pone FIRULAIS. Se oyen ronquidos."},
             "USAR:salchichas": {"run": "distraer_perro"}, "DAR:salchichas": {"run": "distraer_perro"},
             "ABRIR": "Es una caseta. No tiene puerta.", "COGER": "¿Con el perro dentro? ¿Estás loco?"}},
        {"id": "cuenco", "name": "CUENCO", "box": [432, 122, 18, 8], "z": 130, "walkTo": [420, 134], "face": "right",
         "draw": [["ellipse", 441, 127, 7, 2, "#a02020"], ["ellipse", 441, 126, 5, 1, "#3a1010"], ["rect", 434, 127, 15, 1, "#c84040"]],
         "verbs": {"MIRAR": "El cuenco de Firulais. Vacío.", "USAR:salchichas": {"run": "distraer_perro"}, "COGER": "Tiene babas. Paso."}},
        {"id": "llave_clavo", "name": "LLAVE GRANDE", "box": [448, 60, 16, 22], "walkTo": [452, 110], "face": "back",
         "draw": [["rect", 452, 62, 6, 34, "#4a3a2a"], ["rect", 452, 62, 6, 1, "#6a5a4a"], ["rect", 457, 62, 1, 34, "#2a2018"],
                  ["pix", 455, 66, "#9a9aa0"],
                  ["pixels", 452, 67, [".XXX.", "X...X", "X...X", ".XXX.", "..X..", "..X..", "..XX.", "..X..", "..XX."], {"X": "#e0c040"}]],
         "verbs": {"MIRAR": "¡Una llave grande colgada de la valla! Justo al lado del perro, cómo no.",
                   "COGER": [{"hide": "llave_clavo"}, {"pickup": "llave_porton"}, "¡La llave del portón! ¡Por fin!", {"face": "left"}, "Adiós, Firulais. Gracias por nada."]}},
        {"id": "perro", "name": "PERRO", "x": 398, "y": 122, "state": "dentro", "textColor": "#ffb070",
         "box": [-14, -14, 28, 16], "obstacle": [-11, -3, 11, 1], "walkTo": [-80, 2], "face": "right",
         "states": {
             "dentro": {"box": [-10, -18, 20, 18], "obstacle": None, "z": 3, "draw": [
                 ["pixels", -7, -7, ["...DDBB.", ".kLLBBBD", "..LLLBB."], {"B": "#b87a3e", "L": "#f0c888", "D": "#6a4020", "k": "#111111"}],
                 ["frames", 1.6, [[["pixels", 3, -16, ZZZ, {"X": "#b8c4ff"}]], [["pixels", 6, -22, ZZZ, {"X": "#b8c4ff"}]], [["pixels", 9, -28, ZZZ, {"X": "#b8c4ff"}]], []]]]},
             "quieto": {"draw": [["sprite", "perro", "quieto", -11, -12]]},
             "ladra": {"draw": [["sprite", "perro", "ladra", -11, -12]]},
             "corre": {"obstacle": None, "draw": [["sprite", "perro", "corre", -11, -12]]},
             "come": {"walkTo": [30, 2], "face": "left", "draw": [["sprite", "perro", "come", -11, -12]]},
             "duerme": {"walkTo": [30, 2], "face": "left", "draw": [["sprite", "perro", "duerme", -11, -12],
                 ["frames", 1.6, [[["pixels", -8, -12, ZZZ, {"X": "#b8c4ff"}]], [["pixels", -10, -18, ZZZ, {"X": "#b8c4ff"}]], [["pixels", -12, -24, ZZZ, {"X": "#b8c4ff"}]], []]]]}
         },
         "verbs": {
             "MIRAR": {"if": "state:perro=dentro", "then": "Asoma un hocico por la caseta. Está roncando.",
                       "else": {"if": "state:perro=come", "then": "Firulais está entretenido con las salchichas.",
                                "else": {"if": "state:perro=duerme", "then": "Se ha quedado frito. Qué buena vida.", "else": "Un perro con cara de pocos amigos."}}},
             "HABLAR": {"if": "perro_distraido", "then": ["Buen chico, Firulais.", {"say": "¡Guau!", "who": "perro"}],
                        "else": ["¿Quién es un perrito bueno?", {"say": "¡GRRRRR!", "who": "perro"}, "Vale, tú no."]},
             "COGER": "Ni loco. Tiene más dientes que yo.",
             "EMPUJAR": "Prefiero conservar la mano.",
             "USAR:salchichas": {"run": "distraer_perro"}, "DAR:salchichas": {"run": "distraer_perro"},
             "DAR:foto": "No creo que al perro le interese el mayordomo en bañador.",
             "USAR:taco": "¿Pegar al perro? ¡Ni hablar! Pobre animal."
         }},
        {"id": "salchicha_lanzada", "hidden": True, "hotspot": False, "z": 200,
         "draw": [["rect", -4, -1, 3, 2, "#c06050"], ["rect", 0, -1, 3, 2, "#c06050"], ["rect", 4, -1, 3, 2, "#c06050"], ["rect", -4, -1, 11, 1, "#e08070"]]}
    ]
}
R['patio'] = patio

g['scripts']['perro_ladra'] = [
    {"stop": "perro_vuelve"},
    {"if": "!perro_fuera", "then": [
        {"set": "perro_fuera"}, {"state": ["perro", "corre"]}, {"moveTo": ["perro", 382, 128, 0.35]}]},
    {"state": ["perro", "ladra"]},
    {"face": "right"},
    {"say": "¡GUAU! ¡GUAU! ¡GRRRR!", "who": "perro"},
    "¡Uaaah!",
    {"walk": [296, 128], "speed": 95, "face": "right"},
    {"state": ["perro", "quieto"]},
    {"once": "pista_perro", "do": ["Ese chucho no me va a dejar acercarme a la valla.", "Tendré que distraerlo con algo."],
     "else": {"random": ["Vale, vale... Perrito bonito.", "No insisto, no insisto.", "Necesito algo que le guste más que yo."]}},
    {"async": [{"wait": 3}, {"state": ["perro", "corre"]}, {"moveTo": ["perro", 398, 122, 0.5]},
               {"state": ["perro", "dentro"]}, {"unset": "perro_fuera"}], "name": "perro_vuelve"}
]
g['scripts']['distraer_perro'] = [
    {"stop": "perro_vuelve"},
    {"face": "right"},
    "¡Eh, Firulais! ¡Mira lo que tengo!",
    {"drop": "salchichas"}, {"set": "salchichas_usadas"},
    {"placeAt": ["salchicha_lanzada", "player", 0, -22]}, {"show": "salchicha_lanzada"},
    {"face": "left"},
    {"path": ["salchicha_lanzada", [[124, 133]], 170], "arc": 36},
    {"if": "!perro_fuera", "then": [{"set": "perro_fuera"}, {"state": ["perro", "corre"]}, {"moveTo": ["perro", 382, 128, 0.35]}]},
    {"set": "perro_distraido"},
    {"state": ["perro", "ladra"]},
    {"say": "¡GUAU!", "who": "perro"},
    {"state": ["perro", "corre"]},
    {"path": ["perro", [[344, 139], [260, 139], [150, 137], [140, 135]], 125]},
    {"state": ["perro", "come"]},
    {"face": "left"},
    "¡Funciona! Ahora puedo acercarme a la valla.",
    {"async": [{"wait": 9}, {"hide": "salchicha_lanzada"}, {"state": ["perro", "duerme"]}], "name": "perro_siesta"}
]

# ---------------------------------------------------------------- guardar con formato legible
def fmt(v, ind=0):
    sp = '  ' * ind
    one = json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        if len(one) <= 150 or all(not isinstance(x, (dict, list)) for x in v) or (all(isinstance(x, list) for x in v) and all(len(json.dumps(x, ensure_ascii=False)) <= 150 and not any(isinstance(y, dict) for y in x) for x in v) and False):
            if len(one) <= 150: return one
        if all(isinstance(x, list) and not any(isinstance(y, (dict,)) for y in x) and len(json.dumps(x, ensure_ascii=False)) <= 150 for x in v):
            return '[\n' + ',\n'.join(sp + '  ' + json.dumps(x, ensure_ascii=False) for x in v) + '\n' + sp + ']'
        return '[\n' + ',\n'.join(sp + '  ' + fmt(x, ind + 1) for x in v) + '\n' + sp + ']'
    if isinstance(v, dict):
        if len(one) <= 110: return one
        return '{\n' + ',\n'.join(sp + '  ' + json.dumps(k, ensure_ascii=False) + ': ' + fmt(x, ind + 1) for k, x in v.items()) + '\n' + sp + '}'
    return one

order = ["title", "palette", "verbs", "defaultVerb", "lookVerb", "rightClickVerb", "defaults", "player", "start", "intro",
         "items", "scripts", "sprites", "prefabs", "rooms"]
g = {k: g[k] for k in order if k in g} | {k: v for k, v in g.items() if k not in order}
g['rooms'] = {k: g['rooms'][k] for k in ['salon', 'vestibulo', 'cocina', 'patio', 'sotano']}
out = fmt(g) + '\n'
json.loads(out)
open('../aventura.json', 'w').write(out)
print('ok', len(out))
