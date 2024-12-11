file = r"c:\Users\jledg\Documents\not_backed_up\input7.txt"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()

def base3(n):
    # change base 10 to base 3
    i = 0
    n3 = "0t"
    while 3**i < n:
        i += 1
    if 3**i != n:
        i -= 1
    for j in range(i+1):
        k = i-j

        if 2*(3**k) <= n:
            n3 += "2"
            n -= 2*(3**k)
        elif 3**k <= n:
            n3 += "1"
            n -= 3**k
        else:
            n3 += "0"
    
    return n3

def zero_padder(el, length):
    # pad zeroes so that all the binary/tertiary numbers are the same number of digits
    while len(el) < length:
        el = "0" + el

    return el

def vals(length, base):
    # create list of all binary/tertiary numbers of a certain length
    upper = 0
    l = []
    upper = base**length - 1
    for j in range(upper+1):

        if base == 2:
            power = zero_padder(str(bin(j))[2:], len(str(bin(upper))[2:]))
        elif base == 3:
            power = zero_padder(str(base3(j))[2:], len(str(base3(upper))[2:]))
        else:
            return "invalid"
        l.append(power)

    return l

def setup(line, base):

    line = line.split(":")
    test_val = line[0]
    line = line[1:]
    line = (line[0].split(" "))[1:]
    line[-1] = line[-1][:-1]
    l = vals(len(line)-1, base)

    return line, l, test_val

def calc(line, test_val, pm):

    sum = int(line[0])
    for j in range(len(line)-1):
        if pm[j] == '0':
            sum += int(line[j+1])
        elif pm[j] == '1':
            sum *= int(line[j+1])
        else:
            sum = int(str(sum) + line[j+1])

    if sum == int(test_val):
        return True
    
    else:
        return False

def main(part):
    big_sum = 0
    for line in lines:
        line, l, test_val = setup(line, part+1)

        good = False
        for i in range(len(l)):
            pm = l[i]
            good = calc(line, test_val, pm)
            if good:
                big_sum += int(test_val)
                break
            
    return big_sum

#print(main(2))