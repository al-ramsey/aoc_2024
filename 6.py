file = r"c:\Users\jledg\Documents\not_backed_up\input6.txt"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()

def moveup(i, j):
    new_pos = (i-1, j)
    return new_pos

def moveright(i, j):
    new_pos = (i, j+1)
    return new_pos

def movedown(i, j):
    new_pos = (i+1, j)
    return new_pos

def moveleft(i, j):
    new_pos = (i, j-1)
    return new_pos

def runner(inp):
    for i in range(len(inp)):
        if "^" in inp[i]:
            j = inp[i].find("^")
            count = 0
            gone = False
            path = [(i, j)]

            while not gone:
                inp[i] = inp[i][:j] + "X" + inp[i][j+1:]
                if (len(path) > 1) and (len(set(path)) < len(path)):
                    return -1
                
                if count == 0:
                    (ni, nj) = moveup(i, j)
                elif count == 1:
                    (ni, nj) = moveright(i, j)
                elif count == 2:
                    (ni, nj) = movedown(i, j)
                else:
                    (ni, nj) = moveleft(i, j)
                
                if (ni >= len(inp)) or (nj >= len(inp[ni])) or (ni < 0) or (nj < 0):
                    gone = True

                elif inp[ni][nj] == "#":
                    count += 1
                    count = count % 4
                    
                    path.append((i, j, count))

                else:
                    (i, j) = (ni, nj)

    return inp
    
def part1():
    sum = 0
    for line in runner(lines):
        sum += line.count("X")

    return sum

def part2():
    sum = 0
    
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "^" or lines[i][j] == "#":
                continue
            inp = lines.copy()
            inp[i] = inp[i][:j] + "#" + inp[i][j+1:]
            if runner(inp) == -1:
                sum += 1

    return sum

# terrible algorithm but it finished before the heat death of the universe so I'm happy