#! /usr/local/bin/env python3
"""
This file is intended to generate tags on script information
What I mean by "tags" is derivative features - that is, features
which are generated as derivatives of other scripts. One example of
such a feature would be source lines of code, or number of loops.
This script should process a python "job" (mostly just python scripts for now)
and add those "tags" to a data file about them.

There will soon be a document about what exactly a "job" is
"""
import ast
import csv
import numpy as np
import glob


class ASTParser:

    def __init__(self, script):
        self.tree = ""
        self.script = script
        with open(f"{script}", "r") as fh:
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
        return self.get_for_count() + self.get_while_count()

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

    def generate_row(self):
        loops = self.get_loop_count()
        fdefs = self.get_function_defs()
        fcalls = self.get_function_calls()
        loads = self.get_loads()
        asmts = self.get_asmts()
        return {
            "name": self.script.split("/")[-1],
            "loops": loops,
            "fdefs": fdefs,
            "fcalls": fcalls,
            "loads": loads,
            "asmts": asmts
        }




if __name__ == '__main__':
    with open("jobs_features.csv", "w") as fh:
        writer = csv.writer(fh)
        writer.writerow(["name", "loops", "fdefs", "fcalls", "loads", "asmts"])
    with open("jobs_features.csv", "a") as fh:
        writer = csv.DictWriter(fh, fieldnames=["name", "loops", "fdefs", "fcalls", "loads", "asmts"])
        for script in glob.glob("scripts/*.py"):
            p = ASTParser(script)
            writer.writerow(p.generate_row())
