'''
Note: in 2024 I got stuck halfway through day 9, finishing part 1 but not part 2. The code below is my original (very bad and slow, but working) code for part 1.
In 2025 (as I'm writing this) I came back to part 2. I will indicate where my (better) 2025 code begins. I have made no attempt, other than renaming some
functions, to remove duplication between 2024 and 2025; I have not even reread the 2024 code.
'''

file = r"[PATH]"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()

def translate(l):
    new_l = ''
    count = 0
    even = True
    for c in l:
        if even:
            for i in range(int(c)):
                # + "#"
                new_l += str(count) + "#"
            even = False
            count += 1
        else:
            for i in range(int(c)):
                new_l += '.'
            even = True
    
    count -= 1

    return (new_l, count)

def str_item_assignment(s, i, ns, length):
    new_s = s[:i] + ns + s[i+length:]
    return new_s

def stitcher(li, length):
    j = int(len(li)/length)
    new_li = []
    for i in range(j):
        s = ''
        for k in range(length):
            s += li[i*length + k]
        new_li.append(s)

    return new_li

def count_conseq(i, l, length):
    j = length # 1 -> length

    while len(set(list(stitcher(l[i:i+j], length)))) == 1:
        j += length
    j -= length
    j = i + j
    return (int((j-i)/length), i, j)

def find_end_chars(l):
    rev = list(reversed(l))
    for i in range(len(rev)):
        if rev[i] != '.':
            break

    end1 = rev[i+1:].index('#') 
    end2 = rev[i+1:].index('.')
    end = min(end1, end2)
    end += i
    j = l.find('.')
    dig = l[(end*-1 - 1):(i*-1 - 1)] + l[i*-1 -1]
    return i, rev, dig, j

def move2024(l, part):
    i, rev, dig, j = find_end_chars(l)
    # < --> <=
    if count_conseq(i, rev, len(dig))[0] <= count_conseq(j, l, 1)[0]:
        k = (count_conseq(i, rev, len(dig))[0])
        l = str_item_assignment(l, j, dig*k, k)
        l = str_item_assignment(l, len(l) + i*-1 - k*len(dig), '.'*k, len(dig*k))

    else:
        if part == 1:
            k = count_conseq(j, l, 1)[0]
            l = str_item_assignment(l, j, dig*k, k)
            l = str_item_assignment(l, len(l) + i*-1 - k*len(dig), '.'*k, len(dig*k))

    return l

def checker(l):
    ind = l.find('.')

    if len(set((l[ind:].split(".")))) == 1:
        return True
    else:
        return False 

def checksum2024(l):
    #
    l = l.split('#')
    #
    count = -1
    sum = 0
    for char in l:
        # used to be += 1
        #if char == "#":
        #    continue
        count += char.count('.')
        char = char.replace('.', '')
        if char == '':
            continue
        count += 1
        sum += int(char)*count
    
    return sum

def part1():
    l = translate(lines[0])[0]

    while not checker(l):
        l = move2024(l, 1)

    sum = checksum2024(l)
    return sum

#print(part1())

'''
Below is the solution for part 2, written on 02.12.2025.
'''

line = lines[0]
files = line[::2]
spaces = line[1::2]
# solution does assume length of input is odd (not difficult to correct but didn't matter in my case)

indexed_files = [(files[i], i) for i in range(len(files))]
listed_spaces = [space for space in spaces]

def move(i, indexed_files, listed_spaces):
    # moves the ith file in the list to the frontmost available space
    # find correct index
    for f in indexed_files:
        if f[1] == i:
            j = indexed_files.index(f)

    for k in range(j):
        # run through spaces
        # if there's space
        if int(listed_spaces[k]) >= int(indexed_files[j][0]):
            old_if = indexed_files.copy()
            # rearrange file order
            indexed_files = indexed_files[0:k+1] + [indexed_files[j]] + indexed_files[k+1:j] + indexed_files[j+1:]
            # in the case where we move the final element, there are no spaces after it, so the formula is slightly different
            if i == len(indexed_files)-1:
                if j - 1 != k:
                    listed_spaces = listed_spaces[:k] + ["0"] + [str(int(listed_spaces[k]) - int(old_if[j][0]))] + listed_spaces[k+1:j-1] + [str(int(old_if[j][0])+int(listed_spaces[j-1]))]
                # case where we move without changing file order has a simpler formula
                else:
                    listed_spaces = listed_spaces[:k] + ["0"] + [str(int(listed_spaces[k]))]
            elif j-1 == k:
                listed_spaces = listed_spaces[:k] + ["0"] + [str(int(listed_spaces[k]) + int(listed_spaces[j]))] + listed_spaces[k+2:]
            else:
                listed_spaces = listed_spaces[:k] + ["0"] + [str(int(listed_spaces[k]) - int(old_if[j][0]))] + listed_spaces[k+1:j-1] + [str(int(old_if[j][0])+int(listed_spaces[j-1])+int(listed_spaces[j]))] + listed_spaces[j+1:]
            break
    
    return [indexed_files, listed_spaces]

def checksum(indexed_files, listed_spaces):
    count = 0
    sum = 0
    ind = 0
    for f in indexed_files:
        for i in range(int(f[0])):
            sum += f[1]*count
            count += 1
        for i in range(int(listed_spaces[ind])):
            count += 1
        ind += 1

    return sum

def part2(indexed_files, listed_spaces):

    for j in range(len(indexed_files)):
        i = len(indexed_files) - j - 1
        l = move(i, indexed_files, listed_spaces)
        indexed_files = l[0]
        listed_spaces = l[1]

    c = checksum(indexed_files, listed_spaces)
    return c

#print(part2(indexed_files, listed_spaces))
# 6431472344710 (!)