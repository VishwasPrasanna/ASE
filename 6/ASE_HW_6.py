from table import Tbl
from tree import DecisionNode
from tree import LeafNode
import pandas as pd

def main():
    auto_xl = 'auto.xlsx'
    diabetes_xl = 'diabetes.xlsx'
    auto = pd.read_excel(auto_xl)
    diabetes = pd.read_excel(diabetes_xl)
    auto_in = "\n"+auto.to_csv(header=True, index=False, line_terminator="\n")
    diabetes_in = "\n"+diabetes.to_csv(header=True, index=False, line_terminator="\n")

    print("------------Decision Tree-----------------")
    tbl1 = Tbl(diabetes_in)
    tree1 = tbl1.split()
    tree1.print_tree()

    print("------------Regression Tree-----------------")
    tbl2 = Tbl(auto_in)
    tree2 = tbl2.split()
    tree2.print_tree()

main()