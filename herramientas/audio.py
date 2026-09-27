# Añade música, efectos de sonido y voces a aventura.json (se ejecuta después de gen.py)
import json, importlib.util

g = json.load(open('../aventura.json'))
R = g['rooms']
OBJ = {o['id']: o for r in R.values() for o in r['objects']}

def S(name, **kw): return {"sound": name, **kw}
def pre(handler, *cmds):
    """Antepone comandos a un manejador (texto, comando o lista)."""
    if isinstance(handler, list): return list(cmds) + handler
    return list(cmds) + [handler]

# ------------------------------------------------------------------ ajustes globales
g['audio'] = {"master": 0.9, "music": 0.32, "sfx": 0.75}
g['sfx'] = {"pickup": "coger"}
g['voices'] = {
    "player":   {"pitch": 230, "wave": "sawtooth", "formant": 1.1, "vol": 0.42, "rate": 0.11},
    "default":  {"pitch": 160, "wave": "sawtooth", "formant": 0.9, "vol": 0.4, "rate": 0.12},
    "metalica": {"pitch": 82, "wave": "square", "formant": 0.7, "vol": 0.4, "rate": 0.15, "syllable": 0.11}
}
g['player']['voice'] = "player"

# ------------------------------------------------------------------ efectos de sonido (sintetizados)
g['sounds'] = {
    "trueno": {"layers": [
        {"wave": "noise", "dur": 2.8, "vol": 0.9, "attack": 0.04, "sustain": 0.12, "filter": ["lowpass", 700, 70, 0.7]},
        {"wave": "noise", "dur": 0.4, "vol": 0.45, "filter": ["bandpass", 1400, 300, 0.8]},
        {"wave": "sine", "freq": 58, "freqEnd": 28, "dur": 2.0, "vol": 0.55, "attack": 0.05}]},
    "tictac": {"range": 230, "layers": [
        {"wave": "square", "freq": 2400, "dur": 0.03, "vol": 0.45, "filter": ["bandpass", 3000, None, 6]},
        {"wave": "square", "freq": 1700, "dur": 0.03, "vol": 0.4, "delay": 1.0, "filter": ["bandpass", 2200, None, 6]}]},
    "campanada": {"layers": [
        {"wave": "sine", "freq": 523, "dur": 1.6, "vol": 0.35, "repeat": 3, "gap": 0.9},
        {"wave": "sine", "freq": 1311, "dur": 0.7, "vol": 0.12, "repeat": 3, "gap": 0.9},
        {"wave": "triangle", "freq": 261, "dur": 1.6, "vol": 0.22, "repeat": 3, "gap": 0.9}]},
    "chasquido": {"range": 200, "layers": [
        {"wave": "noise", "dur": 0.04, "vol": 0.3, "filter": ["highpass", 1500, None, 1]},
        {"wave": "noise", "dur": 0.03, "vol": 0.2, "delay": 0.07, "filter": ["bandpass", 3000, None, 2]}]},
    "tele_estatica": {"range": 190, "layers": [
        {"wave": "noise", "dur": 0.95, "vol": 0.22, "attack": 0.02, "sustain": 0.85, "filter": ["bandpass", 3500, None, 0.5]}]},
    "tele_on": {"layers": [
        {"wave": "sine", "freq": 90, "freqEnd": 40, "dur": 0.15, "vol": 0.6},
        {"wave": "sine", "freq": 7800, "dur": 1.2, "vol": 0.035, "delay": 0.1, "sustain": 0.8},
        {"wave": "noise", "dur": 0.7, "vol": 0.3, "delay": 0.1, "filter": ["bandpass", 3000, None, 0.6]}]},
    "tele_off": {"layers": [
        {"wave": "sine", "freq": 900, "freqEnd": 60, "dur": 0.25, "vol": 0.3},
        {"wave": "noise", "dur": 0.08, "vol": 0.2, "filter": ["highpass", 2000, None, 1]}]},
    "chillido": {"range": 320, "layers": [
        {"wave": "square", "freq": 3200, "freqEnd": 4800, "dur": 0.06, "vol": 0.16, "repeat": 3, "gap": 0.09},
        {"wave": "square", "freq": 2600, "freqEnd": 3900, "dur": 0.05, "vol": 0.1, "delay": 0.33, "repeat": 2, "gap": 0.08}]},
    "aleteo": {"range": 260, "layers": [{"wave": "noise", "dur": 0.07, "vol": 0.6, "filter": ["bandpass", 700, 300, 1.2]}]},
    "ladrido": {"range": 400, "layers": [
        {"wave": "sawtooth", "freq": 520, "freqEnd": 210, "dur": 0.16, "vol": 0.8, "filter": ["bandpass", 900, None, 1.5], "repeat": 2, "gap": 0.28},
        {"wave": "noise", "dur": 0.12, "vol": 0.22, "filter": ["bandpass", 1500, None, 1], "repeat": 2, "gap": 0.28}]},
    "grunido": {"range": 400, "layers": [
        {"wave": "sawtooth", "freq": 85, "dur": 0.9, "vol": 0.4, "attack": 0.1, "sustain": 0.6, "vibrato": [28, 12], "filter": ["lowpass", 500, None, 1]}]},
    "ronquido": {"range": 220, "layers": [
        {"wave": "noise", "dur": 1.1, "vol": 0.22, "attack": 0.5, "filter": ["lowpass", 420, None, 4]},
        {"wave": "sawtooth", "freq": 70, "dur": 1.0, "vol": 0.1, "attack": 0.5, "vibrato": [30, 8], "filter": ["lowpass", 300, None, 1]}]},
    "nom": {"range": 260, "layers": [{"wave": "noise", "dur": 0.05, "vol": 0.6, "filter": ["lowpass", 900, None, 1], "repeat": 3, "gap": 0.12}]},
    "silbido": {"layers": [{"wave": "sine", "freq": 1500, "freqEnd": 650, "dur": 0.5, "vol": 0.25}]},
    "chirrido": {"layers": [
        {"wave": "sawtooth", "freq": 190, "freqEnd": 430, "dur": 0.75, "vol": 0.75, "attack": 0.05, "sustain": 0.5, "vibrato": [22, 25], "filter": ["bandpass", 1100, None, 3]}]},
    "puerta_cierra": {"layers": [
        {"wave": "sine", "freq": 110, "freqEnd": 50, "dur": 0.25, "vol": 0.6},
        {"wave": "noise", "dur": 0.1, "vol": 0.3, "filter": ["lowpass", 800, None, 1]}]},
    "cerradura": {"layers": [
        {"wave": "square", "freq": 1800, "dur": 0.03, "vol": 0.2, "filter": ["bandpass", 2500, None, 4]},
        {"wave": "square", "freq": 900, "dur": 0.05, "vol": 0.25, "delay": 0.14, "filter": ["bandpass", 1200, None, 4]},
        {"wave": "noise", "dur": 0.06, "vol": 0.2, "delay": 0.14, "filter": ["highpass", 1500, None, 1]}]},
    "clic": {"layers": [
        {"wave": "square", "freq": 2000, "dur": 0.02, "vol": 0.22, "filter": ["bandpass", 2500, None, 3]},
        {"wave": "noise", "dur": 0.02, "vol": 0.15, "filter": ["highpass", 3000, None, 1]}]},
    "coger": {"layers": [
        {"wave": "pulse25", "note": "C6", "dur": 0.07, "vol": 0.18},
        {"wave": "pulse25", "note": "E6", "dur": 0.07, "vol": 0.18, "delay": 0.07},
        {"wave": "pulse25", "note": "G6", "dur": 0.14, "vol": 0.18, "delay": 0.14}]},
    "tintineo": {"layers": [
        {"wave": "triangle", "freq": 2600, "dur": 0.15, "vol": 0.2, "repeat": 3, "gap": 0.06},
        {"wave": "triangle", "freq": 3300, "dur": 0.1, "vol": 0.12, "delay": 0.03, "repeat": 3, "gap": 0.07}]},
    "golpe": {"layers": [
        {"wave": "sine", "freq": 140, "freqEnd": 50, "dur": 0.18, "vol": 0.6},
        {"wave": "noise", "dur": 0.06, "vol": 0.25, "filter": ["lowpass", 1200, None, 1]}]},
    "arrastre": {"layers": [
        {"wave": "noise", "dur": 2.0, "vol": 0.35, "attack": 0.1, "sustain": 0.8, "filter": ["bandpass", 350, 520, 3]},
        {"wave": "sawtooth", "freq": 60, "dur": 2.0, "vol": 0.14, "sustain": 0.8, "vibrato": [9, 15], "filter": ["lowpass", 260, None, 1]}]},
    "tiron": {"layers": [
        {"wave": "square", "freq": 600, "freqEnd": 1400, "dur": 0.35, "vol": 0.14, "vibrato": [40, 60], "filter": ["bandpass", 1200, None, 5]},
        {"wave": "sine", "freq": 180, "freqEnd": 60, "dur": 0.15, "vol": 0.5, "delay": 0.4}]},
    "tela": {"layers": [{"wave": "noise", "dur": 0.5, "vol": 0.55, "attack": 0.15, "filter": ["bandpass", 600, 2500, 1]}]},
    "nevera": {"layers": [
        {"wave": "noise", "dur": 0.12, "vol": 0.25, "filter": ["lowpass", 500, None, 1]},
        {"wave": "sine", "freq": 120, "dur": 1.4, "vol": 0.07, "delay": 0.1, "sustain": 0.8}]},
    "grifo": {"range": 200, "layers": [{"wave": "sine", "freq": 1300, "freqEnd": 2300, "dur": 0.08, "vol": 0.22}]},
    "goteo": {"range": 320, "layers": [{"wave": "sine", "freq": 900, "freqEnd": 1700, "dur": 0.1, "vol": 0.16}]},
    "burbujas": {"range": 180, "layers": [{"wave": "sine", "freq": 280, "freqEnd": 720, "dur": 0.06, "vol": 0.13, "repeat": 3, "gap": 0.11}]},
    "caldera": {"range": 280, "layers": [
        {"wave": "sawtooth", "freq": 42, "dur": 2.6, "vol": 0.35, "attack": 0.4, "sustain": 0.6, "vibrato": [5, 4], "filter": ["lowpass", 220, None, 1]},
        {"wave": "noise", "dur": 2.6, "vol": 0.12, "attack": 0.4, "sustain": 0.6, "filter": ["lowpass", 300, None, 1]}]},
    "zumbido": {"range": 160, "layers": [{"wave": "sawtooth", "freq": 100, "dur": 1.2, "vol": 0.05, "attack": 0.2, "sustain": 0.7, "filter": ["lowpass", 400, None, 1]}]},
    "grillo": {"layers": [{"wave": "sine", "freq": 4300, "dur": 0.035, "vol": 0.12, "repeat": 4, "gap": 0.05}]},
    "grillo2": {"layers": [{"wave": "sine", "freq": 3800, "dur": 0.03, "vol": 0.09, "repeat": 3, "gap": 0.06}]},
    "columpio": {"range": 220, "layers": [
        {"wave": "sawtooth", "freq": 300, "freqEnd": 390, "dur": 0.5, "vol": 0.3, "sustain": 0.4, "filter": ["bandpass", 900, None, 4]}]},
    "sin_linea": {"layers": [
        {"wave": "square", "freq": 950, "dur": 0.3, "vol": 0.1, "repeat": 3, "gap": 0.5},
        {"wave": "square", "freq": 1400, "dur": 0.3, "vol": 0.06, "repeat": 3, "gap": 0.5}]},
    "papel": {"layers": [{"wave": "noise", "dur": 0.3, "vol": 0.2, "attack": 0.05, "filter": ["highpass", 2500, None, 1]}]},
    "caida": {"layers": [
        {"wave": "triangle", "freq": 2400, "dur": 0.2, "vol": 0.25},
        {"wave": "triangle", "freq": 3100, "dur": 0.15, "vol": 0.15, "delay": 0.12}]},
    "metal": {"range": 300, "layers": [
        {"wave": "square", "freq": 620, "dur": 0.35, "vol": 0.4, "filter": ["bandpass", 1800, None, 8]},
        {"wave": "square", "freq": 931, "dur": 0.3, "vol": 0.3, "filter": ["bandpass", 2600, None, 8]}]},
    "sorpresa": {"layers": [
        {"wave": "pulse25", "note": "D5", "dur": 0.1, "vol": 0.15},
        {"wave": "pulse25", "note": "G#5", "dur": 0.25, "vol": 0.15, "delay": 0.1, "vibrato": [9, 20]}]}
}

# ------------------------------------------------------------------ música (tracker: nota:pasos, 1 paso = semicorchea)
g['music'] = {
    "mansion": {"bpm": 126, "vol": 1, "tracks": [
        {"wave": "triangle", "vol": 0.5, "len": 2, "gate": 0.55, "notes":
            "D2 A2 F2 A2 D2 A2 F2 A2 | D2 A2 F2 A2 D2 A2 C#3 A2 | A#1 F2 D2 F2 A#1 F2 D2 F2 | A1 E2 C#2 E2 A1 E2 G2 E2 | "
            "D2 A2 F2 A2 D2 A2 F2 A2 | G1 D2 A#1 D2 G1 D2 A#1 D2 | A#1 F2 D2 F2 A1 E2 C#2 E2 | D2 A2 D2 A1 D2 - - -"},
        {"wave": "pulse25", "vol": 0.14, "len": 2, "gate": 0.7, "vibrato": [6, 0.006], "notes":
            "D4 - F4 - A4 - G#4 A4 | A#4 - A4 - G4 F4 E4 - | F4 - D4 - A#3 - D4 F4 | E4:6 - C#4 E4 A4 - | "
            "D5 - C5 A4 A#4 - A4 F4 | G4 - A#4 - D5 C#5 D5 - | F5 - E5 D5 C#5 - E5 - | D5:4 A4 F4 D4:6 - | "
            "A4 - - A4 - - G#4 A4 | C5 - - A4 - - F4 - | D4 D4 F4 D4 A#3 - - - | C#4 E4 A4 C#5 E5 - - - | "
            "D5 - A4 - F4 - D4 - | G4 A#4 D5 A#4 G4 - D4 - | A#4 A4 G4 F4 E4 D4 C#4 E4 | D4:4 - - D3:4 -:4"},
        {"wave": "pulse12", "vol": 0.05, "len": 2, "gate": 0.4, "notes":
            "-:64 | -:64 | D5 F5 A5 F5 D5 F5 A5 F5 | D5 F5 A5 F5 C#5 E5 A5 E5 | D5 F5 A#5 F5 D5 F5 A#5 F5 | C#5 E5 A5 E5 C#5 E5 G5 E5 | -:64"},
        {"wave": "drums", "vol": 0.3, "len": 1, "notes": "k - h - s - h - k - h k s - h h"}]},
    "sotano": {"bpm": 70, "vol": 1, "tracks": [
        {"wave": "triangle", "vol": 0.45, "len": 16, "gate": 0.98, "notes": "D2 D2 G#1 A1"},
        {"wave": "sine", "vol": 0.16, "len": 2, "gate": 0.95, "vibrato": [5, 0.012], "notes":
            "-:8 A4:4 A#4:4 | A4:8 -:4 F4:2 E4:2 | -:8 D5:6 C#5:2 | C#5:12 -:4"},
        {"wave": "pulse12", "vol": 0.04, "len": 1, "gate": 0.5, "notes": "D6 - - - - - - - - - - - - - - - | -:16 | G#5 - - - - - - - - - - - - - - - | -:16"},
        {"wave": "drums", "vol": 0.18, "len": 4, "notes": "k - - - k - - -"}]},
    "noche": {"bpm": 92, "vol": 1, "tracks": [
        {"wave": "triangle", "vol": 0.4, "len": 16, "gate": 0.95, "notes": "D2 A#1 G1 A1"},
        {"wave": "pulse12", "vol": 0.07, "len": 2, "gate": 0.6, "notes":
            "D4 F4 A4 D5 A4 F4 D4 A3 | A#3 D4 F4 A#4 F4 D4 A#3 F3 | G3 A#3 D4 G4 D4 A#3 G3 D3 | A3 C#4 E4 A4 E4 C#4 A3 E3"},
        {"wave": "sine", "vol": 0.14, "len": 4, "vibrato": [5, 0.01], "notes": "-:16 | A4:8 G4:4 F4:4 | D4:12 -:4 | C#4:8 E4:8"}]},
    "victoria": {"bpm": 150, "loop": False, "vol": 1, "tracks": [
        {"wave": "pulse25", "vol": 0.18, "len": 2, "gate": 0.8, "notes": "A4 D5 F5 A5:4 G5 A5 A#5:4 A5:4 - D6:12"},
        {"wave": "triangle", "vol": 0.5, "len": 4, "gate": 0.8, "notes": "D3 A2 A#2 G2 A2 A2:2 D2:14"},
        {"wave": "drums", "vol": 0.3, "len": 2, "notes": "k h s h k h s h k k s s o:12"}]}
}
for rid, m in [('salon', 'mansion'), ('vestibulo', 'mansion'), ('cocina', 'mansion'), ('sotano', 'sotano'), ('patio', 'noche')]:
    R[rid]['music'] = m
R['salon']['stormSound'] = 'trueno'
R['vestibulo']['stormSound'] = 'trueno'

# ------------------------------------------------------------------ emisores de sonido (objetos que suenan solos)
OBJ['reloj']['sound'] = {"name": "tictac", "every": 2}
OBJ['chimenea']['sound'] = {"name": "chasquido", "every": [0.3, 1.4]}
OBJ['tele']['states']['nieve']['sound'] = {"name": "tele_estatica", "every": 0.85}
OBJ['tele']['states']['carta']['sound'] = {"name": "tele_estatica", "every": 0.85, "vol": 0.6}
OBJ['tele']['states']['apagada']['sound'] = {"name": "zumbido", "every": 1.1, "vol": 0.6}
OBJ['murcielago']['states']['vuela']['sound'] = {"name": "aleteo", "every": 0.17}
OBJ['perro']['states']['dentro']['sound'] = {"name": "ronquido", "every": 2.6}
OBJ['perro']['states']['duerme']['sound'] = {"name": "ronquido", "every": 2.6}
OBJ['perro']['states']['come']['sound'] = {"name": "nom", "every": 0.9}
OBJ['perro']['states']['quieto']['sound'] = {"name": "grunido", "every": [2.5, 4], "first": 1.2}
OBJ['fregadero']['sound'] = {"name": "grifo", "every": 1.7}
OBJ['fogon']['sound'] = {"name": "burbujas", "every": [0.5, 1.3]}
OBJ['caldera']['sound'] = {"name": "caldera", "every": 4.5}
OBJ['columpio']['sound'] = {"name": "columpio", "every": 1.7}
R['patio']['sounds'] = [{"name": "grillo", "every": [0.7, 2.0], "at": 320}, {"name": "grillo2", "every": [1.2, 3.0], "at": 150}]
R['sotano']['sounds'] = [{"name": "goteo", "every": [2.0, 4.5], "at": 200}]

# ------------------------------------------------------------------ voces de personajes
OBJ['perro']['voice'] = False
OBJ['caldera']['voice'] = False
OBJ['armadura']['voice'] = "metalica"

# ------------------------------------------------------------------ la tele se enciende sola al acercarte
R['salon'].setdefault('zones', []).append({
    "id": "tele_fantasma", "rect": [470, 0, 600, 144], "background": True,
    "if": "state:tele=apagada && !tele_susto",
    "onEnter": [{"set": "tele_susto"}, {"state": ["tele", "nieve"]}, S("tele_on", at="tele"), {"wait": 1.4},
                {"state": ["tele", "apagada"]}, S("tele_off", at="tele"), {"wait": 25}, {"unset": "tele_susto"}]})

# ------------------------------------------------------------------ efectos en las acciones
sc = g['scripts']
sc['quitar_freno'].insert(1, S("tiron"))
em = sc['empujar_mesa'][0]['else'][0]
em['then'].insert(0, S("golpe"))
em['else'].insert(1, S("arrastre"))
qa = sc['quitar_alfombra'][0]['else'][0]['else']
qa.insert(0, S("tela"))
qa.insert(2, S("sorpresa"))
sc['vuelo_murcielago'].insert(1, {"async": [{"wait": 1.0}, S("chillido", at="murcielago")]})
for branch in sc['vuelo_murcielago'][2]['random']:
    i = next(k for k, c in enumerate(branch) if c.get('state') == ['murcielago', 'colgado'])
    branch.insert(i + 1, S("chillido", at="murcielago"))
pl = sc['perro_ladra']
i = next(k for k, c in enumerate(pl) if isinstance(c, dict) and c.get('who') == 'perro')
pl.insert(i, S("ladrido", at="perro"))
dp = sc['distraer_perro']
dp.insert(dp.index("¡Eh, Firulais! ¡Mira lo que tengo!") + 1, S("silbido"))
i = next(k for k, c in enumerate(dp) if isinstance(c, dict) and c.get('who') == 'perro')
dp.insert(i, S("ladrido", at="perro"))
sc['periodico'].insert(0, S("papel"))

v = OBJ['trampilla']['verbs']
v['ABRIR']['then'].insert(0, S("chirrido"))
v['CERRAR']['then'] = [S("puerta_cierra"), v['CERRAR']['then']]
v = OBJ['puerta_salon']['verbs']
v['ABRIR']['then'] = [S("chirrido"), v['ABRIR']['then']]
v['CERRAR']['then'] = [S("puerta_cierra"), v['CERRAR']['then']]
v = OBJ['tele']['verbs']
v['ENCENDER']['then'].insert(0, S("tele_on", at="tele"))
v['APAGAR']['else'].insert(0, S("tele_off", at="tele"))
OBJ['reloj']['verbs']['MIRAR'] = [S("campanada"), {"wait": 0.6}, "Las doce en punto. Como el vídeo. Como siempre."]
v = OBJ['lampara']['verbs']
v['ENCENDER']['else'] = [S("clic"), v['ENCENDER']['else']]
v['APAGAR']['else'] = [S("clic"), v['APAGAR']['else']]
v = OBJ['interruptor']['verbs']
for k in ('ENCENDER', 'USAR', 'APAGAR'):
    for br in ('then', 'else'):
        if isinstance(v[k].get(br), list): v[k][br].insert(0, S("clic"))
v = OBJ['baul']['verbs']
v['ABRIR']['else'].insert(0, S("chirrido"))
v['CERRAR']['then'] = [S("puerta_cierra"), v['CERRAR']['then']]
lc = OBJ['llave_colgada']['verbs']['USAR:taco']
lc.insert(2, S("golpe"))
lc.insert(4, S("caida"))
v = OBJ['nevera']['verbs']
v['ABRIR']['else'].insert(0, S("nevera"))
v['CERRAR']['else'] = [S("puerta_cierra", vol=0.5), v['CERRAR']['else']]
v = OBJ['puerta_trasera']['verbs']
v['USAR:llave_patio'].insert(1, S("cerradura"))
v['USAR:llave_patio'].insert(3, S("chirrido"))
v = OBJ['puerta_principal']['verbs']
v['USAR:llave_porton'].insert(2, S("cerradura"))
v['USAR:llave_porton'].insert(4, S("chirrido"))
fin = v['IR A']['then']
fin.insert(len(fin) - 1, {"music": "victoria"})
fin.insert(len(fin) - 1, {"wait": 0.4})
OBJ['telefono']['verbs']['USAR'] = ["Descuelgo...", S("sin_linea"), {"wait": 1.2}, "No hay línea. Qué casualidad.", "Cuelgo."]
OBJ['telefono']['verbs']['COGER'] = OBJ['telefono']['verbs']['USAR']
h = OBJ['armadura']['verbs']['HABLAR']
h['do'].insert(2, S("metal", at="armadura"))
OBJ['armadura']['verbs']['EMPUJAR'] = [S("metal", at="armadura"), "¡Clonc! Mejor la dejo quieta."]
OBJ['caldera']['verbs']['HABLAR'].insert(1, S("caldera", at="caldera"))
OBJ['perro']['verbs']['HABLAR']['else'].insert(1, S("grunido", at="perro"))
OBJ['perro']['verbs']['HABLAR']['then'].insert(1, S("ladrido", at="perro", vol=0.6))
OBJ['llave_clavo']['verbs']['COGER'].insert(0, S("tintineo"))
OBJ['columpio']['verbs']['USAR'] = [S("columpio"), "No es momento de columpiarse. Aunque apetece."]

# ------------------------------------------------------------------ guardar con el mismo formato
spec = importlib.util.spec_from_file_location('gen_fmt', 'fmt.py')
fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
order = ["title", "palette", "audio", "verbs", "defaultVerb", "lookVerb", "rightClickVerb", "defaults", "player", "voices", "sfx",
         "start", "intro", "items", "scripts", "music", "sounds", "sprites", "prefabs", "rooms"]
g = {k: g[k] for k in order if k in g} | {k: x for k, x in g.items() if k not in order}
out = fm.fmt(g) + '\n'
json.loads(out)
open('../aventura.json', 'w').write(out)
print('ok', len(out))
