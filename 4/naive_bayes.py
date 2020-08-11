import re
from table import Tbl

class NaiveBayes():

    def __init__(self, train):
        # make list of tables
        self.tables = []

        #pprint.pprint(train)

        # split into lines
        rows = train.splitlines()
        
        #pprint.pprint(rows)
        
        # remove empty lines
        rows.pop(0) # pops the first line, which is empty
        rows.pop() # pops the last line, which is empty

        #pprint.pprint(rows)

        # store the raw column names line
        self.col_names = rows.pop(0)

        # split column names
        self.class_index = -1
        col_names = self.col_names.split(',')
        self.num_columns = len(col_names)
        for x in range(0, len(col_names)):
            if '!' in col_names[x].strip():
                self.class_index = x
                #print(self.class_index)
                break
        
        # test if class index exists
        if self.class_index == None or self.class_index < 0:
            print("Error; no class attribute")
            exit()
        else :
            #print("about to add rows")
            while (len(rows) > 0):
                self + rows.pop(0)
    
    def __add__(self, row):
        # check class of this row
        comment_regex = r'(# [a-zA-Z0-9]*)'
        new_row = re.sub(comment_regex, ' ', row)
        tokens = row.split(',')
        if len(tokens) != self.num_columns:
            print("skipping row; incorrect number of columns")
            return
        
        row_class = tokens[self.class_index].strip()

        # loop through tables and check their class
        added = False
        for table in self.tables:
            # if we have a table that matches row class, insert
            if table.getClass(self.class_index) == row_class:
                table.add_row(row)
                #print("added row to table for class "+ row_class)
                added = True
                break
        # if we don't have a table, create it 
        if added == False:
            self.tables.append(Tbl('\n'+self.col_names+'\n\n'))
            self.tables[len(self.tables) - 1].add_row(row)
            #print("added new table for class "+ row_class)

    def predict(self, row):
        tokens = row.split(',')
        highest_likeness = 0
        table_number = 0
        # go through tables and get how much they like the data
        # for each table
        for i in range(0, len(self.tables)):
            table = self.tables[i]
            score = 1
            # for each column
            for x in range(0,len(table.cols)):
                # see how much the column likes the data
                # multiply all the likes, giving total like
                try:
                    score *= table.cols[x].like(float(tokens[x].strip()))
                except:
                    continue
            # pick the best score
            if score > highest_likeness:
                highest_likeness = score
                table_number = i
        
        # submit the class of the most liked table
        predicted = self.tables[table_number].getClass(self.class_index)
        actual = tokens[self.class_index].strip()
        # print("predicted: "+predicted+ "; actual: "+actual)
        return predicted
    
    def printTables(self):
        for table in self.tables:
            table.print_tbl()
            