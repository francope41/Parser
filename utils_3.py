from operator import methodcaller

class Parser:
    def __init__(self, tokens):
        self.loc = 0
        self.tokens = tokens

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
    
    def Back(self):
        try:
            self.loc -= 1
            self.curr_token = self.tokens[self.loc]
        except StopIteration:
            self.curr_token = None

    def Program(self):
        "Program : Decl+"
        print("\n   Program: ")
        while self.curr_token is not None:
            self.Decl()

    def Decl(self):
        "Decl : VariableDecl | FunctionDecl"
        try:
            self.VariableDecl()
        except:
            pass
        self.FunctionDecl()

    def VariableDecl(self):
        try:
            type_tk, ident = self.Variable()
            self.Next()
            if self.curr_token[0] == ";":
                print("  {}   VarDecl: ".format(self.curr_token[2]))
                print("         Type: {}".format(type_tk[0]))
                print("  {}      Identifier: {}".format(ident[2],ident[0]))
                self.Next()
            else:
                self.Back()
                self.Back() #Go back twice since Variable decl always moves forward twice
                raise Exception()
        except:
            pass

    def FunctionDecl(self):
        type_tk, ident = self.Variable()
        print("  {}   FnDecl: ".format(self.curr_token[2]))
        print("         (return type) Type: {}".format(type_tk[0]))
        print("  {}      Identifier: {}".format(ident[2],ident[0]))
        self.Next()
        formals = self.Formals()
        if len(formals)>0:
            for formal in formals:
                type_tk = formal[0]
                ident = formal[1]
                print("  {}      (formals) VarDecl: ".format(type_tk[2]))
                print("            Type: {}".format(type_tk[0]))
                print("  {}         Identifier: {}".format(ident[2],ident[0]))

        if self.curr_token[0] == ")":
                self.Next()
        else:
            print("Error closing formals")

        self.StmtBlock()
        if self.curr_token[0] == "}":
            self.Next()
        else:
            print("missnin }")

    def Variable(self):
        try:
            type_tk = self.getType() #Get type returns current token if it is a type
            self.Next()
            if self.curr_token[1] == "T_Identifier":
                ident = self.curr_token
                return type_tk,ident
            else:
                print("passed Variable")
                raise Exception("passed Variable")
        except:
            if self.curr_token[0] == "T_Identifier":
                print("Hello")

    def getType(self):
        if self.curr_token[1] in ['T_Void','T_Int','T_Double','T_String','T_Bool']:
            return self.curr_token
        else:
            print("passed get type")
            raise Exception("passed get type")
    
    def Formals(self):
        formals = []
        if self.curr_token[0] == "(":
            self.Next()
            while self.curr_token[0] != ")":
                if self.curr_token[0] == ",": 
                    self.Next()
                else:
                    type_tk, ident = self.Variable()
                    formals.append([type_tk,ident])
                    
                    self.Next()
        return formals

    def StmtBlock(self):
        if self.curr_token[0] == "{":
            print("         (body) StmtBlock: ")
            self.Next()
            while self.curr_token[0] != "}":  
                if self.curr_token[1] in ['T_Void','T_Int','T_Double','T_String','T_Bool']:
                    self.body_VarDecl()

                else:
                    self.Stmt()
                
                    self.Next()


    def Stmt(self):
        try:
            self.Expr()
        except:
            pass
        
        try:
            formating = str.replace(self.curr_token[0],self.curr_token[0][0],(self.curr_token[0][0]).upper(),1)
            Statement_Type = methodcaller(str(formating+"Stmt"))
            stmt_vals = Statement_Type(self)
        except:
            pass

    def ReturnStmt(self):
        if self.curr_token[0] == "return":
            print("  {}         ReturnStmt: ".format(self.curr_token[2]))
            self.Next()
        self.Expr()       

    def Expr(self):
        if self.curr_token[0] == "(":
            self.Next()
            while self.curr_token[0] != ")":
                self.Expr()
                self.Next()
            
            self.Next()
        

        if self.curr_token[1] == "T_Identifier":
            LValue = self.curr_token
            self.Next()
            if self.curr_token[0] in ['+','-','*','/','%']:
                operator = self.curr_token
                self.Next()
                RValue = self.curr_token
                self.AritmeticExpr(LValue,operator,RValue)

                
            elif self.curr_token[0] in ['=']:
                operator = self.curr_token
                self.Next()
                RValue = self.curr_token
                self.AssignExpr(LValue,operator,RValue)

        

        else:
            raise Exception()
            self.Back()

    def AritmeticExpr(self,LValue,operator,RValue):
        print("  {}            ArithmeticExpr: ".format(LValue[2]))
        #Check Left term in aritmetic expression
        if LValue[1] == "T_Identifier":
            print("  {}               FieldAccess: ".format(LValue[2]))
            print("  {}                   Identifier: {}".format(LValue[2], LValue[0]))
        elif LValue[1] == "T_Int":
            print("  {}               IntConstant: {}".format(LValue[2],LValue[0]))
        else:
            print("  {}               DoubleConstant: {}".format(LValue[2],LValue[0]))

        #Check Operator in aritmetic expression
        print("  {}               Operator: {} ".format(operator[2], operator[0]))

        #Check after Right term
        self.Next()
        if self.curr_token[0] in [";",")",","]:
            if RValue[1] == "T_Identifier":
                print("  {}               FieldAccess: ".format(RValue[2]))
                print("  {}                   Identifier: {}".format(RValue[2], RValue[0]))
            elif RValue[1] == "T_Int":
                print("  {}               IntConstant: {}".format(RValue[2],RValue[0]))
            else:
                print("  {}               DoubleConstant: {}".format(RValue[2],RValue[0]))

    def AssignExpr(self,LValue,operator,RValue):
        print("  {}         AssignExpr: ".format(LValue[2]))
        #Check Left term in aritmetic expression
        if LValue[1] == "T_Identifier":
            print("  {}               FieldAccess: ".format(LValue[2]))
            print("  {}                   Identifier: {}".format(LValue[2], LValue[0]))
        elif LValue[1] == "T_Int":
            print("  {}               IntConstant: {}".format(LValue[2],LValue[0]))
        else:
            print("  {}               DoubleConstant: {}".format(LValue[2],LValue[0]))

        #Check Operator in aritmetic expression
        print("  {}               Operator: {} ".format(operator[2], operator[0]))

        self.Next()
        if self.curr_token[0] == ";": 
            if  RValue[1] == "T_Identifier":
                print("  {}               FieldAccess: ".format(RValue[2]))
                print("  {}                   Identifier: {}".format(RValue[2], RValue[0]))
            elif RValue[1] == "T_Int":
                print("  {}               IntConstant: {}".format(RValue[2],RValue[0]))
            else:
                print("  {}               DoubleConstant: {}".format(RValue[2],RValue[0]))

        
        #We are here rn

    def body_VarDecl(self):
        try:
            type_tk, ident = self.Variable()
            self.Next()
            if self.curr_token[0] == ";":
                    print("  {}         VarDecl: ".format(self.curr_token[2]))
                    print("               Type: {}".format(type_tk[0]))
                    print("  {}           Identifier: {}".format(ident[2],ident[0]))
                    self.Next()
            else:
                self.Back()
                self.Back() #Go back twice since Variable decl always moves forward twice
        except:
            print(self.curr_token)
        
    def Parse(self):
        if self.curr_token is None:
            return None

        res = self.Program()

        return res