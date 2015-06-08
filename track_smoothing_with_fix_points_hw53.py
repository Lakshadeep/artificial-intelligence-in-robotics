# -------------
# User Instructions
#
# Now you will be incorporating fixed points into
# your smoother. 
#
# You will need to use the equations from gradient
# descent AND the new equations presented in the
# previous lecture to implement smoothing with
# fixed points.
#
# Your function should return the newpath that it
# calculates. 
#
# Feel free to use the provided solution_check function
# to test your code. You can find it at the bottom.
#
# --------------
# Testing Instructions
# 
# To test your code, call the solution_check function with
# two arguments. The first argument should be the result of your
# smooth function. The second should be the corresponding answer.
# For example, calling
#
# solution_check(smooth(testpath1), answer1)
#
# should return True if your answer is correct and False if
# it is not.

from math import *

# Do not modify path inside your function.
path=[[0, 0], #fix 
	  [1, 0],
	  [2, 0],
	  [3, 0],
	  [4, 0],
	  [5, 0],
	  [6, 0], #fix
	  [6, 1],
	  [6, 2],
	  [6, 3], #fix
	  [5, 3],
	  [4, 3],
	  [3, 3],
	  [2, 3],
	  [1, 3],
	  [0, 3], #fix
	  [0, 2],
	  [0, 1]]

# Do not modify fix inside your function
fix = [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]

######################## ENTER CODE BELOW HERE #########################

def smooth(path, fix, weight_data = 0.0, weight_smooth = 0.1, tolerance = 0.00001):
    # deep copy
    newpath = [[0 for col in range(len(path[0]))] for row in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]

    change = 1
    while change > tolerance:
        change = 0.0
        for i in range(len(path)):
            if not fix[i]:
                for j in range(len(path[0])):
                    aux = newpath[i][j]
                    newpath[i][j] += weight_data * (path[i][j] - newpath[i][j])
                    newpath[i][j] += weight_smooth * (newpath[(i-1) % len(path)][j] + newpath[(i+1) % len(path)][j] - 2.0 * newpath[i][j])
                    newpath[i][j] += 0.5 * weight_smooth * (2.0 * newpath[(i-1) % len(path)][j] - newpath[(i-2) % len(path)][j] - newpath[i][j])
                    newpath[i][j] += 0.5 * weight_smooth * (2.0 * newpath[(i+1) % len(path)][j] - newpath[(i+2) % len(path)][j] - newpath[i][j])
                    change += abs(aux-newpath[i][j])
    return newpath



#thank you - EnTerr - for posting this on our discussion forum

newpath = smooth(path,fix)
for i in range(len(path)):
   print '['+ ', '.join('%.3f'%x for x in path[i]) +'] -> ['+ ', '.join('%.3f'%x for x in newpath[i]) +']'
