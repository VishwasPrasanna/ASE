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