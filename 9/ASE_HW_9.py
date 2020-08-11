from table import Tbl
import pandas as pd
from row import Row
import copy

def main():
    # xomo_xl = 'xomo10000.csv'
    pom_xl = 'pom310000.csv'
    # xomo = pd.read_csv(xomo_xl)
    pom = pd.read_csv(pom_xl)
    # xomo_in = "\n"+xomo.to_csv(header=True, index=False, line_terminator="\n")
    pom_in = "\n"+pom.to_csv(header=True, index=False, line_terminator="\n")

    pom_tbl = Tbl(pom_in)
    pom_tbl.shuffle()
    pom_tbl.rows[0].tag = 1
    print("Full Tables\n")
    print("Before: ", end='')
    pom_tbl.projection_split().update()
    print("After:")
    for i in range(0, 20):
        pom_tbl.projection_split().update()
    print("\nPartial Tables\n")
    pom_5k_tbl = Tbl(pom_tbl.get_headers())
    for i in range(0, 500):
        pom_5k_tbl.add_constructed_row(pom_tbl.rows[i])
    pom_cluster = pom_5k_tbl.projection_split()
    print("Before: ", end='')
    pom_cluster.update()
    print("After: ")
    for j in range(0, 20):
        pom_cluster_cpy = copy.deepcopy(pom_cluster)
        # 'dribble' in the remaining rows and update kids if new data is anomalous
        for i in range(500, 9999):
            # xomo_cluster.dribble(xomo_tbl.rows[i])
            pom_cluster_cpy.dribble(pom_tbl.rows[i])
        pom_cluster_cpy.update()

    


main()