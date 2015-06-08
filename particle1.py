from math import *
import random

from robot import robot

world_size = 100.0

def evaluate(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))


myrobot = robot()

#myrobot.set(10.0,10.0,0.0)
#myrobot = myrobot.move(pi/2,10.0)
#print myrobot.sense()





print myrobot

N = 1000 #no of particles

T = 10

p = []

for i in range(N):
    x = robot()
    x.set_noise(0.05,0.05,5.0)
    p.append(x)

for t in range(T):

    myrobot = myrobot.move(0.1,5.0)

    Z = myrobot.sense() 

    p2 = []

    for i in range(N):
        p2.append(p[i].move(0.1,5.0))

    p = p2

    w = []

    for i in range(N):
        w.append(p[i].measurement_prob(Z))

    p3 = []

    index = int(random.random() * N)

    beta = 0.0

    mw = max(w)

    for i in range(N):
        beta += random.random() * 2.0 * mw
        while beta > w[index]:
            beta -=w[index]
            index = (index + 1)%N
        p3.append(p[index])

    p = p3


    print evaluate(myrobot,p) 



