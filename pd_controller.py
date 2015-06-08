from math import *
import random
from robot5 import robot


def run(param,param2):
    myrobot = robot()
    myrobot.set(0.0,1.0,0.0)
    speed = 1.0
    N =100

    crosstrack_error = myrobot.y

    for i in range(N):
        diff_crosstrack_error = myrobot.y -crosstrack_error
        crosstrack_error = myrobot.y
        steer = (-param * crosstrack_error)-(param2 * diff_crosstrack_error)
        myrobot = myrobot.move(steer,speed)
        print myrobot, steer

        

    
run(0.2,3.0)
