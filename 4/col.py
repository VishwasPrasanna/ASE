from num import Num
from sym import Sym

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
    
    def like(self, number):
        var = self.sd()**2
        denom = (3.14159*2*var)**.5
        num = 2.71828**(-(number-self.mu)**2/(2*var+0.0001))
        return num/(denom + 10**-64)
        