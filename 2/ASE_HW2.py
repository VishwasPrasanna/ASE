import random
from pprint import pprint

class Tbl():
    "Holds data in rows and updates columns"

    def __init__(self, table):
        # split into lines
        rows = table.splitlines()
        
        # remove empty lines
        rows.pop(0)
        rows.pop()

        # split column names
        col_names = rows.pop(0).split(',')
        self.cols = []
        self.col_names = []
        self.ign = []
        for x in range(0, len(col_names)):
            self.cols.append(Col(col_names[x].strip(), x+1))
            if '?' not in col_names[x]:
                self.col_names.append(col_names[x].strip())
            else:
                self.ign.append(x)
        print(self.col_names)

        # add remaining rows
        self.rows = []
        [self.add_row(row) for row in rows]
    
        # remove columns whose names contain question marks
        del_list = []
        for x in range(0, len(self.cols)):
          if "?" in self.cols[x].name:
            del_list.insert(0, x)
        
        for i in del_list:
          for row in self.rows:
            row.cells.pop(i)
          self.cols.pop(i)
        

    def add_row(self, row):
        tokens = row.split(',')
        if len(tokens) != len(self.cols):
          print("E> skipping line "+str(len(self.cols)))
          return
        elif '?' in row:
            cells = []
            for x in range(0, len(tokens)):
                token = tokens[x].strip()
                if x not in self.ign:
                    cells.append(token)
            print(cells)
            return
        cells = []
        for x in range(0, len(tokens)):
            token = tokens[x].strip()
            self.cols[x] + int(token)
            if x not in self.ign:
                cells.append(int(token))
        self.rows.append(Row(cells))
        print(cells)
    
    def print_tbl(self):
        self.print_cols()
        self.print_rows()
    
    def print_rows(self):
        print("t.rows")
        for row_idx in range(0, len(self.rows)):
            print("  "+str(row_idx + 1))
            self.rows[row_idx].print_mets()

    def print_cols(self):
        print("t.cols")
        for col_idx in range(0, len(self.cols)):
            print("  "+str(col_idx + 1))
            self.cols[col_idx].print_mets()


class Row():
    "Holds numbers in cells, as a horizontal row"

    def __init__(self, inits=[]):
        self.cells = inits
    
    def print_cells(self):
        print(self.cells)
    
    def print_mets(self):
        print("    cells")
        [print(" "*6+str(i)+": "+str(self.cells[i])) for i in range(0, len(self.cells))]

class Num():
    "Track numbers seen in a column"

    def __init__(self, inits=[]):
        self.n, self.mu, self.m2 = 0, 0, 0
        self.lo, self.hi = 10 ** 32, -1 * 10 ** 32
        [self + x for x in inits]

    def delta(self):
        return self.sd()

    def expect(self):
        return self.mu

    def sd(self):
        return 0 if self.n < 2 else (self.m2 / (self.n - 1 + 10 ** -32)) ** 0.5

    def __add__(self, x):
        if x < self.lo:
            self.lo = x
        if x > self.hi:
            self.hi = x

        self.n += 1
        d = x - self.mu
        self.mu += d / self.n
        self.m2 += d * (x - self.mu)

    def __sub__(self, x):
        if self.n < 2:
            self.n, self.mu, self.m2 = 0, 0, 0
        else:
            self.n -= 1
            d = x - self.mu
            self.mu -= d / self.n
            self.m2 -= d * (x - self.mu)

class Col(Num):
    "Represent numbers in a column"

    def __init__(self, name, pos, inits=[]):
        Num.__init__(self, inits)
        self.name = name
        self.pos = pos
    
    def print_mets(self):
      # print("    add: " + )
      print("    col: " + str(self.pos))
      print("    hi: " + str(self.hi))
      print("    lo: " + str(self.lo))
      print("    m2: " + str(self.m2))
      print("    mu: " + str(self.mu))
      print("    n: " + str(self.n))
      print("    sd: " + str(self.sd()))
      print("    txt: " + str(self.name))

def main():
    s="""
  $cloudCover, $temp, ?$humid, <wind,  $playHours
  100,        68,    80,    0,    3
  0,          85,    85,    0,    0

  0,          80,    90,    10,   0
  60,         83,    86,    0,    4
  100,        70,    96,    0,    3
  100,        65,    70,    20,   0
  70,         64,    65,    15,   5
  0,          72,    95,    0,    0
  0,          69,    70,    0,    4
  ?,          75,    80,    0,    ?
  0,          75,    70,    18,   4
  60,         72,
  40,         81,    75,    0,    2
  100,        71,    91,    15,   0
  """
    # part 2
    new_tbl = Tbl(s)
    # part 3
    # new_tbl.print_tbl()

main()
