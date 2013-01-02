import argparse
import sys
from lib.scotch import scotch, arg_parser
from lib.exceptions import ScotchException
import lib.expr as expr
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from __init__ import __version__



args = arg_parser.parse_args()


if args.version:
    print __version__
    sys.exit()

if args.test:
    import tests
    tests.run_tests(verbose=args.verbose)
    sys.exit()

if not sys.stdin.isatty():
    # read and evaluate piped input
    if args.eval is None: args.eval = ''
    args.eval = sys.stdin.read() + args.eval


interactive = (not args.file and not args.eval) or args.interactive


def run():
    if interactive: print '''Scotch %s''' % __version__

    for input_file in args.file:
        try:
            scotch.parse(filename=input_file)
        except KeyboardInterrupt:
            sys.exit()
        
    if args.eval:
        try:
            scotch.parse(text=args.eval)
        except KeyboardInterrupt:
            sys.exit()
    
    if interactive:
        scotch.repl(args)
            
        
if __name__ == '__main__': run()
