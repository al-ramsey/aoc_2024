file = r"c:\Users\jledg\Documents\not_backed_up\input3.txt"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()

simplified_lines = ""
for line in lines:
    simplified_lines += line

def mul_finder(line, first, order):
    index = 0
    end = 0
    pot_muls = []
    count = 0
    while index != -1:
        count += 1
        index = line.find("mul(")

        if index == -1:
            continue
        line = line[index:]
        end = line.find(")")
        potential_mul = line[:end+1]

        # add a counter as the second element to keep track of the correct ordering
        if first:
            pot_muls.append([potential_mul, count])
        else:
            pot_muls.append([potential_mul, order])
        line = line[end:]

    return pot_muls

def tup_giver():
    total_tups = []

    for line in [simplified_lines]:
        pot_muls = mul_finder(line, True, 0)
        tups = []
        bad_muls = []
        while pot_muls != []:
            for pot_mul in pot_muls:
                
                try:
                    test = (pot_mul[0][4:-1]).split(",")
                    tups.append((int(test[0]), int(test[1]), pot_mul[1]))

                except (ValueError, IndexError):
                    bad_muls.append(pot_mul)
            
            pot_muls = []
            for bad_mul in bad_muls:
                bad_mul = (bad_mul[0][1:], bad_mul[1])
                new = mul_finder(bad_mul[0], False, bad_mul[1])
                pot_muls += new
            
            bad_muls = []

        total_tups += tups
    
    return total_tups

def part1():
    sum = 0
    tups = tup_giver()
    # recover ordering
    tups.sort(key=lambda x: x[2])

    for tup in tups:
        sum += tup[0]*tup[1]

    return sum

def sorter_prime(l):
    # sorts a list normally, except that -1 is the biggest integer
    l = sorted(l)
    while l[0] == -1:
        l.remove(-1)
        l.append(-1)
        if l == [-1, -1, -1]:
            return False

    return l


def part2():
    sum = 0
    do = True
    tups = tup_giver()
    # recover ordering
    tups.sort(key=lambda x: x[2])
    strtups = [("mul" + str((tup[0], tup[1]))).replace(" ", "") for tup in tups]

    do = True
    starting_index = 0

    for t in strtups:
        decided = False
        count = 0
        while not decided:

            simp = simplified_lines[starting_index:]
            inddo = simp.find("do()")
            inddont = simp.find("don't()")
            indt = simp.find(t)
            my_l = sorter_prime([inddo, inddont, indt])

            # if inddo is the smallest, set do = True and move along a bit
            if (my_l.index(inddo) < my_l.index(inddont)) and (my_l.index(inddo) < my_l.index(indt)):
                do = True
                starting_index += inddo + 1
                continue
            
            # if inddont is the smallest, set do = False and move along a bit
            elif (my_l.index(inddont) < my_l.index(inddo)) and (my_l.index(inddont) < my_l.index(indt)):
                do = False
                starting_index += inddont + 1
                continue

            # if indt is the smallest, do the multiplication as long as 'do' is set to True
            elif (my_l.index(indt) < my_l.index(inddo)) and (my_l.index(indt) < my_l.index(inddont)):
                if do:
                    vals = t[4:-1].split(",")
                    sum += int(vals[0])*int(vals[1])
                
                decided = True
            
    return sum