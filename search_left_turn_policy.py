#grid format
# 0 = navigable space
# 1 = occupied space

grid = [[1,1,1,0,0,0],
        [1,1,1,0,1,0],
        [0,0,0,0,0,0],
        [1,1,1,0,1,1],
        [1,1,1,0,1,1]]

goal = [2,0]

init = [4,3,0] #first 2 are co-ordinates, 3rd is direction


#there are four motion directions: up/left/down/right
#increasing the index in this array is taking of a left turn
#decreasing is a right turn

forward = [[-1, 0],   #go up
           [ 0,-1],   #go left
           [ 1, 0],   #go down
           [ 0, 1]]   #go right

forward_name = ['up','left','down','right']

#the cost filed has 3 values: right turn, no turn, left turn

cost = [1,1,210]      #action cost

action = [-1,0,1]

action_name = ['R','#','L']


#------------------------------------------------------------------

value = [[[999 for row in range(len(grid[0]))] for col in range(len(grid))],
         [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
         [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
         [[999 for row in range(len(grid[0]))] for col in range(len(grid))]]


policy= [[[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
         [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
         [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
         [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]]

policy2D =  [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

change = True



while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                for orientation in range(4):

                    if goal[0] == x and goal[1] == y:
                        if value[orientation][x][y] > 0:
                            value[orientation][x][y] = 0
                            policy[orientation][x][y] = '*'
                            change = True
                    elif grid[x][y] == 0:

                        # calculate the three ways to propogate value

                        for i in range(3):
                            o2 = (orientation + action[i])%4
                            x2 = x + forward[o2][0]
                            y2 = y + forward[o2][1]
                    

                            if  x2>=0 and x2 < len(grid) and y2 >=0 and  y2 < len(grid[0]) and grid[x2][y2]==0:
                                v2 = value[o2][x2][y2] + cost[i]

                                if v2 < value[orientation][x][y]:
                                    change = True
                                    value[orientation][x][y] = v2
                                    policy[orientation][x][y] = action_name[i]


x = init[0]
y = init[1]
orientation = init[2]

print policy[0][2][0]

policy2D[x][y] = policy[orientation][x][y]


while policy[orientation][x][y] != '*':
    if policy[orientation][x][y] == 'R':
        o2 = (orientation - 1)% 4
    elif policy[orientation][x][y] == 'L':
        o2 = (orientation + 1)%4
    elif policy[orientation][x][y] == '#':
        o2 = orientation

    x = x + forward[o2][0]
    y = y + forward[o2][1]

    orientation = o2

    policy2D[x][y] = policy[orientation][x][y]

for i in range(len(policy2D)):
    print policy2D[i]
    
        
         




