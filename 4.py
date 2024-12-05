file = r"c:\Users\jledg\Documents\not_backed_up\input4.txt"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()
# remove \n
lines = [l[:-1] for l in lines]

def searcher(i, j):
    words = []

    if i-3 >= 0:
        up = lines[i][j] + lines[i-1][j] + lines[i-2][j] + lines[i-3][j]
        words += [up]

        if j-3 >= 0:
            upl = lines[i][j] + lines[i-1][j-1] + lines[i-2][j-2] + lines[i-3][j-3]
            words += [upl]
        
        if j+3 < len(lines[i]):
            upr = lines[i][j] + lines[i-1][j+1] + lines[i-2][j+2] + lines[i-3][j+3]
            words += [upr]

    if i+3 < len(lines):
        down = lines[i][j] + lines[i+1][j] + lines[i+2][j] + lines[i+3][j]
        words += [down]

        if j-3 >= 0:
            downl = lines[i][j] + lines[i+1][j-1] + lines[i+2][j-2] + lines[i+3][j-3]
            words += [downl]

        if j+3 < len(lines[i]):
            downr = lines[i][j] + lines[i+1][j+1] + lines[i+2][j+2] + lines[i+3][j+3]
            words += [downr]

    if j-3 >= 0:
        left = lines[i][j] + lines[i][j-1] + lines[i][j-2] + lines[i][j-3]
        words += [left]

    if j+3 < len(lines[i]):
        right = lines[i][j] + lines[i][j+1] + lines[i][j+2] + lines[i][j+3]
        words += [right]

    return words

def part1():

    sum = 0
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] != "X":
                continue
            words = searcher(i, j)
            sum += words.count("XMAS")
    
    return sum

def xsearcher(i, j):
    dr = lines[i-1][j-1] + lines[i][j] + lines[i+1][j+1]
    dl = lines[i-1][j+1] + lines[i][j] + lines[i+1][j-1]
    return [dr, dl]

def part2():

    sum = 0
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] != "A":
                continue
            if i < 1 or i >= len(lines) - 1:
                continue
            if j < 1 or j >= len(lines[i]) - 1:
                continue
            
            # look at every cross centred at A
            cross = xsearcher(i, j)
            MAS = cross.count("MAS")
            SAM = cross.count("SAM")

            # keep only those which are X-MASes
            if MAS + SAM == 2:
                sum += 1
    
    return sum


print(part2())


