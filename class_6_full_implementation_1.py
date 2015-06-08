from math import *
import random
from robot6 import robot


#------------------------------------------------ 

#noise parameters

steering_noise = 0.1
distance_noise  = 0.03
measurement_noise = 0.3

#-----------------------------------------------


#wrong way of implementation ***********************



#input data and parameters

grid = [[0,1,0,0,0,0],
        [0,1,0,1,1,0],
        [0,1,0,1,0,0],
        [0,0,0,1,0,1],
        [0,1,0,1,0,0]]

init = [0,0]
##
goal = [len(grid)-1,len(grid[0])-1]
##
myrobot = robot()
##
myrobot.set_noise(steering_noise,distance_noise,measurement_noise)
##
##while not myrobot.check_goal(goal):
##
##    theta = atan2(goal[1] - myrobot.y,goal[0] - myrobot.x) - myrobot.orientation
##    myrobot = myrobot.move(grid,theta,0.1)
##    if not myrobot.check_collision(grid):
##        print '######COLLISION######'
##    print myrobot
##

    
    


weight_data       = 0.1
weight_smooth     = 0.2
p_gain            = 2.0
d_gain            = 6.0

    
print myrobot.main(grid,init,goal,steering_noise,distance_noise,measurement_noise,
             weight_data,weight_smooth,p_gain,d_gain)


