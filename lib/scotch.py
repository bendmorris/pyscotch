import argparse
from parser import parse_string, parse_stream, parse_file
from expr import Expr

default = [
           ]


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('file', nargs='*', help='file to be interpreted')
arg_parser.add_argument('-i', '--interactive', help='enter interactive mode after interpreting file', action='store_true')
arg_parser.add_argument('-e', '--eval', help='string to be evaluated')
arg_parser.add_argument('-v', '--verbose', help='print each triple statement as evaluated', action='store_true')
arg_parser.add_argument('--version', help='print version and exit', action='store_true')
arg_parser.add_argument('--test', help='run unit tests and exit', action='store_true')


class Scotch(object):
    def __init__(self):
        self.reinit()
        
        
    def __call__(self, x):
        self.parse(text=x)
        
        
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
        
        
    def repl(self, args=None):
        import readline
        
        if args is None:
            args = object()
            args.verbose = None
            

        exit = False
        while not exit:
            scotch.verbose = args.verbose
        
            try:
                next_line = raw_input('>> ').strip()
                
                if not next_line: continue
                
                if next_line[0] == '-' and next_line.split(' ')[0] in arg_parser._option_string_actions:
                    command = next_line.split(' ')[0]
                    action = arg_parser._option_string_actions[command].dest
                    
                    if len(next_line.split(' ')) > 1:
                        arg = ' '.join(next_line.split(' ')[1:])
                        try: arg = eval(arg)
                        except: pass
                    else: 
                        arg = not getattr(args, action)
                    
                    try: 
                        setattr(args, action, arg)
                    except:
                        print 'Illegal argument: %s %s' % (command, arg)
                
                elif next_line in ('exit', 'quit'):
                    exit = True
                else:
                    stmts = scotch.parse(text=next_line)
                    if stmts == 0:
                        raise ScotchException('Failed to parse line: %s' % next_line)
                    
            except EOFError:
                print
                exit = True
                
            except KeyboardInterrupt:
                print
                continue
                
            except Exception as e:
                raise
                print e
                continue
        
        
scotch = Scotch()
