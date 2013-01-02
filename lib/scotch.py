from parser import parse_string, parse_stream, parse_file
from expr import Expr

default = [
           ]
    

class Scotch(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
    
        self.reinit()
        
        
    def reinit(self):
        self.defs = {}
        
        self.execute(default)


    def execute(self, stmt, context={}):
        if isinstance(stmt, Expr):
            print stmt.eval(context)
        elif hasattr(stmt, '__iter__'):
            for s in stmt: self.execute(s)
        
        
    def parse(self, filename=None, text=None, stream=None):
        if filename:
            parsed = parse_file(filename)
        elif text:
            parsed = parse_string(text)
        elif stream:
            parsed = parse_stream(stream)
        else:
            raise ScotchException('Must specify filename, text, or stream to parse.')
        
        stmts = 0
        for stmt, start, end in parsed:
            stmts += 1
            self.execute(stmt)
        
        return stmts
