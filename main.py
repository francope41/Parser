# Programming Languages and Compilers
# Project 1, Phase II, Parser
# By Eulises Franco - 03/07/2023
#### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -####

# Import required libraries
import sys
import numpy as np
from utils import Parser, Lex_Analyzer

#### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -####


class SintaxAnalyzer:
    def __init__(self, program):
        #Tokenize Program
        Lexer = Lex_Analyzer(program)
        tokens, linesList = Lexer.Tokenize()
        #Parse Program
        parser = Parser(tokens,linesList)
        tree = parser.Parse()
        if tree is not None:
            print(tree)

SintaxAnalyzer(sys.argv[1])