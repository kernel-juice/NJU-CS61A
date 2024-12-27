""" Homework 1: Variables & Functions, Control """

from operator import add, sub, mul, neg

def a_sub_abs_b(a, b):
    r"""Return a-abs(b), but without calling abs.

    >>> a_sub_abs_b(2, 3)
    -1
    >>> a_sub_abs_b(2, -3)
    -1
    >>> # a check that you didn't change the return statement!
    >>> import inspect, re
    >>> re.findall(r'^\s*(return .*)', inspect.getsource(a_sub_abs_b), re.M)
    ['return h(a, b)']
    """
    if b >= 0:
        h = sub
    else:
        h = add
    return h(a, b)

def two_of_three(x, y, z):
    """Return a*a + b*b, where a and b are the two largest members of the
    positive numbers x, y, and z.

    >>> two_of_three(1, 2, 3)
    13
    >>> two_of_three(5, 3, 1)
    34
    >>> two_of_three(10, 2, 8)
    164
    >>> two_of_three(5, 5, 5)
    50
    >>> # check that your code consists of nothing but an expression (this docstring)
    >>> # and a return statement
    >>> import inspect, ast
    >>> [type(x).__name__ for x in ast.parse(inspect.getsource(two_of_three)).body[0].body]
    ['Expr', 'Return']
    """
    return max(x ** 2 + y ** 2, x ** 2 + z ** 2, y ** 2 + z ** 2)

def largest_factor(x):
    """Return the largest factor of x that is smaller than x.

    >>> largest_factor(15) # factors are 1, 3, 5
    5
    >>> largest_factor(80) # factors are 1, 2, 4, 5, 8, 10, 16, 20, 40
    40
    >>> largest_factor(13) # factor is 1 since 13 is prime
    1
    """
    "*** YOUR CODE HERE ***"
    factor = 2
    largest = 1
    while factor <= (x // 2):
        if x % factor == 0:
            largest = max(x // factor, factor)
        factor += 1
    return largest



def if_function(condition, true_result, false_result):
    """Return true_result if condition is a true value, and
    false_result otherwise.

    >>> if_function(True, 2, 3)
    2
    >>> if_function(False, 2, 3)
    3
    >>> if_function(3==2, 3+2, 3-2)
    1
    >>> if_function(3>2, 3+2, 3-2)
    5
    """
    if condition:
        return true_result
    else:
        return false_result


def with_if_statement():
    """
    >>> result = with_if_statement()
    2
    >>> print(result)
    None
    """
    if c():
        return t()
    else:
        return f()

def with_if_function():
    """
    >>> result = with_if_function()
    1
    2
    >>> print(result)
    None
    """
    return if_function(c(), t(), f())

def c():
    "*** YOUR CODE HERE ***"
def t():
    "*** YOUR CODE HERE ***"
    print(1)
def f():
    "*** YOUR CODE HERE ***"
    print(2)
def hailstone(x):
    """Print the hailstone sequence starting at x and return its
    length.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """
    "*** YOUR CODE HERE ***"
    counter = 1
    print(x)
    while x != 1:
        if x % 2 == 0:
            x = x // 2
            print(x)
            counter += 1
        else:
            x = x * 3 + 1
            print(x)
            counter += 1
    return counter


def double_factorial(n):
    """Compute the double factorial of n.

    >>> double_factorial(6)  # 6 * 4 * 2
    48
    >>> double_factorial(5)  # 5 * 3 * 1
    15
    >>> double_factorial(3)  # 3 * 1
    3
    >>> double_factorial(1)  # 1
    1
    """
    "*** YOUR CODE HERE ***"
    if n >= 3:
        return n * double_factorial(n - 2)
    elif n == 2:
        return 2
    else:
        return 1

def double_ones(n):
    """Return true if n has two ones in a row.
    
    >>> double_ones(1)
    False
    >>> double_ones(11)
    True
    >>> double_ones(2112)
    True
    >>> double_ones(110011)
    True
    >>> double_ones(12345)
    False
    >>> double_ones(10101010)
    False
    """
    "*** YOUR CODE HERE ***"
    digit = len(str(n))  #当前处理数字位数
    curr = n  #当前处理数字
    warning = False  #有1啦！！
    while digit != 0:  #遍历每一位
        one = curr // (pow(10, digit - 1))  #某一位是多少?
        if (one) == 1:  #判断某位是否为1
            if warning:  #警告生效？
                return True
            else:
                warning = True
        else:
            warning = False
        curr -= (one * pow(10, digit - 1))  #舍弃处理过的位数
        digit -= 1
    return False