# Música de taberna para la cocina + número de versión.
# Orden: gen.py -> audio.py -> story2.py -> story3.py -> story4.py -> story5.py -> story6.py -> build.py
import json, importlib.util, re
VERSION = "0.18"   # sube 1 en cada iteración

g = json.load(open('../aventura.json'))
g['version'] = "v" + VERSION

# ---------------------------------------------------------- "La taberna de Paco" (composición original, aire caribeño)
PROG = "G C D G G C D G Em C G D Em C D G".split()
mel = ["D4:2 G4:2 B4:3 A4:1 G4:4 D4:4", "E4:2 G4:2 C5:3 B4:1 A4:4 G4:4", "F#4:2 A4:2 D5:3 C5:1 B4:2 A4:2 F#4:4", "G4:6 A4:2 B4:8",
       "D5:2 B4:2 G4:2 B4:2 D5:3 E5:1 D5:4", "C5:2 E5:2 C5:2 A4:2 G4:3 A4:1 G4:4", "F#4:2 G4:2 A4:2 B4:2 C5:3 B4:1 A4:4", "G4:8 -:8",
       "B4:3 B4:1 B4:2 E5:2 D5:4 B4:4", "C5:3 C5:1 C5:2 E5:2 D5:4 C5:4", "B4:2 A4:2 G4:2 A4:2 B4:4 D5:4", "A4:12 -:4",
       "G4:2 B4:2 E5:3 D5:1 B4:4 G4:4", "E4:2 G4:2 C5:3 B4:1 A4:4 E4:4", "F#4:3 G4:1 A4:2 D5:2 C5:3 A4:1 F#4:4", "G4:4 D4:2 G4:2 G4:4 -:4"]
for b in mel: assert sum(int(t.split(':')[1]) for t in b.split()) == 16, b
def down(bar):  # una octava más grave (para el acordeón)
    return re.sub(r'([A-G]#?)(\d)', lambda m: m.group(1) + str(int(m.group(2)) - 1), bar)
BASS = {"G": "G2 - D2 - G2 - D2 F#2", "C": "C2 - G2 - C2 - G2 B1", "D": "D2 - A2 - D2 - F#2 -", "Em": "E2 - B2 - E2 - G2 -"}
HI = {"G": "D4", "C": "E4", "D": "F#4", "Em": "E4"}
LO = {"G": "B3", "C": "C4", "D": "A3", "Em": "B3"}
skank = lambda n: f"- {n} - {n} - {n} - {n}"
# segunda vuelta: el acordeón contesta con la melodía solo en la parte B
acc = ["-:16"] * 8 + [down(b) for b in mel[8:]]
g['music']['taberna'] = {"bpm": 104, "vol": 1, "tracks": [
    {"wave": "triangle", "vol": 0.24, "len": 2, "gate": 0.85, "notes": " | ".join(BASS[c] for c in PROG)},
    {"wave": "pulse12", "vol": 0.05, "len": 2, "gate": 0.3, "filter": ["lowpass", 2200, 1], "notes": " | ".join(skank(HI[c]) for c in PROG)},
    {"wave": "pulse12", "vol": 0.045, "len": 2, "gate": 0.3, "filter": ["lowpass", 2200, 1], "notes": " | ".join(skank(LO[c]) for c in PROG)},
    {"wave": "pulse25", "vol": 0.09, "len": 1, "gate": 0.55, "attack": 0.005, "notes": " | ".join(mel)},
    {"wave": "sawtooth", "vol": 0.06, "len": 1, "gate": 0.9, "attack": 0.04, "vibrato": [6, 0.01], "filter": ["lowpass", 1300, 1.5], "notes": " | ".join(acc)},
    {"wave": "drums", "vol": 0.13, "len": 1, "notes": "k - h - o - h h k - h - o - h -"}]}
g['rooms']['cocina']['music'] = 'taberna'

spec = importlib.util.spec_from_file_location('fm', 'fmt.py'); fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
keys = list(g.keys()); keys.remove('version'); keys.insert(keys.index('title') + 1, 'version')
g = {k: g[k] for k in keys}
out = fm.fmt(g) + '\n'; json.loads(out)
open('../aventura.json', 'w').write(out); print('ok', g['version'])
