from math import *
import random
from robot5 import robot


def run(param):
    myrobot = robot()
    myrobot.set(0.0,1.0,0.0)
    speed = 1.0
    N =100


    for i in range(N):

        crosstrack_error = myrobot.y
        steer = -param* crosstrack_error
        myrobot = myrobot.move(steer,speed)
        print myrobot, steer

        

    
run(0.1)
