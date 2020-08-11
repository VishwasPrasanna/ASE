import pandas as pd

data = pd.read_csv("xomo10000.csv")
# print(data)
# print(data["$Data"][0])
p = 2

def distance_between_rows(row1,row2,cols):
    d = n = 0
    for col in cols:
        n += 1
        if "$" in col[0].name:
            d0 = dist_nums(row1[col[1]], row2[col[1]], col[0])
        else:
            d0 = dist_syms(row1[col[1]], row2[col[1]], col[0])
        d += d0**p
    return d**(1/p) / n**(1/p)

def dist_syms(x, y):
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



    
    

