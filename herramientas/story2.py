# Añade la planta de arriba (pasillo) y la biblioteca (Sokoban) y rehace la historia.
# Orden de generación: gen.py -> audio.py -> story2.py -> build.py
import json, importlib.util

g = json.load(open('../aventura.json'))
R = g['rooms']
OBJ = {o['id']: o for r in R.values() for o in r['objects']}
def S(name, **kw): return {"sound": name, **kw}
def who(txt, w): return {"say": txt, "who": w}

# ------------------------------------------------------------------ verbos: PONER -> GOLPEAR
for v in g['verbs']:
    if v['id'] == 'PONER': v['id'] = v['label'] = 'GOLPEAR'
g['defaults'].pop('PONER', None)
g['defaults']['GOLPEAR'] = ["¡Toc, toc! No pasa nada.", "Golpear cosas no soluciona nada. Casi nunca."]
OBJ['alfombra_mesa']['verbs'].pop('PONER', None)
g['unreachable'] = "No puedo llegar hasta ahí. Algo me corta el paso."
g['pushVerb'] = "EMPUJAR"

# ------------------------------------------------------------------ historia
g['intro'] = [
    {"card": "LA MANSIÓN DEL DOCTOR CHIFLADO", "time": 3},
    "Me llamo Tito. Me colé en esta mansión por una apuesta...",
    "...y la puerta principal se cerró sola detrás de mí.",
    "Qué raro que no haya nadie. Tengo que encontrar la forma de salir."
]
g['scripts']['leer_nota'] = [
    S("papel"), "Es una nota del mayordomo:",
    "La llave del patio la colgué de la viga del sótano. Al sótano se baja por debajo del billar. Quiten el freno.",
    "La llave del portón la lleva Firulais en el collar. Sin comida no deja ni acercarse...",
    "...y aun comiendo, solo obedece a su silbato. Lo guardé en la biblioteca, sección...",
    "Aquí hay una mancha de café. No se lee nada más.",
    "P.D.: Esta noche no me molesten, estaré ARRIBA ensayando para la gala.",
    {"set": "sabe_silbato"}
]
g['items']['silbato'] = {"name": "SILBATO", "desc": "Un silbato para perros con una placa: FIRULAIS. Suena tan agudo que yo no lo oigo.",
                         "verbs": {"USAR": {"run": "usar_silbato"}, "USAR:perro": {"run": "usar_silbato"}, "USAR:collar": {"run": "usar_silbato"}}}

# ------------------------------------------------------------------ patio: la llave va en el collar del perro
patio = R['patio']
patio['objects'] = [o for o in patio['objects'] if o['id'] != 'llave_clavo']
OBJ.pop('llave_clavo', None)
perro = OBJ['perro']
sentado_rows = [
    ["...BBBB...............", "..BBBBBDD..............", ".BwkBBDDD..............", "kLLBBBDDD..............", "LLLLBBBDr..............",
     ".tLLBBrrBB.............", "....BBrBBBB............", "....BBBBBBBB...........", "....BLBBBBBBB..........", "....BL.BBBBBBB..BB.....",
     "....BL..BBBBBBBB.......", "....DD..DDDDDDD........"],
    ["...BBBB...............", "..BBBBBDD..............", ".BwkBBDDD..............", "kLLBBBDDD..............", "LLLLBBBDr..............",
     ".tLLBBrrBB.............", "....BBrBBBB............", "....BBBBBBBB...........", "....BLBBBBBBB..........", "....BL.BBBBBBB.........",
     "....BL..BBBBBBBBBB.....", "....DD..DDDDDDD........"]]
g['sprites']['perro']['anims']['sentado'] = {"fps": 4, "frames": sentado_rows}
perro['states']['sentado'] = {"walkTo": [30, 2], "face": "left", "draw": [["sprite", "perro", "sentado", -11, -12]]}
perro['verbs']['COGER'] = {"run": "coger_llave_collar"}
perro['verbs']['USAR:silbato'] = {"run": "usar_silbato"}
perro['verbs']['MIRAR'] = {"if": "state:perro=dentro", "then": "Asoma un hocico por la caseta. Está roncando.",
    "else": {"if": "state:perro=come", "then": "Firulais está entretenido con las salchichas. Y lleva la llave en el collar.",
    "else": {"if": "state:perro=duerme", "then": "Se ha quedado frito. Qué buena vida.",
    "else": {"if": "state:perro=sentado", "then": "Sentado, formal y moviendo el rabo. Quién lo diría.",
             "else": "Un perro con cara de pocos amigos. ¡Lleva una llave colgada del collar!"}}}}
patio['objects'].append({
    "id": "collar", "name": "LLAVE DEL COLLAR", "parent": "perro", "x": 398, "y": 122, "z": 0.6,
    "when": "perro_fuera && !llave_cogida", "box": [-9, -12, 10, 11], "walkTo": [30, 2], "face": "left",
    "draw": [["pixels", -5, -6, ["y.", "yy", "y.", "yy"], {"y": "#f0d040"}], ["blink", 2.2, 0.12, [["pix", -5, -6, "#ffffff"]]]],
    "verbs": {"MIRAR": "¡La llave del portón! Firulais la lleva colgada del collar.",
              "COGER": {"run": "coger_llave_collar"}, "QUITAR": {"run": "coger_llave_collar"}, "TIRAR": {"run": "coger_llave_collar"}}})
g['scripts']['coger_llave_collar'] = [
    {"if": "perro_obediente",
     "then": [S("tintineo"), "Con permiso, Firulais...", {"set": "llave_cogida"}, {"pickup": "llave_porton"},
              S("ladrido", at="perro", vol=0.5), who("¡Guau!", "perro"), "¡La llave del portón! ¡Por fin!"],
     "else": {"if": "state:perro=come",
              "then": [S("grunido", at="perro"), who("¡GRRRRR!", "perro"), "Vale, vale. No se toca a Firulais mientras come.",
                       {"once": "pista_silbato", "do": {"if": "sabe_silbato", "then": "Necesito que me obedezca. Necesito su silbato.",
                                                         "else": "Necesito que me obedezca de alguna manera."}}],
              "else": {"if": "state:perro=duerme", "then": "Si lo despierto de golpe, me muerde. Mejor con buenos modales.",
                       "else": "Ni de broma, con esos dientes."}}}
]
g['scripts']['usar_silbato'] = [
    {"if": "!room:patio",
     "then": [S("silbato_perro"), "¡FIIIIU!", "No pasa nada. Aquí no hay ningún perro. Ni yo oigo el silbato."],
     "else": [S("silbato_perro"), "¡FIIIIIU!",
        {"if": "!perro_distraido",
         "then": [S("ladrido", at="perro"), who("¡GUAU! ¡GRRR!", "perro"), "No me hace ni caso. Está demasiado nervioso.", "Quizá con el estómago lleno..."],
         "else": {"if": "state:perro=sentado", "then": "Ya está sentado. Buen chico.",
                  "else": [{"stop": "perro_siesta"}, {"hide": "salchicha_lanzada"}, {"state": ["perro", "sentado"]},
                           S("ladrido", at="perro", vol=0.5), who("¡Guau!", "perro"), {"set": "perro_obediente"},
                           "¡Se ha sentado como un señor! Ahora sí podré cogerle la llave del collar."]}}]}
]
pl = g['scripts']['perro_ladra']
for i, c in enumerate(pl):
    if isinstance(c, dict) and c.get('once') == 'pista_perro':
        c['do'] = ["Ese chucho no me deja acercarme.", "¡Y lleva una llave colgada del collar!", "Tendré que distraerlo con algo."]
dp = g['scripts']['distraer_perro']
dp[dp.index("¡Funciona! Ahora puedo acercarme a la valla.")] = "¡Funciona! Aunque no sé si me dejará quitarle la llave mientras come..."
OBJ['caseta']['verbs']['MIRAR'] = {"if": "perro_distraido", "then": "La caseta de Firulais. Ahora está vacía.",
                                   "else": "La caseta de un perro. Pone FIRULAIS. Se oyen ronquidos."}

# ------------------------------------------------------------------ vestíbulo: la escalera ahora sube
hall = R['vestibulo']
OBJ['escalera']['verbs'] = {"MIRAR": "Sube al piso de arriba. De allí vienen unos ruidos... raros.",
                            "IR A": [{"once": "subir_primera", "do": "Voy a ver qué son esos ruidos."}, {"goto": "pasillo", "entry": "escalera"}]}
hall['entries']['escalera'] = {"x": 344, "y": 106, "face": "left"}
hall['sounds'] = hall.get('sounds', []) + [{"name": "risitas", "every": [7, 14], "at": 360, "vol": 0.35}]
hall['onEnter'] = [{"once": "hall_primera", "do": ["El vestíbulo. Y ahí está la puerta principal... cerrada.", "¿Y esa música y ese jaleo que vienen de arriba?"]}]
pp = OBJ['puerta_principal']['verbs']
pp['GOLPEAR'] = "¡Toc, toc! Desde fuera no contesta nadie. Lógico."
pp['IR A']['then'][-1] = {"end": "¡Tito escapó de la mansión del doctor Chiflado y ganó la apuesta! Arriba nadie se enteró: estaban en plena gala. FIN"}
OBJ['armadura']['verbs']['GOLPEAR'] = [S("metal", at="armadura"), "¡Clonc!", who("¡Ay! ¡Que estoy de guardia!", "armadura")]

# ------------------------------------------------------------------ sonidos nuevos
g['sounds'].update({
    "toc_toc": {"layers": [{"wave": "sine", "freq": 190, "freqEnd": 110, "dur": 0.07, "vol": 0.7, "repeat": 3, "gap": 0.2},
                           {"wave": "noise", "dur": 0.04, "vol": 0.3, "filter": ["lowpass", 900, None, 1], "repeat": 3, "gap": 0.2}]},
    "muelles": {"range": 220, "layers": [{"wave": "sine", "freq": 160, "freqEnd": 260, "dur": 0.35, "vol": 0.35, "vibrato": [14, 40], "repeat": 3, "gap": 0.42}]},
    "risitas": {"range": 240, "layers": [{"wave": "square", "freq": 820, "freqEnd": 640, "dur": 0.07, "vol": 0.3, "filter": ["bandpass", 1400, None, 3], "repeat": 5, "gap": 0.11}]},
    "ooh": {"range": 240, "layers": [{"wave": "sawtooth", "freq": 290, "freqEnd": 200, "dur": 1.0, "vol": 0.5, "attack": 0.2, "sustain": 0.6, "vibrato": [6, 7], "filter": ["bandpass", 650, None, 4]}]},
    "hup": {"range": 240, "layers": [{"wave": "sawtooth", "freq": 170, "freqEnd": 260, "dur": 0.13, "vol": 0.35, "filter": ["bandpass", 750, None, 4], "repeat": 2, "gap": 0.45}]},
    "suspiro": {"range": 240, "layers": [{"wave": "noise", "dur": 0.9, "vol": 0.35, "attack": 0.3, "filter": ["bandpass", 1300, 450, 2]}]},
    "acordeon": {"range": 260, "layers": [
        {"wave": "square", "note": "A3", "dur": 0.28, "vol": 0.12, "vibrato": [7, 2], "repeat": 3, "gap": 0.34},
        {"wave": "square", "note": "E4", "dur": 0.28, "vol": 0.08, "vibrato": [7, 2], "repeat": 3, "gap": 0.34},
        {"wave": "square", "note": "C5", "dur": 0.5, "vol": 0.09, "delay": 1.02, "vibrato": [7, 3]}]},
    "silbato_perro": {"layers": [{"wave": "sine", "freq": 2900, "freqEnd": 3400, "dur": 0.25, "vol": 0.12, "repeat": 2, "gap": 0.3}]},
    "arrastre_corto": {"range": 300, "layers": [{"wave": "noise", "dur": 0.45, "vol": 0.35, "attack": 0.05, "sustain": 0.7, "filter": ["bandpass", 400, 550, 3]},
                                               {"wave": "triangle", "freq": 90, "dur": 0.45, "vol": 0.15, "vibrato": [12, 10]}]},
    "campanilla": {"layers": [{"wave": "sine", "freq": 2093, "dur": 0.9, "vol": 0.3}, {"wave": "sine", "freq": 5230, "dur": 0.4, "vol": 0.08},
                              {"wave": "sine", "freq": 2093, "dur": 0.9, "vol": 0.2, "delay": 0.25}]},
    "shh": {"layers": [{"wave": "noise", "dur": 1.1, "vol": 0.3, "attack": 0.1, "sustain": 0.7, "filter": ["highpass", 3500, None, 1]}]},
    "pagina": {"range": 260, "layers": [{"wave": "noise", "dur": 0.18, "vol": 0.2, "attack": 0.03, "filter": ["bandpass", 3000, 1500, 1.5]}]},
    "globo": {"layers": [{"wave": "noise", "dur": 1.2, "vol": 0.25, "sustain": 0.3, "filter": ["bandpass", 900, 300, 2]}]}
})
g['voices'].update({
    "mayordomo": {"pitch": 110, "wave": "sawtooth", "formant": 0.5, "vol": 0.42, "rate": 0.12},
    "cocinera": {"pitch": 320, "wave": "sawtooth", "formant": 0.8, "vol": 0.35, "rate": 0.1},
    "doctor": {"pitch": 150, "wave": "square", "formant": 0.6, "vol": 0.35, "rate": 0.13}
})

# ------------------------------------------------------------------ música nueva
g['music']['pasillo'] = {"bpm": 84, "vol": 1, "tracks": [
    {"wave": "sawtooth", "vol": 0.3, "len": 2, "gate": 0.7, "filter": ["lowpass", 420, 2], "notes":
        "A1 - A1 C2 D2 - E2 G2 | A1 - A1 C2 D2 C2 A1 G1 | D2 - D2 F2 G2 - A2 C3 | E2 - E2 G#2 B2 - E2 -"},
    {"wave": "pulse25", "vol": 0.06, "len": 1, "gate": 0.6, "slide": 0.9, "notes": "-:2 E4:1 -:1 E4:2 -:2 G4:1 -:1 E4:1 -:1 D4:4"},
    {"wave": "sawtooth", "vol": 0.12, "len": 2, "attack": 0.06, "gate": 0.9, "vibrato": [5, 0.012], "filter": ["lowpass", 1500, 1.5], "notes":
        "E4:6 D4:2 C4:4 A3:4 | -:4 C4:2 D4:2 E4:4 G4:4 | A4:6 G4:2 F4:4 D4:4 | E4:12 -:4 | "
        "A4:4 C5:4 B4:2 A4:2 G4:4 | A4:6 E4:2 -:8 | D5:4 C5:2 A4:2 F4:4 D4:4 | E4:8 G#4:4 B4:4"},
    {"wave": "drums", "vol": 0.2, "len": 1, "notes": "k - - - s - - h k - k - s - h -"}]}
g['music']['biblioteca'] = {"bpm": 120, "vol": 1, "tracks": [
    {"wave": "pulse12", "vol": 0.12, "len": 2, "gate": 0.5, "decay": 0.3, "notes":
        "D5 F#5 A5 F#5 D5 A4 | B4 D5 G5 D5 B4 G4 | A4 C#5 E5 A5 G5 E5 | F#5 D5 A4 D5:4 - | "
        "G5 F#5 E5 D5 C#5 B4 | A4 B4 C#5 D5 E5 F#5 | G5 E5 C#5 A4 B4 C#5 | D5:4 A4:4 D4:4"},
    {"wave": "sawtooth", "vol": 0.22, "len": 4, "gate": 0.45, "filter": ["lowpass", 650, 1], "notes":
        "D3 A3 A3 | G2 D3 D3 | A2 E3 E3 | D3 A3 A3 | G2 D3 D3 | A2 E3 E3 | A2 C#3 E3 | D3 D2 -"},
    {"wave": "triangle", "vol": 0.1, "len": 12, "gate": 0.3, "slide": 1.5, "notes": "-:84 A5:12"},
    {"wave": "drums", "vol": 0.14, "len": 4, "notes": "k h h"}]}

# ------------------------------------------------------------------ PASILLO (planta de arriba)
def puerta(n, x, texto_mirar, sonidos, voz, color, deco):
    return {
        "id": f"puerta{n}", "name": f"PUERTA {n}", "box": [x - 2, 30, 38, 62], "walkTo": [x + 17, 104], "face": "back",
        "state": "ruido", "voice": voz, "textColor": color,
        "draw": [["rect", x - 2, 28, 38, 3, "#b08a48"], ["rect", x, 31, 34, 61, "#3a200c"], ["rect", x + 2, 33, 30, 59, "#6a3a18"],
                 ["rect", x + 5, 36, 24, 20, "#5a3010"], ["rect", x + 5, 36, 24, 1, "#8a5228"], ["rect", x + 5, 60, 24, 28, "#5a3010"], ["rect", x + 5, 60, 24, 1, "#8a5228"],
                 ["rect", x + 27, 62, 3, 3, "#e0c040"], ["rect", x + 12, 40, 10, 8, "#d8c090"], ["text", x + 14, 41, str(n), "#5a3014"]] + deco,
        "states": {
            "ruido": {"sound": {"name": sonidos, "every": [1.6, 3.2], "first": 0.6},
                      "draw": [["glow", x + 2, 90, 30, 3, "255,200,90", 0.5, 0.25, 7], ["light", x + 17, 92, 22, "255,190,80", 0.35, 0.3]]},
            "silencio": {"draw": []}
        },
        "verbs": {
            "MIRAR": texto_mirar,
            "ABRIR": "Está cerrada por dentro. ¿Qué estarán tramando ahí?",
            "EMPUJAR": "Está cerrada por dentro.",
            "HABLAR": ["¿Hola? ¿Hay alguien?", "No me oyen. Tendré que GOLPEAR la puerta."],
            "GOLPEAR": {"run": f"golpear_{n}"}
        }}

pasillo = {
    "name": "Pasillo de arriba", "width": 480, "walk": [8, 100, 334, 126], "music": "pasillo",
    "ambient": "#b890b8", "vignette": 0.45,
    "lights": [{"x": 60, "y": 40, "r": 50, "color": "255,190,140", "a": 0.3, "flicker": 0.04},
               {"x": 200, "y": 40, "r": 50, "color": "255,190,140", "a": 0.3, "flicker": 0.04},
               {"x": 410, "y": 60, "r": 70, "color": "255,210,150", "a": 0.35, "flicker": 0.05}],
    "entries": {"escalera": {"x": 314, "y": 114, "face": "left"}, "biblioteca": {"x": 26, "y": 112, "face": "right"}},
    "onEnter": [{"once": "pasillo_primera", "do": ["La planta de arriba...", "¿Esos ruidos son... muelles? ¿Un platillo volante? ¿Un acordeón?", "Esta familia es muy rara."]}],
    "background": [
        ["wallpaper", 0, 6, 480, 56, "#3a1430", "#44183a", "#c0708a"],
        ["repeat", 12, 40, 0, [["use", "moldura", 0, 0], ["use", "arrimadero", 0, 0]]],
        ["planks", 0, 90, 340, 40, 170, "#6a3a1e", "#5e3218", "#2a1408", "#52301a", "#40240e"],
        ["rect", 0, 102, 340, 16, "#7a1a2a"], ["rect", 0, 102, 340, 1, "#a8303e"], ["rect", 0, 117, 340, 1, "#4a0e18"],
        ["repeat", 34, 10, 0, [["pix", 4, 109, "#c8a040"]]],
        ["grad", 340, 62, 140, 82, ["#1a0e18", "#0c0610", "#1a1420"]],
        ["checker", 340, 112, 140, 32, 410, "#8a8478", "#1e1e24", 7, 4],
        ["rug", 380, 440, 122, 136, 4, "#2a2a6a", "#c89030", "#8a1a1a", "#22225a", "#e8d8b0"],
        ["rect", 340, 112, 140, 32, "rgba(0,0,0,0.45)"],
        ["rect", 430, 118, 4, 7, "#9898a8"], ["rect", 430, 116, 4, 2, "#c02020"], ["pix", 431, 125, "#707080"],
        ["line", 410, 0, 410, 46, "#8a6a2a"], ["use", "lampara_arana", 410, 40],
        ["glow", 380, 44, 60, 30, "255,210,140", 0.08, 0.03, 9],
        ["rect", 336, 0, 4, 144, "#1a0a08"],
        ["rect", 300, 118, 40, 3, "#5a3014"], ["rect", 304, 121, 36, 3, "#4a2410"], ["rect", 308, 124, 32, 3, "#3a1a0a"], ["rect", 312, 127, 28, 3, "#2a1206"],
        ["rect", 0, 0, 2, 144, "#120804"], ["rect", 478, 0, 2, 144, "#120804"],
        ["use", "aplique", 58, 36], ["use", "aplique", 198, 36],
        ["rect", 262, 22, 26, 30, "#b8902c"], ["rect", 264, 24, 22, 26, "#2a1a2a"],
        ["circle", 275, 33, 6, "#e0b098"], ["rect", 269, 26, 12, 5, "#8a2a2a"], ["rect", 268, 41, 14, 9, "#9a2a4a"],
        ["blink", 4, 0.08, [["pix", 273, 32, "#e0b098"]]], ["pix", 273, 32, "#1a1a1a"], ["pix", 277, 32, "#1a1a1a"], ["rect", 274, 36, 3, 1, "#c02040"],
        ["rect", 292, 76, 12, 14, "#2a3a6a"], ["rect", 293, 74, 10, 2, "#3a4a7a"],
        ["line", 296, 74, 292, 62, "#2a6a2a"], ["line", 298, 74, 298, 60, "#2a6a2a"], ["line", 300, 74, 305, 63, "#2a6a2a"],
        ["circle", 292, 61, 2, "#c02040"], ["circle", 298, 59, 2, "#e02850"], ["circle", 305, 62, 2, "#c02040"]
    ],
    "objects": [
        {"id": "puerta_biblio", "name": "PUERTA DE LA BIBLIOTECA", "box": [6, 26, 40, 66], "walkTo": [26, 104], "face": "back",
         "draw": [["rect", 6, 26, 40, 3, "#b08a48"], ["rect", 8, 29, 36, 63, "#3a200c"], ["rect", 12, 32, 28, 60, "#e0b060"],
                  ["books", 13, 36, 26, 12, ["#8a1a1a", "#1a3a7a", "#2a6a2a", "#7a5a1a"], 4], ["rect", 12, 48, 28, 2, "#6a3a18"],
                  ["books", 13, 51, 26, 12, ["#5a1a5a", "#1a5a5a", "#9a7a3a", "#3a3a3a"], 7], ["rect", 12, 63, 28, 2, "#6a3a18"],
                  ["rect", 12, 72, 28, 20, "#8a5a2a"], ["rect", 14, 20, 24, 6, "#c8a040"], ["rect", 15, 21, 22, 4, "#2a1a08"],
                  ["light", 26, 70, 30, "255,200,120", 0.3]],
         "verbs": {"MIRAR": "Una placa dice: BIBLIOTECA. SILENCIO, POR FAVOR. Ja. Con este jaleo...",
                   "IR A": {"goto": "biblioteca", "entry": "pasillo"}}},
        puerta(1, 70, "Habitación 1. Cuelga un cartel: NO MOLESTAR, ENSAYO. Se oyen muelles y alguien que cuenta: ¡y uno, y dos!",
               ["muelles", "hup", "muelles"], "mayordomo", "#d0a0ff",
               [["rect", x, 50, 8, 10, "#e8e0d0"] for x in [96]] + [["line", 99, 46, 99, 50, "#8a8a8a"]]),
        puerta(2, 140, "Habitación 2. Tiene una nota musical pintada. Se oye un «uuuuuh» de platillo volante.",
               ["ooh", "risitas", "ooh"], "cocinera", "#ff9ad0",
               [["circle", 153, 50, 3, "#e0c030"], ["rect", 155, 40, 1, 10, "#e0c030"], ["rect", 155, 40, 5, 2, "#e0c030"], ["rect", 159, 42, 1, 2, "#e0c030"]]),
        puerta(3, 210, "Habitación 3. Suena un acordeón. ¿Están bailando un tango?",
               ["acordeon", "risitas"], "doctor", "#ffb070",
               [["rect", 216, 70, 12, 3, "#c02020"], ["pix", 222, 69, "#c02020"]]),
        {"id": "escalera_arriba", "name": "ESCALERA", "box": [296, 110, 44, 22], "walkTo": [318, 114], "face": "right",
         "verbs": {"MIRAR": "Baja al vestíbulo.", "IR A": {"goto": "vestibulo", "entry": "escalera"}}},
        {"id": "barandilla", "name": "BARANDILLA", "box": [340, 60, 140, 84], "walkTo": [330, 112], "face": "right",
         "verbs": {"MIRAR": ["Desde la barandilla se ve el vestíbulo. ¡Qué altura!", "Y la armadura... juraría que me está mirando."],
                   "USAR": "¿Tirarme por la barandilla? Prefiero las escaleras, gracias.",
                   "GOLPEAR": "¡Clonc! Es de hierro. Y ahora me duele la mano."}},
        {"id": "retrato_guino", "name": "RETRATO", "box": [262, 22, 26, 30], "walkTo": [275, 104], "face": "back",
         "verbs": {"MIRAR": "La señora del doctor Chiflado. Juraría que me acaba de guiñar un ojo.", "HABLAR": "Buenas noches, señora. ...Sí, me ha guiñado un ojo."}},
        {"id": "jarron_rosas", "name": "ROSAS", "box": [288, 56, 20, 34], "walkTo": [298, 104], "face": "back",
         "verbs": {"MIRAR": "Rosas rojas de plástico. En esta casa todas las plantas son de mentira.", "COGER": "No son para mí. Y pinchan."}},
        {"id": "balaustrada", "layer": "front", "hotspot": False,
         "draw": [["rect", 0, 124, 480, 3, "#6a3a18"], ["rect", 0, 124, 480, 1, "#9a6430"], ["rect", 0, 141, 480, 3, "#4a2410"],
                  ["repeat", 60, 8, 0, [["rect", 3, 127, 3, 14, "#5a3014"], ["rect", 3, 127, 1, 14, "#7a4a20"]]],
                  ["repeat", 7, 70, 0, [["rect", 0, 118, 6, 26, "#4a2410"], ["rect", -1, 116, 8, 3, "#8a5228"]]]]}
    ]
}
R['pasillo'] = pasillo

def golpe(n, respuesta_normal, extra=None):
    body = [S("toc_toc", at=f"puerta{n}"), {"state": [f"puerta{n}", "silencio"]}, {"stop": f"ruido_{n}"}, {"wait": 0.9}]
    body += respuesta_normal
    body += [{"async": [{"wait": 7}, {"state": [f"puerta{n}", "ruido"]}], "name": f"ruido_{n}"}]
    return body

g['scripts']['golpear_1'] = golpe(1, [
    {"if": "sabe_silbato",
     "then": ["¡Perdone! ¿Sabe dónde está el silbato de Firulais?",
              who("¡¿Hup?! ¡Estoy... hup... OCUPADÍSIMO! ¡Y uno, y dos!", "puerta1"),
              who("¿El silbato? Biblio... hup... ¡ZETA-TRES! ¡ZE-TA-TRES!", "puerta1"),
              who("¡Y no vuelvas a llamar, que pierdo el ritmo! ¡Y arriba, y abajo!", "puerta1"),
              {"set": "codigo_z3"},
              "¿Zeta-tres? Suena al código de una sección de la biblioteca.",
              "¡Y esa voz era la del mayordomo! ¿Haciendo aeróbic a estas horas?"],
     "else": [who("¡¿Hup?! ¡OCUPADO! ¡Ensayando mi número de aeróbic!", "puerta1"), "Esa voz me suena... ¿el mayordomo?"]}])
g['scripts']['golpear_2'] = golpe(2, [
    who("¡Uy! ¡Qué susto!", "puerta2"),
    who("Si buscas algo, pregúntale al de la puerta 1, que es un ratón de biblioteca. ¡Ji, ji!", "puerta2"),
    "¿Esa era la cocinera?"])
g['scripts']['golpear_3'] = golpe(3, [
    who("¡Estamos ensayando el tango! Un, dos, tres... ¡OLÉ!", "puerta3"),
    who("¡Y no molesten, que soy doctor!", "puerta3"),
    "¿El doctor Chiflado bailando tango? Esta casa es un sinvivir."])

# ------------------------------------------------------------------ BIBLIOTECA (Sokoban)
# rejilla 10x3: celdas de 32x14 px. Solución (6 empujes) comprobada con sokoban.py
GRID = {"x0": 0, "y0": 98, "cw": 32, "ch": 14, "cols": 10, "rows": 3, "pushSound": "arrastre_corto", "pushTime": 0.45, "resetEntry": "pasillo"}
generos = [
    ("est_poesia", "POESÍA", (4, 0), ["#c04060", "#e080a0", "#a02040"], "«Poemas para mayordomos». Todo rima con «bandeja»."),
    ("est_cocina", "COCINA", (7, 0), ["#e0a030", "#c07020", "#f0d060"], "«Cien recetas con salchichas». Muy útil, tarde."),
    ("est_astro", "ASTRONOMÍA", (4, 1), ["#2040a0", "#4060c0", "#8090e0"], "«Cómo contar estrellas sin dormirse». Me duermo."),
    ("est_misterio", "MISTERIO", (7, 1), ["#404040", "#606060", "#8a2020"], "«El asesino fue el mayordomo». Tomo 34."),
    ("est_autoayuda", "AUTOAYUDA", (6, 2), ["#30a060", "#60c080", "#208040"], "«Sal de la mansión en 10 pasos». Solo tiene 9 páginas."),
    ("est_romantica", "AVENTURAS", (9, 2), ["#e04080", "#ff80b0", "#a02060"], "«Perdido en el piso de arriba». Eso explica muchas cosas.")
]
def estanteria(oid, nombre, cell, cols, titulo, seed):
    return {
        "id": oid, "name": "ESTANTERÍA (" + nombre + ")", "cell": list(cell), "pushable": True,
        "box": [-14, -30, 28, 31], "obstacle": [-14, -12, 14, -1],
        "draw": [["ellipse", 0, 0, 14, 2, "rgba(0,0,0,0.35)"],
                 ["rect", -13, -28, 26, 25, "#5a3014"], ["rect", -13, -28, 26, 2, "#8a5228"], ["rect", -13, -28, 2, 25, "#7a4a20"], ["rect", 11, -28, 2, 25, "#3a1a08"],
                 ["books", -11, -26, 22, 9, cols, seed], ["rect", -11, -17, 22, 2, "#6a3a18"],
                 ["books", -11, -15, 22, 9, cols, seed + 1], ["rect", -13, -5, 26, 2, "#3a1a08"],
                 ["circle", -9, -2, 1, "#2a2a2a"], ["circle", 9, -2, 1, "#2a2a2a"]],
        "verbs": {
            "MIRAR": ["Una estantería con ruedas. Sección: " + nombre + ".", {"once": "pista_empujar", "do": "Si me pongo a un lado, puedo EMPUJARLA hacia el otro."}],
            "LEER": [S("pagina", at=oid), titulo],
            "EMPUJAR": {"push": oid, "ok": [], "fail": {"random": ["No se mueve. Hay algo detrás.", "Por ahí no hay sitio.", "¡Uf! Choca con algo."]}},
            "TIRAR": "Con ruedas o sin ellas, prefiero EMPUJAR. Tirar me da hernia.",
            "COGER": "Pesa demasiado. Pero rueda..."
        }}

fijos = [
    {"id": "busto", "name": "BUSTO DE BEETHOVEN", "cell": [2, 0], "box": [-12, -44, 24, 45], "obstacle": [-14, -12, 14, -1], "voice": "mayordomo", "textColor": "#e0e0e0",
     "draw": [["rect", -8, -18, 16, 17, "#8a8478"], ["rect", -8, -18, 16, 1, "#b0a898"], ["rect", -10, -3, 20, 3, "#6a6458"],
              ["circle", 0, -30, 7, "#d8d4c8"], ["rect", -9, -36, 18, 5, "#b0aca0"], ["rect", -9, -24, 18, 6, "#c8c4b8"],
              ["pix", -3, -31, "#6a6458"], ["pix", 3, -31, "#6a6458"], ["rect", -2, -27, 4, 1, "#8a8478"]],
     "verbs": {"MIRAR": "Beethoven. Tiene cara de no oír nada. Normal.", "EMPUJAR": "Está atornillado al suelo. Y pesa como una sinfonía.",
               "HABLAR": ["¿Qué tal, Ludwig?", "...", "No me oye. Lógico."]}},
    {"id": "globo", "name": "GLOBO TERRÁQUEO", "cell": [5, 0], "box": [-12, -34, 24, 35], "obstacle": [-14, -12, 14, -1],
     "draw": [["rect", -1, -14, 2, 12, "#6a3a18"], ["rect", -7, -3, 14, 3, "#5a3014"],
              ["circle", 0, -22, 9, "#3a6aa8"], ["ellipse", -3, -25, 4, 3, "#4a8a3a"], ["ellipse", 4, -19, 3, 2, "#4a8a3a"], ["ellipse", 2, -28, 2, 1, "#4a8a3a"],
              ["ring", 0, -22, 10, "#c8a040", 1], ["pix", 5, -18, "#1a1a1a"], ["pix", 6, -18, "#1a1a1a"]],
     "verbs": {"MIRAR": "Un globo terráqueo. Alguien le ha pintado un bigote a Australia.", "EMPUJAR": "Gira, pero no se mueve de sitio.",
               "USAR": [S("globo"), "¡Vueltaaa al mundooo!", "...Me he mareado."]}},
    {"id": "estatua", "name": "ESTATUA", "cell": [9, 0], "box": [-12, -58, 24, 59], "obstacle": [-14, -12, 14, -1],
     "draw": [["rect", -10, -8, 20, 8, "#8a8478"], ["rect", -10, -8, 20, 1, "#b0a898"],
              ["rect", -5, -40, 10, 32, "#c8c4b8"], ["rect", -5, -40, 2, 32, "#e0dcd0"], ["rect", -8, -38, 3, 16, "#c8c4b8"], ["rect", 5, -38, 3, 18, "#b8b4a8"],
              ["circle", 0, -46, 5, "#d8d4c8"], ["rect", -4, -48, 8, 2, "#1a1a1a"], ["rect", -3, -41, 6, 3, "#b0aca0"]],
     "verbs": {"MIRAR": "Un filósofo griego con gafas de sol. Muy moderno.", "EMPUJAR": "Es de mármol. Ni lo sueñes.", "HABLAR": "Pienso, luego no te contesto."}},
    {"id": "mesa_lectura", "name": "MESA DE LECTURA", "cell": [4, 2], "box": [-15, -22, 30, 23], "obstacle": [-14, -12, 14, -1],
     "draw": [["rect", -15, -12, 30, 3, "#6a3a18"], ["rect", -15, -12, 30, 1, "#9a6430"], ["rect", -13, -9, 3, 9, "#4a2410"], ["rect", 10, -9, 3, 9, "#4a2410"],
              ["rect", 4, -20, 2, 8, "#8a6a2a"], ["poly", [[1, -22], [11, -22], [9, -18], [3, -18]], "#2a7a4a"], ["light", 6, -16, 46, "255,220,140", 0.45, 0.03],
              ["rect", -11, -14, 10, 2, "#f0ece0"], ["rect", -6, -14, 1, 2, "#8a8478"]],
     "verbs": {"MIRAR": "Una mesa de lectura con una lámpara verde. Muy de estudiar. Encima hay una campanilla.", "EMPUJAR": "Está clavada al suelo. Qué manía con clavar cosas.",
               "LEER": [S("pagina", at="mesa_lectura"), "El libro abierto se titula «Estanterías con ruedas: un error de diseño»."]}},
]

biblioteca = {
    "name": "Biblioteca", "width": 320, "walk": [2, 98, 318, 140], "music": "biblioteca", "grid": GRID,
    "ambient": "#b0a098", "vignette": 0.4,
    "lights": [{"x": 272, "y": 50, "r": 34, "color": "255,230,160", "a": 0.18, "flicker": 0.05}],
    "entries": {"pasillo": {"x": 16, "y": 119, "face": "right"}},
    "sounds": [{"name": "pagina", "every": [5, 11], "at": 160, "vol": 0.6}],
    "onEnter": [{"once": "biblio_primera", "do": ["¡Una biblioteca! Y las estanterías tienen ruedas... como los carritos del súper.",
                                                  "Si me pongo a un lado de una estantería, podré EMPUJARLA hacia el otro."]}],
    "background": [
        ["rect", 0, 0, 320, 98, "#3a2012"], ["rect", 0, 0, 320, 5, "#6a3a18"], ["rect", 0, 4, 320, 1, "#9a6430"],
        ["repeat", 10, 32, 0, [["rect", 2, 8, 28, 88, "#1a0c04"], ["rect", 0, 8, 2, 90, "#5a3014"], ["rect", 30, 8, 2, 90, "#4a2410"]]],
        *[["books", 3 + 32 * c, 11 + 21 * s, 26, 17, ["#8a1a1a", "#1a3a7a", "#2a6a2a", "#7a5a1a", "#5a1a5a", "#1a5a5a", "#9a7a3a", "#3a3a3a"], 11 + c * 7 + s]
          for c in range(1, 10) for s in range(4)],
        ["repeat", 4, 0, 21, [["rect", 2, 28, 316, 2, "#6a3a18"], ["rect", 2, 28, 316, 1, "#8a5228"]]],
        *[x for c, L in [(1, "A"), (2, "B"), (3, "H"), (4, "M"), (5, "P"), (6, "Q"), (7, "T"), (8, "Z"), (9, "?")]
          for x in (["rect", 32 * c + 10, 2, 12, 9, "#c8a040"], ["rect", 32 * c + 11, 3, 10, 7, "#2a1a08"], ["text", 32 * c + 13, 3, L, "#e0c050"])],
        ["rect", 2, 32, 28, 66, "#1a0c04"], ["rect", 4, 34, 24, 64, "#e0b060"], ["rect", 4, 34, 24, 40, "#44183a"], ["rect", 4, 74, 24, 24, "#6a3a1e"],
        ["tiles", 0, 98, 320, 42, 32, 14, "#7a4a24", "#6e4220", "#4a2a12"],
        ["rect", 0, 140, 320, 4, "#2a1408"],
        ["rect", 0, 0, 2, 144, "#120804"], ["rect", 318, 0, 2, 144, "#120804"]
    ],
    "objects": [
        {"id": "puerta_biblio_salida", "name": "PUERTA", "box": [2, 30, 28, 66], "walkTo": [16, 105], "face": "back",
         "verbs": {"MIRAR": "Vuelve al pasillo.", "IR A": {"goto": "pasillo", "entry": "biblioteca"}}},
        {"id": "estanterias_pared", "name": "ESTANTERÍAS", "box": [34, 8, 220, 80], "walkTo": [48, 105], "face": "back",
         "verbs": {"MIRAR": "Miles de libros. Huele a polvo y a sabiduría. Sobre todo a polvo.",
                   "LEER": {"random": [[S("pagina"), "«Física cuántica para gatos». No entiendo nada. El gato tampoco."],
                                       [S("pagina"), "«Historia del bostezo, tomo XII». ...¡Aaaah!"],
                                       [S("pagina"), "«Matemáticas sin números». Todo el libro está en blanco."],
                                       [S("pagina"), "«Cómo hacer amigos en una mansión encantada». Capítulo 1: huye."]]},
                   "COGER": "Si cojo uno, se cae toda la fila. Lo he visto en las películas."}},
        {"id": "seccion_z", "name": "SECCIÓN Z", "box": [258, 8, 28, 80], "walkTo": [272, 105], "face": "back",
         "draw": [["rect", 263, 51, 10, 19, "#1a0c04"],
                  ["rect", 264, 52, 8, 18, "#a01818"], ["rect", 264, 52, 1, 18, "#d04040"], ["rect", 271, 52, 1, 18, "#600808"], ["rect", 264, 69, 8, 1, "#500606"],
                  ["rect", 264, 54, 8, 1, "#f0d060"], ["rect", 264, 66, 8, 1, "#f0d060"], ["rect", 266, 57, 4, 5, "#f0d060"], ["pix", 267, 59, "#a01818"], ["pix", 268, 59, "#a01818"],
                  ["if", "codigo_z3 && !silbato_cogido", [
                      ["frames", 3, [[["pix", 272, 50, "#ffffff"], ["pix", 271, 50, "#fff0a0"], ["pix", 273, 50, "#fff0a0"], ["pix", 272, 49, "#fff0a0"], ["pix", 272, 51, "#fff0a0"]],
                                     [["pix", 272, 50, "#fff0a0"]], [], [], [], []]],
                      ["light", 268, 60, 14, "255,220,120", 0.18, 0.2]]]],
         "verbs": {"MIRAR": {"if": "codigo_z3", "then": "Sección Z, zoología. Ese libro rojo gordo es el Z-3. ¡Tiene que ser ese!", "else": "Sección Z: zoología. Hay cientos de libros de animales. Uno rojo muy gordo destaca."},
                   "COGER": {"run": "coger_z3"}, "LEER": {"run": "coger_z3"}}},
        *[estanteria(oid, nom, cell, cols, tit, 20 + i * 5) for i, (oid, nom, cell, cols, tit) in enumerate(generos)],
        *fijos,
        {"id": "campanilla", "name": "CAMPANILLA", "box": [129, 117, 12, 11], "z": 140.5, "walkTo": [112, 133], "face": "right",
         "draw": [["rect", 132, 123, 5, 3, "#e0c040"], ["rect", 134, 121, 1, 2, "#c8a040"], ["pix", 132, 123, "#fff0a0"]],
         "verbs": {"MIRAR": "Una campanilla de bibliotecaria. Seguro que hace algo mágico. O suena. Una de dos.",
                   "USAR": {"run": "reset_biblio"}, "GOLPEAR": {"run": "reset_biblio"}, "COGER": "Mejor la dejo donde está. Por si acaso."}}
    ]
}
R['biblioteca'] = biblioteca
g['scripts']['coger_z3'] = [
    {"if": "silbato_cogido", "then": "Ya tengo lo que buscaba. No voy a leerme toda la sección.",
     "else": {"if": "!codigo_z3", "then": ["Hay cientos de libros de animales.", "Sin saber cuál busco, podría pasarme aquí un siglo."],
              "else": [S("pagina", at="seccion_z"), "Zeta-tres... ¡aquí! «Cómo educar a tu perro sin morir en el intento».",
                       "¡Está hueco! Dentro hay un silbato. Pone: FIRULAIS.", {"pickup": "silbato"}, {"set": "silbato_cogido"}]}}
]
g['scripts']['reset_biblio'] = [
    S("campanilla"), {"wait": 0.4}, S("shh"), who("¡SSSSSSHHHHH!", "busto"), {"gridReset": True},
    "¡Las estanterías han vuelto solas a su sitio!", "Esta biblioteca está embrujada... y es muy ordenada."
]

# ------------------------------------------------------------------ guardar
spec = importlib.util.spec_from_file_location('fm', 'fmt.py'); fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
order = ["title", "palette", "audio", "verbs", "defaultVerb", "lookVerb", "rightClickVerb", "pushVerb", "unreachable", "defaults", "player", "voices", "sfx",
         "start", "intro", "items", "scripts", "music", "sounds", "sprites", "prefabs", "rooms"]
g = {k: g[k] for k in order if k in g} | {k: x for k, x in g.items() if k not in order}
g['rooms'] = {k: g['rooms'][k] for k in ['salon', 'vestibulo', 'pasillo', 'biblioteca', 'cocina', 'patio', 'sotano']}
out = fm.fmt(g) + '\n'; json.loads(out)
open('../aventura.json', 'w').write(out)
print('ok', len(out))
