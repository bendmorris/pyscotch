from lib.expr import *
from lib.parser import *
import doctest
import sys


def parse_test():
    '''
    >>> statement.parseString('1', parseAll=True)[0]
    1
    >>> statement.parseString('1.0', parseAll=True)[0]
    1.0
    >>> statement.parseString('"abc"', parseAll=True)[0]
    "abc"
    >>> statement.parseString('1 + 1', parseAll=True)[0]
    (1 + 1)
    >>> statement.parseString('1 + (2.0 + 3.0)', parseAll=True)[0]
    (1 + (2.0 + 3.0))
    >>> a = statement.parseString('1(2, 3)', parseAll=True)[0]; print a
    (1 2 3)
    >>> isinstance(a, CurriedExpr)
    True
    >>> statement.parseString("""{ 1 + 1; 2 + 1 }""", parseAll=True)[0]
    {(1 + 1); (2 + 1)}
    >>> statement.parseString("[1, 2.0, 'three']", parseAll=True)[0]
    [1, 2.0, "three"]
    '''

def expr_test():
    '''
    >>> convert(FloatValue(1.2), IntValue)
    1
    >>> convert(StrValue("1"), IntValue)
    1
    >>> statement.parseString('1 + 2', parseAll=True)[0].eval()
    3
    >>> statement.parseString('3 * 2', parseAll=True)[0].eval()
    6
    >>> statement.parseString('1 + 2 * 3;', parseAll=True)[0].eval()
    7
    >>> statement.parseString('(1 + 2) * 3;', parseAll=True)[0].eval()
    9
    '''
    pass
    
    
doctest.testmod()
