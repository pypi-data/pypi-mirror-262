"""
Usage: hello [-ghv]

OPTIONS
  -h, --help           display this help text and exit
  -v, --version        display version information and exit
  -g, --global         print a familiar message
"""

__version__ = '1.2.3'

import sys
from helptext import parse

opts, _ = parse(sys.argv[1:], __doc__, __version__)
if opts['--global']['enabled']:
    print('Hello, world!')
