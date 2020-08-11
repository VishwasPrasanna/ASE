def dominates(row1,row2,goals): # i and j are rows.
    #print("Dominates Calculation")
    #print("Row 1: ", end='')
    #row1.print_cells()
    #print("Row 2: ", end='')
    #row2.print_cells()
    z = 0.00001
    s1, s2, n = z,z,z+len(goals)
    for goal in goals:
      #print("Goal: "+str(goal.name))
      a =  row1[goal.pos]
      #print("Row 1 value: "+str(a))
      b =  row2[goal.pos]
      #print("Row 2 value: "+str(b))
      a = norm(a, goal.lo, goal.hi)
      #print("Goal Low: "+str(goal.lo)+", Goal High: "+str(goal.hi))
      #print("Normalized Value row 1: "+str(a))
      b = norm(b, goal.lo, goal.hi)
      #print("Normalized Value row 2: "+str(b))
      #print("Goal direction (-1 min, 1 max): "+str(goal.w))
      s1 -= 10**(goal.w * (a-b)/n)
      s2 -= 10**(goal.w * (b-a)/n)
      #print(str(s1)+" "+str(s2))
    #print("")
    return s1/n - s2/n # i is better if it losses least (i.e. this number under 0)
  
def norm(z, low, hi):
  return (z - low)/(hi - low + 10**-32)
    