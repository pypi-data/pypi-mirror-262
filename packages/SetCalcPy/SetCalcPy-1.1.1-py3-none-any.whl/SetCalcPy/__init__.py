from powerSetCalc import calcPSetOf


class Set:
    def __init__(self, *elements, universe=[]):
        """
        Constructs a set object/converts lists to Sets
        :param elements: A list of elements in the set (repeating elements will be removed)
        :param universe: Universe of discourse (Set that should be used when calculating the complement)
        """
        # Iteration variable for tracking iterations
        self.current = 0

        # If the user mistakenly enters a single list to contain all elements then that list is converted into an
        # elements list
        if len(elements) == 1 and (type(elements[0]) == list or type(elements[0]) == tuple):
            elements = elements[0]

        if type(universe) != list or isinstance((universe, Set)):
            print("Error! Universal sets must be specified as a list or Set!")
            raise TypeError

        self.elements = elements
        # elements = self.duplicateRemoval()
        elements = self.elements
        # universe of discourse
        self.universe = Set(universe) if not isinstance(universe, Set) else universe
        # Converts each iterable element in the set into a set object
        self.elements = tuple(self.toSet(elements))
        self.isProduct = False
    
    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        # This is strictly used for the beginning of iteration
        return self

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
        """
        Converts the current instance of the set object into a standard list (along with each of its set elements)
        :return: A list of the elements the set
        """

        return_list = [0 for i in range(len(self.elements))]
        
        for i in range(len(self.elements)):
            # Checks if the current element is iterable
            isIter = Set.isIterable(self.elements[i])
            
            if isIter and type(self.elements[i]) != tuple and not isinstance(self.elements[i], Set):
                # List/dictionaries and other iterable objects are converted to lists using the standard constructor
                return_list[i] = list(self.elements[i])
            elif isIter and type(self.elements[i]) != tuple:
                # Converts set objects to lists
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

    @staticmethod
    def tryConvert(obj):
        """
        Tries to convert the input object into a set object.
        :param obj: Object to be converted into a set
        :return: Unchanged obj if it is already a set object; otherwise, the object is attempted to be converted into a
        set if possible, if this can't be done, a value error is thrown
        """
        if not isinstance(obj, Set):
            if Set.isIterable(obj) and type(obj) != tuple:
                obj = Set(obj)
            else:
                print("Please input a set object")
                raise TypeError
        return obj

    def union(self, setb):
        """
        Takes the union of two sets
        :param setb: Set object to be unionized with self
        :return: The set of all elements in either the calling set or setb
        """
        setb = Set.tryConvert(setb)

        result = []

        for x in self:
            if x not in result:
                result.append(x)
        for x in setb:
            if x not in result:
                result.append(x)

        return Set(result)

    def setMinus(self, setb):
        """
        Calculates the disjoint of self - setb
        :param setb: The return set should be disjoint with
        :return: A set containing all elements of the calling that are not in setb
        """
        setb = Set.tryConvert(setb)
        result = []

        for x in self:
            if x not in setb:
                result.append(x)
        return Set(result)

    def complement(self):
        """
        Calculates the complement of the calling set with its declared universe
        :return: All elements in the calling set, but not in the universal set
        """
        return self.setMinus(self.universe)


    @staticmethod
    def isIterable(obj):
        """
        Checks if the object passed is ierable
        :param obj: Any object
        :return: True if the object is iterable and false if not
        """
        try:
            getattr(obj, '__iter__')
        except AttributeError:
            return False
        return True

    def intersection(self, setb):
        """
        Calculates the intersection of two sets
        :param setb: set to be intersected with the calling set
        :return: All elements in the calling set and in setb
        """
        setb = Set.tryConvert(setb)
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

            # Checks to see if the current element is iterable
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
        """
        Checks if an element is in set (this was used for purposes of preventing infinite recursion using the
        __contains__ operator
        :param element: Any object to be inspected for membership of set
        :param set: The Set that element should be checked for membership against
        :return:
        """
        for x in set:
            if x == element:
                return True
        return False

    def powerSet(self):
        '''
        Calculates the powerset of a set
        :return: A set containing all subsets of the calling set
        '''

        _self = self.__list__()
        # This relies on the compiled python extension imported
        powerSet = calcPSetOf(_self)
        return Set(powerSet)

    def subsetof(self, setb):
        """
        Checks if the current set is a subset of the input set
        :param setb: comparison set
        :return: Is this set a subset of setb
        """
        setb = Set.tryConvert(setb)
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
        """
        Checks if the calling set is equal to setb (that it is a subset of setb and setb is a subset of it)
        :param setb: It's checked if the calling set is a subset of this set
        :return: True if the calling set is a subset of this set and false if not
        """

        if isinstance(setb, Set):
            if self.subsetof(setb) and setb.subsetof(self):
                return True
        return False

    def setDisplayMode(self):
        """
        Displays each element of the current set by hitting enter each time. This is a good way to display a very long
        set especially when copying
        :return: Nothing
        """

        for x in self:
            print(x, end="\n")
            input()

    def cartesianProduct(self, *setb):
        """
        Calculates the cartesian product of the calling set and the variable number of sets input.
        Input 2 sets for a normal product =
        Input 3 sets for a triple product
        etc.
        :param setb: Multiple sets separated by commas
        :return: A set of ordered pairs. When doing a normal product (A*B), each element is of the form (a,b),
        where a is in the calling set (A) and b is in B
        """
        return Set(self.aCartesianProduct(setb))

    def aCartesianProduct(self, *setb):
        """
        The helper function to calculate various cartesian products
        :param setb: A list of sets to be used in the cartesian product
        :return: A list of ordered pairs representing the cartesian product of self with all the sets in setb
        """

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
