file = r"c:\Users\jledg\Documents\not_backed_up\input8.txt"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()
lines = [line[:-1] for line in lines]

def find(char, grid):
    # find all coordinates of a given character
    inds = [(i, j) for i in range(len(grid)) for (j, x) in enumerate(grid[i]) if x == char]
    return inds

# the function below is from day 5
def all_tuples(l):
    # take a list and return a list l of tuples where for each tuple, the index of the first
    # element is less than the index of the second element in l
    tups = [(l[i], l[j]) for i in range(len(l)) for j in range(len(l)) if i < j]
    return tups

def find_pairs():
    # find all pairs of each character
    done = ['.']
    tups = []

    for line in lines:
        for char in line:
            if char in done:
                continue
            else:
                tups.append(all_tuples(find(char, lines)))
                done.append(char)

    return tups

def distance(c1, c2):
    vi = c2[0] - c1[0]
    vj = c2[1] - c1[1]
    return (vi, vj)

def bound(l, length):
    # take a list of coordinates and return only those within the bounds of the grid
    nl = [el for el in l if (el[0] >= 0 and el[0] < length[0] and el[1] >= 0 and el[1] < length[1])]
    return nl

def part1():
    antinodes = []
    tups = find_pairs()

    for char_type in tups:
        for pair in char_type:
            d = distance(pair[0], pair[1])
            n1 = (pair[0][0]-d[0], pair[0][1]-d[1])
            n2 = (pair[1][0]+d[0], pair[1][1]+d[1])
            antinodes.append(n1)
            antinodes.append(n2)
    
    # remove repeats and out of bounds coords
    antinodes = list(set(bound(antinodes, (len(lines[0]), len(lines)))))
    antinodes.sort()

    return len(antinodes)
    
def part2():
    antinodes = []
    tups = find_pairs()

    for char_type in tups:
        for pair in char_type:
            d = distance(pair[0], pair[1])
            k = 0
            # slightly lazy and inefficient while loops
            # will end up with out of bounds coords and duplicates but I remove them later
            while (pair[0][0]-k*d[0] >= 0) and (pair[0][0]-k*d[0] < len(lines[0])):
                antinodes.append((pair[0][0]-k*d[0], pair[0][1]-k*d[1]))
                k += 1

            k = 0
            while (pair[1][0]+k*d[0] >= 0) and (pair[1][0]+k*d[0] < len(lines[0])):
                antinodes.append((pair[1][0]+k*d[0], pair[1][1]+k*d[1]))
                k += 1
        
    antinodes = list(set(bound(antinodes, (len(lines[0]), len(lines)))))
    antinodes.sort()

    return len(antinodes)

print(part2())