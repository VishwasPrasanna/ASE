from table import Tbl
import pandas as pd

def main():
    auto_xl = 'auto.xlsx'
    auto = pd.read_excel(auto_xl)
    auto_in = "\n"+auto.to_csv(header=True, index=False, line_terminator="\n")

    tbl1 = Tbl(auto_in)
    tbl1.contrast_set()

main()