from table import Tbl
from tree import SplitNode
import pandas as pd

def main():
    xomo_xl = 'xomo10000.csv'
    pom_xl = 'pom310000.csv'
    xomo = pd.read_csv(xomo_xl)
    pom = pd.read_csv(pom_xl)
    xomo_in = "\n"+xomo.to_csv(header=True, index=False, line_terminator="\n")
    pom_in = "\n"+pom.to_csv(header=True, index=False, line_terminator="\n")

    tbl_xomo = Tbl(xomo_in)
    tbl_pom = Tbl(pom_in)
    root1 = tbl_xomo.projection_split()
    root2 = tbl_pom.projection_split()

    root1.print_tree()
    root2.print_tree()

main()