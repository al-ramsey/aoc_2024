from aoc_useful_functions import * 

file = r"[PATH]"
filein = open(file, "r", encoding='UTF-8')
lines = filein.readlines()
filein.close()
lines = [l[:-1] for l in lines]

def component(l, lines, el):
    # find the connected component of `l` which the element `el` is contained in
    surr = surroundings(el, lines)
    surr = [s for s in surr if s in l]
    old_track = [[el]]
    new_track = [[el], surr.copy()]

    while len(set(flatten(new_track))) > len(set(flatten(old_track))):
        new_end = []
        for coord in new_track[-1]:
            if coord not in set(flatten(old_track)):
                surr = surroundings(coord, lines)
                surr = [s for s in surr if s in l]
                new_end += surr.copy()
        
        new_end = list(set(new_end))
        old_track = new_track.copy()
        new_track.append(new_end)
            
    return list(set(flatten(new_track)))

def connected_components(l, lines):
    # find connected components of a list of coordinates (not including diagonals)
    components = []
    flat_components = []
    while len(flat_components) < len(l):
        for el in l:
            if el not in flat_components:
                components.append(component(l, lines, el))
                flat_components = flatten(components)
                break
    
    return components

def area(comp):
    return len(comp)

def perimeter(comp, lines):
    count = 0
    for c in comp:
        # find edges which don't border another block in the component
        nontouching = 4 - len(set(surroundings(c, lines)).intersection(set(comp)))
        count += nontouching

    return count

def part1(lines):
    possible_plants = list(set(flatten(lines)))
    all_components = []

    for plant in possible_plants:
        appearances = find(plant, lines)
        all_components += connected_components(appearances, lines)

    price = 0
    for comp in all_components:
        price += area(comp)*perimeter(comp, lines)

    return price

def vertex_surroundings(v, comp):
    i = v[0]
    j = v[1]
    vsurr = [(i,j), (i-1, j), (i, j-1), (i-1, j-1)]
    vsurr = set(vsurr).intersection(set(comp))
    return vsurr

def sides(comp):
    all_vs = []

    for c in comp:
        i = c[0] 
        j = c[1]
        # label a vertex by its bottom right square
        vertices = [(i,j), (i+1, j), (i, j+1), (i+1, j+1)]
        all_vs += vertices

    all_vs = list(set(all_vs))
    count = 0
    to_remove = []

    for v in all_vs:
        i = v[0]
        j = v[1]
        # find blocks that share the vertex
        vsurr = vertex_surroundings(v, comp)

        if len(vsurr) == 4:
            # remove interior vertex
            to_remove.append(v)

        elif len(vsurr) == 2:
            if vsurr == {(i,j), (i-1, j-1)} or vsurr == {(i-1, j), (i, j-1)}:
                # this vertex needs to be counted twice, since it encodes two corners
                count += 1
            else:
                # this is just part of a side, so can be removed
                to_remove.append(v)

    all_vs = set(all_vs) - set(to_remove)

    return len(all_vs) + count

def part2(lines):
    possible_plants = list(set(flatten(lines)))
    all_components = []

    for plant in possible_plants:
        appearances = find(plant, lines)
        all_components += connected_components(appearances, lines)

    price = 0
    for comp in all_components:
        price += area(comp)*sides(comp)

    return price

print(part1(lines))
print(part2(lines))