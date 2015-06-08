#wrong way of implementation ***********************


from math import *
import random


# ------------------------------------------------
# 
# this is the robot class
#

#------------------------------------------------ 

#noise parameters

steering_noise = 0.1
distance_noise  = 0.03
measurement_noise = 0.3

#-----------------------------------------------


# ------------------------------------------------
# 
# this is the particle filter class
#

class particles:

    # --------
    # init: 
    #	creates particle set with given initial position
    #

    def __init__(self, x, y, theta, 
                 steering_noise, distance_noise, measurement_noise, N = 100):
        self.N = N
        self.steering_noise    = steering_noise
        self.distance_noise    = distance_noise
        self.measurement_noise = measurement_noise
        
        self.data = []
        for i in range(self.N):
            r = robot()
            r.set(x, y, theta)
            r.set_noise(steering_noise, distance_noise, measurement_noise)
            self.data.append(r)


    # --------
    #
    # extract position from a particle set
    # 
    
    def get_position(self):
        x = 0.0
        y = 0.0
        orientation = 0.0

        for i in range(self.N):
            x += self.data[i].x
            y += self.data[i].y
            # orientation is tricky because it is cyclic. By normalizing
            # around the first particle we are somewhat more robust to
            # the 0=2pi problem
            orientation += (((self.data[i].orientation
                              - self.data[0].orientation + pi) % (2.0 * pi)) 
                            + self.data[0].orientation - pi)
        return [x / self.N, y / self.N, orientation / self.N]

    # --------
    #
    # motion of the particles
    # 

    def move(self, grid, steer, speed):
        newdata = []

        for i in range(self.N):
            r = self.data[i].move(grid, steer, speed)
            newdata.append(r)
        self.data = newdata

    # --------
    #
    # sensing and resampling
    # 

    def sense(self, Z):
        w = []
        for i in range(self.N):
            w.append(self.data[i].measurement_prob(Z))

        # resampling (careful, this is using shallow copy)
        p3 = []
        index = int(random.random() * self.N)
        beta = 0.0
        mw = max(w)

        for i in range(self.N):
            beta += random.random() * 2.0 * mw
            while beta > w[index]:
                beta -= w[index]
                index = (index + 1) % self.N
            p3.append(self.data[index])
        self.data = p3

    


#---------------------------------------------------------------------



class robot:


   

    # --------
    # init: 
    #    creates robot and initializes location/orientation to 0, 0, 0
    #

    def __init__(self, length = 0.5):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0
        self.num_collisions    = 0
        self.num_steps         = 0
        self.measurement_noise = 0.0


# --------
# set: 
#	sets a robot coordinate
#

    def set(self, new_x, new_y, new_orientation):

        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)


# --------
# set_noise: 
#	sets the noise parameters
#

    def set_noise(self, new_s_noise, new_d_noise, new_m_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)
        self.measurement_noise = float(new_m_noise)



#----------------
#check:
        #checks of the robot pose collides with a obstacle or is too far outside the plane

    def check_collision(self,grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    dist = sqrt((self.x - float(i))**2 + (self.y - float(j))**2)

                    if dist < 0.5:
                        self.num_collisions += 1
                        return False

        return True
                            
#--------------------
    def check_goal(self,goal,threshold=1.0):
        dist =sqrt((float(goal[0])-self.x)**2 + (float(goal[1])-self.y)**2)
        return dist < threshold

# --------
# set_steering_drift: 
#	sets the systematical steering drift parameter
#

    def set_steering_drift(self, drift):
        self.steering_drift = drift

# --------
# move: 
#    steering = front wheel steering angle, limited by max_steering_angle
#    distance = total distance driven, most be non-negative

    def move(self,grid, steering, distance, 
                     tolerance = 0.001, max_steering_angle = pi / 4.0):

        if steering > max_steering_angle:
                steering = max_steering_angle
        if steering < -max_steering_angle:
                steering = -max_steering_angle
        if distance < 0.0:
                distance = 0.0


        # make a new copy
        res = robot()
        res.length         = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = tan(steering2) * distance2 / res.length

        if abs(turn) < tolerance:

                # approximate by straight line motion

                res.x = self.x + (distance2 * cos(self.orientation))
                res.y = self.y + (distance2 * sin(self.orientation))
                res.orientation = (self.orientation + turn) % (2.0 * pi)

        else:

                # approximate bicycle model for motion

                radius = distance2 / turn
                cx = self.x - (sin(self.orientation) * radius)
                cy = self.y + (cos(self.orientation) * radius)
                res.orientation = (self.orientation + turn) % (2.0 * pi)
                res.x = cx + (sin(res.orientation) * radius)
                res.y = cy - (cos(res.orientation) * radius)

        return res

#-----------------------------


    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)


#-----------------------------

    def sense(self):
        return [random.gauss(self.x,self.measurement_noise),random.gauss(self.y,self.measurement_noise)]
#-----------------------------

    def measurement_prob(self,measurement):

        #compute error
        error_x = measurement[0] - self.x
        error_y = measurement[1] - self.y

        
        #calculate gaussian
        error = exp(-(error_x**2)/(self.measurement_noise **2)/2.0)\
                /sqrt(2.0 * pi *(self.measurement_noise **2))

        error *= exp(-(error_y **2)/(self.measurement_noise **2/2.0)\
                     /sqrt(2.0 * pi * (self.measurement_noise **2)))

        return error

#--------------------------------
    def run(self,grid,goal,spath,params,printflag = True, speed = 0.1, timeout = 1000):
        myrobot = robot()
        myrobot.set(0.,0.,0.)
        myrobot.set_noise(steering_noise,distance_noise,measurement_noise)
        filter = particles(myrobot.x,myrobot.y,myrobot.orientation,steering_noise
                        ,distance_noise,measurement_noise)

        cte = 0.0
        err = 0.0
        N = 0

        index = 0 #index into the path

        while not myrobot.check_goal(goal) and N < timeout:
            diff_cte = -cte
            #---------------------------------------------
            estimate  = filter.get_position()


            dx = spath[index+1][0] - spath[index][0]
            dy = spath[index+1][1] - spath[index][1]
            drx = estimate[0] - spath[index][0]
            dry = estimate[1] - spath[index][1]


            u = (drx*dx+dry*dy)/(dx*dx+dy*dy)

            cte = (dry*dx-drx*dy)/(dx*dx+dy*dy)


            if u > 1.0:
                index +=1
            
            cte =  spath[index][0] - spath[index][1]


            #---------------------------------------------


            diff_cte += cte

            steer = -params[0] * cte - params[1] * diff_cte

            myrobot = myrobot.move(grid,steer,speed)

            filter.move(grid,steer,speed)

            Z = myrobot.sense()

            filter.sense(Z)

            if not myrobot.check_collision(grid):
                print '####COLLISION####'

            err += (cte**2)

            N+=1

            if printflag:
                print myrobot,cte,index,u

        return [myrobot.check_goal(goal),myrobot.num_collisions,myrobot.num_steps]

           
    


#-------------------------
        
    def main(self,grid,init,goal,steering_noise,distance_noise,measurement_noise,
             weight_data,weight_smooth,p_gain,d_gain):
        #path = plan(grid,init,goal)
        path = self.astar(grid,init,goal)
        spath = self.smooth(path)
        return self.run(grid,goal,spath,[p_gain,d_gain])

#------------------------------------------------


    def astar(self,grid,init,goal):
       
        heuristic = [[10,9,8,7,6,5],
                     [9,8,7,6,5,4],
                     [8,7,6,5,4,3],
                     [7,6,5,4,3,2],
                     [6,5,4,3,2,1],
                     [5,4,3,2,1,0]]


        delta = [[-1,0],      #go up
                 [0,-1],      #go left
                 [1,0],       #go down
                 [0,1]]       #go right


        delta_name = ['^','<','v','>']

        cost = 1




        # open list elements are of the type: [g,x,y]

        closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
        closed[init[0]][init[1]] = 1


        action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]

        x = init[0]
        y = init[1]
        g = 0
        h = heuristic[x][y]
        f = g+h

        open = [[f,g,h,x,y]]  # g first for sorting purpose

        found = False # flag that is set when search is complete

        resign = False # flag set if we cant find expand

        count = 0


        path = [[x,y]]


        while found is False and resign is False:

            #check if we still have elments on the open list

            if len(open) == 0:
                resign = True
                print  'fail'

                #print '###### Search Terminated without success'

            else:
                # remove node from list
                open.sort()
                open.reverse()
                next = open.pop()

                #print 'take list item'
                #print next

                x = next[3]
                y = next[4]
                g = next[1]

                

                #check if we are done

                if x == goal[0] and y == goal[1]:
                    found = True
                    #print next
                    # print '##### Search successful'

                else:
                    #expand winning element and add to new open list
                    for i in range(len(delta)):
                        x2 = x + delta[i][0]
                        y2 = y + delta[i][1]

                        if  x2>=0 and x2 < len(grid) and y2 >=0 and  y2 < len(grid[0]):
                            if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                                g2 = g + cost
                                h2 = heuristic[x2][y2]
                                f2 = g2 + h2
                                open.append([f2,g2,h2,x2,y2])

                                path.append([x2,y2])

                                #print 'append list item'
                                #print [g2,x2,y2]
                                closed[x2][y2] = 1
                                action[x2][y2] = i  

                  
        return path


#----------------------------------------------------------------

    def smooth(self,path, weight_data = 0.5, weight_smooth = 0.1, tolerence = 0.000001):

        newpath = [[0 for row in range(len(path[0]))] for col in range(len(path))]

        for i in range(len(path)):
            for j in range(len(path[0])):
                newpath[i][j] = path[i][j]


        change  = tolerence

        while change >= tolerence:
            change = 0.0

            for i in range(1,len(path)-1):
                for j in range(len(path[0])):
                    aux = newpath[i][j]
                    newpath[i][j] += weight_data * (path[i][j] - newpath[i][j])
                    newpath[i][j] += weight_smooth * (newpath[i-1][j]+ newpath[i+1][j] - (2.0 * newpath[i][j]))
                    change += abs(aux - newpath[i][j])

        return newpath

#-------------------------------------------------------------------------

