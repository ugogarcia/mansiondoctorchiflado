import json
g=open('../aventura.json').read(); json.loads(g)
t=open('../motor.html').read()
assert '/*GAME_JSON*/' in t
open('../index.html','w').write(t.replace('/*GAME_JSON*/', g))
print('ok', len(g))
