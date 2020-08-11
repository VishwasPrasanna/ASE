import re
from col import Col

class Tbl():
    "Holds data in rows and updates columns"
    # These contain indexes of the columns of Number or String values.
    def __init__(self, table):
        self.num_columns = []
        self.sym_columns = []
        self.ign_columns = []
        self.goal_columns = []
        self.weight_columns = []
        self.xs_columns = []
        self.xnums_columns = []
        # split into lines
        rows = table.splitlines()
        
        #pprint.pprint(rows)

        # remove empty lines
        rows.pop(0) # pops the first line, which is empty
        rows.pop() # pops the last line, which is empty

        #pprint.pprint(rows)

        # split column names
        col_names = rows.pop(0).split(',')
        self.cols = []
        for x in range(0, len(col_names)):
            self.cols.append(Col(col_names[x].strip()))

        # col_names holds the list of columns names extracted from the first row
        # of the data
        col_names = [temp.strip() for temp in col_names]
        #print(col_names)
        self.weight_columns = [1 for temp in col_names]
        for x in range(0, len(col_names)):
            if '?' in col_names[x]:
                self.ign_columns.append(x)
                continue
            elif '$' in col_names[x] or '<' in col_names[x] or '>' in col_names[x]:
                #print("appending "+str(x)+" to num columns")
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
                #print("appending "+str(x)+" to sym columns")
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
                self.cols[x] + float(token)
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

    def zeroRClassify(self, row):
        for col in self.cols:
            if '!' in col.name:
                return col.mode
    
    def getClass(self, index):
        return self.rows[0].get_data(index)


class Row():
    "Holds numbers in cells, as a horizontal row"

    def __init__(self, inits=[]):
        self.cells = inits
    
    def print_cells(self):
        print(self.cells)
    
    def get_data(self, index):
        return self.cells[index]