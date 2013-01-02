import os

def make_dir(path):
    if not os.path.exists(path):
        try: os.makedirs(path)
        except OSError: pass

HOME_DIR = os.path.expanduser('~/.scotch/')
DEFAULT_PATH = '~/.scotch/lib/'
make_dir(DEFAULT_PATH)

PATH = os.environ.get('SCOTCHPATH')
if PATH is None: PATH = DEFAULT_PATH
PATH = '.:%s' % PATH

SEARCH_PATHS = [os.path.expanduser(p) for p in PATH.split(':')]

def find_module(mod_name):
    mod_name = mod_name.replace('.', '/')
    mod_paths = [os.path.join(path, mod_name) for path in SEARCH_PATHS]
    for path in SEARCH_PATHS:
        if os.path.exists(path): return path
    return None
