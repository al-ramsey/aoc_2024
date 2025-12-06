'''
Context for why this file is so long:

I did part 1 by brute force, which doesn't work for part 2 because the inputs are just too big. 
To solve the problem "efficiently", you need to know all solutions to an equation of the form
aX + bY = c. There are no solutions unless c = mgcd(a, b) for some m. If you have one solution, 
you can easily find all others, so the problem reduces to finding one solution. Usually this 
is done by using the extended Euclidian algorithm to find Bezout coefficients n, p such that 
gcd(a, b) = na + pb. Then mna + mpb = c. But the extended Euclidean algorithm involves a LOT
of recursion, and since the numbers are so big I ended up constantly hitting the maximum
recursion depth.

The equations we needed to solve were of the form:
aX + bY = c
a'X + b'Y = c'
Matrix methods solve this easily, as long as the matrix isn't singular (in which case you have
lots of solutions, and you need to choose the best one in the problem). I was worried about 
the singular case, which is why I did all the diophantine nonsense, but it turns out
(presumably by design) that the singular case never happens. There go several hours of my life!
'''

from aoc_useful_functions import *
from math import gcd, floor, ceil
import sys

#sys.setrecursionlimit(1000000)

file = r"[PATH]"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()

lines = [l[:-1] for l in lines]

def ABprize_trimmer(i, p):
    #print("new!")
    l = [lines[4*j+i] for j in range((int((len(lines)+1)/4)))]
    #print(l)
    l = [el.split(" ") for el in l]
    #print(l)
    l = [[int(el[2-p][2:-1]), int(el[3-p][2:])] for el in l]
    #print(l)
    return l

As = ABprize_trimmer(0, 0)
Bs = ABprize_trimmer(1, 0)
prizes = ABprize_trimmer(2, 1)

def max_times_to_press(button, maxvals):
    # button, maxvals of the form [X,Y]
    # returns maximum number of times you can press the button while still being under maxvals
    maxX = floor(maxvals[0]/button[0])
    maxY = floor(maxvals[1]/button[1])
    return min(maxX, maxY)

def part1():

    tot = 0
    for i in range(len(As)):
        possible_tokens_spent = []
        gX = gcd(As[i][0], Bs[i][0])
        gY = gcd(As[i][1], Bs[i][1])

        # solution is only possible in this case (diophantine eqns of the form aX + bY = c)
        if (prizes[i][0] % gX == 0) and (prizes[i][1] % gY == 0):
            maxA = max_times_to_press(As[i], prizes[i])
            # brute force
            for j in range(min(100, maxA)):
                pressX = prizes[i][0] - (j+1)*As[i][0]
                pressY = prizes[i][1] - (j+1)*As[i][1]

                if pressX % Bs[i][0] == 0 and pressY % Bs[i][1] == 0:
                    if int(pressX/Bs[i][0]) == int(pressY/Bs[i][1]):
                        possible_tokens_spent.append([j+1, int(pressX/Bs[i][0])])
                        break
            
            possible_tokens_spent = [3*el[0] + el[1] for el in possible_tokens_spent]
            if possible_tokens_spent != []:
                tot += min(possible_tokens_spent)

    return tot

#print(part1())

def diophantine_solutions(a, b, c):
    # all positive solutions to ax + by = c
    # need a > b
    g = gcd(a, b)
    sols = []
    if c % g != 0:
        return sols
    else:
        m = int(c/g)
        albe = bezout(a,b)
        x = m*albe[0]
        y = m*albe[1]
        u = int(a/g)
        v = int(b/g)
        for k in range(-ceil(x/v), ceil(y/u)+1):
            sols.append((x+k*v, y - k*u))
        
        return sols

def backsubs(rs, ms):
    if len(rs) == 1:
        alpha = 1
        beta = -1*ms[0]
        return (alpha, beta)
    elif len(rs) == 2:
        alpha = -1*ms[-1]
        beta = 1 + ms[0]*ms[1]
        return (alpha, beta)
    else:
        albe1 = backsubs(rs[:-2], ms[:-2])
        albe2 = backsubs(rs[:-1], ms[:-1])
        alpha = albe1[0] - albe2[0]*ms[-1]
        beta = albe1[1] - albe2[1]*ms[-1]
        return (alpha, beta)

def bezout(a, b):
    # requires b < a
    r = a % b
    rs = []
    m = int((a-r)/b)
    ms = []

    while r != 0:
        rs.append(r)
        ms.append(m)
        a = b
        b = r
        r = a % b
        m = int((a-r)/b)

    return backsubs(rs, ms)

prizes = [[p[0] + 10000000000000, p[1]+10000000000000] for p in prizes]

'''
this solution hits the maximum recursion depth no matter how high I set it. 

def part2():

    tot = 0
    for i in range(len(As)):
        if As[i][0] >= Bs[i][0]:
            possible_sols1 = diophantine_solutions(As[i][0], Bs[i][0], prizes[i][0])
        else:
            possible_sols1 = diophantine_solutions(Bs[i][0], As[i][0], prizes[i][0])
            possible_sols1 = [tuple(reversed(list(s))) for s in possible_sols1]
        if As[i][1] >= Bs[i][1]:
            possible_sols2 = diophantine_solutions(As[i][1], Bs[i][1], prizes[i][1])
        else:
            possible_sols2 = diophantine_solutions(Bs[i][1], As[i][1], prizes[i][1])
            possible_sols2 = [tuple(reversed(list(s))) for s in possible_sols2]
        possible_sols = list(set(possible_sols1).intersection(set(possible_sols2)))
        possible_tokens = [3*el[0] + el[1] for el in possible_sols]
        if possible_tokens != []:
            tot += min(possible_tokens)

    return tot
'''
# trivial solution actually works

def part2():
    tot = 0
    for i in range(len(As)):
        # if determinant of matrix is nonzero
        if As[i][0]*Bs[i][1] - As[i][1]*Bs[i][0] != 0:
            det = (As[i][0]*Bs[i][1] - As[i][1]*Bs[i][0])
            alpha = (1/det)*(Bs[i][1]*prizes[i][0] - Bs[i][0]*prizes[i][1])
            beta = (1/det)*(-As[i][1]*prizes[i][0] + As[i][0]*prizes[i][1])

            # this originally checked if floor == ceil, but I ran into floating point errors
            if (Bs[i][1]*prizes[i][0] - Bs[i][0]*prizes[i][1]) % det == 0 and (-As[i][1]*prizes[i][0] + As[i][0]*prizes[i][1]) % det == 0:
                if alpha >= 0 and beta >= 0:
                    tot += 3*round(alpha)+round(beta)

        elif As[i][0]/As[i][1] == Bs[i][0]/Bs[i][1]:
            print("whoops, you needed Diophantine equations after all")
    
    return tot

#print(part1())
#print(part2())