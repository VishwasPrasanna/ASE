from table import Tbl
from tree import DecisionNode
from tree import LeafNode

def main():
    color = '''
    $score, $quality, $potency, !color
    15, 22.7, 2, green
    15, 22.8, 17, green
    15, 22.9, 4, green
    16, 23.0, 27, green
    16, 23.1, 3, green
    16, 23.1, 18, green
    16, 23.2, 15, green
    16, 23.2, 4, blue
    16, 23.3, 7, blue
    16, 23.3, 44, blue
    16, 23.4, 13, blue
    16, 23.4, 1, blue
    16, 23.6, 23, blue
    16, 23.7, 11, blue
    16, 23.7, 12, blue
    16, 23.8, 9, blue
    17, 23.4, 26, yellow
    17, 23.5, 6, yellow
    17, 23.6, 21, yellow
    17, 23.7, 14, yellow
    17, 23.8, 3, yellow
    '''
    tbl = Tbl(color)
    tree = tbl.split()
    tree.print_tree()

    # test, on same data, so its not a good test
    for row in tbl.rows:
        clas = tree.classify(row)
        print("Expected: "+row[3]+" Actual: "+clas)

main()
