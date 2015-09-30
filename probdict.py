from collections import UserDict
import itertools
import bisect
import random

class ProbDict(UserDict):

    def __init__(self):
        super().__init__(self)
        return

    def __getitem__(self,key):
        weightedoptions = list(self.data[key].items())
        choices, weights = zip(*weightedoptions)
        cumdist = list(itertools.accumulate(weights))
        x = random.random() * cumdist[-1]
        return choices[bisect.bisect(cumdist, x)]

    def __setitem__(self,key,value):
        if key not in self.data:
            self.data[key] = {value:1}
        else:
            if value in self.data[key]:
                self.data[key][value] += 1
            else:
                self.data[key][value] = 1
        return
