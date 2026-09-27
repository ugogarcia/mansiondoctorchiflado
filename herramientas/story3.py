# Gags con puntos, escena exterior (intro y final), cronómetro y puntuación.
# Orden: gen.py -> audio.py -> story2.py -> story3.py -> build.py
import json, importlib.util

g = json.load(open('../aventura.json'))
R = g['rooms']
OBJ = {o['id']: o for r in R.values() for o in r['objects']}
def S(name, **kw): return {"sound": name, **kw}
def who(txt, w): return {"say": txt, "who": w}

# ------------------------------------------------------------------ sonidos nuevos
g['sounds'].update({
    "clack": {"layers": [{"wave": "square", "freq": 1900, "dur": 0.03, "vol": 0.3, "filter": ["bandpass", 2500, None, 3]},
                         {"wave": "noise", "dur": 0.03, "vol": 0.2, "filter": ["highpass", 2000, None, 1]}]},
    "tronera": {"layers": [{"wave": "sine", "freq": 220, "freqEnd": 90, "dur": 0.12, "vol": 0.4}]},
    "taco_golpe": {"layers": [{"wave": "square", "freq": 900, "dur": 0.04, "vol": 0.3, "filter": ["bandpass", 1400, None, 2]},
                              {"wave": "noise", "dur": 0.05, "vol": 0.25, "filter": ["bandpass", 2500, None, 1]}]},
    "punto": {"layers": [{"wave": "pulse25", "note": "E6", "dur": 0.08, "vol": 0.16}, {"wave": "pulse25", "note": "B6", "dur": 0.25, "vol": 0.16, "delay": 0.08}]},
    "wow": {"layers": [{"wave": "pulse25", "note": "C5", "dur": 0.08, "vol": 0.16}, {"wave": "pulse25", "note": "E5", "dur": 0.08, "vol": 0.16, "delay": 0.08},
                       {"wave": "pulse25", "note": "G5", "dur": 0.08, "vol": 0.16, "delay": 0.16}, {"wave": "pulse25", "note": "C6", "dur": 0.4, "vol": 0.18, "delay": 0.24, "vibrato": [8, 20]},
                       {"wave": "triangle", "note": "C4", "dur": 0.6, "vol": 0.3, "delay": 0.24}]},
    "tv_canal": {"layers": [{"wave": "square", "freq": 1200, "freqEnd": 300, "dur": 0.12, "vol": 0.15},
                            {"wave": "noise", "dur": 0.2, "vol": 0.2, "filter": ["bandpass", 3000, None, 0.7]}]},
    "apagar_fuego": {"layers": [{"wave": "noise", "dur": 0.6, "vol": 0.3, "attack": 0.02, "filter": ["lowpass", 1500, 200, 1]}]},
    "portazo": {"layers": [{"wave": "sine", "freq": 120, "freqEnd": 35, "dur": 0.5, "vol": 0.9},
                           {"wave": "noise", "dur": 0.25, "vol": 0.5, "filter": ["lowpass", 1200, None, 1]}]},
    "petardo": {"layers": [{"wave": "noise", "dur": 0.5, "vol": 0.35, "filter": ["lowpass", 2500, 300, 1]}, {"wave": "sine", "freq": 90, "freqEnd": 40, "dur": 0.3, "vol": 0.4}]}
})
g['sfx']['score'] = "punto"

# ------------------------------------------------------------------ puntuación
g['scoring'] = {
    "timeLabel": "TIEMPO", "pointsLabel": "PUNTOS DE DISPARATE",
    "ranks": [[100, "¡MAESTRO DEL DISPARATE! Lo has probado todo."],
              [60, "¡Nada mal! Pero aún quedan tonterías por hacer."],
              [25, "Aventurero serio. Demasiado serio."],
              [0, "¿Has venido a jugar o a trabajar?"]]
}

# ------------------------------------------------------------------ GAG 1: carambola mágica (25)
mesa = OBJ['mesa']
bolas = [("b_amarilla", 56, 108, "#e8d020", [(90, 104), (115, 101)]), ("b_roja", 53, 106, "#c02020", [(41, 101)]),
         ("b_azul", 53, 110, "#2040c0", [(40, 114), (29, 118)]), ("b_naranja", 50, 104, "#e07020", [(70, 103), (78, 101)]),
         ("b_negra", 50, 108, "#111111", [(100, 116), (127, 118)]), ("b_morada", 50, 112, "#8a2090", [(78, 118)]),
         ("b_blanca", 98, 109, "#f4f4f4", None)]
coords = {(b[1], b[2]) for b in bolas}
mesa['draw'] = [d for d in mesa['draw'] if not (d[0] in ('rect', 'pix') and (d[1], d[2]) in coords)]
salon = R['salon']
idx = next(i for i, o in enumerate(salon['objects']) if o['id'] == 'freno')
for k, (bid, bx, by, col, _) in enumerate(bolas):
    salon['objects'].insert(idx + k, {"id": bid, "parent": "mesa", "x": 52, "y": 0, "z": 134.3, "hotspot": False,
                                      "draw": [["rect", bx, by, 2, 2, col], ["pix", bx, by, "rgba(255,255,255,0.6)"]]})
def ruta(bx, by, pts): return [[52 + px - bx, py - by] for px, py in pts]
car = [{"face": "right"}, "A ver... el truco del almendruco.", S("taco_golpe"),
       {"path": ["b_blanca", ruta(98, 109, [(60, 109)]), 260]}, S("clack")]
for bid, bx, by, col, pts in bolas[:-1]:
    car.append({"async": [{"path": [bid, ruta(bx, by, pts), 110 + (bx % 7) * 12]}, S("tronera"), {"hide": bid}]})
car += [{"wait": 0.3}, S("clack"), {"wait": 0.25}, S("clack"),
        {"path": ["b_blanca", ruta(98, 109, [(60, 109), (90, 114), (120, 104), (115, 101)]), 140]}, S("tronera"), {"hide": "b_blanca"},
        {"wait": 0.5}, {"set": "carambola_hecha"},
        {"banner": "¡CARAMBOLA MÁGICA!", "sub": "¡Siete bolas de un solo golpe!", "style": "super", "time": 2.6, "sound": "wow"},
        {"score": ["carambola", 25]},
        "Soy un genio. Un genio del billar que debería estar buscando la salida."]
g['scripts']['carambola'] = [{"if": "carambola_hecha", "then": "Ya no quedan bolas. Las metí todas de un golpe, por si no lo recuerdas.", "else": car}]
g['items']['taco']['verbs']['USAR:mesa'] = {"run": "carambola"}
mesa['verbs']['USAR'] = {"if": "has:taco", "then": {"run": "carambola"}, "else": "Sin taco no puedo jugar. Y con las manos es trampa."}
mesa['verbs']['MIRAR'] = {"if": "carambola_hecha", "then": "Ni una bola en la mesa. Qué limpieza.",
                          "else": {"if": "state:mesa=movida", "then": "Ya no tapa la alfombra.", "else": "Una mesa de billar. Alguien dejó la partida a medias."}}

# ------------------------------------------------------------------ GAG 2: sintonizar la tele (15)
tele = OBJ['tele']
bg = lambda c: ["rect", 252, 54, 20, 18, c]
alien = [bg("#1a2a5a"), ["rect", 254, 67, 16, 5, "#6a3a18"], ["rect", 255, 66, 14, 1, "#8a5228"],
         ["circle", 262, 62, 4, "#60d060"], ["pix", 260, 61, "#000000"], ["pix", 264, 61, "#000000"], ["rect", 261, 64, 3, 1, "#206020"],
         ["rect", 258, 55, 8, 3, "#ffffff"], ["circle", 262, 55, 3, "#ffffff"], ["line", 267, 58, 270, 66, "#c0c0c0"]]
alien2 = [bg("#1a2a5a"), ["rect", 254, 67, 16, 5, "#6a3a18"], ["rect", 255, 66, 14, 1, "#8a5228"],
          ["circle", 262, 62, 4, "#60d060"], ["pix", 260, 61, "#000000"], ["pix", 264, 61, "#000000"], ["rect", 261, 64, 3, 2, "#206020"],
          ["rect", 258, 55, 8, 3, "#ffffff"], ["circle", 262, 55, 3, "#ffffff"], ["line", 265, 58, 262, 66, "#c0c0c0"],
          ["pix", 258, 64, "#f0f0a0"], ["pix", 266, 63, "#f0f0a0"]]
gato = [bg("#60a0e0"), ["rect", 253, 57, 5, 2, "#ffffff"], ["rect", 266, 68, 4, 2, "#ffffff"],
        ["rect", 256, 63, 14, 3, "#b0b0c0"], ["rect", 261, 60, 3, 9, "#9090a0"], ["rect", 256, 61, 2, 2, "#9090a0"],
        ["circle", 265, 62, 2, "#f0a040"], ["pix", 264, 59, "#f0a040"], ["pix", 267, 59, "#f0a040"], ["pix", 265, 62, "#000000"]]
gato2 = [bg("#60a0e0"), ["rect", 256, 57, 5, 2, "#ffffff"], ["rect", 262, 68, 4, 2, "#ffffff"],
         ["rect", 254, 62, 14, 3, "#b0b0c0"], ["rect", 259, 59, 3, 9, "#9090a0"], ["rect", 254, 60, 2, 2, "#9090a0"],
         ["circle", 263, 61, 2, "#f0a040"], ["pix", 262, 58, "#f0a040"], ["pix", 265, 58, "#f0a040"], ["pix", 263, 61, "#000000"]]
aero = [bg("#30b0b0"), ["circle", 262, 58, 2, "#e0b090"], ["rect", 260, 56, 5, 1, "#ff3080"], ["rect", 261, 61, 3, 5, "#ff60a0"],
        ["line", 261, 62, 256, 57, "#e0b090"], ["line", 263, 62, 268, 57, "#e0b090"],
        ["line", 261, 66, 258, 71, "#ffe040"], ["line", 263, 66, 266, 71, "#ffe040"]]
aero2 = [bg("#30b0b0"), ["circle", 262, 60, 2, "#e0b090"], ["rect", 260, 58, 5, 1, "#ff3080"], ["rect", 261, 63, 3, 4, "#ff60a0"],
         ["line", 261, 64, 256, 66, "#e0b090"], ["line", 263, 64, 268, 66, "#e0b090"],
         ["line", 261, 67, 257, 71, "#ffe040"], ["line", 263, 67, 267, 71, "#ffe040"]]
esquinas = [["pix", 252, 54, "#2a2a2a"], ["pix", 271, 54, "#2a2a2a"], ["pix", 252, 71, "#2a2a2a"], ["pix", 271, 71, "#2a2a2a"]]
tele['states']['canal'] = {
    "sound": {"name": ["ooh", "risitas", "muelles"], "every": 1.3, "vol": 0.7},
    "draw": [["frames", 0.9, [alien, alien2, alien, alien2, gato, gato2, gato, gato2, aero, aero2, aero, aero2]], ["roll", 252, 54, 20, 18], *esquinas,
             ["glow", 240, 86, 54, 22, "160,220,255", 0.07, 0.03, 20]]}
tele['verbs']['USAR'] = {"if": "state:tele=apagada", "then": "Primero tendré que ENCENDERLA.",
    "else": {"if": "state:tele=canal", "then": [S("tv_canal", at="tele"), {"state": ["tele", "carta"]}, "Mejor vuelvo a la carta de ajuste. Es más educativa."],
             "else": [S("tv_canal", at="tele"), "A ver qué echan en el canal de madrugada...", {"state": ["tele", "nieve"]}, {"wait": 0.6},
                      S("tv_canal", at="tele"), {"state": ["tele", "canal"]}, {"wait": 1.5},
                      "¿Un extraterrestre cocinero? ¿Un gato piloto? ¿Aeróbic con calentadores?", "Juraría que esto suena igual que el piso de arriba...",
                      {"score": ["tele", 15]}]}}
tele['verbs']['MIRAR'] = {"if": "state:tele=apagada", "then": "Una tele de tubo. Pesa como una nevera.",
    "else": {"if": "state:tele=canal", "then": "Imágenes muy raras. Esto no lo emiten ni a las tres de la mañana.",
             "else": "Emiten la carta de ajuste. Quizá si la USO pueda cambiar de canal."}}

# ------------------------------------------------------------------ GAG 3: apagar la olla (10)
fogon = OBJ['fogon']
anim = [d for d in fogon['draw'] if d[0] in ('flame', 'steam')]
fogon['draw'] = [d for d in fogon['draw'] if d[0] not in ('flame', 'steam')]
fogon['state'] = 'encendido'
fogon['states'] = {"encendido": {"draw": anim, "sound": fogon.pop('sound', {"name": "burbujas", "every": [0.5, 1.3]})},
                   "apagado": {"draw": [["rect", 105, 42, 1, 2, "rgba(200,200,210,0.4)"]]}}
fogon['verbs']['APAGAR'] = {"if": "state:fogon=apagado", "then": "Ya está apagado.",
    "else": [S("apagar_fuego"), {"state": ["fogon", "apagado"]}, "Apago el fuego. Hala, se acabó el guiso.", {"wait": 0.8},
             {"say": "(Desde arriba) ¡¡MI COCIDOOOOO!!", "color": "#ff9ad0", "voice": "cocinera"},
             "Ups. Creo que la cocinera tiene un oído finísimo.", {"score": ["olla", 10]}]}
fogon['verbs']['ENCENDER'] = {"if": "state:fogon=encendido", "then": "Ya está encendido.",
    "else": [{"state": ["fogon", "encendido"]}, "Vuelvo a encenderlo. Que luego me echan la culpa."]}
fogon['verbs']['MIRAR'] = {"if": "state:fogon=apagado", "then": "El puchero se está enfriando. Por mi culpa.",
                           "else": "Un puchero hierve a fuego lento. Huele a... ¿calcetín?"}

# ------------------------------------------------------------------ GAG 4: home run al murciélago (30)
murci = OBJ['murcielago']
murci['states']['aturdido'] = {"draw": [["sprite", "murcielago", "colgado", -2, -4], ["moths", 0, -8, 6, 4]]}
salon['timers'][0]['name'] = "vuelo_murci"
g['scripts']['golpe_murcielago'] = [
    "¡Toma, bicho!", S("taco_golpe"), {"stop": "vuelo_murci"}, S("chillido", at="murcielago"),
    {"state": ["murcielago", "aturdido"]}, {"path": ["murcielago", [[0, 18]], 70], "rel": True},
    {"banner": "¡¡¡WOW!!!", "sub": "¡Le has dado al murciélago! SUPERBONUS: home run nocturno", "style": "super", "time": 2.8, "sound": "wow"},
    {"score": ["murcielago", 30]},
    {"state": ["murcielago", "vuela"]}, S("chillido", at="murcielago"),
    {"path": ["murcielago", [[660, 8]], 190]}, {"hide": "murcielago"}, {"unset": "murcielago_fuera"},
    {"random": ["Se ha ido volando hacia Transilvania. Con chichón.", "Juraría que me ha hecho un gesto muy feo con el ala.",
                "Ha dejado caer una nota: «Me mudo a una cueva más tranquila». Qué sensible."]}
]
murci['verbs']['USAR:taco'] = {"run": "golpe_murcielago"}
g['items']['taco']['verbs']['USAR:murcielago'] = {"run": "golpe_murcielago"}
murci['verbs']['GOLPEAR'] = "No llego con la mano. Necesitaría algo largo..."

# ------------------------------------------------------------------ GAG 5 y 6: globo (10) y foto a la armadura (10)
OBJ['globo']['verbs']['USAR'] = [S("globo"), "¡Vueltaaa al mundooo!", {"banner": "¡VUELTA AL MUNDO!", "sub": "en 1,5 segundos", "style": "super", "time": 1.8, "sound": "wow"},
                                 "...Me he mareado.", {"score": ["globo", 10]}]
arm = OBJ['armadura']['verbs']['DAR:foto']
arm.append({"score": ["armadura", 10]})

# ------------------------------------------------------------------ ESCENA EXTERIOR (intro y final)
def ventana(x, y, w, h, lit=True):
    base = [["rect", x - 1, y - 1, w + 2, h + 2, "#0a0814"]]
    if lit: base += [["rect", x, y, w, h, "#f0c060"], ["rect", x + w // 2, y, 1, h, "#6a4020"], ["rect", x, y + h // 2, w, 1, "#6a4020"]]
    else: base += [["rect", x, y, w, h, "#10142a"], ["pix", x + 1, y + 1, "#3a4070"]]
    return base
ventanas = []
for x in (112, 140, 222, 240): ventanas += ventana(x, 82, 10, 14, lit=(x in (112, 240)))
for x in (104, 118): ventanas += ventana(x, 36, 8, 12, lit=(x == 104))
for x in (256, 268): ventanas += ventana(x, 42, 8, 10, lit=False)
arriba = [(150, 56), (176, 56), (202, 56), (228, 56)]
ventanas_arriba = []
for x, y in arriba: ventanas_arriba += [["rect", x - 1, y - 1, 12, 14, "#0a0814"], ["rect", x, y, 10, 12, "#ffd860"], ["rect", x + 5, y, 1, 12, "#6a4a20"]]
CORA = ["..XX", "..X.", "..X.", "XXX.", "XXX."]
corazones = ["frames", 2.5, [[["pixels", x + 2, y - 6 - k * 5, CORA, {"X": ["#ffe040", "#60e0ff", "#ff80c0", "#80ff80"][(x // 26 + k) % 4]}] for x, y in arriba[i::2]] for i in range(2) for k in range(3)]]

exterior = {
    "name": "Exterior", "width": 320, "walk": [2, 120, 318, 141], "noUI": True, "storm": True, "stormSound": "trueno",
    "music": "titulo", "ambient": "#8088c0", "vignette": 0.5,
    "lights": [{"x": 190, "y": 88, "r": 40, "color": "255,200,120", "a": 0.35, "flicker": 0.06},
               {"x": 117, "y": 90, "r": 26, "color": "255,200,120", "a": 0.25}, {"x": 245, "y": 90, "r": 26, "color": "255,200,120", "a": 0.25}],
    "entries": {"camino": {"x": 8, "y": 134, "face": "right"}, "puerta": {"x": 190, "y": 124, "face": "front"}},
    "background": [
        ["grad", 0, 0, 320, 112, ["#060a20", "#0e1640", "#1c2458", "#3a3470", "#5a4478"]],
        ["stars", 0, 0, 320, 60, 50, 31], ["moon", 290, 20, 9],
        ["if", "final", [["fireworks", 20, 4, 280, 60, 5]]],
        ["clouds", 0, 4, 320, 30, 5, "#1c2454", "#34407a", 2, 9],
        ["hills", 0, 72, 320, 40, "#12163a", 4, 0], ["hills", 0, 90, 320, 24, "#0a0e28", 11, 3],
        ["poly", [[92, 52], [190, 26], [290, 52]], "#140f22"],
        ["rect", 96, 50, 190, 70, "#1e1830"], ["rect", 96, 50, 190, 1, "#3a3060"],
        ["rect", 100, 28, 34, 92, "#221a36"], ["poly", [[96, 28], [117, 4], [138, 28]], "#140f22"], ["rect", 133, 28, 1, 92, "#3a3060"],
        ["rect", 250, 34, 32, 86, "#221a36"], ["poly", [[246, 34], [266, 14], [286, 34]], "#140f22"], ["rect", 281, 34, 1, 86, "#3a3060"],
        ["rect", 214, 26, 8, 18, "#1a1428"], ["rect", 214, 26, 8, 2, "#2a2240"],
        ["line", 117, 4, 117, 0, "#2a2240"], ["pix", 117, 0, "#c8a040"],
        *ventanas,
        ["if", "!final", [["rect", c[0], c[1], 10, 12, "#10142a"] for c in arriba]],
        ["if", "final", [*ventanas_arriba, corazones, *[["light", x + 5, y + 6, 22, "255,210,120", 0.35, 0.3] for x, y in arriba]]],
        ["rect", 176, 88, 28, 32, "#0a0814"], ["poly", [[174, 88], [190, 80], [206, 88]], "#140f22"],
        ["rect", 176, 118, 28, 3, "#4a4a54"], ["rect", 172, 121, 36, 3, "#3a3a44"],
        ["rect", 206, 84, 4, 6, "#2a2a2a"], ["rect", 207, 85, 2, 4, "#ffe8a0"],
        ["grad", 0, 112, 320, 32, ["#0e1c16", "#16281c", "#1e3222"]],
        ["speckle", 0, 114, 320, 30, "#2a4a2a", 0.08, 5],
        ["poly", [[0, 132], [0, 142], [120, 138], [186, 126], [194, 126], [178, 124], [110, 130]], "#34343e"],
        ["speckle", 0, 124, 190, 18, "#44444e", 0.12, 8],
        ["grass", 0, 116, 320, 28, ["#2a4a2a", "#3a5a30", "#1a3020"], 200, 6],
        ["line", 34, 118, 34, 84, "#0a0c18"], ["line", 34, 96, 22, 84, "#0a0c18"], ["line", 34, 92, 46, 78, "#0a0c18"], ["line", 40, 86, 48, 88, "#0a0c18"],
        ["line", 35, 118, 35, 86, "#0a0c18"], ["line", 28, 90, 24, 82, "#0a0c18"],
        ["repeat", 9, 8, 0, [["rect", 50, 110, 1, 12, "#0a0a14"], ["pix", 50, 109, "#2a2a3a"]]], ["rect", 50, 112, 66, 1, "#0a0a14"],
        ["repeat", 5, 8, 0, [["rect", 262, 110, 1, 12, "#0a0a14"], ["pix", 262, 109, "#2a2a3a"]]], ["rect", 262, 112, 34, 1, "#0a0a14"],
        ["fireflies", 0, 100, 320, 30, 6]
    ],
    "objects": [
        {"id": "puerta_ext", "state": "cerrada", "hotspot": False,
         "states": {"cerrada": {"draw": [["rect", 178, 90, 24, 30, "#4a2410"], ["rect", 189, 90, 2, 30, "#2a1408"], ["rect", 186, 104, 2, 2, "#e0c040"], ["rect", 192, 104, 2, 2, "#e0c040"]]},
                    "abierta": {"draw": [["rect", 178, 90, 24, 30, "#f0c060"], ["rect", 178, 90, 4, 30, "#4a2410"], ["light", 190, 110, 40, "255,200,120", 0.4]]}}}
    ]
}
R['exterior'] = exterior
g['music']['titulo'] = {"bpm": 76, "vol": 1, "tracks": [
    {"wave": "sawtooth", "vol": 0.13, "len": 1, "gate": 0.95, "attack": 0.01, "filter": ["lowpass", 2400, 1], "notes":
        "A5 G5 A5:6 -:2 G5 F5 E5 D5 C#5:4 | D5:12 -:4 | A4 G4 A4:6 -:2 E4:2 F4:2 C#4:4 | D4:12 -:4 | "
        "A3 G3 A3:6 -:2 G3 F3 E3 D3 C#3:4 | D3:16 | -:16 | -:16"},
    {"wave": "triangle", "vol": 0.25, "len": 16, "gate": 0.98, "notes": "D2 D2 A1 D2 D1 D1 G1 A1"},
    {"wave": "square", "vol": 0.05, "len": 1, "gate": 0.95, "notes":
        "A4 G4 A4:6 -:2 G4 F4 E4 D4 C#4:4 | D4:12 -:4 | -:16 | -:16 | -:16 | -:16 | -:16 | -:16"}]}

# intro
salon.pop('onEnter', None)
g['start'] = {"room": "exterior", "entry": "camino"}
g['intro'] = [
    {"banner": "LA MANSIÓN DEL DOCTOR CHIFLADO", "sub": "Una aventura de Tito", "style": "title", "time": 4.5},
    {"walk": [150, 130], "face": "right"},
    "Así que esta es la mansión del doctor Chiflado...",
    "Apuesto diez euros a que aquí no hay fantasmas.",
    {"walk": [190, 122], "face": "back"},
    S("chirrido"), {"state": ["puerta_ext", "abierta"]}, {"wait": 0.5},
    {"walk": [190, 120], "face": "back"}, {"hidePlayer": True},
    {"wait": 0.4}, {"state": ["puerta_ext", "cerrada"]}, S("portazo"), {"flash": True},
    {"banner": "¡BLAM!", "style": "super", "time": 1.2},
    {"say": "¡Eh! ¡¿Quién ha cerrado la puerta?!", "color": "#ffe25a"},
    {"goto": "salon", "entry": "inicio"}, {"showPlayer": True},
    "Genial. La puerta principal se ha cerrado sola detrás de mí.",
    "Qué raro que no haya nadie. Tengo que encontrar la forma de salir.",
    {"clock": "start"}
]
# final
pp = OBJ['puerta_principal']['verbs']
pp['IR A']['then'] = [
    {"walk": [240, 100], "face": "back"}, {"clock": "stop"},
    {"goto": "exterior", "entry": "puerta"}, {"music": "victoria"}, {"set": "final"}, {"state": ["puerta_ext", "abierta"]},
    {"walk": [110, 134], "face": "front"},
    {"banner": "¡¡LIBRE!!", "sub": "Tito ha escapado de la mansión", "style": "super", "time": 2.6, "sound": "wow"},
    "¡Y he ganado la apuesta!",
    {"face": "right"}, {"wait": 0.6},
    "...¿Esas notas musicales salen de las ventanas de arriba?",
    S("petardo"), {"wait": 0.4}, S("petardo"),
    "Bueno. Parece que la gala está siendo un éxito.",
    {"wait": 0.8},
    {"end": "¡Tito escapó de la mansión del doctor Chiflado y ganó la apuesta! Arriba nadie se enteró: estaban en plena gala."}
]

# ------------------------------------------------------------------ guardar
spec = importlib.util.spec_from_file_location('fm', 'fmt.py'); fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
order = ["title", "palette", "audio", "verbs", "defaultVerb", "lookVerb", "rightClickVerb", "pushVerb", "unreachable", "scoring", "defaults", "player", "voices", "sfx",
         "start", "intro", "items", "scripts", "music", "sounds", "sprites", "prefabs", "rooms"]
g = {k: g[k] for k in order if k in g} | {k: x for k, x in g.items() if k not in order}
g['rooms'] = {k: g['rooms'][k] for k in ['exterior', 'salon', 'vestibulo', 'pasillo', 'biblioteca', 'cocina', 'patio', 'sotano']}
out = fm.fmt(g) + '\n'; json.loads(out)
open('../aventura.json', 'w').write(out)
print('ok', len(out))
