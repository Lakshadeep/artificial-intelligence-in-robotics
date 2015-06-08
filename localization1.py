p = [0.2,0.2,0.2,0.2,0.2]

n = 5

world = ['green','red','red','green','green']

measurements = ['red','red']
motions = [1,1]

#for i in range(n):
#    p.append(1./n)

    
z = 'red'
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1


def sense(p,z):
    q =[]
    r = []
    for i in range(len(p)):
        hit = (z == world[i])
        q.append(p[i]*(hit*pHit + (1-hit)*pMiss))


    sum_p = sum(q)

    for k in range(len(p)):
        s  = q[k]/sum_p
        r.append(s)
        
    return r




def move(p,U):
    q = []
    for i in range(len(p)):
        s = pExact * p[(i-U)%len(p)]
        s = s + pOvershoot * p[(i-U-1)%len(p)]
        s = s+pUndershoot * p[(i-U+1)%len(p)]
        q.append(s)
    return q

for k in range(len(measurements)):
    p = sense(p,measurements[k])
    p = move(p,motions[k])    

##for i in range(1000):
##    p = move(p,1)
print p
