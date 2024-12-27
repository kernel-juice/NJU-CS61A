
""" Homework 3: Recursion """

from operator import sub, mul
HW_SOURCE_FILE = 'hw03.py'


#####################
# Required Problems #
#####################


def integrate(f, l, r, min_interval):
    """Return the definite integration of function f over interval 
    [l,r], with interval length limit min_interval.

    >>> abs(integrate(lambda x: x * x, 1, 2, 0.01) - (7 / 3)) < 0.001
    True
    >>> abs(integrate(lambda x: x, 1, 2, 0.01) - 1.5) < 0.0001
    True
    >>> from construct_check import check
    >>> # ban while or for loops
    >>> check(HW_SOURCE_FILE, 'integrate', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    if r - l < min_interval:
        return (f(l) + f(r)) * (r - l) / 2
    else:
        return integrate(f, l, (l + r) / 2, min_interval) + \
            integrate(f, (l + r) / 2, r, min_interval)


def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(7)
    5
    >>> pingpong(8)
    4
    >>> pingpong(15)
    3
    >>> pingpong(21)
    5
    >>> pingpong(22)
    6
    >>> pingpong(30)
    10
    >>> pingpong(68)
    0
    >>> pingpong(69)
    1
    >>> pingpong(70)
    0
    >>> pingpong(71)
    -1
    >>> pingpong(72)
    -2
    >>> pingpong(100)
    6
    >>> from construct_check import check
    >>> # ban assignment statements
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """
    def reverse_judge(n):  # O(logn)
        if n % 6 == 0:
            return True

        def inner(n):
            if n % 10 == 6:
                return True
            elif not n:
                return False
            else:
                return inner(n // 10)
        return inner(n)

    # O(n)
    def increase_recur(n):
        if n == 1:
            return 1
        if reverse_judge(n):
            return decrease_recur(n - 1) - 1
        return increase_recur(n - 1) + 1

    def decrease_recur(n):
        if n == 1:
            raise AssertionError
        if reverse_judge(n):
            return increase_recur(n - 1) + 1
        return decrease_recur(n - 1) - 1

    try:
        return increase_recur(n)
    except:
        return decrease_recur(n)


def balanced(s):
    """Returns whether the given parentheses sequence s is balanced.
    >>> balanced('()')
    True
    >>> balanced(')')
    False
    >>> balanced('(())')
    True
    >>> balanced('()()')
    True
    >>> balanced('()())')
    False
    >>> balanced('()(()')
    False
    """

    def divide(s, k):
        """Divide the given parentheses sequence s into two parts at position k.
        >>> left, right = divide('()()', 2)
        >>> left
        '()'
        >>> right
        '()'
        >>> left, right = divide('(())()', 4)
        >>> left
        '(())'
        >>> right
        '()'
        >>> left, right = divide('(())()', 6)
        >>> left
        '(())()'
        >>> right
        ''
        """
        return (s[:k], s[k:])

    def peel(s):
        """Peel off the leftmost and rightmost parentheses in s to obtain the
        internal part of the parentheses sequence.
        >>> peel('(())')
        '()'
        >>> peel('()')
        ''
        >>> peel('))((')
        ')('
        """
        return s[1:-1]

    def match(s):
        """Returns whether the leftmost and the rightmost parentheses in s match.
        >>> match('()')
        True
        >>> match('()()')
        True
        >>> match('()))')
        True
        >>> match('))')
        False
        >>> match(')())')
        False
        """
        return s[0] == '(' and s[-1] == ')'

    def judge_div(s):  # O(n!)
        """Divide s into all posibilities to see if two parts can be all balanced."""
        for i in range(2, len(s), 2):
            left, right = divide(s, i)
            if balanced(left) and balanced(right):
                return True
        return False

    if s == '':
        return True
    if match(s):
        return balanced(peel(s)) or judge_div(s)
    else:
        return False


def count_change(total, money):
    """Return the number of ways to make change for total,
    under the currency system described by money.

    >>> def chinese_yuan(ith):
    ...     if ith == 1:
    ...         return 1
    ...     if ith == 2:
    ...         return 5
    ...     if ith == 3:
    ...         return 10
    ...     if ith == 4:
    ...         return 20
    ...     if ith == 5:
    ...         return 50
    ...     if ith == 6:
    ...         return 100
    >>> def us_cent(ith):
    ...     if ith == 1:
    ...         return 1
    ...     if ith == 2:
    ...         return 5
    ...     if ith == 3:
    ...         return 10
    ...     if ith == 4:
    ...         return 25
    >>> count_change(15, chinese_yuan)
    6
    >>> count_change(49, chinese_yuan)
    44
    >>> count_change(49, us_cent)
    39
    >>> count_change(49, lambda x: 2 ** (x - 1))
    692
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'count_change', ['While', 'For'])
    True
    """
    def val_max_ith(total, money, count=1):  # Find the biggest useful index
        if money(count):
            if total <= money(count):
                return count
            else:
                return val_max_ith(total, money, count + 1)
        else:
            return count - 1

    def inner_1(total, money):
        max_ith = val_max_ith(total, money)

        def inner_2(total, ith):
            if total == 0:
                return 1
            elif total < 0:
                return 0
            elif ith == 0:
                return 0
            else:
                return inner_2(total - money(ith), ith) + \
                    inner_2(total, ith - 1)

        return inner_2(total, max_ith)

    return inner_1(total, money)


def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)


def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"

    other = 6 - start - end

    if n == 0:
        return move_stack(1, start, end)
    elif n == 1:
        return print_move(start, end)
    else:
        move_stack(n - 1, start, other)
        move_stack(1, start, end)
        move_stack(n - 1, other, end)


def multiadder(n):
    """Return a function that takes N arguments, one at a time, and adds them.
    >>> f = multiadder(3)
    >>> f(5)(6)(7) # 5 + 6 + 7
    18
    >>> multiadder(1)(5)
    5
    >>> multiadder(2)(5)(6) # 5 + 6
    11
    >>> multiadder(4)(5)(6)(7)(8) # 5 + 6 + 7 + 8
    26
    >>> from construct_check import check
    >>> # Make sure multiadder is a pure function.
    >>> check(HW_SOURCE_FILE, 'multiadder',
    ...       ['Nonlocal', 'Global'])
    True
    """
    def inner(i, sum):
        if i == 0:
            return sum
        return lambda x: inner(i - 1, sum + x)

    return inner(n, 0)
##########################
# Just for fun Questions #
##########################


def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> # ban any assignments or recursion
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial', ['Assign', 'AugAssign', 'FunctionDef', 'Recursion'])
    True
    """
    return (lambda x: x(x))(lambda x: lambda n: 1 if n == 0 else n * x(x)(n - 1))


def Y(f): return (lambda x: x(x))(lambda x: f(lambda z: x(x)(z)))


def fib_maker(f): return lambda r: 0 if r == 0 else 1 if r == 1 else f(
    r - 1) + f(r - 2)


def number_of_six_maker(f): return lambda r: (
    1 if r == 6 else 0) if r // 10 == 0 else (f(r // 10) + (1 if (r % 10) == 6 else 0))


my_fib = Y(fib_maker)
my_number_of_six = Y(number_of_six_maker)

# This code sets up doctests for my_fib and my_number_of_six.

my_fib.__name__ = 'my_fib'
my_fib.__doc__ = """Given n, returns the nth Fibonacci nuimber.

>>> my_fib(0)
0
>>> my_fib(1)
1
>>> my_fib(2)
1
>>> my_fib(3)
2
>>> my_fib(4)
3
>>> my_fib(5)
5
"""

my_number_of_six.__name__ = 'my_number_of_six'
my_number_of_six.__doc__ = """Return the number of 6 in each digit of a positive integer n.

>>> my_number_of_six(666)
3
>>> my_number_of_six(123456)
1
"""
