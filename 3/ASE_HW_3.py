import random
import re
import operator

class Tbl():
    "Holds data in rows and updates columns"
    # These contain indexes of the columns of Number or String values.
    num_columns = []
    sym_columns = []
    ign_columns = []
    goal_columns = []
    weight_columns = []
    xs_columns = []
    xnums_columns = []
    def __init__(self, table):
        # split into lines
        rows = table.splitlines()
        
        # remove empty lines
        rows.pop(0) # pops the first line, which is empty
        rows.pop() # pops the last line, which is empty

        # split column names
        col_names = rows.pop(0).split(',')
        self.cols = []
        for x in range(0, len(col_names)):
            self.cols.append(Col(col_names[x].strip()))

        # col_names holds the list of columns names extracted from the first row
        # of the data
        col_names = [temp.strip() for temp in col_names]
        self.weight_columns = [1 for temp in col_names]
        for x in range(0, len(col_names)):
            if '?' in col_names[x]:
                self.ign_columns.append(x)
                continue
            elif '$' in col_names[x] or '<' in col_names[x] or '>' in col_names[x]:
                self.num_columns.append(x)
                if '<' in col_names[x] or '>' in col_names[x]:
                    self.goal_columns.append(x)
                if '<' in col_names[x]:
                    self.weight_columns[x] = -1
                if '!' in col_names[x]:
                    self.goal_columns.append(x)
                elif "$" in col_names[x]:
                    self.xnums_columns.append(x)
            else:
                self.sym_columns.append(x)
                if '!' in col_names[x]:
                    self.goal_columns.append(x)
                else:
                    self.xs_columns.append(x)
        # print(col_names)
        # print(self.num_columns)
        # print(self.sym_columns)
        # print(self.goal_columns)
        # print(self.ign_columns)
        # print(self.weight_columns)
        # throw out rows with question marks
        del_list = []
        for x in range(0, len(rows)):
            if "?" in rows[x]:
                del_list.insert(0, x)
        
        for i in del_list:
            rows.pop(i)

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
            # self.cols.pop(i)
        

    def add_row(self, row):
        '''
        This function cleans the data, removes Whitespace and creates a list of
        objects for of class Row().
        For Columsn of type NUM it adds the value of each number to the self.cols[]
        with the overloaded __add__ function
        For Column of type SYM
        '''
        comment_regex = r'(# [a-zA-Z0-9]*)'
        row = re.sub(comment_regex, ' ', row)
        tokens = row.split(',')
        if len(tokens) != len(self.cols):
            print("skipping row; incorrect number of columns")
            return
        cells = []
        for x in range(0, len(tokens)):
            token = tokens[x].strip()
            if x in self.num_columns:
                self.cols[x] + int(token)
            elif x in self.sym_columns:
                self.cols[x].calc_counts(token)
            cells.append(token)
        self.rows.append(Row(cells))
    
    def print_tbl(self):
        self.print_rows()
        self.print_cols()
        print("\n")
        print('Class:\n______' + str(len(self.cols)))
        self.print_my_lists("Goal", self.goal_columns)
        self.print_my_lists("Nums", self.num_columns)
        self.print_my_lists("Syms", self.sym_columns)
        self.print_my_lists("Weight", [x-1 for x in self.weight_columns if x == -1])
        self.print_my_lists("XS ", self.xs_columns)
        self.print_my_lists("XNUMS", self.xnums_columns)

    def print_rows(self):
        print("Rows:")
        [row.print_cells() for row in self.rows]

    def print_cols(self):
        print("Columns:")
        # [col.print_mets() for col in self.cols]
        # print(self.num_columns)
        # print(self.sym_columns)
        for x in range(0, len(self.cols)):
            if x in self.num_columns:
                self.cols[x].print_mets(x)
            if x in self.sym_columns:
                self.cols[x].print_syms(x)

    def print_my_lists(self, list_name, _list):
        print(list_name + ":")
        for item in _list:
            print("______" + str(item + 1))




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
            
class Sym():
    def __init__(self, name):
        self.n=0
        self.mode = ""
        self.most = 0
        self.name = name
        self.hash = {}
        self.entropy = 0
        self.probability = 0
        self.count = 0

    def calc_counts(self, item):
        if item in self.hash:
            self.hash[item] = self.hash[item]+1
        else:
            self.hash[item] = 1
        self.mode = max(self.hash.items(), key=operator.itemgetter(1))[0]
        self.most = self.hash[self.mode]
        self.n = len(self.hash.keys())
        self.count += 1

    def calc_ent(self):
        import math
        for key, val in self.hash.items():
            self.probability = val/self.count
            self.entropy += -self.probability*math.log10(self.probability)/math.log10(2)
        return self.entropy



class Col(Num, Sym):
    "Represent numbers in a column"

    def __init__(self, name, inits=[]):
        Num.__init__(self, inits)
        Sym.__init__(self, name)
        self.name = name
    
    def print_mets(self, col_number):
        print("\n")
        print("Name: " + self.name)
        print("Column Number: " + str(int(col_number)+1))
        print("Add: Num")
        print("Mean: " + str(self.mu))
        print("Variance: " + str(self.m2))
        print("Standard Deviation: " + str(self.sd()))
        print("Lo: " + str(self.lo))
        print("Hi: " + str(self.hi))

    def print_syms(self, col_number):
        '''
        To be defined
        Will work similar to print_mets() but for columns identified as Sym (look at 
        sym_columsn to figure out which is which).
        Remember to add 1 to each column index when printing as the requirement is to 
        print indices starting at 1
        '''
        print("\n")
        print("Add: Sym")
        print("Column Number: " + str(int(col_number)+1))
        print("Column Name: " + self.name)
        print("Count:")
        for key, value in self.hash.items():
            print("\t" + key + " : " + str(value))
        print("Mode: " + str(self.mode))
        print("Most: " + str(self.most))
        print("Number " + str(self.n))
        print("Entropy " + str(self.calc_ent()))

class Abcd():

    def __init__(self, data="data", rx="rx"):
        self.data = data
        self.rx = rx
        self.n = 0
        self.confusion_mat = [[0,0,0],[0,0,0],[0,0,0]]
        self.confusion_hash = {"yes": 0, "no": 1, "maybe": 2}
        self.abcd = [[[0,0],[0,0]],[[0,0],[0,0]],[[0,0],[0,0]]]
        self.accuracy = [0,0,0]
        self.precision = [0,0,0]
        self.recall = [0,0,0]
        self.false_alarm = [0,0,0]
        self.f_measure = [0,0,0]
        self.g_measure = [0,0,0]

    def update_confusion(self, actual, predicted):
        column_index = self.confusion_hash[actual]
        row_index = self.confusion_hash[predicted]
        self.confusion_mat[column_index][row_index] += 1
        self.n+=1
    
    def calc_abcd(self):
        '''
        self.abcd[yes/no/maybe][col][row]
            [0][0][0] => Yes a
            [0][1][0] => Yes b
            [0][0][1] => Yes c
            [0][1][1] => Yes d
            and so on...
        '''
        # For YES Values
        self.abcd[0][0][0] = self.abcd[0][0][0] + self.confusion_mat[1][1] +\
                            self.confusion_mat[2][1] + self.confusion_mat[1][2] +\
                            self.confusion_mat[2][2]
        self.abcd[0][1][0] = self.abcd[0][1][0] + self.confusion_mat[0][1] + self.confusion_mat[0][2]
        self.abcd[0][0][1] = self.abcd[0][0][1] + self.confusion_mat[1][0] + self.confusion_mat[2][0]
        self.abcd[0][1][1] += self.confusion_mat[0][0]
        
        # For NO Values
        self.abcd[1][0][0] = self.abcd[1][0][0] + self.confusion_mat[0][0] +\
                            self.confusion_mat[2][2] + self.confusion_mat[0][2] +\
                            self.confusion_mat[2][0]
        self.abcd[1][1][0] = self.abcd[1][1][0] + self.confusion_mat[1][0] + self.confusion_mat[1][2]
        self.abcd[1][0][1] = self.abcd[1][0][1] + self.confusion_mat[0][1] + self.confusion_mat[2][1]
        self.abcd[1][1][1] += self.confusion_mat[1][1]
        
        # For MAYBE Values
        self.abcd[2][0][0] = self.abcd[2][0][0] + self.confusion_mat[0][0] +\
                            self.confusion_mat[1][1] + self.confusion_mat[1][0] +\
                            self.confusion_mat[0][1]
        self.abcd[2][1][0] = self.abcd[2][1][0] + self.confusion_mat[2][0] + self.confusion_mat[2][1]
        self.abcd[2][0][1] = self.abcd[2][0][1] + self.confusion_mat[0][2] + self.confusion_mat[1][2]
        self.abcd[2][1][1] += self.confusion_mat[2][2]
    
    def calc_perfomance(self):
        for key,val in self.confusion_hash.items():
            a = self.abcd[val][0][0]
            b = self.abcd[val][1][0]
            c = self.abcd[val][0][1]
            d = self.abcd[val][1][1]
            self.accuracy[val] = round((a+d)/(a+b+c+d), 2)
            self.recall[val] = round(d/(b+d), 2)
            self.false_alarm[val] = round(c/(a+c), 2)
            self.precision[val] = round(d/(c+d), 2)
            import math
            self.f_measure[val] = round(math.sqrt((1-self.precision[val])**2 + self.false_alarm[val]**2),2 )
            self.g_measure[val] = round((b+d)/(a+c), 2)
            
    
    def print_confusion(self):
        print(self.confusion_mat)
        print(self.abcd)
        print(self.accuracy)
        print(self.recall)
        print(self.false_alarm)
        print(self.precision)
        print(self.f_measure)
        print(self.g_measure)
        
    def pretty_print(self):
        print(" db |\trx|\tnum|\ta|\tb|\tc|\td|\tacc|\tpre|\tpd|\tpf|\t  f|\t  g| class")
        for key,val in self.confusion_hash.items():
            print(self.data + '|\t' + self.rx + '|\t' + str(self.n) + '|\t' + str(self.abcd[val][0][0]) + '|\t' +\
                  str(self.abcd[val][1][0]) + '|\t' + str(self.abcd[val][0][1]) + '|\t' + str(self.abcd[val][1][1])\
                   + '|\t' + str(self.accuracy[val]) + '|\t' + str(self.precision[val]) + '|\t' + str(self.recall[val])\
                  + '|\t' + str(self.false_alarm[val]) + '|\t' + str(self.f_measure[val]) + '|\t'\
                  + str(self.g_measure[val]) + '|\t' + key)




def main():
    s="""
    $cloudCover, $temp, ?$humid, <wind,  $playHours
    100,        68,    80,    0,    3    # comments
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
    s2 = '''
    outlook, ?$temp,  <humid, wind, !play
    rainy, 68, 80, FALSE, yes # comments
    sunny, 85, 85,  FALSE, no
    sunny, 80, 90, TRUE, no
    overcast, 83, 86, FALSE, yes
    rainy, 70, 96, FALSE, yes
    rainy, 65, 70, TRUE, no
    overcast, 64, 65, TRUE, yes
    sunny, 72, 95, FALSE, no
    sunny, 69, 70, FALSE, yes
    rainy, 75, 80, FALSE, yes
    sunny, 75, 70, TRUE, yes
    overcast, 72, 90, TRUE, yes
    overcast, 81, 75, FALSE, yes
    rainy, 71, 91, TRUE, no
    '''
    new_tbl = Tbl(s2)
    new_tbl.print_tbl()
    test_obj = Abcd()

    for i in range(0,6):
        test_obj.update_confusion('yes', 'yes')
    for i in range(0,2):
        test_obj.update_confusion('no', 'no')
    for i in range(0, 5):
        test_obj.update_confusion('maybe', 'maybe')
    test_obj.update_confusion('maybe', 'no')

    test_obj.calc_abcd()
    test_obj.calc_perfomance()
    print('\n')
    test_obj.pretty_print()

main()
