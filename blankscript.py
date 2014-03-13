#! /usr/bin/env python

"""blankscript.py - Do nothing

    But do it neatly.

    Version 2012-12-12

    Usage:
        blankscript.py <arg1> <arg2>
    
"""

import os, sys, getopt
import Image

def blankscript(arg1, arg2):
    pass
    

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hf", ["help", "force"])
        except getopt.error, msg:
            raise Usage(msg)
        clobber = False
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                return 1
            if o in ("-f", "--force"):
                clobber = True
        if len(args) in (2,):
            arg1, arg2 = args
            blankscript(arg1, arg2)
        else:
            raise Usage("Wrong number of arguments")
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "For help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
