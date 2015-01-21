# Prototype code to implement a linear time algorithm for finding the
# interseciton of 2 2D, convex polygons.  Algorithm from Computational
# Geometry in C by O'Rourke.

# to represent the quad
#P = [[1.0,1.0],[2.0,1.0],[2.0,2.0],[1.0,2.0]]
#n=4

# to represent the intersection of the tet with the quad plane
# first a simple case
#Q = ((1.5,1.5),(3.0,1.5),(1.5,3.0))
#m=3
#inP = (0, 0, 1, 0)
#inQ = (1, 0 , 0)
# answer should be ((1.5,1.5), (2.0,1.5), (2.0,2.0), (1.5,2.0))

#Q = ((1.5,1.5),(3.0,1.75),(1.75,3.0))
#m=3
#inP = (0, 0, 1, 0)
#inQ = (1, 0 , 0)
# answer should be ((1.5,1.5), (2.0,1.5833), (2.0,2.0), (1.5833,2.0))

#Q = [[1.5,.6],[2.4,1.5],[1.5,2.4],[.6,1.5]]
#m=4
# answer should be
# move to  [1.0, 1.1000000000000001]
# line to [1.0, 1.1000000000000001]
# line to [1.0999999999999999, 1.0]
# line to [1.8999999999999999, 1.0]
# line to [2.0, 1.1000000000000001]
# line to [2.0, 1.9000000000000001]
# line to [1.8999999999999999, 2.0]
# line to [1.1000000000000001, 2.0]
# line to [1.0, 1.8999999999999999]

# a special case where a point in Q is on one of the segments in P
#Q = [[1.5,1.5],[2.0,1.5],[1.5,1.75]]
#m=3
# this case breaks the code given by O'Rourke

# case from code
Q = [[17,19],[17,20],[16,20],[16,19]]
m=4

P = [[16.66666,19], [19,16.66666], [20, 17.66666], [17.66666,20]]
n=4


def MoveTo(p):
    print "move to ", p

def LineTo(p):
    print "line to", p

# 2D cross product of A-O and B-O
def AreaSign( O, A, B):
    return (A[0]-O[0])*(B[1]-O[1]) - (A[1]-O[1])*(B[0]-O[0])

def ParallelInt(a, b, c, d, p):
    return 'e'

def InOut(p, inflag, aHB, bHA):

    LineTo(p)

    if aHB > 0:
        return 'Pin'
    if bHA > 0:
        return 'Qin'
    else: 
        return inflag
        

def SegSegInt(a, b, c, d, p):

    code = -1

    denom = a[0] * (d[1] - c[1]) + b[0] * (c[1] - d[1]) + d[0] * (b[1] - a[1]) + c[0] * (a[1] - b[1])
    if denom == 0.0:
        return ParallelInt(a, b, c, d, p)
    
    num = a[0] * (d[1] - c[1]) + c[0] * (a[1] - d[1]) + d[0] * (c[1] - a[1])  
    if num == 0.0 or num == denom:
        code = 'v';
    s = num / denom

    num = - (a[0] * (c[1] - b[1]) + b[0] * (a[1] - c[1]) + c[0] * (b[1] - a[1]) )    
    if num == 0.0 or num == denom:
        code = 'v';
    t = num / denom

    if s > 0.0 and s < 1.0 and t > 0.0 and t < 1.0 :
        code = '1'
    elif s < 0.0 and s > 1.0 and t < 0.0 and t > 1.0:
        code = '0'
    
    p[0] = a[0] + s * (b[0] - a[0]);
    p[1] = a[1] + s * (b[1] - a[1]);

    return code

def Advance(a, aa, n, inside, v):
    if(inside):
        LineTo(v)
    aa += 1
    return (a+1) % n, aa
        

a = 0
b = 0
aa = 0
ba = 0
inflag = 'unknown'
firstPoint = True
p0 = [0.0,0.0]
loopcontrol = 0

while ( (aa < n or ba < m) and aa < 2*n and ba < 2*m and loopcontrol < 10) :

    loopcontrol += 1

    a1 = (a + n - 1) % n
    b1 = (b + m - 1) % m

    print "\n"
    print "P seg", P[a1], P[a]
    print "Q seg", Q[b1], Q[b]

    A = (P[a][0] - P[a1][0], P[a][1] - P[a1][1])
    B = (Q[b][0] - Q[b1][0], Q[b][1] - Q[b1][1])

    cross = AreaSign((0.0,0.0),A,B)
    aHB = AreaSign(Q[b1], Q[b], P[a])
    bHA = AreaSign(P[a1], P[a], Q[b])

    p = [0.0,0.0]
    code = SegSegInt( P[a1], P[a], Q[b1], Q[b], p)

    print cross, aHB, bHA, inflag
    print "intersection code ", code

    if code == '1' or code == 'v':
        #print "intersection at ", p
        if inflag == "unknown" and firstPoint:
            aa = ba = 0;
            firstPoint = False
            p0[0] = p[0]
            p0[1] = p[1]
            MoveTo(p0)
        inflag = InOut(p, inflag, aHB, bHA)
        #print inflag

    # advance rules
    # special cases

    # A & B overlap and are oppositely oriented
    if code == 'e' and A[0]*B[0]+A[1]*B[1] < 0:
        print "no intersection of polys"
        break

    # A & B parallel but separate
    elif cross == 0 and aHB < 0 and bHA < 0:
        print "P and Q are disjoint"
        break

    # A & B collinear
    elif cross == 0 and aHB == 0 and bHA == 0:
        if inflag == 'Pin':
            b = Advance(b, ba, m, inflag == 'Qin', Q[b])
        else:
            a = Advance(a, aa, n, inflag == 'Pin', P[a])
        
    # general cases
    elif cross >= 0:
        if bHA > 0:
            a, aa = Advance(a, aa, n, inflag == 'Pin', P[a])
        else:
            b, ba = Advance(b, ba, m, inflag == 'Qin', Q[b])

    else: # cross < 0 
        if aHB > 0:
            b, ba = Advance(b, ba, m, inflag == 'Qin', Q[b])
        else:
            a, aa = Advance(a, aa, n, inflag == 'Pin', P[a])
    
