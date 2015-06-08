from math import *
import random
from robot5 import robot


def run(param,param2,param3):
    myrobot = robot()
    myrobot.set(0.0,1.0,0.0)
    speed = 1.0
    N =100
    myrobot.set_steering_drift(10.0/180.0*pi)  #10 degrees

    crosstrack_error = myrobot.y

    int_crosstrack_error = 0.0

    for i in range(N):
        diff_crosstrack_error = myrobot.y -crosstrack_error
        crosstrack_error = myrobot.y
        int_crosstrack_error += crosstrack_error
        steer = (-param * crosstrack_error)-(param2 * diff_crosstrack_error) - (param3* int_crosstrack_error)
        myrobot = myrobot.move(steer,speed)
        print myrobot, steer

        

    
run(0.2,3.0,0.004)
