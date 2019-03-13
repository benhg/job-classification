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
    numfors = 0
    tree = ""
    with open(f"scripts/{script}" , "r") as fh:
        tree = ast.parse(fh.read())
    for stmt in ast.walk(tree):
        if isinstance(stmt, ast.For):
            numfors += 1
    return numfors

def get_while_count(script):
    whiles = 0
    tree = ""
    with open(f"scripts/{script}" , "r") as fh:
        tree = ast.parse(fh.read())
    for stmt in ast.walk(tree):
        if isinstance(stmt, ast.While):
            whiles += 1
    return whiles

def get_loop_count(script):
    return get_for_count(script) + get_while_count(script)

def get_function_defs(script):
    defs = 0
    tree = ""
    with open(f"scripts/{script}" , "r") as fh:
        tree = ast.parse(fh.read())
    for stmt in ast.walk(tree):
        if isinstance(stmt, ast.FunctionDef):
            defs += 1
            print(stmt)
    return defs


def get_function_calls(script):
    calls = 0
    tree = ""
    with open(f"scripts/{script}" , "r") as fh:
        tree = ast.parse(fh.read())
    for stmt in ast.walk(tree):
        if isinstance(stmt, ast.Call):
            calls += 1
            print(stmt)
    return calls


def get_loads(script):
    loads = 0
    tree = ""
    with open(f"scripts/{script}" , "r") as fh:
        tree = ast.parse(fh.read())
    for stmt in ast.walk(tree):
        if isinstance(stmt, ast.Load):
            loads += 1
            print(stmt)
    return loads

def get_deepest_stmt(script, depth=0):
    depth = 0
    tree = ""
    with open(f"scripts/{script}" , "r") as fh:
        tree = ast.parse(fh.read())
    for stmt in ast.walk(tree):
        pass



if __name__ == '__main__':
    print(get_function_calls("p7.py"))

