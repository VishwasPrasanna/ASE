from row import Row

class TreeNode:
    def __init__(self):
        pass

    def classify(self, row):
        pass
    
    def print_tree(self, i=0):
        pass

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

