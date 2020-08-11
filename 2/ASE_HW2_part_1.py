import random

class Tbl():
    "Holds data in rows and updates columns"

    def __init__(self, table):
        rows = table.splitlines()
        rows.pop(0)
        rows.pop()
        col_names = rows.pop(0).split(',')
        self.cols = []
        [self.cols.append(Col(x.strip())) for x in col_names]
        self.rows = []
        [self.add_row(row) for row in rows]
    
    def add_row(self, row):
        tokens = row.split(',')
        cells = []
        for x in range(0,len(tokens)):
            token = tokens[x].strip()
            self.cols[x] + int(token)
            cells.append(int(token))
        self.rows.append(Row(cells))
    
    def print_tbl(self):
        self.print_rows()
        self.print_cols()
    
    def print_rows(self):
        print("Rows:")
        [row.print_cells() for row in self.rows]

    def print_cols(self):
        print("Columns:")
        [col.print_mets() for col in self.cols]



class Row():
    "Holds numbers in cells, as a horizontal row"

    def __init__(self, inits=[]):
        self.cells = inits
    
    def print_cells(self):
        print(self.cells)

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

    def __init__(self, name, inits=[]):
        Num.__init__(self, inits)
        self.name = name
    
    def print_mets(self):
      print("\n")
      print("Name: " + self.name)
      print("Mean: " + str(self.mu))
      print("Standard Deviation: " + str(self.sd()))
      print("Lo: " + str(self.lo))
      print("Hi: " + str(self.hi))

def main():
    s="""
 $cloudCover, $temp, $humid, $wind,  $playHours
  100,         68,    80,     0,      3   
  0,           85,    85,     0,      0
  0,           80,    90,     10,     0
  60,          83,    86,     0,      4
  100,         70,    96,     0,      3
  100,         65,    70,     20,     0
  70,          64,    65,     15,     5
  0,           72,    95,     0,      0
  0,           69,    70,     0,      4
  80,          75,    80,     0,      3
  0,           75,    70,     18,     4
  60,          72,    83,     15,     5
  40,          81,    75,     0,      2
  100,         71,    91,     15,     0
    """
    rows = []
    lines = s.splitlines()
    lines.pop(0)
    rows.append(Row(lines.pop(0).split(',')))
    lines.pop()
    for line in lines:
      tokens = line.split(',')
      row = []
      for token in tokens:
        tmp = token.strip()
        row.append(int(tmp))
      rows.append(Row(row))
    
    for row in rows:
      row.print_cells()

main()
