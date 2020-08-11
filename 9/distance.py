import pandas as pd
import col

# print(data)
# print(data["$Data"][0])
p = 2
no = '?'

def distance_between_rows(row1,row2,cols):
    d = n = 0
    for col in cols:
        n += 1
        if "$" in col.name:
            d0 = dist_nums(row1[col.pos], row2[col.pos], col)
        else:
            d0 = dist_syms(row1[col.pos], row2[col.pos], col)
        d += d0**p
    return d**(1/p) / n**(1/p)

def dist_syms(x, y, col):
    if ((x is no) and (y is no)): return 1
    if x != y: return 1
    return 0
    
def dist_nums(x, y, col):
    if col.lo == col.hi:
        return 0
    norm = lambda z: (z - col.lo)/(col.hi - col.lo)
    x = norm(x)
    y = norm(y)
    return abs(x-y)



    
    

