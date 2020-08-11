import re
from col import Col
from div import Div
from pprint import pprint
from copy import copy
from tree import DecisionNode
from tree import LeafNode
from row import Row
import math
import operator

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
        self.threshold = .05
        self.min_dp = 4
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
            # print(col_names[x])
            self.cols.append(Col(col_names[x].strip()))

        # col_names holds the list of columns names extracted from the first row
        # of the data
        col_names = [temp.strip() for temp in col_names]
        #print(col_names)
        self.weight_columns = [1 for temp in col_names]
        for x in range(0, len(col_names)):
            # print(col_names[x])
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
                    self.class_col = x
                    self.goal_columns.append(x)
                elif "$" in col_names[x]:
                    self.xnums_columns.append(x)
            else:
                self.sym_columns.append(x)
                #print("appending "+str(x)+" to sym columns")
                if '!' in col_names[x]:
                    self.class_col = x
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
                row.ign_indices.append(i)
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
        self.rows.append(Row(cells, self.num_columns))
    
    def add_constructed_row(self, row):
        if len(row.cells) != len(self.cols):
            print("skipping row; incorrect number of columns")
            return
        self.rows.append(copy(row))
        for x in range(0, len(self.cols)):
            if x in self.num_columns:
                self.cols[x] + float(row[x])
            elif x in self.sym_columns:
                self.cols[x].calc_counts(row[x])
    
    # sorts the entire table by a column
    def sort(self, col1, col2):
        self.rows = sorted(self.rows, key=lambda x: (x[col1], x[col2]))

    # constructs two new tables, one left of, and one right of the chosen split, with instructions
    # to ignore the chosen column for the split
    # returns the left and right tables
    def split(self, iteration=0, last_col=-1, last_val=None, last_score=1):
        #score columns
        best_split = None
        best_col = 0
        for col_idx in range(0, len(self.cols)):
            if col_idx in self.ign_columns: continue
            #print("Testing split on column: "+self.cols[col_idx].name)
            self.sort(col_idx, self.class_col)
            list1 = []
            list2 = []
            for row in self.rows:
                if col_idx in self.num_columns:
                    list1.append(float(row[col_idx]))
                else:
                    list1.append(row[col_idx])
                list2.append(row[self.class_col])
            
            zipped_pairs = zip(list1, list2)
            list3 = []
            for item in zipped_pairs:
                list3.append(list(item))
            #pprint(list3)

            # Div on column to get score
            if col_idx != self.class_col:
                if self.class_col in self.num_columns:
                    div = Div(list3, 'NUM')
                    # print("Best Split Index: "+str(div.split_idx)+", Score: "+str(div.score)+", le: "+str(div.le)+", re: "+str(div.re))
                    if best_split == None or div.score < best_split.score:
                        best_split = div
                        best_col = col_idx
                elif self.class_col in self.sym_columns:
                    div = Div(list3, 'SYM')
                    # print("Best Split Index: "+str(div.split_idx)+", Score: "+str(div.score)+", le: "+str(div.le)+", re: "+str(div.re))
                    if best_split == None or div.score < best_split.score:
                        best_split = div
                        best_col = col_idx
            # else:
                # print("we are ignoring this column: "+ self.cols[col_idx].name)
            # print("")
        # print("Splitting on column: "+self.cols[best_col].name)
        # print("Best Split: "+str(best_split.split_idx))
        # print("Split Score: "+ str(best_split.score))
        # sort list by chosen stuff
        if best_split.score > last_score:
            # print("previous split option was better")
            if self.class_col in self.num_columns:
                avg = 0.0
                [avg + row[self.class_col] for row in self.rows]
                avg = avg / len(self.rows)
                return LeafNode(self.cols[self.class_col].mu, self.cols[self.class_col].sd())
            if self.class_col in self.sym_columns:
                mode = dict()
                for row in self.rows:
                    if row[self.class_col] in mode:
                        mode[row[self.class_col]] = mode[row[self.class_col]] + 1
                    else:
                        mode[row[self.class_col]] = 1
                cur_key = None
                cur_prob = 0
                for key, val in mode.items():
                    probability = val/sum(mode.values())
                    if probability > cur_prob:
                        cur_key = key
                        cur_prob = probability
                return LeafNode(self.cols[self.class_col].mode, self.cols[self.class_col].calc_ent())

        self.sort(best_col, self.class_col)
        # self.print_rows()
        # print("split at index: "+str(best_split.split_idx))

        if last_col == best_col and last_val == self.rows[best_split.split_idx][best_col]:
            if self.class_col in self.num_columns:
                return LeafNode(self.cols[self.class_col].mu, self.cols[self.class_col].sd())
            if self.class_col in self.sym_columns:
                return LeafNode(self.cols[self.class_col].mode, self.cols[self.class_col].calc_ent())
        
        # construct tables
        headers = "a\n"
        for i in range(0, len(self.cols) - 1):
            headers = headers + self.cols[i].name + ", "
        headers = headers + self.cols[len(self.cols) - 1].name + "\na"

        # print(headers)
        lft_tbl = Tbl(headers)
        for i in range(0, best_split.split_idx):
            lft_tbl.add_constructed_row(self.rows[i]) 
        rgt_tbl = Tbl(headers)
        for i in range(best_split.split_idx + 1, len(self.rows)):
            rgt_tbl.add_constructed_row(self.rows[i]) 
        
        # for each table, determine if it needs to be split, or if it needs a leaf node
        # print("split index: "+str(best_split.split_idx))
        # print("best column: " +str(best_col))
        root = DecisionNode(best_col, self.rows[best_split.split_idx][best_col], self.cols[best_col].name)
        
        # print("LE: "+str(best_split.le)+" RE: "+str(best_split.re))
        if best_split.le < self.threshold or iteration >= self.min_dp or len(lft_tbl.rows) < self.min_dp:
            if self.class_col in self.num_columns:
                root.set_left_child(LeafNode(lft_tbl.cols[lft_tbl.class_col].mu, lft_tbl.cols[lft_tbl.class_col].sd()))
            if self.class_col in self.sym_columns:
                root.set_left_child(LeafNode(lft_tbl.cols[lft_tbl.class_col].mode, lft_tbl.cols[lft_tbl.class_col].calc_ent()))
        else:
            root.set_left_child(lft_tbl.split(iteration+1, best_col, self.rows[best_split.split_idx][best_col], best_split.le))

        if best_split.re < self.threshold or iteration >= self.min_dp or len(rgt_tbl.rows) < self.min_dp:
            if self.class_col in self.num_columns:
                root.set_right_child(LeafNode(rgt_tbl.cols[rgt_tbl.class_col].mu, rgt_tbl.cols[rgt_tbl.class_col].sd()))
            if self.class_col in self.sym_columns:
                root.set_right_child(LeafNode(rgt_tbl.cols[rgt_tbl.class_col].mode, rgt_tbl.cols[rgt_tbl.class_col].calc_ent()))
        else:
            root.set_right_child(rgt_tbl.split(iteration+1, best_col, self.rows[best_split.split_idx][best_col], best_split.re))

        # return the root node
        return root


    
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
