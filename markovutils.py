from random import random as rand
from random import choice
from collections import deque as queue
from math import floor

class ObjectProbPair:
    def __init__(self):
        self.pairs = []
    def __contains__(self,key):
        return key.element in [obj.element for obj in self.pairs]


class ProbDict:
    def __init__(self):
        self.mappings = {}
        return
    def insert(self,key,value):
        if key in self.mappings:
            if value in self.mappings[key].iterkeys():
                self.mappings[key][value] += 1
            else:
                self.mappings[key][value] = 1
        else:
            self.mappings[key] = {}
            self.mappings[key][value] = 1
        return
    def getByKey(self,key):
        weightedlist = []
        for elem, weight in self.mappings[key].iteritems():
            weightedlist.extend([elem]*weight)
        return choice(weightedlist)

class AbstractElement:
    def __init__(self, element, terminal=False):
        self.element = element
        self.isTerminal = terminal

        return

#MarkovModel takes a sequence of sequences and a depth and creates a model using
# the ProbDict class. Class must be instantiated before calling any of its methods.

#resynth- method used in instantiation and in strengthening based on new
# sequences to feed the model.

#generate- method used to put out new sequence based on succession probabilities
# in the mappings ProbDict.
class MarkovModel:

    def __init__(self,metasequence = [],depth = 1):
        self.mappings = ProbDict()
        self.depth = depth
        for sequence in metasequence:
            self.resynth(sequence)
        return

    def resynth(self,sequence):
        running_list = queue([])
        for i, element in enumerate(sequence):
            wrappedelem = AbstractElement(element,i == len(sequence)-1)
            if (len(running_list) < self.depth):
                running_list.append(wrappedelem)
            else:
                self.mappings.insert(tuple(running_list),wrappedelem)
                running_list.popleft()
                running_list.append(wrappedelem)
        return

    def generate(self):
        running_list = queue(choice(list(self.mappings.mappings.iterkeys())))
        generated_sequence = []
        for elem in running_list:
            generated_sequence.append(elem.element)
            if elem.isTerminal:
                return generated_sequence
        next_elem = self.mappings.getByKey(tuple(running_list))
        running_list.popleft()
        running_list.append(next_elem)
        generated_sequence.append(next_elem.element)

        while not next_elem.isTerminal:
            next_elem = self.mappings.getByKey(tuple(running_list))
            running_list.popleft()
            running_list.append(next_elem)
            generated_sequence.append(next_elem.element)

        return generated_sequence
