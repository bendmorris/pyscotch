from lib.expr import *
from lib.parser import *
import inspect
import doctest
import sys


def parser_tests():
    '''
    >>> def parseTest(s):
    ...     return statement.parseString(s, parseAll=True)[0]
    >>> parseTest('1')
    1
    >>> parseTest('1.0')
    1.0
    >>> parseTest('"abc"')
    'abc'
    >>> parseTest('1 + 1')
    (1 + 1)
    >>> parseTest('1 + (2.0 + 3.0)')
    (1 + (2.0 + 3.0))
    >>> a = parseTest('1(2, 3)'); print a
    (1 2 3)
    >>> isinstance(a, CurriedExpr)
    True
    >>> parseTest("""{ 1 + 1; 2 + 1 }""")
    {(1 + 1); (2 + 1)}
    >>> parseTest("[1, 2.0, 'three']")
    [1, 2.0, 'three']
    >>> parseTest('True')
    True
    >>> parseTest('False')
    False
    >>> parseTest('None')
    None
    '''

def expr_tests():
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
    
    
def run_tests(verbose=False):
    doctest.testmod(inspect.getmodule(parser_tests), verbose=verbose)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        verbose = eval(sys.argv[1])
    else: verbose=False

    run_tests(verbose=verbose)
