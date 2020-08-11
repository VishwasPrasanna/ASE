from row import Row
from distance import distance_between_rows

class TreeNode:
    def __init__(self):
        pass

    def classify(self, row):
        pass
    
    def print_tree(self, i=0):
        pass

class SplitNode(TreeNode):
    def __init__(self, tbl, lft, rgt, dist):
        self.left_child = None
        self.right_child = None
        self.tbl_size = tbl
        # store pivots instead of table so you can calc which one
        # the new point is closer to
        self.l_pivot = lft
        self.r_pivot = rgt
        self.pivot_dist = dist
        self.tbl = None
        self.goals = []
    
    def set_left_child(self, lc):
        self.left_child = lc
    
    def set_right_child(self, rc):
        self.right_child = rc
    
    def add_goal(self, goal):
        self.goals.append(goal)
    
    def is_leaf(self):
        return self.left_child == None and self.right_child == None
    
    def set_tbl(self, tbl):
        self.tbl = tbl

    def print_tree(self, i=0):
        print("|."*i+str(self.tbl_size))
        if self.left_child != None:
            self.left_child.print_tree(i+1)
        if self.right_child != None:
            self.right_child.print_tree(i+1)
        if len(self.goals) > 0:
            print("|."*(i+1), end='')
            for x in range(0, len(self.goals)):
                print(str(self.goals[x].name)+" = "+str(round(self.goals[x].mean(),2))+" ("+str(round(self.goals[x].var(), 2))+")", end='')
                if x != (len(self.goals) - 1):
                    print(", ", end="")
            print()
    
    def is_anomaly(self, row):
        a = distance_between_rows(self.l_pivot, row, self.goals)
        b = distance_between_rows(self.r_pivot, row, self.goals)
        x = (a**2+self.pivot_dist**2-b**2)/(2*self.pivot_dist)
        median = (self.cosdist(self.l_pivot)+self.cosdist(self.r_pivot))/2
        alpha = .6
        if median < .5:
            if x < median*alpha:
                return True
            return False
        else:
            if x > (1-median)*alpha:
                return True
            return False

    def dribble(self, row):
        # if anomaly, add to goal columns, then
        if self.is_anomaly(row):
            for goal in self.goals:
                goal + row[goal.pos]
            #if self.is_leaf():
            #    print("Is leaf")
            #else:
            #    print("need to recurse")
            # check pivots to see which it's closer to and dribble it into that subtree
            median = (self.cosdist(self.l_pivot)+self.cosdist(self.r_pivot))/2
            #print(median)
            dist = self.cosdist(row)
            #print(dist)
            # project the row onto the line and see which point its closer to.
            if dist <= median:
                #print("recursing on left")
                self.left_child.dribble(row)
            elif dist > median:
                #print("recursing on right")
                self.right_child.dribble(row)
        else:
            return

    def cosdist(self,current_row):
        return (distance_between_rows(self.l_pivot,current_row,self.goals)**2 + self.pivot_dist**2 - distance_between_rows(self.r_pivot,current_row,self.goals)**2)/(2*self.pivot_dist)

    def update(self):
        if self.is_leaf():
            for row in self.tbl.rows:
                if row.tag != 0:
                    for x in range(0, len(self.goals)):
                        print(str(self.goals[x].name)+" = "+str(round(self.goals[x].mean(),2))+" ("+str(round(self.goals[x].var(), 2))+")", end='')
                        if x != (len(self.goals) - 1):
                            print(", ", end="")
                        else:
                            print("")
        else:
            if self.left_child != None:
                self.left_child.update()
            if self.right_child != None:
                self.right_child.update()



class DecisionNode(TreeNode):
    def __init__(self, comparison_col, comparison_val, col_name):
        self.left_child = None
        self.right_child = None
        self.col_name = col_name
        self.comp_idx = comparison_col
        self.comp_val = comparison_val
    
    def set_left_child(self, lc):
        self.left_child = lc
    
    def set_right_child(self, rc):
        self.right_child = rc

    def classify(self, row):
        # print(str(self.comp_val)+str(self.comp_op)+str(self.comp_idx))
        if row[self.comp_idx] < self.comp_val:
            return self.left_child.classify(row)
        else:
            return self.right_child.classify(row)

    def print_tree(self, i=0):
        print("  " * i + self.col_name + " = ", end='')
        print("-inf .. "+str(self.comp_val), end='')
        if type(self.left_child) == LeafNode:
            print(": ", end='')
        else:
            print("")
        self.left_child.print_tree(i+1)
        print("  " * i + self.col_name + " = ", end='')
        print(str(self.comp_val) + " .. inf", end='')
        if type(self.right_child) == LeafNode:
            print(": ", end='')
        else:
            print("")
        self.right_child.print_tree(i+1)

class LeafNode(TreeNode):
    def __init__(self, cv, var):
        self.class_val = cv
        self.variance = var
    
    def classify(self, row):
        return self.class_val
    
    def print_tree(self, i=0):
        print(str(self.class_val)+" ("+str(self.variance)+")")


