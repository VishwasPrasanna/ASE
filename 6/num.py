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