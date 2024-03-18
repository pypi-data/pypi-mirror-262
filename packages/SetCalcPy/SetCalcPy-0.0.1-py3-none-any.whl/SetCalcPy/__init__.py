from powerSetCalc import calcPSetOf


class Set:
    def __init__(self, *elements, universe=[]):
        # Iteration variable for tracking iterations
        self.current = 0

        # If the user mistakenly enters a single list to contain all elements then that list is converted into an
        # elements list
        if len(elements) == 1 and (type(elements[0]) == list or type(elements[0]) == tuple):
            elements = elements[0]

        self.elements = elements
       # elements = self.duplicateRemoval()
        elements = self.elements
        # universe of discourse
        self.universe = universe
        # Converts each iterable element in the set into a set object
        self.elements = tuple(self.toSet(elements))
        self.isProduct = False
    
    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        # This is strictly used for the beginning of iteration
        return self

    '''def __setitem__(self, index, newitem):
        self.elements[index] = newitem
    '''

    def __getitem__(self, index):
        # Used for brackets element accessing
        return self.elements[index]

    def __next__(self):
        # Accesses the next element during iteration
        if self.current < len(self):
            c = self.current
            self.current += 1
            return self.elements[c]
        else:
            self.current = 0
            raise StopIteration

    def __str__(self):
        return str(self.__list__()).replace("[", '{').replace(']','}')

    def __list__(self):
        '''
        Converts the current instance of the set object into a standard list (along with each of its set elements)
        :return: A list of the elements the set
        '''

        return_list = [0 for i in range(len(self.elements))]
        
        for i in range(len(self.elements)):
            # Checks if the current element is iterable
            isIter = Set.isIterable(self.elements[i])
            
            if isIter and type(self.elements[i]) != tuple and not isinstance(self.elements[i], Set):
                # If the current element is mutable, then it's converted to a list
                # notice that even set objects will call the current method to convert to a list until the primitive
                # types are reached
                #print(self.elements[i].elements)
                return_list[i] = list(self.elements[i])
                #return_list[i] = list(self.elements[i])
            elif isIter:
                return_list[i] = self.elements[i].__list__()
            else:
                # If an element is not mutable than it can be added to the return list as is
                return_list[i] = self.elements[i]
        return return_list

    def __set__(self):
        return set(self.__list__())

    def __eq__(self, other):
        return self.equal(other)

    def __abs__(self):
        return len(self)

    def __add__(self, other):
        return self.union(other)

    def __sub__(self, other):
        return self.setMinus(other)

    def __and__(self, other):
        return self.intersection(other)

    def __mul__(self, other):
        return self.cartesianProduct(other)

    '''def __contains__(self, other):
        if isinstance(self, Set) and isinstance(other, Set):
            return Set(other).subsetof(self)
        else:
            return other in self.elements
            '''

    def union(self, setb):
        Set.count = 0
        result = []

        for x in self:
            if x not in result:
                result.append(x)
        for x in setb:
            if x not in result:
                result.append(x)

        return Set(result)

    def setMinus(self, setb):
        result = []

        for x in self:
            if x not in setb:
                result.append(x)
        return Set(result)

    def complement(self):
        return self.setMinus(self.universe)


    @staticmethod
    def isIterable(obj):
        try:
            getattr(obj, '__iter__')
        except AttributeError:
            return False
        return True

    def intersection(self, setb):
        result = []

        for x in self:
            if x in setb:
                result.append(x)

        return Set(result)

    def toSet(self, elements):
        '''
        A helper function used to convert a list of elements to a set; however the constructor should be called for this
        purpose not this method
        :param elements: A list of elements
        :return: A list of elements where all mutable elements have been converted to set objects
        '''

        return_list = [0 for i in range(len(elements))]

        for i in range(len(elements)):

            # Checks to see if the current element is mutable
            isIter = Set.isIterable(elements[i])
            
            if isIter and type(elements[i]) != tuple and not isinstance(elements[i], Set):
                # Converts the current element to a set object
                return_list[i] = Set(elements[i], universe=self.universe)
            else:
                # If the current object is a base type, then it does not need to be converted and is kept as is
                return_list[i] = elements[i]
        return return_list
        
    def duplicateRemoval(self):
        '''
        Removes duplicate elements from the given set object (this is not intended to be called from outside the class
        :return: A list of non-repeating elements
        '''
        clean = []
        for element in self.elements:
            if element not in clean:
                clean.append(element)
        return clean

    @staticmethod
    def inCheck(element, set):
        for x in set:
            if x == element:
                return True
        return False

    def powerSet(self):
        '''
        Calculates the power set of a set
        :return: A power set set object
        '''

        _self = self.__list__()
        powerSet = calcPSetOf(_self)
        return Set(powerSet)

    def subsetof(self, setb):
        """
        Checks if the current set is a subset of the input set
        :param setb: comparison set
        :return: Is this set is a subset of setb
        """
        for y in self.elements:
            found = False
            for x in setb.elements:
                found = x == y
                if found:
                    break
            if not found:
                return False
        return True

    def equal(self, setb):
        '''
        This set is equal to set b
        :param setb:
        :return:
        '''
        if isinstance(setb, Set):

            if self.subsetof(setb) and setb.subsetof(self):
                return True
        return False

    def setDisplayMode(self):
        '''
        Displays each element of the current set by hitting enter each time. This is a good way to display a very long
        set especially when copying
        :return:
        '''

        for x in self:
            print(x, end="\n")
            input()

    def cartesianProduct(self, *setb):
        return Set(self.aCartesianProduct(setb))


    def aCartesianProduct(self, *setb):
        result = []
        if type(setb[0]) == list or type(setb[0]) == tuple and len(setb) == 1:
            setb = setb[0]

        if len(setb) == 1:
            for x in self:
                for y in setb[0]:
                    result.append((x,y))
        else:
            otherComb = setb[0].cartesianProduct(setb[1:])
            for i in range(len(self)):
                for y in otherComb:
                    _y = list(y)
                    _y.insert(0, self[i])
                    result.append(tuple(_y))
        return result
