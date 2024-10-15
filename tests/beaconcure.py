import doctest
from enum import Enum

######################
# I Love Palindromes #
######################


def is_palindrome(item):
    """
    Check if an iterable (strings included), dictonary or integer is palindrome.

    Iterables:
    >>> is_palindrome([1, 2, 1])
    True
    >>> is_palindrome([1, 2])
    False

    # Strings (case insensetive):
    >>> is_palindrome("hello")
    False
    >>> is_palindrome("a")
    True
    >>> is_palindrome("Madam")
    True

    # Integers:
    >>> is_palindrome(121)
    True
    >>> is_palindrome(56)
    False

    A dictinary is palindrome if it consists of palindromes (both keys and values)
    >>> is_palindrome({"madam": "Hannah", "level": 121})
    True
    >>> is_palindrome({"madam": "Adam", "level": 10})
    False
    """

    def check_palindrome(s):
        s = str(s).lower()  # Convert to string and normalize case
        return s == s[::-1]

    # Check if the item is a dictionary
    if isinstance(item, dict):
        # Check if both keys and values are palindromes
        for key, value in item.items():
            if not check_palindrome(key) or not check_palindrome(value):
                return False
        return True

    # Check if the item is a list or tuple
    elif isinstance(item, (list, tuple)):
        item = ''.join(map(str, item))  # Convert to string by joining elements

    else:
        item = str(item)  # Convert to string if it's not a list, tuple, or dictionary

    # Normalize case and check if the string is a palindrome
    item = item.lower()
    return item == item[::-1]  # Check if the string is equal to its reverse


def filter_palindromes(items):
    """
    Remove palindromes from iterable.

    >>> filter_palindromes(["abc", "abba", 535, "leeroy", {"key": "value"}])
    ['abc', 'leeroy', {'key': 'value'}]
    """

    non_polindromes = []

    for item in items:
        if not is_palindrome(item):
            non_polindromes.append(item)

    return non_polindromes


class Palindrome:
    """
    Palindrome class

    >>> palindrome1 = Palindrome("ab")
    >>> palindrome1
    Palindrome("abba")
    >>> palindrome2 = Palindrome("madam")
    >>> palindrome2
    Palindrome("madam")
    >>> sum1 = palindrome1 + palindrome2
    >>> sum1
    Palindrome("abbamadamabba")
    >>> sum2 = palindrome1 + "madam"
    >>> sum2
    Palindrome("abbamadamabba")
    >>> sum1 == sum2
    True
    """
    pass


#############
# The Magic #
#############
def decorate_me(some_int):
    """
    Decorate (but do not modify) this function
    so it runs and passes the following doctest:
    >>> decorate_me(25)
    'Result: 50'
    >>> decorate_me(196)
    'Result: 392'
    """
    return some_int * 2


def magic(hat=[]):
    """
    Complete doctest:

    >>> magic()
    ???
    >>> magic()
    ???
    >>> hat = []
    >>> magic(hat)
    ???
    >>> hat = 45
    >>> magic(hat)
    ???
    >>> hat == _
    ???
    """
    dove = '🕊️'
    if hasattr(hat, 'append') and callable(hat.append):
        hat.append(dove)
    elif hasattr(hat, 'add') and callable(hat.add):
        hat.add(dove)
    else:
        hat = dove

    return hat


################
# Paint It All #
################

# Make the code work without any
# changes to PaintIt{Color} classes!

class Color(Enum):
    BLACK = '⚫'
    RED = '🔴'
    GREEN = '🟢'


# This one is just a stub, you can remove it
PaintIt = type('_', (type,), {'__new__': lambda *a, **_: type.__new__(*a)})('_', (), {})


class PaintItBlack(PaintIt, color=Color.BLACK):
    ...


class PaintItGreen(PaintIt, color=Color.GREEN):
    ...


class PaintItRed(PaintIt, color=Color.RED):
    ...


def paint_it_all():
    """
    >>> paint_it_all()
    ⚫ 🟢 🔴
    """
    print(PaintItBlack(), PaintItGreen(), PaintItRed())


############
# No No No #
############

# Make all the classes themselves which names start with `No` be actual None

class PositiveStatementsOnly:
    ...


class Fear(PositiveStatementsOnly):
    ...


class NoFear(PositiveStatementsOnly):
    ...


def fear_no_fear():
    """
    This function tests fears

    >>> Fear, NoFear = fear_no_fear()

    Test Fear
    >>> Fear is None
    False
    >>> callable(Fear)
    True
    >>> fear = Fear()
    >>> isinstance(fear, PositiveStatementsOnly)
    True
    >>> isinstance(fear, Fear)
    True

    Test No Fear
    >>> NoFear is None
    True
    >>> callable(NoFear)
    False
    >>> isinstance(NoFear, type)
    False
    """
    return Fear, NoFear


###########
# Doctest #
###########

if __name__ == "__main__":
    globs = globals()

    for test in (
            is_palindrome, filter_palindromes, Palindrome,
            decorate_me, magic, paint_it_all, fear_no_fear
    ):
        # Use context managers here
        name = test.__name__
        line = "#" * (len(name) + 4)
        print(f"{line}\n# {name} #\n{line}\n")
        doctest.run_docstring_examples(test, globs, name=name)
        print()
