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
import csv
import numpy as np

class ASTParser:

    def __init__(self, script):
        self.tree = ""
        with open(f"scripts/{script}" , "r") as fh:
            self.tree = ast.parse(fh.read())

    def get_for_count(self):
        numfors = 0
        for stmt in ast.walk(self.tree):
            if isinstance(stmt, ast.For):
                numfors += 1
        return numfors

    def get_while_count(self):
        whiles = 0
        for stmt in ast.walk(self.tree):
            if isinstance(stmt, ast.While):
                whiles += 1
        return whiles

    def get_loop_count(self):
        return get_for_count() + get_while_count()

    def get_function_defs(self):
        defs = 0
        for stmt in ast.walk(self.tree):
            if isinstance(stmt, ast.FunctionDef):
                defs += 1
        return defs


    def get_function_calls(self):
        calls = 0
        for stmt in ast.walk(self.tree):
            if isinstance(stmt, ast.Call):
                calls += 1
        return calls


    def get_loads(self):
        loads = 0
        for stmt in ast.walk(self.tree):
            if isinstance(stmt, ast.Load):
                loads += 1
        return loads

    def get_deepest_stmt(self):
        depth = 0
        for stmt in ast.walk(self.tree):
            pass
        return 0

    def get_asmts(self):
        asm = 0
        for stmt in ast.walk(self.tree):
            if isinstance(stmt, ast.Assign):
                asm += 1
        return asm



if __name__ == '__main__':
    p = ASTParser("p7.py")
    print(p.get_function_calls())

