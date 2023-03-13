#Parser class in charge of top-down parsing the inputted file

import numpy as np
from operator import methodcaller

#Tokens item come as an array of 3 alements [Token, Type, Location]
class Parser:
    def __init__(self, tokens):
        self.loc = 0
        self.tokens = tokens
        self.token_lst = [list(x) for x in self.tokens]
        #Open and read inputed file
        lines_file = open("lines_read", "rb")
        self.lines = np.load('arr')
        if len(self.tokens) > 0:
            self.curr_token = self.tokens[self.loc]
        else:
            self.curr_token = None
            print("Empty program is syntactically incorrect.")

    def Next(self):
        try:
            self.loc += 1
            self.curr_token = self.tokens[self.loc]
        except StopIteration:
            self.curr_token = None

    def Program(self):
        "Program : Decl+"
        print("\n   Program: ")
        self.Decl()
        if self.curr_token is not None:
            self.Decl()
        else:
            print("ERROR")

    def Decl(self):
        "Decl : VariableDecl | FunctionDecl"
        first_tkn = self.curr_token
        curr_type = self.GetType()
        if curr_type is not False:
            self.Next()
            next_tkn = self.curr_token
            if next_tkn[1] == "T_Identifier":
                self.Next()
                next_next_tkn = self.curr_token
                if next_next_tkn[0] == "(":
                    self.FunctionDecl(first_tkn,next_tkn)
                else:
                    self.VariableDecl(first_tkn,next_tkn)
            else:
                print("Report SyntaxErr") #Create syntax error function

    def VariableDecl(self, first_tkn,next_tkn):
        "Decl : Variable ;"
        if self.curr_token[0] ==";":
                print("  {}   VarDecl: ".format(self.curr_token[2]))
                self.Variable(first_tkn,next_tkn)
        else:
            raise Exception()
        
    def FunctionDecl(self,first_tkn,next_tkn):
        "Decl : Type ident ( Formals ) StmtBlock | void ident ( Formals ) StmtBlockType ident ( Formals ) StmtBlock | void ident ( Formals ) StmtBlock"            
        FuncDecl = self.curr_token
        print("  {}   FnDecl: ".format(self.curr_token[2]))
        self.Next()
        if self.curr_token[0] == ")":
            print("         (return type) Type: {}".format(first_tkn[0]))
            print("  {}      Identifier: {}".format(next_tkn[2], next_tkn[0]))
            self.Next()
            if self.curr_token[0] == "{":
                self.StmtBlock()
                
        else:
            print("         (return type) Type: {}".format(first_tkn[0]))
            print("  {}      Identifier: {}".format(next_tkn[2], next_tkn[0]))
            self.Formals()
            if self.curr_token[0] == ")":
                self.Next()
                if self.curr_token[0] =="{":
                    self.StmtBlock()
                else:
                    print("Syntax func {")    

            else:
                print("Syntax func )")    
            
    def Variable(self,first_tkn,next_tkn, t=0):
        if t == 0:
            print("         Type: {}".format(first_tkn[0]))
            print("  {}      Identifier: {}".format(next_tkn[2],next_tkn[0]))
        elif t == 1:
            print("            Type: {}".format(first_tkn[0]))
            print("  {}         Identifier: {}".format(next_tkn[2],next_tkn[0]))
        self.Next()

    def GetType(self):
        if (self.curr_token is not None and self.curr_token[1] == "T_Void" or self.curr_token[1] == "T_Int" or self.curr_token[1] == "T_Double" or self.curr_token[1] == "T_String" 
            or self.curr_token[1] == "T_Bool"):
            return self.curr_token
        else:
            return False

    def Formals(self):
        'Formals : Variable+, | ϵ'
        print("  {}      (formals) VarDecl: ".format(self.curr_token[2]))
        first_tkn = self.curr_token
        self.Next()
        next_tkn = self.curr_token
        self.Variable(first_tkn, next_tkn, t=1)

    def StmtBlock (self):
        "StmtBlock : { VariableDecl* Stmt* }"
        StmtBlock = self.curr_token
        print("         (body) StmtBlock: ")
        self.Statement()

    def Statement(self):
        statemen_types = ["if","While","for","break","return","Print"]
        self.Next()
        curr_statement = self.curr_token
        if curr_statement[0] in statemen_types:
            formating = str.replace(curr_statement[0],curr_statement[0][0],(curr_statement[0][0]).upper(),1)
            #print("            {}: ".format(formating+"Stmt"))
            if curr_statement[0] in statemen_types: #PrintStmt
                Statement_Type = methodcaller(str(formating+"Stmt"))
                Statement_Type(self)
        
            else:
                self.StmtBlock()
        self.Next()

    def ifStmt(self):
        pass

    def PrintStmt(self):
        print("            {}: ".format("PrintStmt"))
        self.Next()
        if self.curr_token[0] == "(":
            self.Next() 
            print("  {}            (args) StringConstant: {}".format(self.curr_token[2],self.curr_token[0]))

    def ReturnStmt(self):
        print("  {}         ReturnStmt: ".format(self.curr_token[2]))
        self.Next()
        if self.curr_token[0] == "(":
            self.Next() #FIGURE OUT ARITMETIC EXPRESION
            

    def Parse(self):
        if self.curr_token is None:
            return None

        res = self.Program()

        return res


    