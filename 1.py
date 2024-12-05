file = r"c:\Users\jledg\Documents\not_backed_up\input1.txt"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()

lines2 = [l.split("   ") for l in lines]
lines3 = [[l[0], l[1][:-1]] for l in lines2[:-1]] + [lines2[-1]]
left = [l[0] for l in lines3]
right = [l[1] for l in lines3]

def part1():
    left.sort()
    right.sort()
    sum = 0
    for i in range(len(left)):
        sum += abs(int(left[i])-int(right[i]))

    return sum

def part2():
    sum = 0
    
    for l in left:
        sum += int(l)*(right.count(l))

    print("\n")
    return sum