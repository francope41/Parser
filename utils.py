#Parser class in charge of top-down parsing the inputted file

import numpy as np
from operator import methodcaller

#Tokens item come as an array of 3 alements [Token, Type, Location]
class Parser:
    def __init__(self, tokens):
        self.zcount = 0
        self.loc = 0
        self.tokens = tokens
        self.token_lst = [list(x) for x in self.tokens]
        self.keyword = ['while','if','else','return','break', 'null', 'for', 'Print', 'ReadInteger', 'ReadLine']
        self.Keyfunctions = ['Print', 'ReadInteger', 'ReadLine']
        self.KeyLogical = [ '<','<=','>','>=','==','!=','&&','||','!']
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
        # while self.zcount <= len(self.tokens):
        #     self.Decl()
        #     self.zcount+=1
            #print("Cur Token",self.curr_token)
        while self.curr_token is not None:
            self.Decl()
            # self.zcount+=1
        #print("Cur Token",self.curr_token)

    def Decl(self):
        "Decl : VariableDecl | FunctionDecl"
        first_tkn = self.curr_token
        curr_type, mode = self.GetType()
        if curr_type is not False and mode == "Type": #Check if it is instance
            self.Next()
            next_tkn = self.curr_token
            if next_tkn[1] == "T_Identifier":
                self.Next()
                next_next_tkn = self.curr_token
                if next_next_tkn[0] == "(":
                    self.FunctionDecl(first_tkn,next_tkn)

                elif next_next_tkn[0] == ";":
                    self.VariableDecl(first_tkn,next_tkn)

        elif self.curr_token[1] == "T_Identifier": #Check if is Assign
            Lterm = self.curr_token
            self.Next()
            operator = self.curr_token
            if operator[0] == "+" or operator[0] == "-" or operator[0] == "/" or operator[0] == "*": 
                self.Next()
                Rterm = self.curr_token
                self.AritmeticExpression(Lterm, operator, Rterm)
            
            elif operator[0] == "=":
                self.Next()
                if self.curr_token[1] == "T_Int":
                    Rterm = self.curr_token
                    self.AssignExpression(Lterm,operator,Rterm)
                else:
                    NewLterm = self.curr_token
                    self.Next()
                    Newoperator = self.curr_token
                    self.Next()
                    NewRterm = self.curr_token
                    print("  {}         AssignExpr: ".format(self.curr_token[2]))
                    print("  {}               FieldAccess: ".format(Lterm[2]))
                    print("  {}                   Identifier: {}".format(Lterm[2], Lterm[0]))
                    print("  {}               Operator: {} ".format(operator[2], operator[0]))
                    if NewLterm[0] not in self.Keyfunctions:
                        self.AritmeticExpression(NewLterm,Newoperator,NewRterm)
                    else:
                        formating = str.replace(NewLterm[0],NewLterm[0][0],(NewLterm[0][0]).upper(),1)
                        Statement_Type = methodcaller(str(formating+"Stmt"))
                        Statement_Type(self)

        elif curr_type is not False and mode =="Keywrd":
            formating = str.replace(self.curr_token[0],self.curr_token[0][0],(self.curr_token[0][0]).upper(),1)
            Statement_Type = methodcaller(str(formating+"Stmt"))
            Statement_Type(self)

        elif self.curr_token[0] == ";":
            self.Next()

        else:
            if self.curr_token[0] == ";":
                try:
                    self.Next()
                except:
                    self.curr_token = None
            if self.curr_token[0] == "}":
                try:
                    self.Next()
                except:
                    self.curr_token = None
            else:
                self.Call()

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

        if self.curr_token[0] == ")": #If int test () Open close parenthesis
            print("         (return type) Type: {}".format(first_tkn[0]))
            print("  {}      Identifier: {}".format(next_tkn[2], next_tkn[0]))
            self.Next()
            if self.curr_token[0] == "{":
                self.StmtBlock()

        else: #If it has formals inside parenthesis
            print("         (return type) Type: {}".format(first_tkn[0]))
            print("  {}      Identifier: {}".format(next_tkn[2], next_tkn[0]))
            self.Formals()
            if self.curr_token[0] == ")":
                self.Next()
                if self.curr_token[0] =="{":
                    self.StmtBlock()
                else:
                    print("Syntax func {")
                
                if self.curr_token[0] != "}":
                    self.Next()

                self.Next()
                                
            else:
                print("Syntax func )")    
            
    def Variable(self,first_tkn,next_tkn, t=0):
        if t == 0:#Less Spacing
            print("         Type: {}".format(first_tkn[0]))
            print("  {}      Identifier: {}".format(next_tkn[2],next_tkn[0]))
        elif t == 1:#More Spacing
            print("            Type: {}".format(first_tkn[0]))
            print("  {}         Identifier: {}".format(next_tkn[2],next_tkn[0]))
        self.Next()

    def GetType(self):
        if (self.curr_token is not None and self.curr_token[1] == "T_Void" or self.curr_token[1] == "T_Int" or
            self.curr_token[1] == "T_Double" or self.curr_token[1] == "T_String" or self.curr_token[1] == "T_Bool"):
            return self.curr_token , 'Type'
        elif (self.curr_token is not None and self.curr_token[0] in self.keyword):
            return self.curr_token, "Keywrd"
        else:
            return False , False

    def Formals(self):
        'Formals : Variable+, | ϵ'
        print("  {}      (formals) VarDecl: ".format(self.curr_token[2]))
        first_tkn = self.curr_token
        self.Next()
        next_tkn = self.curr_token
        self.Variable(first_tkn, next_tkn, t=1)
        while self.curr_token[0] != ")":
            self.Next()
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
            if curr_statement[0] in statemen_types:
                Statement_Type = methodcaller(str(formating+"Stmt"))
                Statement_Type(self)
                
            else:
                self.StmtBlock()

        #self.Next()

    def ifStmt(self):
        pass

    def PrintStmt(self):
        print("            {}: ".format("PrintStmt"))
        self.Next()
        if self.curr_token[0] == "(":
            self.Next()
            First_print_val = self.curr_token
            if First_print_val[1] == "T_String":
                print("  {}            (args) StringConstant: {}".format(First_print_val[2],First_print_val[0]))
            elif First_print_val[1] == "T_Identifier":
                self.Next()
                if self.curr_token[0] == "(":
                    print("  {}            (args) Call: ".format(self.curr_token[2]))
                    print("  {}               Identifier: {}".format(First_print_val[2],First_print_val[0]))
                    self.Next()
                    if self.curr_token[1] == "T_Identifier":
                        self.Actuals("FieldAccess",self.curr_token)
                else:
                    self.loc -= 1
                    self.curr_token = self.tokens[self.loc] #Go back one token
                    print("  {}               (actuals) FieldAccess: ".format(First_print_val[2]))
                    print("  {}                  Identifier: {}".format(First_print_val[2],First_print_val[0]))
                    self.Next()
                    if self.curr_token[0] == ",":
                        while self.curr_token[0] != ")":
                            self.Next()
                            if self.curr_token[0] != "," and self.curr_token[0]!=")":
                                print("  {}               (actuals) FieldAccess: ".format(self.curr_token[2]))
                                print("  {}                  Identifier: {}".format(self.curr_token[2],self.curr_token[0]))
                        
                        if self.curr_token[0] == ")":
                            self.Next()
                            if self.curr_token[0] == ";":
                                pass
                            else:
                                print("orerrosr")
                        else:
                            print("errrorsts")
                            
                    else:
                        print("  {}            (args) Call: ".format(self.curr_token[2]))
                        print("  {}               Identifier: {}".format(self.curr_token[2],self.curr_token[0]))
                        self.Next()
                        if self.curr_token[0] == "(":
                            self.Next()
                            if self.curr_token[1]== "T_Identifier":
                                print("  {}               (actuals) FieldAccess: ".format(self.curr_token[2]))
                                print("  {}                  Identifier: {}".format(self.curr_token[2],self.curr_token[0]))

    def ReturnStmt(self):
        print("  {}         ReturnStmt: ".format(self.curr_token[2]))
        self.Next()
        if self.curr_token[0] == "(":
            if self.curr_token[0] != ")":
                self.Next()
                if self.curr_token[1] == "T_Identifier":
                    Lterm = self.curr_token
                    self.Next()
                    if (str(self.curr_token[0]) == "+" or str(self.curr_token[0]) == "-" or 
                        str(self.curr_token[0]) == "*" or str(self.curr_token[0]) == "/"):
                        operator = self.curr_token
                        self.Next()
                        if self.curr_token[1] == "T_Identifier":
                            Rterm = self.curr_token

                            self.AritmeticExpression(Lterm,operator,Rterm)

                        

        elif self.curr_token[1] == "T_IntConstant" or self.curr_token[1] == "T_Double" or self.curr_token[1] == "T_Identifier":
            Lterm = self.curr_token
            self.Next()
            if (str(self.curr_token[0]) == "+" or str(self.curr_token[0]) == "-" or 
                str(self.curr_token[0]) == "*" or str(self.curr_token[0]) == "/"):
                operator = self.curr_token
                self.Next()
                if self.curr_token[1] == "T_Int" or self.curr_token[1] == "T_Double" or self.curr_token[1] == "T_Identifier":
                    Rterm = self.curr_token

                    self.AritmeticExpression(Lterm,operator,Rterm)

    def ReadIntegerStmt(self):
        print("  {}            ReadIntegerExpr: ".format(self.curr_token[2]))
        if self.curr_token[0] == ")":
            self.Next()
            if self.curr_token[0]==";":
                self.Next()
        else:
            print("ReadInteger Sintax error")

    def AritmeticExpression(self,Lterm,operator,Rterm):
        print("  {}            ArithmeticExpr: ".format(self.curr_token[2]))
        #Check Left term in aritmetic expression
        if Lterm[1] == "T_Identifier":
            print("  {}               FieldAccess: ".format(Lterm[2]))
            print("  {}                   Identifier: {}".format(Lterm[2], Lterm[0]))
        elif Lterm[1] == "T_Int":
            print("  {}               IntConstant: {}".format(Lterm[2],Lterm[0]))
        else:
            print("  {}               DoubleConstant: {}".format(Lterm[2],Lterm[0]))

        #Check Operator in aritmetic expression
        print("  {}               Operator: {} ".format(operator[2], operator[0]))

        #Check after Right term
        self.Next()
        if self.curr_token[0] in [";",")"]:
            if Rterm[1] == "T_Identifier":
                print("  {}               FieldAccess: ".format(Rterm[2]))
                print("  {}                   Identifier: {}".format(Rterm[2], Rterm[0]))
            elif Rterm[1] == "T_Int":
                print("  {}               IntConstant: {}".format(Rterm[2],Rterm[0]))
            else:
                print("  {}               DoubleConstant: {}".format(Rterm[2],Rterm[0]))

        else:
            if self.curr_token[0] in ["*","/"]:
                Lterm = Rterm
                operator = self.curr_token
                self.Next()
                Rterm = self.curr_token
                self.AritmeticExpression(Lterm,operator,Rterm)
            elif self.curr_token[0] in ["+","-"]:
                if Rterm[1] == "T_Identifier":
                    print("  {}               FieldAccess: ".format(Rterm[2]))
                    print("  {}                   Identifier: {}".format(Rterm[2], Rterm[0]))
                elif Rterm[1] == "T_Int":
                    print("  {}               IntConstant: {}".format(Rterm[2],Rterm[0]))
                else:
                    print("  {}               DoubleConstant: {}".format(Rterm[2],Rterm[0]))

                print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
                self.Next()
            
            if self.curr_token[0] == "(":
                self.Next()
                Lterm = self.curr_token
                self.Next()
                operator  = self.curr_token
                self.Next()
                Rterm = self.curr_token
                self.AritmeticExpression(Lterm,operator,Rterm)

            if self.curr_token[0]==")":
                self.Next()
            if self.curr_token[0] == ";":
                self.Next()


        # if self.curr_token[0] != ";":
        #     if self.curr_token[0] in ["*","/"]:
        #         Lterm = Rterm
        #         operator = self.curr_token
        #         self.Next()
        #         Rterm = self.curr_token
        #         print("  {}            ArithmeticExpr: ".format(self.curr_token[2]))
        #         print("  {}                IntConstant: {}".format(Lterm[2],Lterm[0]))
        #         print("  {}                Operator: {}".format(operator[2],operator[0]))
        #         print("  {}                IntConstant: {}".format(Rterm[2],Rterm[0]))

        #         self.Next()
        #         if self.curr_token[0] != ";":
        #             if self.curr_token[0] in ["+","-"]:
        #                 print("  {}            Operator: {}".format(self.curr_token[2],self.curr_token[0]))
        #                 self.Next()
        #                 if self.curr_token[0] == "(":
        #                     self.Next()
        #                     Lterm = self.curr_token
        #                     self.Next()
        #                     operator = self.curr_token
        #                     self.Next()
        #                     Rterm = self.curr_token
        #                     self.AritmeticExpression(Lterm,operator,Rterm)
            
        #     elif self.curr_token[0] == ',':
        #         if Rterm[1] == "T_Identifier":
        #             print("  {}               FieldAccess: ".format(Rterm[2]))
        #             print("  {}                   Identifier: {}".format(Rterm[2], Rterm[0]))
        #         elif Rterm[1] == "T_Int":
        #             print("  {}               IntConstant: {}".format(Rterm[2],Rterm[0]))
        #         else:
        #             print("  {}               DoubleConstant: {}".format(Rterm[2],Rterm[0]))

        #         self.Next()
        #         Lterm = self.curr_token
        #         self.Next()
        #         operator = self.curr_token
        #         if operator[0] in self.KeyLogical:
        #             self.Actuals("LogicalExpr_Arit",Lterm) #HERE
        #         else:
        #             self.Next()
        #             Rterm = self.curr_token
        #             self.AritmeticExpression(Lterm,operator,Rterm)
            
        #     else:
        #         #Check Right term in aritmetic expression
        #         if Rterm[1] == "T_Identifier":
        #             print("  {}               FieldAccess: ".format(Rterm[2]))
        #             print("  {}                   Identifier: {}".format(Rterm[2], Rterm[0]))
        #         elif Rterm[1] == "T_Int":
        #             print("  {}               IntConstant: {}".format(Rterm[2],Rterm[0]))
        #         else:
        #             print("  {}               DoubleConstant: {}".format(Rterm[2],Rterm[0]))

        #         self.Next()
        #         if self.curr_token[0] == ";":
        #             self.Next()
        #         elif self.curr_token[0] == ")":
        #             self.Next()
        #             if self.curr_token[0] == ";":
        #                 self.Next()
        #             else:
        #                 print("sintax error ar exp ;")

        # else:
        #     print("  {}               IntConstant: {}".format(Rterm[2],Rterm[0]))
        #     self.Next()

    def AssignExpression(self, Lterm, operator, Rterm):
        print("  {}         AssignExpr: ".format(self.curr_token[2]))
        
        if Lterm[1] == "T_Identifier":
            print("  {}               FieldAccess: ".format(Lterm[2]))
            print("  {}                   Identifier: {}".format(Lterm[2], Lterm[0]))
        elif Lterm[1] == "T_Int":
            print("  {}               IntConstant: {}".format(Lterm[2],Lterm[0]))
        else:
            print("  {}               DoubleConstant: {}".format(Lterm[2],Lterm[0]))

        print("  {}               Operator: {} ".format(operator[2], operator[0]))

        self.Next()
        if self.curr_token[0] == ";": 
            if  Rterm[1] == "T_Identifier":
                print("  {}               FieldAccess: ".format(Rterm[2]))
                print("  {}                   Identifier: {}".format(Rterm[2], Rterm[0]))
            elif Rterm[1] == "T_Int":
                print("  {}               IntConstant: {}".format(Rterm[2],Rterm[0]))
            else:
                print("  {}               DoubleConstant: {}".format(Rterm[2],Rterm[0]))
            self.Next()
        else:
            self.loc -= 1
            self.curr_token = self.tokens[self.loc] #Go back one token

            #Check after Rterm if done or if new aritmetic
            NewLterm = self.curr_token
            self.Next()
            Newoperator = self.curr_token
            if Newoperator[0] in ['+','-']:
                print("  {}            ArithmeticExpr: ".format(self.curr_token[2]))
                self.Next()
                NewRterm = self.curr_token
                self.AritmeticExpression(NewLterm,Newoperator,NewRterm)
            else:
                print("erro de lamader")

    def Actuals(self, actual_type, prev_tkn):
        if actual_type == "FieldAccess":
            print("  {}            (actuals) {}: ".format(prev_tkn[2],actual_type))
            print("  {}               Identifier: {}".format(prev_tkn[2],prev_tkn[0]))
        
        if actual_type == "LogicalExpr":
            print("  {}            (actuals) {}: ".format(self.curr_token[2],actual_type))
            if self.curr_token[0] in self.KeyLogical:
                if self.curr_token[0] == "!":
                    print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
                    self.Next()
                    print("  {}               BoolConstant: {}".format(self.curr_token[2],self.curr_token[0]))
                elif self.curr_token[0] == "&&":
                    print("  {}               Operator: &&".format(self.curr_token[2]))
                    print("  {}               RelationalExpr: ".format(self.curr_token[2]))
                    prev_tkn = self.curr_token
                    self.Next()
                    self.Actuals("LogicalExpr",prev_tkn)
                elif self.curr_token[0] in [">=","<=",">","<","!="]:
                    print("  {}                  FieldAccess: ".format(self.curr_token[2]))
                    print("  {}                     Identifier: {}".format(self.curr_token[2],prev_tkn[0]))
                    print("  {}                  Operator: {}".format(self.curr_token[2],self.curr_token[0]))
                    self.Next()
                    print("  {}                  DoubleConstant: {}".format(self.curr_token[2],self.curr_token[0]))


        if actual_type == "ArithmeticExpr":
            print("  {}            (actuals) {}: ".format(self.curr_token[2],actual_type))
            Lterm = prev_tkn
            operator = self.curr_token
            self.Next()
            Rterm = self.curr_token
            self.AritmeticExpression(Lterm,operator,Rterm)
        
        if actual_type == "LogicalExpr_Arit":
            print("  {}            (actuals) {}: ".format(self.curr_token[2],'LogicalExpr'))
            if self.curr_token[0] in self.KeyLogical:
                print("  {}               EqualityExpr: ".format(self.curr_token[2]))
                print("  {}                  FieldAccess: ".format(self.curr_token[2]))
                print("  {}                     Identifier: {}".format(self.curr_token[2],prev_tkn[0]))
                print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
                self.Next()
                print("  {}                  FieldAccess: ".format(self.curr_token[2]))
                print("  {}                     Identifier: {}".format(self.curr_token[2],self.curr_token[0]))

    def Call(self):
        self.Next()
        if self.curr_token[1] != "T_Identifier":
            pass
        else:
            print("  {}         Call: ".format(self.curr_token[2]))
            print("  {}            Identifier: {}".format(self.curr_token[2],self.curr_token[0]))
            self.Next()
            if self.curr_token[0] == "(":
                while self.curr_token[0] != ")":
                    self.Next()
                    if self.curr_token[1] == "T_Identifier":
                        prev_tkn = self.curr_token
                        #print('prev',prev_tkn)
                        self.Next()
                        #print('post',self.curr_token)
                        if self.curr_token[0] == ",":
                            self.Actuals("FieldAccess",prev_tkn)
                        elif self.curr_token[0] in ['+','-','*','/']:
                            self.Actuals("ArithmeticExpr",prev_tkn)


                    elif (self.curr_token[1] == "T_BoolConstant (value = true)" or self.curr_token[1] == "T_BoolConstant (value = false)" 
                        or self.curr_token[0] in self.KeyLogical):
                        self.Actuals("LogicalExpr",prev_tkn)
                
                if self.curr_token[0] == ")":
                    self.Next()
                    if self.curr_token[0] == ";":
                        pass
                    else:
                        print("erorhere")
                else:
                    print("eroro")

    def Parse(self):
        if self.curr_token is None:
            return None

        res = self.Program()

        return res


    