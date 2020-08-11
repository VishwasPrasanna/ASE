from num import Num
from sym import Sym
import math
import operator

class Div():
    '''
    Class for splitting the data 
    '''
    def __init__(self, input_data_string, y_is='NUM'):
        '''
        Constructor method
        '''
        self.list_of_data = sorted(self.convert_string_to_list(input_data_string), key=lambda i: i[1]) # if y_is == 'NUM' else self.convert_string_to_list(input_data_string)
        self.y_is = y_is
        self.trivial = 1.025
        self.cohen = 0.3
        self.step = math.floor((len(self.list_of_data))**0.5)
        self.n = len(self.list_of_data)
        self.split = 1
        self.old_sd = 0
        self.best_lists = []
        self.initial_calculations(self.list_of_data, self.y_is)
        if y_is == 'NUM':
            self.num_recursive(0, self.n, [float(elem[1]) for elem in self.list_of_data])
        elif y_is == 'SYM':
            self.sym_recursive(0, self.n, [elem[1].strip('\'') for elem in self.list_of_data])
        else:
            print('Incorrect value for y_is provided.')

    def sd(self, _list, mean):
        sum_of_means = 0
        for elem in _list:
            sum_of_means += (mean - elem)**2
        return (sum_of_means/(len(_list) + 10**-32))**0.5

    def mean(self, _list):
        mean = 0
        for elem in _list:
            mean += float(elem)
        return mean/len(_list)

    def convert_string_to_list(self, string):
        temp_list = string.split('\n')
        temp_list = [x.strip('\t').strip(']').replace('[', '').replace(',', ' ').split() for x in temp_list]
        temp_list.pop(0)
        temp_list.pop()
        # print(temp_list)
        return temp_list

    def initial_calculations(self, list_of_data, yis):
        if yis == 'NUM':
            mean = self.mean([float(elem[1]) for elem in list_of_data])
            self.old_sd = self.sd([float(elem[1]) for elem in list_of_data], mean)
        elif yis == 'SYM':
            # mode = self.mode(self.mode_hash([elem[1] for elem in list_of_data]))
            self.old_sd = self.entropy(self.mode_hash([elem[1] for elem in list_of_data]))
        else:
            print('Incorrect value for y_is provided.')

    def num_recursive(self, first, last, _list):
        flag = False
        sd_of_list = self.sd(_list, self.mean(_list))
        for i in range(first, last):
            left_list = [float(elem[1]) for elem in self.list_of_data[first:i]]
            right_list = [float(elem[1]) for elem in self.list_of_data[i:last]]
            # print(left_list)
            # print(right_list)
            # print('----------------')
            if len(left_list) >= self.step and len(right_list) >= self.step:
                # print(1)
                if abs(float(self.list_of_data[i][1]) - float(self.list_of_data[0][1])) >= self.cohen*self.old_sd and abs(float(self.list_of_data[i-1][1]) - float(self.list_of_data[-1][1])) >= self.cohen*self.old_sd:
                    # print(2)
                    if abs(self.mean(right_list) - self.mean(left_list)) >= self.old_sd*self.cohen:
                        # print(3)
                        right_mean = self.mean(right_list)
                        left_mean = self.mean(left_list)
                        right_sd = self.sd(right_list, right_mean)
                        left_sd = self.sd(left_list, left_mean)
                        number = len(left_list) + len(right_list)
                        expected_value = len(left_list)/number*left_sd + len(right_list)/number*right_sd
                        # print(expected_value)
                        # print(expected_value*self.trivial)
                        # print(sd_of_list)
                        if expected_value*self.trivial < sd_of_list:
                            # print(self.split)
                            sd_of_list = expected_value
                            self.split = i
                            flag = True
        if flag:
            # print(self.split)
            self.num_recursive(first, self.split, [float(elem[1]) for elem in self.list_of_data[first :self.split]])
            self.num_recursive(self.split, last, [float(elem[1]) for elem in self.list_of_data[self.split:last]])
        else:
            self.best_lists.append([elem for elem in self.list_of_data[first:last]])
        return 0

    def entropy(self, _hash):
        entropy = 0
        for key, val in _hash.items():
            probability = val/sum(_hash.values())
            entropy += -probability*math.log10(probability)/math.log10(2)
        return entropy

    def mode_hash(self, _list):
        _hash = dict()
        for item in _list:
            if item in _hash:
                _hash[item] = _hash[item]+1
            else:
                _hash[item] = 1
        return _hash

    def mode(self, _hash):
        return max(_hash.items(), key=operator.itemgetter(1))[0]

    def sym_recursive(self, first, last, _list):
        flag = False
        entropy_of_list = self.entropy(self.mode_hash(_list))
        for i in range(first, last):
            left_list = [elem[1].strip('\'') for elem in self.list_of_data[first:i]]
            right_list = [elem[1].strip('\'') for elem in self.list_of_data[i:last]]
            # print(left_list)
            # print(right_list)
            # print('----------------')
            if len(left_list) >= self.step and len(right_list) >= self.step:
                # print(1)
                if abs(ord(self.list_of_data[i][1].strip('\'')) - ord(self.list_of_data[0][1].strip('\''))) >= self.cohen*self.old_sd\
                    and abs(ord(self.list_of_data[i-1][1].strip('\'')) - ord(self.list_of_data[-1][1].strip('\''))) >= self.cohen*self.old_sd:
                    # print(2)
                    if abs(ord(self.mode(self.mode_hash(right_list))) - ord(self.mode(self.mode_hash(left_list)))) >= self.old_sd*self.cohen:
                        # print(3)
                        right_entropy = self.entropy(self.mode_hash(right_list))
                        left_entropy = self.entropy(self.mode_hash(left_list))
                        number = len(left_list) + len(right_list)
                        expected_value = len(left_list)/number*left_entropy + len(right_list)/number*right_entropy
                        # print(expected_value)
                        # print(expected_value*self.trivial)
                        # print(entropy_of_list)
                        if expected_value*self.trivial < entropy_of_list:
                            # print(self.split)
                            # print(expected_value)
                            # print(expected_value*self.trivial)
                            # print(entropy_of_list)
                            entropy_of_list = expected_value
                            self.split = i
                            flag = True
        if flag:
            # print(self.split)
            self.sym_recursive(first, self.split, [elem[1].strip('\'') for elem in self.list_of_data[first :self.split]])
            self.sym_recursive(self.split, last, [elem[1].strip('\'') for elem in self.list_of_data[self.split:last]])
        else:
            # print(self.split)
            self.best_lists.append([elem for elem in self.list_of_data[first:last]])
        return 0