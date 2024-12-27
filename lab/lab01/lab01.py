def both_odd(a, b):
    """Returns True if both a and b are odd numbers.

    >>> both_odd(-1, 1)
    True
    >>> both_odd(2, 1)
    False
    """
    return a % 2 == 1 and b % 2 == 1 # You can replace this line!


def factorial(n):
    """Return the factorial of a positive integer n.

    >>> factorial(3)
    6
    >>> factorial(5)
    120
    """
    "*** YOUR CODE HERE ***"
    if n > 0:
        return factorial(n - 1) * n
    else:
        return 1


def is_triangle(a, b, c):
    """Given three integers (may be nonpositive), judge whether the three
    integers can form the three sides of a triangle.

    >>> is_triangle(2, 1, 3)
    False
    >>> is_triangle(5, -3, 4)
    False
    >>> is_triangle(2, 2, 2)
    True
    """
    "*** YOUR CODE HERE ***"
    if a < 0 or b < 0 or c < 0:
        return False
    else:
        if (a + b > c) and (b + c > a) and (a + c > b):
            return True
        else:
            return False

def number_of_nine(n):
    """Return the number of 9 in each digit of a positive integer n.

    >>> number_of_nine(999)
    3
    >>> number_of_nine(9876543)
    1
    """
    "*** YOUR CODE HERE ***"
    digit = len(str(n))  #当前处理数字位数
    curr = n  #当前处理数字
    total = 0  #9的个数
    while digit != 0:  #遍历每一位
        one = curr // (pow(10, digit - 1))  #某一位是多少
        if (one) == 9:  #判断某位是否为9
            total += 1
        curr -= (one * pow(10, digit - 1))  #舍弃处理过的位数
        digit -= 1
    return total



def min_digit(x):
    """Return the min digit of x.

    >>> min_digit(10)
    0
    >>> min_digit(4224)
    2
    >>> min_digit(1234567890)
    0
    >>> # make sure that you are using return rather than print
    >>> a = min_digit(123)
    >>> a
    1
    """
    "*** YOUR CODE HERE ***"
    digit = len(str(x))  #当前处理数字位数
    curr = x  #当前处理数字
    min = 9  #9的个数
    while digit != 0:  #遍历每一位
        one = curr // (pow(10, digit - 1))  #某一位是多少
        if (one) < min:  #判断某位是否为9
            min = one
        curr -= (one * pow(10, digit - 1))  #舍弃处理过的位数
        digit -= 1
    return min