from exceptions import ScotchException


def eval(expr, context=None):
    return expr.eval(context)

class Expr(object):
    def __repr__(self): return str(self)
    def eval(self, context=None):
        raise ScotchException('Expression type not yet implemented: %s' % self.__class__.__name__)
    def generator(self):
        raise ScotchException('This expression type has no generator.')
    def __add__(self, x):
        return AddExpr(self, x)
    def __sub__(self, x):
        return SubExpr(self, x)
    def __mul__(self, x):
        return MulExpr(self, x)
    def __div__(self, x):
        return DivExpr(self, x)
    def __eq__(self, x):
        return eval(expr)
    @classmethod
    def make(cls, *x):
        if len(x) > 1:
            return CurriedExpr(*x)
        return x[0]
class CurriedExpr(Expr):
    def __init__(self, *exprs):
        self.exprs = exprs
    def __str__(self): return '(%s)' %  ' '.join([str(s) for s in self.exprs])
    def eval(self, context=None):
        return self
class ExprBlock(Expr):
    def __init__(self, *exprs):
        self.exprs = exprs
    def __str__(self): return '{%s}' % '; '.join([str(x) for x in self.exprs])
    def eval(self, context=None):
        for expr in self.exprs:
            last = eval(expr, context)
        return last


# values

def convert(value, cls):
    return cls.convert(value)

class Value(Expr):
    @classmethod
    def make(cls, x):
        for value_type in value_types:
            if isinstance(x, value_type.converter):
                return value_type(x)
    @classmethod
    def convert(cls, x):
        if isinstance(x, Value):
            return cls.converter(x.value)
        return None
    def __add__(self, x):
        if isinstance(x, Value): return Value.make(self.value + x.value)
        return Expr.__add__(self, x)
    def __sub__(self, x):
        if isinstance(x, Value): return Value.make(self.value - x.value)
        return Expr.__sub__(self, x)
    def __mul__(self, x):
        if isinstance(x, Value): return Value.make(self.value * x.value)
        return Expr.__mul__(self, x)
    def __div__(self, x):
        if isinstance(x, Value): return Value.make(self.value / x.value)
        return Expr.__div__(self, x)
    def eval(self, context=None):
        return self
class BoolValue(Value):
    converter = bool
    def __init__(self, x):
        self.value = bool(x)
    def __str__(self): return '"%s"' % str(self.value).replace('"', '\\"')
class IntValue(Value):
    converter = int
    
    def __init__(self, x):
        self.value = int(x)
    def __str__(self): return str(self.value)
class FloatValue(Value):
    converter = float
    def __init__(self, x):
        self.value = float(x)
    def __str__(self): return str(self.value)
class StrValue(Value):
    converter = str
    def __init__(self, x):
        self.value = str(x)
    def __str__(self): return '"%s"' % str(self.value).replace('"', '\\"')

value_types = [BoolValue, IntValue, FloatValue, StrValue]
    

# expressions

class VarExpr(Expr):
    '''A variable.'''
    def __init__(self, name):
        self.name = name
    def __str__(self): return self.name
    def eval(self, context=None):
        pass
class AddExpr(Expr):
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __str__(self): return '(%s + %s)' % (self.x, self.y)
    def eval(self, context=None):
        x = eval(self.x, context)
        y = eval(self.y, context)
        return x + y
class SubExpr(Expr):
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __str__(self): return '(%s - %s)' % (self.x, self.y)
    def eval(self, context=None):
        x = eval(self.x, context)
        y = eval(self.y, context)
        return x - y
class MulExpr(Expr):
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __str__(self): return '(%s * %s)' % (self.x, self.y)
    def eval(self, context=None):
        x = eval(self.x, context)
        y = eval(self.y, context)
        return x * y
class DivExpr(Expr):
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __str__(self): return '(%s / %s)' % (self.x, self.y)
    def eval(self, context=None):
        x = eval(self.x, context)
        y = eval(self.y, context)
        return x / y
        
class ListExpr(Expr):
    def __init__(self, *values):
        self.values = values
    def __str__(self): return '[%s]' % ', '.join([str(s) for s in self.values])
    def eval(self, context=None):
        return self
    def generator(self):
        for value in self.values: yield value
        
class AssignExpr(Expr):
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __str__(self): return '%s = %s' % (self.x, self.y)
