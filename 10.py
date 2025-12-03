file = r"[PATH]" # change to path to file
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()

lines = [line[:-1] for line in lines]
zeroes = []
nines = []

for i in range(len(lines)):
    for j in range(len(lines[0])):
        if int(lines[i][j]) == 0:
            zeroes.append((i,j))
        if int(lines[i][j]) == 9:
            nines.append((i,j))

def surroundings(en : list, lines):
    # check if m is next to en (en is a coordinate)
    i = en[0]
    j = en[1]
    left = (i, j-1)
    right = (i, j+1)
    up = (i+1, j)
    down = (i-1, j)
    cs = [left, right, up, down]
    cs = [c for c in cs if (c[0] >= 0 and c[0] < len(lines) and c[1] >= 0 and c[1] < len(lines))]

    return cs

def expand(components, lines):
    # components is a list of reachable 8s, 7s, ..., ns
    # expand computes the reachable (n-1)s
    i = 10 - len(components)
    
    com = components[-1]
    new_component = []
    for c in com:
        surr = surroundings(c, lines)
        moves = [s for s in surr if int(lines[s[0]][s[1]]) == i - 1]
        new_component += moves

    components.append(new_component)
    components = [list(set(component)) for component in components]

    return components

def part1(lines):

    zero_counts = [0]*len(zeroes)

    for nine in nines:
        components = [[nine]]
        while len(components) < 10:
            components = expand(components, lines)

        for c in components[-1]:
            if c in zeroes:
                zero_counts[zeroes.index(c)] += 1

    return sum(zero_counts)

#print(part1(lines))

def all_trails(basepoint, lines):
    # compute all trails from the basepoint
    # (basepoint must be 0)
    trails = [[basepoint]]
    count = 0
    while count < 9:
        new_trails = []
        for t in trails:
            surr = surroundings(t[-1], lines)
            moves = [s for s in surr if int(lines[s[0]][s[1]]) == count + 1]
            new_trails += [t + [move] for move in moves]

        trails = new_trails
        count += 1

    return len(trails)

def part2(lines):

    counter = 0
    for z in zeroes:
        counter += all_trails(z, lines)

    return counter

#print(part2(lines))