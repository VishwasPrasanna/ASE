from distance import distance_between_rows
import random
from row import Row

def fastMap(rows, non_goal_cols):
    rand = random.randint(0,len(rows)-1)
    #print("ROW INDEX: "+str(rand))
#     bool validIndex = False;
    # choose random row
    randRow = rows[rand]
    #randRow.print_cells()
    list1 = []
    list2 = []
    # find 90th %ile row from it
    for i in range(0,len(rows)):
        dist = distance_between_rows(randRow, rows[i], non_goal_cols)
        # print(dist)
        list1.append(dist)
        list2.append(i)
    zipped_pairs = zip(list1,list2)
    z = [x for _, x in sorted(zipped_pairs)]
    index_90th  = round(len(z)*0.9)
    pivot1 = z[index_90th]
    # print(pivot1, end=', ')
    
    list1 = []
    list2 = []
    for i in range(0,len(rows)):
        dist = distance_between_rows(rows[pivot1], rows[i], non_goal_cols)
        list1.append(dist)
        list2.append(i)
    zipped_pairs = zip(list1,list2)
    z = [x for _, x in sorted(zipped_pairs)]
    index_90th  = round(len(z)*0.9)
    pivot2 = z[index_90th]
    # print(pivot2, end=', ')
    # print(list1[pivot2])
    
    return pivot1,pivot2,list1[pivot2]

# import math
# l1 = []
# l2=[]
# for i in range(0,10):
#     l1.append(i)
#     print(i)
#     rand = random.random()
#     print(rand)
#     l2.append(rand)
# print(l1)
# print(l2)

# zipped_pairs = zip(l2, l1) 
  
# z = [x for _, x in sorted(zipped_pairs)]
# print(round(256*0.9))

