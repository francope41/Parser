#Parser class in charge of top-down parsing the inputted file

import numpy as np
#Tokens item come as an array of 3 alements [Token, Type, Location]
class Parser:
    def __init__(self, tokens):
        self.loc = 0
        self.tokens = tokens
        #Open and read inputed file
        lines_file = open("lines_read", "rb")
        self.lines = np.load('arr')
        self.parsed = []
        self.curr_token = self.tokens[self.loc]

    def Next(self):
        try:
            self.loc += 1
            self.curr_token = self.tokens[self.loc]
        except StopIteration:
            self.curr_token = None

    def Program(self):
        "Program : Decl+"
        print("   Program: ")
        self.parsed.append("   Program: ")
        self.Decl()

    def Decl(self):
        "Decl : VariableDecl | FunctionDecl"
        Decl = self.curr_token
        self.Next()

        while self.curr_token[1] == "T_Identifier":
            self.Next()
            if self.curr_token[1] ==";":
                print("  {}   VarDecl: ".format(self.curr_token[2]))
                self.parsed.append("  {}   VarDecl: ".format(self.curr_token[2]))
                self.VariableDecl()
            else:
                print("  {}   FnDecl: ".format(self.curr_token[2]))
                self.parsed.append("  {}   FnDecl: ".format(self.curr_token[2]))
                self.FunctionDecl()

    def VariableDecl(self):
        "Decl : Variable ;"
        variable = self.Variable()
        if variable != False:
            return True
        else:
            return False
        
    def FunctionDecl(self):
        "Decl : Type ident ( Formals ) StmtBlock | void ident ( Formals ) StmtBlockType ident ( Formals ) StmtBlock | void ident ( Formals ) StmtBlock"
        FuncDecl = self.curr_token
        self.Next()
        if self.curr_token[0] == ")":
            print("         (return type) Type: {}".format(self.tokens[0][0]))
            print("  {}      Identifier: {}".format(self.curr_token[2],self.tokens[1][0]))
        else:
            self.Formals()



    def Variable(self):
        return True

    def GetType(self):
        if (self.curr_token is not None and self.curr_token[1] == "T_Void" or self.curr_token[1] == "T_Int" or self.curr_token[1] == "T_Double" or self.curr_token[1] == "T_String" 
            or self.curr_token[1] == "T_Bool"):
            return self.curr_token[1]
        else:
            return False

    def Formals(self):
        'Formals : Variable+, | ϵ'
        form = self.curr_token
        self.Next()
        if self.curr_token[0] == ")":
            print("         (return type) Type: void")
            print("  {}      Identifier: main".format(self.curr_token[2]))
        else:
            pass



    def Parse(self):
        if self.curr_token is None:
            return None

        res = self.Program()

        return res


    