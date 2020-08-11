import re
from col import Col
from div import Div
from pprint import pprint
from copy import copy
from tree import SplitNode
from row import Row
import math
import operator
from fastmap import fastMap
from math import floor,ceil
from distance import distance_between_rows

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
        self.non_goal_columns = []
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
                    self.non_goal_columns.append(x)
                    self.xnums_columns.append(x)
            else:
                self.sym_columns.append(x)
                #print("appending "+str(x)+" to sym columns")
                if '!' in col_names[x]:
                    self.class_col = x
                    self.goal_columns.append(x)
                else:
                    self.non_goal_columns.append(x)
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

    def projection_split(self, initial=0):
        #print(len(self.rows))
        # get fastmap lists
        fastmap_lists = []
        # make list of non-goal column names
        ng_cols = []
        for col_idx in range(0, len(self.cols)):
            if col_idx in self.non_goal_columns:
                ng_cols.append([self.cols[col_idx], col_idx])
        for i in range(0, 10):
            fastmap_lists.append(fastMap(self.rows, ng_cols))
        # print(fastmap_lists)
        best_l,best_r = self.choose_pivots(fastmap_lists, ng_cols)
        # tmp = best_l + best_r
        # tmp.sort()
        # print(tmp)

        # construct tables
        headers = "a\n"
        for i in range(0, len(self.cols) - 1):
            headers = headers + self.cols[i].name + ", "
        headers = headers + self.cols[len(self.cols) - 1].name + "\na"

        lft_tbl = Tbl(headers)
        [lft_tbl.add_constructed_row(self.rows[i]) for i in best_l]
        rgt_tbl = Tbl(headers)
        [rgt_tbl.add_constructed_row(self.rows[i]) for i in best_r]

        # choose whether to iterate on the left and right
        iter_depth = 0
        if initial == 0:
            iter_depth = int(floor(len(self.rows)**(1/2)))
        else:
            iter_depth = initial
        
        # make a tree node
        root = SplitNode(len(self.rows))

        if len(best_l) < iter_depth or len(best_r) < iter_depth:
            [root.add_goal(self.cols[i]) for i in self.goal_columns]

        if len(best_l) > iter_depth:
            # iterate on left table
            lft_child = lft_tbl.projection_split(iter_depth)
            # set left child of tree node
            root.set_left_child(lft_child)
        
        if len(best_r) > iter_depth:
            # iterate on right table
            rgt_child = rgt_tbl.projection_split(iter_depth)
            # set right child of tree node
            root.set_right_child(rgt_child)
        
        return root
        
    def choose_pivots(self, fastmap_lists, cols):
        # choose fastmap pivots
        # for pivots in fastmap_lists:
        best_pivots = None
        best_l = []
        best_r = []
        for pivots in fastmap_lists:
            # list of distances from pivots split line
            cdist = []
            # list of row indices for point in cdist
            cdist_index = []
            for i in range(0, len(self.rows)):
                cos_dist = self.cosdist(pivots[0],pivots[1],pivots[2],i, cols)
                cdist.append(cos_dist)
                cdist_index.append(i)
            cos_zipped = zip(cdist,cdist_index)
            cz = [x for _, x in sorted(cos_zipped)]
            # print(cz)
            #median = None
            #if len(self.rows)%2 == 0:
            #    median = (cdist[cz[int(floor(len(self.rows)/2))]] + cdist[cz[int(ceil(len(self.rows)/2))]])/2
            #else:
            #    median = cdist[cz[int(len(self.rows)/2)]]
            median = (self.cosdist(pivots[0],pivots[1],pivots[2],pivots[0], cols) + self.cosdist(pivots[0],pivots[1],pivots[2],pivots[1], cols))/2

            #creating left and right lists
            left = []
            right = []
            for i in range(0,len(cdist)):
                if cdist[i]<median:
                    left.append(i)
                else:
                    right.append(i)

            if best_pivots == None:
                best_pivots = pivots
                best_l = left
                best_r = right
                # print("first pivot set: "+str(pivots[0])+" "+str(pivots[1])+" with left and right len: "+str(len(left))+", "+str(len(right)))
            elif abs(len(left)-len(right)) < abs(len(best_l)-len(best_r)):
                best_pivots = pivots
                best_l = left
                best_r = right
                # print("new best pivots: "+str(pivots[0])+" "+str(pivots[1])+" with left and right len: "+str(len(left))+", "+str(len(right)))
            # else:
                # print("not replacing pivots with: "+str(pivots[0])+" "+str(pivots[1])+" with left and right len: "+str(len(left))+", "+str(len(right)))
        #till here
        return best_l,best_r

        
    def cosdist(self, pivot1,pivot2,pivot_dist,current_row, cols):
        return (distance_between_rows(self.rows[pivot1], self.rows[current_row], cols)**2 + pivot_dist**2 - distance_between_rows(self.rows[pivot2], self.rows[current_row], cols)**2)/(2*pivot_dist)
    
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
