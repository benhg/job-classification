#! /usr/local/bin/env python3
"""
This file is intended to generate tags on script information
What I mean by "tags" is derivative features - that is, features
which are generated as derivatives of other scripts. One example of
such a feature would be source lines of code, or number of loops.
This script should process a python "job" (mostly just python scripts for now)
and add those "tags" to a data file about them.
"""
import ast
import pprint


def get_for_count(script):
    tree = ""
    with open(f"scripts/{script}" , "r") as fh:
        tree = ast.parse(fh.read())
    pprint.pprint(ast.dump(tree))



if __name__ == '__main__':
    get_for_count("rudpclient.py")

