import pprint

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
        # print("Update with actual: "+actual+" predicted: "+predicted)
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
            if (a+b+c+d) > 0:
                self.accuracy[val] = round((a+d)/(a+b+c+d), 2)
            if (b+d) > 0:
                self.recall[val] = round(d/(b+d), 2)
            if (a+c) > 0:
                self.false_alarm[val] = round(c/(a+c), 2)
            if (c+d) > 0:
                self.precision[val] = round(d/(c+d), 2)
            import math
            self.f_measure[val] = round(math.sqrt((1-self.precision[val])**2 + self.false_alarm[val]**2),2 )
            if (a+c) > 0:
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
                  