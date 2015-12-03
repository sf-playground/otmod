#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  ------------------------------------------------------------------------------
#  otmod.py
#  Copyright 2015 Christopher Simpkins
#  MIT license
#  ------------------------------------------------------------------------------

import sys
import codecs
import unicodedata
import fontTools
import yaml


#------------------------------------------------------------------------------
# [ Argument Class ]
#   all command line arguments (object inherited from Python list)
#------------------------------------------------------------------------------
class Argument(list):
    """Argument class is a list for command line arguments.  It provides methods for positional argument parsing"""
    def __init__(self, argv):
        self.argv = argv
        list.__init__(self, self.argv)


    # return argument at position specified by the 'position' parameter
    def _getArg(self, position):
        if ( self.argv ) and ( len(self.argv) > position ):
            return self.argv[position]
        else:
            return ""

    # return position of user specified argument in the argument list
    def _getArgPosition(self, test_arg):
        if ( self.argv ):
            if test_arg in self.argv:
                return self.argv.index(test_arg)
            else:
                return -1  ## TODO: change the return code that indicates an error

    # return the argument at the next position following a user specified positional argument (e.g. for argument to an option in cmd)
    def _getArgNext(self, position):
        if len(self.argv) > (position + 1):
            return self.argv[position + 1]
        else:
            return ""


def read_utf8(filepath):
    """read_utf8() is a function that reads text in as UTF-8 NFKD normalized text strings"""
    try:
        import codecs
        f = codecs.open(filepath, encoding='utf_8', mode='r')
    except IOError as ioe:
        sys.stderr.write("[otmod.py] ERROR: Unable to open '" + filepath + "' for read.\n")
        raise ioe
    try:
        textstring = f.read()
        norm_text = unicodedata.normalize('NFKD', textstring) # NKFD normalization of the unicode data before returns
        return norm_text
    except Exception as e:
        sys.stderr.write("[otmod.py] ERROR: Unable to read " + filepath + " with UTF-8 encoding using the read_utf8() method.\n")
        raise e
    finally:
        f.close()


def main(arguments):
    args = Argument(arguments)

    # Define command line syntax
    if "--in" in args.argv:
        infile = args._getArgNext(args._getArgPosition("--in"))
        if infile is "":
            sys.stderr.write("[otmod.py] ERROR: please define the font input file path as an argument to the --in command line flag.\n")
    elif "-i" in args.argv:
        infile = args._getArgNext("--in")
        if infile is "":
            print("ERROR")
    else:
        sys.stderr.write("[otmod.py] Please include the `--in` flag with an input font file defined as an argument.\n")
        sys.exit(1)

    if "--opentype" in args.argv:
        print("opentype")
    else:
        sys.stderr.write("[otmod.py] Please include the `--opentype` and define it with an path argument to the YAML formatted OpenType changes file.\n")
        sys.exit(1)

    if "--out" in args.argv:
        print("out")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        sys.stderr.write("[otmod.py] ERROR: no arguments detected in your command.\n")
        sys.exit(1)
