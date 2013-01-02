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

'''add_expr = expression + Suppress("+") + expression
add_expr.setParseAction(lambda x, y: AddExpr(x, y))
sub_expr = expression + Suppress("-") + expression
sub_expr.setParseAction(lambda x, y: SubExpr(x, y))
mul_expr = expression + Suppress("*") + expression
mul_expr.setParseAction(lambda x, y: MulExpr(x, y))
div_expr = expression + Suppress("/") + expression
div_expr.setParseAction(lambda x, y: DivExpr(x, y))
arithmetic = add_expr | sub_expr | mul_expr | div_expr'''

list_expr = Suppress('[') + Optional(delimitedList(expression), default=[]) + Suppress(']')

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
expression << operatorPrecedence(
    term,
    [
        (oneOf('*','/'), 2, opAssoc.LEFT, operator_expr),
        (oneOf('+','-'), 2, opAssoc.LEFT, operator_expr),
    ],
)
statement = Forward()
curried_expr = OneOrMore(expression)
curried_expr.setParseAction(lambda x: Expr.make(*x))
command = Word('NOTYETIMPLEMENTED')
expr_block = (Suppress('{') + OneOrMore(statement) + Suppress('}'))
expr_block.setParseAction(lambda x: ExprBlock(*x))
statement << (curried_expr | command | expr_block) + Optional(';').suppress()

def parse_string(string):
    handle = StringIO(string)
    return parse_stream(handle)

def parse_file(filename):
    with open(filename, 'r') as handle:
        return parse_stream(handle)

def parse_stream(handle):
    text = handle.read()
    return expression.scanString(text)
