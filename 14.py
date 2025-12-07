from aoc_useful_functions import product, dict_adder
import time

file = r"[PATH]"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()

lines = [l[:-1] for l in lines]
lines = [l.split(" ") for l in lines]
lines = [[[int(x.split(",")[0][2:]), int(x.split(",")[1])] for x in l] for l in lines]

def picture(lines, height, width):
    d = {}
    for line in lines:
        d = dict_adder(d, tuple(line[0]), 1)

    ls = []
    for i in range(height):
        l = ''
        for j in range(width):
            if (j, i) in d:
                l += str(d[(j,i)])
            else:
                l += '.'

        ls.append(l)
        print(l)
    
    return None

def move_one_second(lines, height, width):
    lines = [[[(l[0][0] + l[1][0]) % width, (l[0][1] + l[1][1]) % height], l[1]] for l in lines]
    return lines

def move_n_seconds(n, lines, height, width):
    if n == 1:
        return move_one_second(lines, height, width)
    else:
        return move_one_second(move_n_seconds(n-1, lines, height, width), height, width)

def part1(lines, height, width):
    lines = move_n_seconds(100, lines, height, width)
    d = {}
    for line in lines:
        d = dict_adder(d, tuple(line[0]), 1)
    quads = []

    for i in range(2):
        midheight = int((height - 1)/2)
        midwidth = int((width - 1)/2)
        for j in range(2):
            quad = 0

            for el in d:
                if el[0] in range(j*(midwidth+1), j*(midwidth+1)+midwidth) and el[1] in range(i*(midheight+1), i*(midheight+1)+midheight):
                    quad += d[el]
            quads.append(quad)
    
    return product(quads)

#print(part1(lines, 103, 101))

#print(len(lines))
#print(101*103)
#expected_robots_per_square = len(lines)/(101*103)

# a christmas tree is pointy, so you would expect vastly more robots in the bottom than in the top of the picture
# the check below is tedious, partly because I expected the number of top robots to be much lower and the picture 
# be much bigger. But it worked for my input. 

def part2(lines):

    l = lines
    midheight = int((103+1)/2)
    for i in range(10000):
        l = move_one_second(l, 103, 101)
        toptop = 0
        d = {}
        for line in l:
            d = dict_adder(d, tuple(line[0]), 1)
        for el in d:
            if el[1] in range(0, int(midheight/2)):
                toptop += d[el]
        
        # unusually low number of robots at the very top
        if toptop < 41:
            print(i+1)
            picture(l, 103, 101)
            # wait enough time for me to verify
            # (I'm printing in the terminal so if I printed all at once some would be cut off)
            time.sleep(4)
    
    return None

