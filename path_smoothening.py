path = [[0,0],
        [0,1],
        [0,2],
        [1,2],
        [2,2],
        [3,2],
        [4,2],
        [4,3],
        [4,4]]


def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerence = 0.000001):

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

                    

#----------------------------------------------------------------------

newpath = smooth(path,0.5,0.1,0.000001)

for i in range(len(newpath)):
    print newpath[i]
