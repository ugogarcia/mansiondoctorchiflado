import json

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

