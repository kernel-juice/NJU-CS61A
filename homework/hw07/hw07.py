""" Homework 07: Special Method, Linked Lists and Mutable Trees"""

#####################
# Required Problems #
#####################


class Polynomial:
    """Polynomial.

    >>> a = Polynomial([0, 1, 2, 3, 4, 5, 0])
    >>> a
    Polynomial([0, 1, 2, 3, 4, 5])
    >>> print(a)
    0 + 1*x^1 + 2*x^2 + 3*x^3 + 4*x^4 + 5*x^5
    >>> b = Polynomial([-1, 0, -2, 1, -3])
    >>> print(b)
    -1 + 0*x^1 + -2*x^2 + 1*x^3 + -3*x^4
    >>> print(a + b)
    -1 + 1*x^1 + 0*x^2 + 4*x^3 + 1*x^4 + 5*x^5
    >>> print(a * b)
    0 + -1*x^1 + -2*x^2 + -5*x^3 + -7*x^4 + -12*x^5 + -11*x^6 + -15*x^7 + -7*x^8 + -15*x^9
    >>> print(a)
    0 + 1*x^1 + 2*x^2 + 3*x^3 + 4*x^4 + 5*x^5
    >>> print(b) # a and b should not be changed
    -1 + 0*x^1 + -2*x^2 + 1*x^3 + -3*x^4
    >>> zero = Polynomial([0])
    >>> zero
    Polynomial([0])
    >>> print(zero)
    0
    """

    def __init__(self, lst: list) -> None:
        while lst:
            if lst[-1] == 0:
                lst.pop(-1)
            else:
                break
        if lst:
            self.lst = lst
        else:
            self.lst = [0]

    def __repr__(self) -> str:
        return f'Polynomial({self.lst})'

    def __str__(self) -> str:
        string = f'{self.lst[0]}'
        for i in range(1, len(self.lst)):
            string += f' + {self.lst[i]}*x^{i}'
        return string

    def __add__(self, other):
        if isinstance(other, int):
            return Polynomial([self.lst[0] + other] + self.lst[1:])
        elif isinstance(other, Polynomial):
            shorter_lst = self.lst if len(self.lst) < len(other.lst)\
                else other.lst
            longer_lst = other.lst if shorter_lst is self.lst else self.lst
            copy_shorter_lst = shorter_lst[:]
            for _ in range(len(shorter_lst), len(longer_lst)):
                copy_shorter_lst.append(0)
            return Polynomial([i + j for i, j in zip(copy_shorter_lst, longer_lst)])

    def __radd__(self, other):
        return Polynomial([self.lst[0] + other] + self.lst[1:])

    def __mul__(self, other):
        if isinstance(other, int):
            return Polynomial([other * i for i in self.lst])
        elif isinstance(other, Polynomial):
            result_lst = [0] * 2 * max(len(self.lst), len(other.lst))
            for i in range(len(self.lst)):
                for j in range(len(other.lst)):
                    result_lst[i + j] += self.lst[i] * other.lst[j]
            return Polynomial(result_lst)

    def __rmul__(self, other):
        return Polynomial([other * i for i in self.lst])


def remove_duplicates(lnk):
    """ Remove all duplicates in a sorted linked list.

    >>> lnk = Link(1, Link(1, Link(1, Link(1, Link(5)))))
    >>> Link.__init__, hold = lambda *args: print("Do not steal chicken!"), Link.__init__
    >>> try:
    ...     remove_duplicates(lnk)
    ... finally:
    ...     Link.__init__ = hold
    >>> lnk
    Link(1, Link(5))
    """
    if isinstance(lnk, Link) and lnk.rest:
        if lnk.first == lnk.rest.first:
            lnk.rest = lnk.rest.rest
            remove_duplicates(lnk)
        else:
            remove_duplicates(lnk.rest)


def reverse(lnk):
    """ Reverse a linked list.

    >>> a = Link(1, Link(2, Link(3)))
    >>> # Disallow the use of making new Links before calling reverse
    >>> Link.__init__, hold = lambda *args: print("Do not steal chicken!"), Link.__init__
    >>> try:
    ...     r = reverse(a)
    ... finally:
    ...     Link.__init__ = hold
    >>> print(r)
    <3 2 1>
    >>> a.first # Make sure you do not change first
    1
    """
    if isinstance(lnk, Link):
        temp = lnk
        while lnk.rest:
            temp_refer = lnk.rest.rest
            lnk.rest.rest = temp
            temp = lnk.rest
            lnk.rest = temp_refer
        return temp
    else:
        return Link.empty


class Tree:
    """
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """

    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str

        return print_tree(self).rstrip()

    def __eq__(self, other):  # Does this line need to be changed?
        """Returns whether two trees are equivalent.

        >>> t1 = Tree(1, [Tree(2, [Tree(3), Tree(4)]), Tree(5, [Tree(6)]), Tree(7)])
        >>> t1 == t1
        True
        >>> t2 = Tree(1, [Tree(2, [Tree(3), Tree(4)]), Tree(5, [Tree(6)]), Tree(7)])
        >>> t1 == t2
        True
        >>> t3 = Tree(0, [Tree(2, [Tree(3), Tree(4)]), Tree(5, [Tree(6)]), Tree(7)])
        >>> t4 = Tree(1, [Tree(5, [Tree(6)]), Tree(2, [Tree(3), Tree(4)]), Tree(7)])
        >>> t5 = Tree(1, [Tree(2, [Tree(3), Tree(4)]), Tree(5, [Tree(6)])])
        >>> t1 == t3 or t1 == t4 or t1 == t5
        False
        """
        if isinstance(other, Tree):
            if self.is_leaf():
                if (other.is_leaf()) and (self.label == other.label):
                    return True
                else:
                    return False
            elif other.is_leaf():
                return False
            elif self.label != other.label:
                return False
            elif len(self.branches) != len(other.branches):
                return False
            else:
                return all([i == j for i, j in zip(self.branches, other.branches)])
        else:
            return False


def generate_paths(t, value):
    """Yields all possible paths from the root of t to a node with the label value
    as a list.

    >>> t1 = Tree(1, [Tree(2, [Tree(3), Tree(4, [Tree(6)]), Tree(5)]), Tree(5)])
    >>> print(t1)
    1
      2
        3
        4
          6
        5
      5
    >>> next(generate_paths(t1, 6))
    [1, 2, 4, 6]
    >>> path_to_5 = generate_paths(t1, 5)
    >>> sorted(list(path_to_5))
    [[1, 2, 5], [1, 5]]

    >>> t2 = Tree(0, [Tree(2, [t1])])
    >>> print(t2)
    0
      2
        1
          2
            3
            4
              6
            5
          5
    >>> path_to_2 = generate_paths(t2, 2)
    >>> sorted(list(path_to_2))
    [[0, 2], [0, 2, 1, 2]]
    """
    def with_list(t, value, lst=[]):
        assert isinstance(t, Tree) and isinstance(lst, list)
        lst.append(t.label)
        if value == t.label:
            yield lst
        if t.branches:
            for i in t.branches:
                yield from with_list(i, value, lst[:])
    return with_list(t, value)


def count_coins(total, denominations):
    """
    Given a positive integer `total`, and a list of denominations,
    a group of coins make change for `total` if the sum of them is `total` 
    and each coin is an element in `denominations`.
    The function `count_coins` returns the number of such groups. 
    """
    if total == 0:
        return 1
    if total < 0:
        return 0
    if len(denominations) == 0:
        return 0
    without_current = count_coins(total, denominations[1:])
    with_current = count_coins(total - denominations[0], denominations)
    return without_current + with_current


def count_coins_tree(total, denominations):
    """
    >>> count_coins_tree(1, []) # Return None since there is no way to make change with empty denominations
    >>> t = count_coins_tree(3, [1, 2]) 
    >>> print(t) # 2 ways to make change for 3 cents
    3, [1, 2]
      2, [1, 2]
        2, [2]
          1
        1, [1, 2]
          1
    >>> # 6 ways to make change for 15 cents
    >>> t = count_coins_tree(15, [1, 5, 10, 25]) 
    >>> print(t)
    15, [1, 5, 10, 25]
      15, [5, 10, 25]
        10, [5, 10, 25]
          10, [10, 25]
            1
          5, [5, 10, 25]
            1
      14, [1, 5, 10, 25]
        13, [1, 5, 10, 25]
          12, [1, 5, 10, 25]
            11, [1, 5, 10, 25]
              10, [1, 5, 10, 25]
                10, [5, 10, 25]
                  10, [10, 25]
                    1
                  5, [5, 10, 25]
                    1
                9, [1, 5, 10, 25]
                  8, [1, 5, 10, 25]
                    7, [1, 5, 10, 25]
                      6, [1, 5, 10, 25]
                        5, [1, 5, 10, 25]
                          5, [5, 10, 25]
                            1
                          4, [1, 5, 10, 25]
                            3, [1, 5, 10, 25]
                              2, [1, 5, 10, 25]
                                1, [1, 5, 10, 25]
                                  1
    """
    def can_make_amount(total, denominations):
        dp = [False] * (total + 1)
        if dp:
            dp[0] = True
            for bill in denominations:
                for amount in range(bill, total + 1):
                    if dp[amount - bill]:
                        dp[amount] = True
                if dp[total]:
                    return True
        return False

    if not can_make_amount(total, denominations):
        return None
    else:
        if total == 0:
            not_using = Tree(1)
        else:
            not_using = count_coins_tree(total, denominations[1:])
        if total - denominations[0] == 0:
            using = Tree(1)
        else:
            using = count_coins_tree(total - denominations[0], denominations)
        if using:
            if not_using:
                return Tree(f"{total}, {denominations}", [not_using, using])
            else:
                return Tree(f"{total}, {denominations}", [using])
        elif not_using:
            return Tree(f"{total}, {denominations}", [not_using])
        else:
            return Tree(f"{total}, {denominations}")


def is_bst(t):
    """Returns True if the Tree t has the structure of a valid BST.

    >>> t1 = Tree(6, [Tree(2, [Tree(1), Tree(4)]), Tree(7, [Tree(7), Tree(8)])])
    >>> is_bst(t1)
    True
    >>> t2 = Tree(8, [Tree(2, [Tree(9), Tree(1)]), Tree(3, [Tree(6)]), Tree(5)])
    >>> is_bst(t2)
    False
    >>> t3 = Tree(6, [Tree(2, [Tree(4), Tree(1)]), Tree(7, [Tree(7), Tree(8)])])
    >>> is_bst(t3)
    False
    >>> t4 = Tree(1, [Tree(2, [Tree(3, [Tree(4)])])])
    >>> is_bst(t4)
    True
    >>> t5 = Tree(1, [Tree(0, [Tree(-1, [Tree(-2)])])])
    >>> is_bst(t5)
    True
    >>> t6 = Tree(1, [Tree(4, [Tree(2, [Tree(3)])])])
    >>> is_bst(t6)
    True
    >>> t7 = Tree(2, [Tree(1, [Tree(5)]), Tree(4)])
    >>> is_bst(t7)
    False
    """
    def all_smaller(t, value):
        """
        return True if all nodes of a tree are smaller than or equal to a value.
        """
        assert isinstance(t, Tree)
        if t.is_leaf():
            if t.label <= value:
                return True
            else:
                return False
        else:
            return t.label <= value and all([all_smaller(i, value) for i in t.branches])

    def all_bigger(t, value):
        """
        return True if all nodes of a tree are bigger than a value.
        """
        assert isinstance(t, Tree)
        if t.is_leaf():
            if t.label > value:
                return True
            else:
                return False
        else:
            return t.label > value and all([all_bigger(i, value) for i in t.branches])
    assert isinstance(t, Tree)
    if t.is_leaf():
        return True
    elif len(t.branches) > 2:
        return False
    elif len(t.branches) == 1:
        if t.branches[0].label <= t.label:
            return all_smaller(t.branches[0], t.label) and is_bst(t.branches[0])
        else:
            return all_bigger(t.branches[0], t.label) and is_bst(t.branches[0])
    elif (not all_smaller(t.branches[0], t.label)) or (not all_bigger(t.branches[1], t.label)):
        return False
    else:
        return all([is_bst(t.branches[0]), is_bst(t.branches[1])])


##########################
# Just for fun Questions #
##########################

def has_cycle(lnk):
    """ Returns whether lnk has cycle.

    >>> lnk = Link(1, Link(2, Link(3)))
    >>> has_cycle(lnk)
    False
    >>> lnk.rest.rest.rest = lnk
    >>> has_cycle(lnk)
    True
    >>> lnk.rest.rest.rest = lnk.rest
    >>> has_cycle(lnk)
    True
    """
    "*** YOUR CODE HERE ***"


def balance_tree(t):
    """Balance a tree.

    >>> t1 = Tree(1, [Tree(2, [Tree(2), Tree(3), Tree(3)]), Tree(2, [Tree(4), Tree(4)])])
    >>> balance_tree(t1)
    >>> t1
    Tree(1, [Tree(2, [Tree(3), Tree(3), Tree(3)]), Tree(3, [Tree(4), Tree(4)])])
    """
    "*** YOUR CODE HERE ***"


#####################
#        ADT        #
#####################

class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'
