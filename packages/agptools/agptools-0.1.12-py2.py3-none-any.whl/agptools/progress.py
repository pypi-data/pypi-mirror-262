import time
# ----------------------------------------------------------
# Progress
# ----------------------------------------------------------
class Progress:
    def __init__(self, x0=0, N=10):
        self.N = N
        self.samples = []
        self.update(x0)

    def update(self, x):
        sample = time.time(), x
        self.samples.append(sample)
