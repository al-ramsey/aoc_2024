file = r"c:\Users\jledg\Documents\not_backed_up\input5.txt"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()

def all_tuples(l):
    # take a list and return a list l of tuples where for each tuple, the index of the first
    # element is less than the index of the second element in l
    tups = [(l[i], l[j]) for i in range(len(l)) for j in range(len(l)) if i < j]
    return tups

def iscorrect(update, rules):
    tups = all_tuples(update)
    revd = [tup[::-1] for tup in tups]

    # the update is incorrect if any of the tuples appear reversed in the rules 
    if set(revd).intersection(set(rules)) == set():
        return True
    else:
        return False


def sorter():

    rules = []
    updates = []
    correct = []
    incorrect = []

    for line in lines:
        if "|" in line:
            line = line.split("|")
            # remove \n
            rules.append((line[0], line[1][:-1]))

        else:
            if line == "\n":
                continue
            line = line.split(",")
            # remove \n
            line[-1] = line[-1][:-1]
            updates.append(line)

    for update in updates:
        if iscorrect(update, rules):
            correct.append(update)
        else:
            incorrect.append(update)

    return (correct, incorrect, rules)

def part1():
    sum = 0
    correct = sorter()[0]

    for c in correct:
        sum += int(c[int((len(c)-1)/2)])

    return sum

def part2():
    sum = 0
    incorrect = sorter()[1]
    correct = []
    rules = sorter()[2]

    for i in incorrect:
        while not iscorrect(i, rules):

            tups = all_tuples(i)
            revd = [tup[::-1] for tup in tups]
            # can't use set intersection here because it messes up order
            # so use slower list comprehension instead
            broken_rules = [x for x in revd if x in rules]

            for rule in broken_rules:
                # swap the offending pairs 
                ind0 = i.index(rule[0])
                ind1 = i.index(rule[1])
                i[ind0] = rule[1]
                i[ind1] = rule[0]
        
        correct.append(i)
        
    for i in correct:
        sum += int(i[int((len(i)-1)/2)])

    return sum

print(part2())
