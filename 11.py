# I have left in some failed attempt as a reminder to myself

import time

#file = r"[PATH]"
#filein = open(file, "r", encoding='UTF-8')
#lines = filein.readlines()
#filein.close()

#line = lines[0][:-1]
#stones = line.split(" ")

# part 1
 
def blink(stones):
    new_stones = []
    
    for stone in stones:
        if stone == "0":
            new_stones.append("1")
        elif len(stone) % 2 == 0:
            new_stones.append(str(int(stone[:int(len(stone)/2)])))
            new_stones.append(str(int(stone[int(len(stone)/2):])))
        else:
            new_stones.append(str(int(stone)*2024))
    
    return new_stones

def blink_n_times(n, stones):
    for i in range(n):
        t0 = time.time()   
        print(i)
        stones = blink(stones)
        t1 = time.time()
        print(t1-t0)

    return stones

def part1(stones):
    stones = blink_n_times(75, stones)
    return len(stones)

#print(part1(stones))

# part 2, attempt 1 (after brute force) - memoization as I shakily remember it

def memblink(stones, vals):
    # vals is a dictionary of known values
    new_stones = []
    
    for stone in stones:
        # first check it hasn't already been computed
        if stone in vals:
            new_stones += vals[stone]
        # otherwise compute and add to vals
        else:
            if stone == "0":
                new_stones.append("1")
                vals[stone] = ["1"]
            elif len(stone) % 2 == 0:
                new_stones.append(str(int(stone[:int(len(stone)/2)])))
                new_stones.append(str(int(stone[int(len(stone)/2):])))
                vals[stone] = [str(int(stone[:int(len(stone)/2)])), str(int(stone[int(len(stone)/2):]))]
            else:
                new_stones.append(str(int(stone)*2024))
                vals[stone] = [str(int(stone)*2024)]
    
    return new_stones, vals

# recursion is apparently slightly quicker
def memblink_n_times(n, stones, vals):
    if n == 1:
        return memblink(stones, vals)
    else:
        s, v = memblink_n_times(n-1, stones, vals)
        return memblink(s, v)
    
# tests below show it still takes far too long
#t0 = time.time()
#print(len(memblink_n_times(43, stones, {})[0]))
#t1 = time.time()
#print(t1-t0)

# part 2 attempt 2: store only the number of times a stone appears

def super_dict_adder(d, s, n):
    # add n copies of s to d
    if s in d:
        d[s] += n
    else:
        d[s] = n
    
    return d

def super_memblink(super_stones, vals):
    # super_stones is a dict storing the number of times each stone appears, val is a dict of known values
    new_super_stones = {}
    
    for sstone in super_stones:
        # check if it's been computed
        if sstone in vals:
            va = vals[sstone]
            for v in va:
                new_super_stones = super_dict_adder(new_super_stones, v, super_stones[sstone])
        else:
            if len(sstone) % 2 == 0:
                new_super_stones = super_dict_adder(new_super_stones, (str(int(sstone[:int(len(sstone)/2)]))), super_stones[sstone])
                new_super_stones = super_dict_adder(new_super_stones, (str(int(sstone[int(len(sstone)/2):]))), super_stones[sstone])
                vals[sstone] = [str(int(sstone[:int(len(sstone)/2)])), str(int(sstone[int(len(sstone)/2):]))]
            else:
                new_super_stones = super_dict_adder(new_super_stones, str(int(sstone)*2024), super_stones[sstone])
                vals[sstone] = [str(int(sstone)*2024)]
    
    return new_super_stones, vals

def smemblink_n_times(n, stones, vals):
    if n == 1:
        return super_memblink(stones, vals)
    else:
        s, v = smemblink_n_times(n-1, stones, vals)
        return super_memblink(s, v)

def part2(stones):

    # no point computing something we already know  
    vals = {"0":"1"}
    # set up the super dictionary
    d = {}
    for s in stones:
        d[s] = 1

    count = 0
    newd = smemblink_n_times(75, d, vals)[0]
    for el in newd:
        count += newd[el]

    return count

#print(part2(stones))
# 229557103025807