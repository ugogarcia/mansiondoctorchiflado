# Pantalla de título previa a la intro (instrucciones + aviso de sonido; el clic activa el audio).
# Orden: gen.py -> audio.py -> story2.py -> story3.py -> story4.py -> story5.py -> build.py
import json, importlib.util
g = json.load(open('../aventura.json'))
g['titleScreen'] = {
  "title": ["LA MANSIÓN DEL", "DOCTOR CHIFLADO"],
  "sub": "UNA MINI AVENTURA GRÁFICA HECHA 100% POR IA",
  "spacing": 6,
  "howtoTitle": "CÓMO SE JUEGA",
  "howto": [
    "ELIGE UN VERBO Y HAZ CLIC EN ALGO.",
    "CLIC EN EL SUELO: ANDAR. DOBLE CLIC: ¡YA!",
    "ESC: SALTAR ESCENAS. ¡HAY PUNTOS EXTRA!"
  ],
  "warn": [
    "¡OJO! ESTO TIENE MÚSICA Y RUIDOS.",
    "¿REUNIÓN? ¿BIBLIOTECA? ¿BEBÉ DORMIDO?",
    "MIRA A TU ALREDEDOR... (M = SILENCIO)"
  ],
  "prompt": "HAZ CLIC PARA ACTIVAR EL SONIDO Y EMPEZAR"
}

# ------------------------------------------------------------------ créditos finales
import glob, os
def nlines(f): return sum(1 for _ in open(f, encoding='utf-8'))
L_MOTOR = nlines('../motor.html')
L_PY = sum(nlines(f) for f in glob.glob('*.py'))
L_JSON = nlines('../aventura.json')
L_PROTO = 847   # líneas del primer prototipo (mansion.html), que ya no está en el repositorio
N_ROOMS = len(g['rooms']); N_OBJ = sum(len(r['objects']) for r in g['rooms'].values())
N_SND = len(g['sounds']); N_MUS = len(g['music']); N_SCRIPTS = len(g['scripts'])
def pts(n): return f"{n:,}".replace(',', '.')
AI_TIME = "UNAS 3 HORAS Y MEDIA"     # estimación del procesamiento de la IA en toda la sesión
HUMAN_TIME = "UNOS 45 MINUTOS"       # estimación del tiempo escribiendo los prompts
PROMPTS = 13
g['creditsMusic'] = 'titulo'
g['creditsSpeed'] = 16
g['credits'] = [
  {"t": "LA MANSIÓN DEL"}, {"t": "DOCTOR CHIFLADO"},
  {"gap": 30},
  {"h": "TU PARTIDA", "color": "#ffe25a"},
  "TIEMPO: {TIEMPO}", "PUNTOS: {PUNTOS} DE {MAX}", {"c": "{RANGO}", "color": "#ff9ad0"},
  {"gap": 26},
  {"h": "PROTAGONISTA"}, "TITO, EL QUE APOSTÓ DIEZ EUROS",
  {"gap": 14},
  {"h": "REPARTO"},
  "PACO ...... COCINERO Y PANDERETERO",
  "ROSITA ...... INVENTORA Y THEREMINISTA",
  "FIRULAIS ........ EL PERRO",
  "EL DOCTOR CHIFLADO ... BAILARÍN DE TANGO",
  "EL MAYORDOMO ...... MONITOR DE AERÓBIC",
  "EL MURCIÉLAGO ...... ÉL MISMO",
  {"gap": 26},
  {"h": "GUION, GRÁFICOS, MÚSICA, SONIDO Y CÓDIGO"},
  "HECHO ÍNTEGRAMENTE POR IA",
  {"c": "(CLAUDE, DE ANTHROPIC)", "color": "#9090b0"},
  {"gap": 26},
  {"h": "EL RODAJE EN NÚMEROS", "color": "#ffe25a"},
  {"c": "TIEMPO DE PROCESAMIENTO DE LA IA", "color": "#9090b0"}, AI_TIME + " (APROX.)",
  {"gap": 6},
  {"c": "TIEMPO DEL HUMANO ESCRIBIENDO PROMPTS", "color": "#9090b0"}, HUMAN_TIME + " (APROX.)",
  {"gap": 6},
  {"c": "PROMPTS ESCRITOS", "color": "#9090b0"}, str(PROMPTS),
  {"gap": 6},
  {"c": "LÍNEAS DE CÓDIGO Y DATOS", "color": "#9090b0"},
  f"MOTOR DEL JUEGO: {pts(L_MOTOR)}",
  f"SCRIPTS DE PYTHON: {pts(L_PY)}",
  f"AVENTURA EN JSON: {pts(L_JSON)}",
  f"PROTOTIPO ORIGINAL: {pts(L_PROTO)}",
  f"TOTAL: {pts(L_MOTOR + L_PY + L_JSON + L_PROTO)}",
  {"gap": 6},
  {"c": "Y ADEMÁS", "color": "#9090b0"},
  f"{N_ROOMS} ESTANCIAS, {N_OBJ} OBJETOS, {N_SCRIPTS} GUIONES",
  f"{N_MUS} MELODÍAS Y {N_SND} EFECTOS DE SONIDO",
  "1 COCINERO GORDO",
  {"gap": 26},
  {"h": "AGRADECIMIENTOS"},
  "A LAS AVENTURAS GRÁFICAS DE LOS 80,",
  "POR LA INSPIRACIÓN",
  "A QUIEN PULSÓ SONIDO SÍ, SONIDO NO",
  {"gap": 14},
  {"c": "NINGÚN MURCIÉLAGO SUFRIÓ DAÑOS DURANTE EL RODAJE.", "color": "#9090b0"},
  {"c": "BUENO, UNO. PERO SE LO BUSCÓ.", "color": "#9090b0"},
  {"gap": 26},
  {"h": "CÓDIGO FUENTE"},
  "EL CÓDIGO ESTÁ EN GITHUB:",
  {"c": "HTTPS://GITHUB.COM/UGOGARCIA/MANSIONDOCTORCHIFLADO", "color": "#5ae0e0"},
  {"gap": 40},
  {"h": "UNA IDEA Y DIRECCIÓN DE", "color": "#ffe25a"},
  {"gap": 4},
  {"n": "UGO GARCIA"},
  {"gap": 30},
  {"t": "FIN"}
]
# el rótulo de la intro ya no repite el título a pantalla completa tanto rato
for c in g['intro']:
    if isinstance(c, dict) and c.get('style') == 'title': c['time'] = 3
spec = importlib.util.spec_from_file_location('fm', 'fmt.py'); fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
keys = list(g.keys())
for k in ['titleScreen','credits','creditsMusic','creditsSpeed']: keys.remove(k)
i0 = keys.index('start'); keys[i0:i0] = ['titleScreen','creditsMusic','creditsSpeed','credits']
g = {k: g[k] for k in keys}
out = fm.fmt(g) + '\n'; json.loads(out)
open('../aventura.json', 'w').write(out); print('ok', len(out))
