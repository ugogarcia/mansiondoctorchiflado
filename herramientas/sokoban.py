# Solver del puzzle de la biblioteca (rejilla 10x3). Uso: python3 sokoban.py
from collections import deque
COLS, ROWS = 10, 3
def solve(fixed, movable, start, goal, maxd=40):
    fixed=set(fixed)
    def region(p, shelves):
        seen={p}; q=[p]
        while q:
            c,r=q.pop()
            for dc,dr in ((1,0),(-1,0),(0,1),(0,-1)):
                n=(c+dc,r+dr)
                if 0<=n[0]<COLS and 0<=n[1]<ROWS and n not in fixed and n not in shelves and n not in seen:
                    seen.add(n); q.append(n)
        return seen
    s0=frozenset(movable); reg=region(start,s0)
    key=lambda sh,reg: (sh,min(reg))
    Q=deque([(s0,start,[])]); seen={key(s0,reg)}
    while Q:
        sh,p,path=Q.popleft()
        reg=region(p,sh)
        if goal in reg: return path
        if len(path)>=maxd: continue
        for b in sh:
            for dc,dr in ((1,0),(-1,0),(0,1),(0,-1)):
                side=(b[0]-dc,b[1]-dr); tgt=(b[0]+dc,b[1]+dr)
                if side in reg and 0<=tgt[0]<COLS and 0<=tgt[1]<ROWS and tgt not in fixed and tgt not in sh:
                    ns=frozenset((sh-{b})|{tgt}); k=key(ns,region(b,ns))
                    if k not in seen:
                        seen.add(k); Q.append((ns,b,path+[(b,(dc,dr))]))
    return None
if __name__=='__main__':
    import sys
    L = [
      "...F...ZGF".replace('Z','.'),
    ]
