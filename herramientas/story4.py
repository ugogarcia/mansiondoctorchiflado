# Cocinero Paco (PNJ con rutina y conversación), iconos de objetos y poses de acción.
# Orden: gen.py -> audio.py -> story2.py -> story3.py -> story4.py -> build.py
import json, importlib.util

g = json.load(open('../aventura.json'))
R = g['rooms']
OBJ = {o['id']: o for r in R.values() for o in r['objects']}
def S(name, **kw): return {"sound": name, **kw}
def who(txt, w): return {"say": txt, "who": w}

# ------------------------------------------------------------------ poses de acción
g['verbPoses'] = {"COGER": "reach", "ABRIR": "reach", "CERRAR": "reach", "EMPUJAR": "push", "TIRAR": "reach", "QUITAR": "reach",
                  "USAR": "reach", "DAR": "give", "ENCENDER": "reach", "APAGAR": "reach", "GOLPEAR": "knock"}
for oid in ['freno', 'alfombra_mesa', 'trampilla', 'baul', 'cuenco', 'collar', 'perro', 'caseta']:
    if oid in OBJ: OBJ[oid]['pose'] = 'reach_low'
for oid in ['llave_colgada', 'arana1', 'arana2', 'bombilla', 'lampara_cocina', 'farol']:
    if oid in OBJ: OBJ[oid]['pose'] = 'reach_up'
g['items']['taco']['pose'] = 'taco'
g['items']['silbato']['pose'] = 'whistle'
g['items']['salchichas']['pose'] = 'give'
lc = OBJ['llave_colgada']['verbs']['USAR:taco']
lc.insert(lc.index("¡A ver con el taco...!") + 1, {"pose": "taco", "time": 0.9})
car = g['scripts']['carambola'][0]['else']
car.insert(1, {"pose": "taco", "time": 1.3})
gm = g['scripts']['golpe_murcielago']
gm.insert(1, {"pose": "taco", "time": 0.9})

# ------------------------------------------------------------------ iconos de los objetos del inventario (40x28)
icons = {
    "taco": [["line", 4, 24, 36, 5, "#d8b070"], ["line", 4, 25, 36, 6, "#b08850"], ["line", 3, 24, 14, 18, "#3a1a08"], ["line", 3, 25, 14, 19, "#5a2a10"],
             ["line", 3, 26, 13, 20, "#3a1a08"], ["rect", 35, 4, 3, 2, "#f0f0f0"], ["rect", 36, 3, 2, 2, "#4080ff"]],
    "nota": [["rect", 8, 3, 24, 22, "#f0ead8"], ["poly", [[26, 3], [32, 3], [32, 9]], "#c8c0a8"], ["repeat", 5, 0, 3, [["rect", 11, 7, 15, 1, "#8a8a9a"]]],
             ["rect", 11, 22, 9, 1, "#3a3a6a"], ["ring", 24, 19, 4, "#8a5a2a", 1], ["circle", 24, 19, 2, "rgba(138,90,42,0.45)"]],
    "llave_patio": [["ring", 10, 12, 5, "#c0c0c8", 2], ["rect", 15, 11, 16, 3, "#c0c0c8"], ["rect", 25, 14, 2, 3, "#c0c0c8"], ["rect", 29, 14, 2, 4, "#c0c0c8"],
                    ["rect", 15, 11, 16, 1, "#f0f0f8"], ["line", 8, 17, 6, 21, "#a08050"], ["rect", 1, 21, 14, 6, "#f0e0b0"], ["rect", 3, 23, 10, 1, "#6a4a20"], ["rect", 3, 25, 7, 1, "#6a4a20"]],
    "llave_porton": [["ring", 9, 14, 7, "#d8a830", 3], ["rect", 16, 12, 21, 4, "#d8a830"], ["rect", 29, 16, 3, 6, "#d8a830"], ["rect", 34, 16, 2, 4, "#d8a830"],
                     ["rect", 16, 12, 21, 1, "#fff0a0"], ["pix", 20, 14, "#8a5a20"], ["pix", 26, 13, "#8a5a20"], ["pix", 6, 9, "#fff0a0"], ["pix", 4, 12, "#fff0a0"]],
    "salchichas": [["ellipse", 7, 18, 5, 3, "#c06050"], ["ellipse", 16, 13, 5, 3, "#c06050"], ["ellipse", 25, 12, 5, 3, "#c06050"], ["ellipse", 33, 16, 5, 3, "#c06050"],
                   ["ellipse", 6, 17, 3, 1, "#e08878"], ["ellipse", 15, 12, 3, 1, "#e08878"], ["ellipse", 24, 11, 3, 1, "#e08878"], ["ellipse", 32, 15, 3, 1, "#e08878"],
                   ["pix", 11, 16, "#e8d8b0"], ["pix", 21, 12, "#e8d8b0"], ["pix", 29, 14, "#e8d8b0"]],
    "foto": [["rect", 7, 1, 26, 26, "#f4f4f0"], ["rect", 9, 3, 22, 17, "#6ab0e0"], ["rect", 9, 14, 22, 6, "#2a6aa8"], ["circle", 13, 6, 2, "#ffe060"],
             ["circle", 21, 8, 2, "#f0b088"], ["rect", 19, 9, 5, 1, "#3a2a1a"], ["rect", 19, 11, 5, 6, "#e02828"], ["rect", 19, 12, 5, 1, "#ffffff"], ["rect", 19, 14, 5, 1, "#ffffff"],
             ["rect", 19, 17, 1, 3, "#f0b088"], ["rect", 23, 17, 1, 3, "#f0b088"], ["rect", 17, 11, 2, 1, "#f0b088"], ["rect", 24, 10, 2, 1, "#f0b088"], ["rect", 11, 22, 18, 1, "#8a8a9a"]],
    "silbato": [["rect", 4, 13, 7, 4, "#a8a8b0"], ["rect", 10, 11, 16, 8, "#c8c8d0"], ["circle", 26, 15, 4, "#c8c8d0"], ["rect", 14, 11, 4, 2, "#2a2a30"],
                ["rect", 10, 11, 16, 1, "#ffffff"], ["ring", 31, 9, 3, "#a08040", 1], ["line", 29, 11, 31, 18, "#a08040"], ["rect", 27, 18, 11, 5, "#d8b050"], ["rect", 29, 20, 7, 1, "#6a4a20"]],
}
for k, v in icons.items():
    if k in g['items']: g['items'][k]['icon'] = v

# ------------------------------------------------------------------ sprite del cocinero (24x40, de frente y de espaldas)
def grid(): return [['.'] * 24 for _ in range(40)]
def rect(G, x, y, w, h, ch):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            if 0 <= xx < 24 and 0 <= yy < 40: G[yy][xx] = ch
def ell(G, cx, cy, rx, ry, ch):
    for yy in range(cy - ry, cy + ry + 1):
        for xx in range(cx - rx, cx + rx + 1):
            if ((xx - cx) / (rx + .5)) ** 2 + ((yy - cy) / (ry + .5)) ** 2 <= 1 and 0 <= xx < 24 and 0 <= yy < 40: G[yy][xx] = ch
def px(G, x, y, ch):
    if 0 <= x < 24 and 0 <= y < 40: G[y][x] = ch
def hat(G):
    ell(G, 12, 4, 6, 4, 'W'); ell(G, 7, 5, 3, 3, 'W'); ell(G, 17, 5, 3, 3, 'W')
    for x in (5, 19): px(G, x, 6, 'w')
    rect(G, 7, 8, 11, 2, 'W'); rect(G, 7, 9, 11, 1, 'w'); px(G, 10, 3, 'w'); px(G, 14, 2, 'w')
def legs(G, mode=0):
    for lx in (7, 14):
        short = (mode == 1 and lx == 7) or (mode == 2 and lx == 14)
        for yy in range(35, 38 if short else 39):
            for xx in range(lx, lx + 4): px(G, xx, yy, 'p' if (xx + yy) % 2 else 'P')
        rect(G, lx - 1, 38 if short else 39, 5, 1, 'k')
def body(G, back=False):
    ell(G, 12, 27, 10, 8, 'W')
    for yy in range(21, 34): px(G, 21, yy, 'w')
    if not back:
        rect(G, 9, 22, 7, 5, 'A'); rect(G, 6, 27, 13, 8, 'A'); rect(G, 6, 27, 1, 8, 'a'); rect(G, 18, 27, 1, 8, 'a')
        for x, y in ((8, 21), (16, 21), (8, 24), (16, 24)): px(G, x, y, 'w')
    else:
        rect(G, 3, 28, 18, 1, 'A'); px(G, 11, 27, 'A'); px(G, 13, 27, 'A'); px(G, 12, 28, 'a'); px(G, 11, 29, 'A'); px(G, 13, 29, 'A')
def arms_down(G, left=True, right=True):
    if left: rect(G, 0, 21, 3, 9, 'W'); rect(G, 0, 30, 3, 2, 's'); rect(G, 2, 21, 1, 9, 'w')
    if right: rect(G, 21, 21, 3, 9, 'W'); rect(G, 21, 30, 3, 2, 's'); rect(G, 21, 21, 1, 9, 'w')
def front(mouth=False, leg=0, arms='down', angry=False):
    G = grid(); legs(G, leg); body(G); hat(G)
    ell(G, 12, 14, 5, 4, 's'); px(G, 6, 14, 's'); px(G, 18, 14, 's'); rect(G, 9, 18, 7, 2, 'n')
    px(G, 10, 13, 'k'); px(G, 14, 13, 'k')
    if angry: px(G, 9, 11, 'm'); px(G, 10, 12, 'm'); px(G, 15, 11, 'm'); px(G, 14, 12, 'm'); px(G, 8, 14, 'r'); px(G, 16, 14, 'r')
    else: px(G, 9, 12, 'm'); px(G, 10, 12, 'm'); px(G, 14, 12, 'm'); px(G, 15, 12, 'm')
    px(G, 12, 14, 'r'); px(G, 12, 15, 'r'); px(G, 9, 15, 'r'); px(G, 15, 15, 'r')
    rect(G, 9, 16, 7, 1, 'm'); px(G, 8, 15, 'm'); px(G, 16, 15, 'm')
    if mouth: rect(G, 11, 17, 3, 1, 'k')
    if arms == 'down': arms_down(G)
    elif arms == 'wave': arms_down(G, right=False); rect(G, 20, 12, 3, 10, 'W'); rect(G, 20, 10, 3, 2, 's')
    elif arms == 'up': rect(G, 1, 12, 3, 10, 'W'); rect(G, 1, 10, 3, 2, 's'); rect(G, 20, 12, 3, 10, 'W'); rect(G, 20, 10, 3, 2, 's')
    return [''.join(r) for r in G]
def back(arm='down'):
    G = grid(); legs(G); body(G, back=True); hat(G)
    ell(G, 12, 14, 5, 4, 's'); px(G, 6, 14, 's'); px(G, 18, 14, 's'); rect(G, 8, 15, 9, 2, 'm'); rect(G, 9, 18, 7, 1, 'n')
    arms_down(G, right=(arm == 'down'))
    if arm == 'chop_up': rect(G, 19, 13, 3, 9, 'W'); rect(G, 19, 11, 3, 2, 's'); rect(G, 20, 6, 1, 5, 'g'); px(G, 20, 11, 'h')
    elif arm == 'chop_down': rect(G, 19, 20, 3, 6, 'W'); rect(G, 19, 26, 3, 2, 's'); rect(G, 22, 26, 2, 1, 'h'); rect(G, 22, 25, 2, 1, 'g')
    elif arm == 'stir_r': rect(G, 18, 20, 5, 3, 'W'); rect(G, 22, 19, 2, 2, 's'); rect(G, 22, 14, 1, 5, 'h')
    elif arm == 'stir_l': rect(G, 12, 20, 9, 3, 'W'); rect(G, 11, 19, 2, 2, 's'); rect(G, 11, 14, 1, 5, 'h')
    elif arm == 'reach': rect(G, 19, 9, 3, 13, 'W'); rect(G, 19, 7, 3, 2, 's')
    return [''.join(r) for r in G]

g['sprites']['cocinero'] = {
    "palette": {"W": "#f4f4f0", "w": "#b8bcc8", "s": "#f0b088", "k": "#1a1a1a", "m": "#4a2a14", "r": "#e06060", "n": "#d02828",
                "A": "#dce8f4", "a": "#a8b8cc", "p": "#2a2a2a", "P": "#e8e8e8", "g": "#c0c0c8", "h": "#6a3a18"},
    "anims": {
        "quieto": {"fps": 1, "frames": [front()]},
        "anda": {"fps": 6, "frames": [front(leg=1), front(leg=2)]},
        "habla": {"fps": 7, "frames": [front(mouth=True, arms='wave'), front(arms='wave')]},
        "enfado": {"fps": 8, "frames": [front(mouth=True, arms='up', angry=True), front(arms='up', angry=True)]},
        "corta": {"fps": 4, "frames": [back('chop_up'), back('chop_down')]},
        "remueve": {"fps": 3, "frames": [back('stir_r'), back('stir_l')]},
        "nevera": {"fps": 1, "frames": [back('reach')]}
    }}
g['voices']['cocinero'] = {"pitch": 112, "wave": "sawtooth", "formant": 0.75, "vol": 0.45, "rate": 0.12}
g['sounds'].update({
    "chop": {"range": 240, "layers": [{"wave": "noise", "dur": 0.05, "vol": 0.35, "filter": ["lowpass", 1400, None, 1]}, {"wave": "sine", "freq": 300, "freqEnd": 120, "dur": 0.05, "vol": 0.3}]},
    "tarareo": {"range": 260, "layers": [{"wave": "triangle", "note": n, "dur": 0.22, "vol": 0.14, "delay": i * 0.24, "vibrato": [6, 4]}
                                         for i, n in enumerate(["D4", "F4", "A4", "G4", "F4", "E4", "D4"])]}
})

# ------------------------------------------------------------------ cocinero en la cocina
cocina = R['cocina']
def sp(anim): return [["sprite", "cocinero", anim, -12, -40]]
cocina['objects'].append({
    "id": "cocinero", "name": "COCINERO", "x": 106, "y": 106, "state": "remueve", "voice": "cocinero", "textColor": "#ffd0a0",
    "box": [-12, -41, 24, 42], "walkTo": [30, 4], "face": "left", "pose": False,
    "when": "!cocinero_fuera",
    "talkDraw": sp("habla"),
    "states": {
        "quieto": {"draw": sp("quieto"), "sound": {"name": "tarareo", "every": [5, 8], "first": 2}},
        "anda": {"draw": sp("anda")},
        "habla": {"draw": sp("habla")},
        "enfado": {"draw": sp("enfado")},
        "corta": {"draw": sp("corta"), "sound": {"name": "chop", "every": 0.55}},
        "remueve": {"draw": sp("remueve")},
        "nevera": {"draw": sp("nevera")}
    },
    "verbs": {
        "MIRAR": "Un cocinero gordo con un gorro enorme. Tiene pinta de defender su nevera con la vida.",
        "HABLAR": [{"stop": "ronda_cocinero"}, {"set": "charlando"}, {"state": ["nevera", "cerrada"]}, {"state": ["cocinero", "quieto"]},
                   {"once": "saludo_paco", "do": who("¡Hombre, visita! ¿Tienes hambre? Pues te aguantas.", "cocinero"),
                    "else": who("¿Otra vez tú? ¿Qué quieres ahora?", "cocinero")},
                   {"dialog": "paco"}, {"unset": "charlando"}],
        "EMPUJAR": "Es como empujar un armario. Un armario con bigote.",
        "COGER": "No me cabe en el bolsillo. Ni en la habitación.",
        "DAR:foto": [who("¿El mayordomo en bañador? ¡Ja! Eso ya lo hemos visto todos.", "cocinero"), "Vaya. Qué poca exclusiva."],
        "DAR:salchichas": [who("¡Mis salchichas! ...Ah, no, ya las has cogido tú. ¡LADRÓN!", "cocinero")]
    }})
cocina['timers'] = [{"every": [2, 4], "first": 2, "if": "!cocinero_fuera && !charlando", "name": "ronda_cocinero", "script": "ronda_cocinero"}]
g['scripts']['ronda_cocinero'] = [{"random": [
    [{"state": ["cocinero", "anda"]}, {"path": ["cocinero", [[106, 106]], 26]}, {"state": ["cocinero", "remueve"]}, {"wait": [3, 6]}],
    [{"state": ["cocinero", "anda"]}, {"path": ["cocinero", [[152, 106]], 26]}, {"state": ["cocinero", "corta"]}, {"wait": [3, 6]}],
    [{"state": ["cocinero", "anda"]}, {"path": ["cocinero", [[66, 107]], 26]}, {"state": ["cocinero", "nevera"]}, {"state": ["nevera", "abierta"]}, S("nevera", at="nevera"),
     {"wait": 1.6}, {"state": ["nevera", "cerrada"]}, S("puerta_cierra", at="nevera", vol=0.4), {"state": ["cocinero", "quieto"]}, {"wait": 1.5}],
    [{"state": ["cocinero", "quieto"]}, {"wait": [2, 4]}]]}]
g['dialogs'] = {"paco": {"options": [
    {"text": "Rosita dice que subas a la gala con tu pandereta.", "if": "recado_rosita", "exit": True, "do": {"run": "cocinero_se_va"}},
    {"text": "¿Quién eres tú?", "once": True, "do": [who("Soy Paco, el cocinero de la mansión.", "cocinero"),
                                                   who("Y esta es MI cocina. MIS fogones. MI nevera. Y MIS salchichas.", "cocinero")]},
    {"text": "¿Qué estás cocinando?", "do": [who("¡Mi famoso cocido Chiflado! Lleva garbanzos, tocino y un calcetín.", "cocinero"), "¿Un calcetín?",
                                             who("¡Para el sabor, hombre!", "cocinero")]},
    {"text": "¿Me das algo de la nevera?", "do": [who("¡Ni hablar! Ahí dentro están mis salchichas de concurso.", "cocinero"),
                                                  who("Nadie toca esa nevera mientras yo esté en esta cocina.", "cocinero"),
                                                  "Mientras él esté en la cocina... Tengo que sacarlo de aquí."]},
    {"text": "¿Dónde está todo el mundo?", "do": [who("Arriba, ensayando para la gala de talentos. A mí nunca me invitan...", "cocinero"),
                                                  who("¡Y eso que toco la pandereta como nadie! Chin, chin, chin.", "cocinero"),
                                                  who("La gala la organiza Rosita, la inventora de la habitación 2. Pero me da vergüenza pedírselo...", "cocinero"), {"set": "sabe_rosita"}]},
    {"text": "Tu cocido huele fatal.", "once": True, "exit": True, "do": [{"state": ["cocinero", "enfado"]}, who("¡¿CÓMO DICES?! ¡Largo de mi cocina!", "cocinero"),
                                                                        {"state": ["cocinero", "quieto"]}]},
    {"text": "Nada, me voy.", "exit": True, "do": [who("¡Y no toques NADA!", "cocinero")]}
]}}
g['scripts']['cocinero_se_va'] = [
    who("¡¿ROSITA?! ¡¿Me quiere en la GALA?!", "cocinero"),
    who("¡Voy volando con mi pandereta! Tú vigílame el cocido... ¡y ni se te ocurra tocar mi nevera!", "cocinero"),
    {"state": ["cocinero", "anda"]}, {"path": ["cocinero", [[44, 106], [26, 103]], 48]}, S("chirrido"), {"hide": "cocinero"}, {"set": "cocinero_fuera"},
    "Bueno... yo no he prometido nada.", {"async": [{"wait": 2}, S("risitas", vol=0.9)]}]
# el cocinero protege la nevera, las salchichas y los fogones
nv = OBJ['nevera']['verbs']
enfado = lambda frase: [{"stop": "ronda_cocinero"}, {"state": ["cocinero", "enfado"]}, who(frase, "cocinero"), {"state": ["cocinero", "quieto"]}]
nv['ABRIR'] = {"if": "!cocinero_fuera", "then": enfado("¡QUIETO AHÍ! ¡Esa nevera es MÍA!") + ["Vale, vale. Qué carácter."], "else": nv['ABRIR']}
sn = OBJ['salchichas_nevera']['verbs']
sn['COGER'] = {"if": "!cocinero_fuera", "then": enfado("¡Eh! ¡Mis salchichas de concurso! ¡Fuera esas manos!"), "else": sn['COGER']}
fg = OBJ['fogon']['verbs']
old = fg['APAGAR']['else']
for c in old:
    if isinstance(c, dict) and c.get('say', '').startswith('(Desde arriba)'):
        c.update({"say": "(Desde arriba) ¡¡MI COCIDOOOOO!! ¡¿QUIÉN HA SIDO?!", "voice": "cocinero", "color": "#ffd0a0"})
fg['APAGAR'] = {"if": "!cocinero_fuera", "then": enfado("¡Ni se te ocurra tocar mis fogones, chaval!"), "else": fg['APAGAR']}
old = [c for c in old if c != "Ups. Creo que la cocinera tiene un oído finísimo."]
for c in old: pass
g_else = fg['APAGAR']['else']['else']
for i, c in enumerate(g_else):
    if c == "Ups. Creo que la cocinera tiene un oído finísimo.": g_else[i] = "Ups. Paco tiene un oído finísimo."
cocina['onEnter'] = [{"once": "cocina_primera", "do": ["La cocina. Aquí huele a puchero...", "...y hay un cocinero enorme vigilándolo."]}]

# ------------------------------------------------------------------ Rosita (puerta 2)
p2 = OBJ['puerta2']
p2['verbs']['MIRAR'] = "Habitación 2. Tiene una nota musical pintada. Se oye un «uuuuuh», como de película de marcianos."
g['scripts']['golpear_2'] = [
    S("toc_toc", at="puerta2"), {"state": ["puerta2", "silencio"]}, {"stop": "ruido_2"}, {"wait": 0.9},
    {"if": "cocinero_fuera",
     "then": [who("¡Ensayando! ¡Ji, ji!", "puerta2"), {"say": "¡Gracias por el recado, chaval! ¡Chin, chin, chin!", "who": "puerta2", "voice": "cocinero", "color": "#ffd0a0"}],
     "else": [who("¡Uy! ¡Qué susto!", "puerta2"),
              {"if": "sabe_rosita",
               "then": ["¿Es usted Rosita?", who("¡La misma! Inventora oficial de la mansión. Estoy probando mi theremín para la gala.", "puerta2"), "Paco, el cocinero, se muere por tocar la pandereta en la gala.",
                        who("¿Paco? ¡Justo me falta alguien con pandereta! Dile que suba ya, ¡ji, ji!", "puerta2"),
                        {"set": "recado_rosita"}, "Creo que acabo de fichar a un panderetero."],
               "else": [who("Si buscas algo, pregúntale al de la puerta 1, que es un ratón de biblioteca. ¡Ji, ji!", "puerta2"), "¿Quién será esta?"]}]},
    {"async": [{"wait": 7}, {"state": ["puerta2", "ruido"]}], "name": "ruido_2"}]

# ------------------------------------------------------------------ guardar
spec = importlib.util.spec_from_file_location('fm', 'fmt.py'); fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
order = ["title", "palette", "audio", "verbs", "defaultVerb", "lookVerb", "rightClickVerb", "pushVerb", "unreachable", "verbPoses", "scoring", "defaults", "player", "voices", "sfx",
         "start", "intro", "items", "scripts", "dialogs", "music", "sounds", "sprites", "prefabs", "rooms"]
g = {k: g[k] for k in order if k in g} | {k: x for k, x in g.items() if k not in order}
out = fm.fmt(g) + '\n'; json.loads(out)
open('../aventura.json', 'w').write(out)
print('ok', len(out))
