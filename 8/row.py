class Row():
    "Holds numbers in cells, as a horizontal row"

    def __init__(self, inits, num_columns):
        self.cells = []
        for i in range(0, len(inits)):
            if i in num_columns:
                self.cells.append(float(inits[i]))
            else:
                self.cells.append(inits[i])
        self.ign_indices = []
    
    def __getitem__(self, key):
        return self.cells[key]
    
    def print_cells(self):
        print(self.cells)
    
    def get_data(self, index):
        return self.cells[index]

    def add_item(self, item):
        self.cells.append(item)
