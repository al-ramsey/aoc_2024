file = r"c:\Users\jledg\Documents\not_backed_up\input2.txt"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()
lines = [l[:-1] for l in lines]

def issafe(chars):
    inc = True
    safe = True

    if int(chars[0]) - int(chars[1]) > 0:
        inc = False
    for i in range(len(chars) - 1):
        if (int(chars[i]) - int(chars[i+1]) > 0) and inc:
            safe = False
        elif (int(chars[i]) - int(chars[i+1]) < 0) and (not inc):
            safe = False
        elif (abs(int(chars[i]) - int(chars[i+1])) > 3) or (abs(int(chars[i]) - int(chars[i+1])) == 0):
            safe = False
        else:
            continue

    return safe


def part1():
    safe_count = 0

    for l in lines:
        chars = l.split(" ")
        
        if issafe(chars):
            safe_count += 1
    
    return safe_count

def part2():
    safe_count = 0

    for l in lines:
        chars = l.split(" ")
        
        if issafe(chars):
            safe_count += 1
        else:
            for i in range(len(chars)):
                chars_bar = chars.copy()
                chars_bar.pop(i)

                if issafe(chars_bar):
                    safe_count += 1
                    break

    return safe_count
