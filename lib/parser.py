from cStringIO import StringIO
from pyparsing import *
ParserElement.enablePackrat()
from expr import *


def parens(x):
    return Suppress('(') + x + Suppress(')')

# expressions
expression = Forward()

ident = (alphas + "_") + Optional(Word(alphanums + "_"))
variable = ident
variable.setParseAction(lambda x: VarExpr(''.join(x)))

comment = pythonStyleComment.suppress()
literalString = (sglQuotedString | dblQuotedString)
literalString.setParseAction(lambda x: StrValue(''.join(x)[1:-1]))
integer = Word(nums)
integer.setParseAction(lambda x: IntValue(int(''.join(x))))
real = ( Combine(Word(nums) + Optional("." + Word(nums))
                 + oneOf("E e") + Optional( oneOf('+ -')) + Word(nums))
         | Combine(Word(nums) + "." + Word(nums))
         )
real.setParseAction(lambda x: FloatValue(float(''.join(x))))
literalNumber = real | integer
value = literalString | literalNumber

list_expr = Suppress('[') + Optional(delimitedList(expression), default=[]) + Suppress(']')
list_expr.setParseAction(lambda x: ListExpr(*x))
term = (list_expr | variable | value)

ops = {
       '+': AddExpr,
       '-': SubExpr,
       '*': MulExpr,
       '/': DivExpr,
       }            
def operator_expr(args=None):
    if args is None:
        raise Exception()
        
    a, op, b = args[0]
    
    try: return ops[op](a,b)
    except KeyError: raise

expression << ((operatorPrecedence(
    term,
    [
        (oneOf('*','/'), 2, opAssoc.LEFT, operator_expr),
        (oneOf('+','-'), 2, opAssoc.LEFT, operator_expr),
    ],
) + Optional(parens(OneOrMore(delimitedList(expression))))) | parens(OneOrMore(expression)))
expression.setParseAction(lambda x: Expr.make(*x))
statement = Forward()


assignment = expression + Suppress('=') + expression
assignment.setParseAction(lambda x: AssignExpr(*x))
command = assignment
expr_block = (Suppress('{') + OneOrMore(statement) + Suppress('}'))
expr_block.setParseAction(lambda x: ExprBlock(*x))
statement << (expression | command | expr_block) + Optional(';').suppress()

def parse_string(string):
    handle = StringIO(string)
    return parse_stream(handle)

def parse_file(filename):
    with open(filename, 'r') as handle:
        return parse_stream(handle)

def parse_stream(handle):
    text = handle.read()
    return expression.scanString(text)
