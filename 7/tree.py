from row import Row

class TreeNode:
    def __init__(self):
        pass

    def classify(self, row):
        pass
    
    def print_tree(self, i=0):
        pass

class SplitNode(TreeNode):
    def __init__(self, tbl):
        self.left_child = None
        self.right_child = None
        self.tbl_size = tbl
        self.goals = []
    
    def set_left_child(self, lc):
        self.left_child = lc
    
    def set_right_child(self, rc):
        self.right_child = rc
    
    def add_goal(self, goal):
        self.goals.append(goal)

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
