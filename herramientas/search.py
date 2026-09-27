from sokoban import solve, COLS, ROWS
import random
random.seed(7)
G=(8,0); start=(0,1)
base_fixed=[(9,0),(4,2),(2,0)]   # estatua, escritorio, busto
best=[]
for it in range(300000):
    fixed=set(base_fixed)
    if random.random()<0.6: fixed.add((5,0))
    free=[(c,r) for c in range(1,COLS) for r in range(ROWS) if (c,r) not in fixed and (c,r)!=G and (c,r)!=start]
    n=random.randint(5,7)
    mov=random.sample(free,n)
    # G debe estar inicialmente cerrado
    from sokoban import solve as S
    sol0=S(fixed,mov,start,G,maxd=0)
    if sol0 is not None: continue
    # la zona inicial debe ser amplia (el bloqueo está junto a la sección Z)
    seen={start}; q=[start]
    while q:
        c,r=q.pop()
        for dc,dr in ((1,0),(-1,0),(0,1),(0,-1)):
            nb=(c+dc,r+dr)
            if 0<=nb[0]<COLS and 0<=nb[1]<ROWS and nb not in fixed and nb not in mov and nb not in seen: seen.add(nb); q.append(nb)
    if len(seen)<11: continue
    sol=S(fixed,mov,start,G,maxd=14)
    if sol and 6<=len(sol)<=10:
        best.append((len(sol),sorted(fixed),sorted(mov),sol))
        if len(best)>=12: break
best.sort(key=lambda x:-x[0])
for b in best[:6]:
    L,f,m,s=b
    rows=[''.join('G' if (c,r)==G else 'F' if (c,r) in f else 'M' if (c,r) in m else ('S' if (c,r)==start else '.') for c in range(COLS)) for r in range(ROWS)]
    print(L, rows, s)
