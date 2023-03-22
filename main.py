# Programming Languages and Compilers
# Project 1, Phase II, Parser
# By Eulises Franco - 03/07/2023
#### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -####

# Import required libraries
import sys
import numpy as np
from utils_3 import Parser

#### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -####


class SintaxAnalyzer:
    def __init__(self, arr_dir, lines_dir):
        #Open and read array with tokens
        arr_file = open(arr_dir, "rb")
        tokens = np.load(arr_file)
        parser = Parser(tokens)
        tree = parser.Parse()
        if tree is not None:
            print(tree)

SintaxAnalyzer(sys.argv[1], sys.argv[2])