__author__ = 'cort'


class Comparable:
    """
    Implements all other comparison methods based on the __lt__() method.
    Code courtesy of Alex Martelli via stackoverflow: http://stackoverflow.com/questions/1061283/lt-instead-of-cmp
    """
    def __eq__(self, other):
        return not self < other and not other<self
    def __ne__(self, other):
        return self < other or other<self
    def __gt__(self, other):
        return other < self
    def __ge__(self, other):
        return not self < other
    def __le__(self, other):
        return not other < self

class Keyed:
    """
    Implements hashing and __lt__ comparison for any class with a __key__() method.
    Code courtesy of Alex Martelli via stackoverflow: http://stackoverflow.com/questions/1061283/lt-instead-of-cmp
    """
    def __lt__(self, other):
        return self.__key__() < other.__key__()
    # and so on for other comparators, as above, plus:

    def __hash__(self):
        return hash(self.__key__())

    def __str__(self):
        return self.__key__()

    def __repr__(self):
        return self.__key__()

