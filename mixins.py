__author__ = 'cort'


class ComparableMixin:
    """
    Implements all other comparison methods based on the __lt__() method.
    Code courtesy of Alex Martelli via stackoverflow: http://stackoverflow.com/questions/1061283/lt-instead-of-cmp
    """

    def __eq__(self, other):
        return not self < other and not other < self

    def __ne__(self, other):
        return self < other or other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self


class KeyedMixin:
    """
    Implements hashing and __lt__ comparison for any class with a __key__() method.
    Code courtesy of Alex Martelli via stackoverflow: http://stackoverflow.com/questions/1061283/lt-instead-of-cmp
    """

    def __lt__(self, other):
        return self.__key__() < other.__key__()

    def __hash__(self):
        return hash(self.__key__())

    def __str__(self):
        return self.__key__()

    def __repr__(self):
        return self.__key__()


class ListableMixin:  # todo: test
    """
    Adds listing of specificed attribute names and values to any implementing class.
    """

    def gen_header_list(self, attrs):
        """
        Generates an objects list of attributes iff those attributes are specified in attrs. Order of returned list
        corresponds to order of attrs

        :param attrs: iterable of attribute names to check for
        :return header_list: list of names for all attributes specified in attrs possessed by object. order corresponds
            to order of attrs
        """
        header_list = [a for a in attrs if hasattr(self, a)]
        # for a in attrs:
        # if hasattr(self, a):
        #         header_list.append(a)
        return header_list

    def gen_attr_list(self, attrs):
        """
        Returns a list of all attribute values specified by attrs. Nonexistent attributes are ignored.

        :param attrs: iterable of attribute names to get values for
        :return attr_list: list of values for all attributes specified in attrs possessed by object. order corresponds
            to order of attrs
        """
        attr_list = [str(getattr(self, n)) for n in self.gen_header_list(attrs)]
        # for k in self.gen_header_list(attrs):
        # attr_list.append(str(getattr(self, k)))
        return attr_list