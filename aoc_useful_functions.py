'''
useful functions for the advent of code
'''

# random

def dict_adder(d : dict, s, n : int):
    '''if d is a dictionary storing an integer for each key, add n to the value of the key s

    Parameters
    ----------
    d : _dict_
        dictionary storing integer keys for each value
    s : _Any_
        value to be added to d
    n : _int_
        integer to increase value of s by

    Returns
    -------
    d : _dict_
        new dictionary
    '''
    if s in d:
        d[s] += n
    else:
        d[s] = n
    
    return d

def periodic(n : str):
    '''check if a string is periodic

    Parameters
    ----------
    n : _str_
        string to be checked

    Returns
    -------
    _Bool_
        True if `n` is periodic, False otherwise
    '''
    for i in range(2, len(n)+1):
        if len(n) % i == 0:
            k = int(len(n)/i)
            pieces = [n[k*j:k*j+k] for j in range(int((len(n)-k)/k)+1)]
            if len(set(pieces)) == 1:
                return True
            
    return False

def flatten(l : list):
    '''flatten list of lists

    Parameters
    ----------
    l : _list_
        list of lists to flatten

    Returns
    -------
    _list_
        flat(er) list
    '''
    return [x for xs in l for x in xs]

# grid functions

def surroundings(en : list | tuple, lines : list):
    '''find the surrounding (non-diagonal) squares of a square `en` in a grid `lists`

    Parameters
    ----------
    en : _list | tuple_
        middle point of the form (i,j) or [i,j]
    lines : _list_
        grid (list of lines)

    Returns
    -------
    cs : _list_
        list of surrounding (non-diagonal) coordinates 
    '''
    i = en[0]
    j = en[1]
    left = (i, j-1)
    right = (i, j+1)
    up = (i+1, j)
    down = (i-1, j)
    cs = [left, right, up, down]
    cs = [c for c in cs if (c[0] >= 0 and c[0] < len(lines) and c[1] >= 0 and c[1] < len(lines[0]))]

    return cs

def diag_surroundings(en : list | tuple, lines : list):
    '''find the surrounding (including diagonal) squares of a square `en` in a grid `lists`

    Parameters
    ----------
    en : _list | tuple_
        middle point of the form (i,j) or [i,j]
    lines : _list_
        grid (list of lines)

    Returns
    -------
    cs : _list_
        list of surrounding (including diagonal) coordinates 
    '''
    i = en[0]
    j = en[1]
    left = (i, j-1)
    right = (i, j+1)
    up = (i+1, j)
    down = (i-1, j)
    dl = (i-1, j-1)
    dr = (i-1, j+1)
    ul = (i+1, j-1)
    ur = (i+1, j+1)
    cs = [left, right, up, down, dl, dr, ul, ur]
    cs = [c for c in cs if (c[0] >= 0 and c[0] < len(lines) and c[1] >= 0 and c[1] < len(lines))]

    return cs

def replace_l(lines : list, l : list, r):
    '''replace coordinates in the list `l` by `r`

    Parameters
    ----------
    lines : _list_
        grid (list of lists)
    l : _list_
        list of coordinates to be replaced
    replacement : _Any_
        term to replace anything at a coordinate in `l` by

    Returns
    -------
    newlines : _list_
        new grid after replacement
    '''
    newlines = []
    for i in range(len(lines)):
        newline = []
        for j in range(len(lines[0])):
            if (i,j) in l:
                newline += r
            else:
                newline += lines[i][j]
        newlines.append(newline)
    
    return newlines

def find(char, lines : list):
    '''find coordinates of all appearances of `char` in the grid `lines`

    Parameters
    ----------
    char : _Any_
        thing to find in grid
    lines : _list_
        grid (list of lines)

    Returns
    -------
    appearances : _list_
        list of all coordinates where `char` appears in `lines`
    '''
    appearances = []
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == char:
                appearances.append((i,j))
    
    return appearances

# optimisation

def dict_update(d : dict, key, val):
    '''add key:val to a dictionary `d`

    Parameters
    ----------
    d : _dict_
        dictionary to be updated
    key : _Any_
        new key
    val : _Any_
        new key's value

    Returns
    -------
    d : _dict_
        updated dictionary
    '''
    d[key] = val
    return d

def memoize(func, vals : dict):
    '''take in a function and a dictionary of known values, and output a function which checks against those values first (returning new values too)

    Parameters
    ----------
    func : _function_
        function to be memoized
    vals : _dict_
        dictionary of known values

    Returns
    -------
    m : _function_
        new memoized function (which also returns new known values)

    !!!untested!!!
    '''
    # can't do a lambda function for stupid reasons
    # (can't have both an if else statement and value assignment)
    def m(l : list):
        # l zipped list of inputs for f
        if l not in vals:
            x = func(*l)
            return (x, dict_update(vals, l, x))
        else:
            return (vals[l], vals)
    
    return m

def mem_func_list(func, el : list):
    '''apply a memoized func to every element in a list

    Parameters
    ----------
    func : _function_
        function to be applied
    el : _list_
        list to have func applied to

    Returns
    -------
    new_list : _list_
        el, with func having been efficiently applied to each element

    !!!untested!!!
    '''
    vals = {}
    new_list = []
    for l in el:
        v, vals = memoize(func, vals)(l)
        new_list.append(v)

    return new_list