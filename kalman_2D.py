from matrix import matrix

measurements = [[5.,10.],[6.,8.],[7.,6.],[8.,4.],[9.,2.],[10.,1.]]

initial_xy = [4. ,12.]


dt = 0.1  #time interval

x = matrix([[initial_xy[0]],
            [initial_xy[1]],
            [0.],
            [0.]]) #initial state matrix

u = matrix([[0.],[0.],[0.],[0.]])  #external motion

P = matrix([[0. , 0. , 0. , 0. ],
            [0. , 0. , 0. , 0. ],
            [0. , 0. , 1000. , 0.],
            [0. , 0. , 0. , 1000.]]) #initial uncertainity (high for velocity)

F = matrix([[1. , 0. , dt , 0.],
            [0. , 1. , 0. , dt],
            [0. , 0. , 1. , 0.],
            [0. , 0. , 0. , 1.]])  #next state function


H = matrix([[1. , 0. , 0. , 0. ],
            [0. , 1. , 0. , 0. ]]) #measurement function


R = matrix([[0.1 , 0.],
            [0. , 0.1]])           #measurement uncertainty

I = matrix([[ 1. , 0. , 0. , 0. ],
            [ 0. , 1. , 0. , 0. ],
            [ 0. , 0. , 1. , 0. ],
            [ 0. , 0. , 0. , 1. ]])


def filter(x,P):
    for n in range(len(measurements)):
        #measurement update
        Z = matrix([measurements[n]])  #doesnt give proper results ...error can be here
       

        k = H*x
 
        Z.show()
       
        y = Z.transpose() - k

        S = H * P * H.transpose() + R

        K = P * H.transpose() * S.inverse()

        x = x + (K*y)

        P = (I - (K*H)) * P        

        #prediction

        x = (F * x) + u
        P = F * P * F.transpose()
         
        print 'x= '
        x.show()
        print 'P= '
        P.show()



print '### 4-dimensional example ###'

filter(x,P)





 






