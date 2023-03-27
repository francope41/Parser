import numpy as np
from operator import methodcaller

#Tokens item come as an array of 3 alements [Token, Type, Location]
class Parser:
    def __init__(self,tokens):
        self.zcount = 0
        self.loc = 0
        self.tokens = tokens
        self.token_lst = [list(x) for x in self.tokens]
        self.types = ["T_Void",'T_Int',"T_Double","T_String","T_Bool"]
        self.keyword = ['while','if','else','return','break', 'null', 'for', 'Print', 'ReadInteger', 'ReadLine']
        self.keyStmts = ['if','while','for','break','return','Print']
        self.Keyfunctions = ['Print', 'ReadInteger', 'ReadLine']
        self.KeyLogical = [ '<','<=','>','>=','==','!=','&&','||','!']
        self.KeyAritmetic = ["+","-","*","/"]
        self.formals, self.body, self.expressions = [],[],[]

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
        while self.curr_token is not None:
            self.Decl()
        
    def Decl(self):
        "Decl : VariableDecl | FunctionDecl"
        try:
            try:
                Type, Ident = self.p_VariableDecl()
                self.VariableDecl(Type,Ident)
            except:
                self.loc = self.loc - 2
                self.curr_token = self.tokens[self.loc]
            try:
                self.p_FunctionDecl()
            except:
                raise Exception()
                
        except:
            self.curr_token=None

    def p_VariableDecl(self):
        "Decl : Variable ;"
        Type = self.curr_token
        try:
            Ident = self.Variable()
        except:
            raise Exception()
        
        self.Next()
        if self.curr_token[0] == ";":
            self.Next()
            return Type,Ident
        
        elif self.curr_token[0] == ",":
            self.Next()
            return Type,Ident
        
        elif self.curr_token[0] == ")":
            self.Next()
            return Type,Ident

        else:
            raise Exception()
        
    def VariableDecl(self,Type,Ident):
        print("  {}   VarDecl: ".format(Type[2]))
        print("         Type: {}".format(Type[0]))
        print("  {}      Identifier: {}".format(Ident[2],Ident[0]))

    def p_FunctionDecl(self):
        "Decl : Type ident ( Formals ) StmtBlock | void ident ( Formals ) StmtBlock"  
        try:
            Type = self.curr_token
            try:
                Ident = self.Variable()
            except:
                raise Exception()
        except:
            raise Exception()
        
        self.Next()
        if self.curr_token[0] == "(":
            self.Next()
            if self.curr_token[0] == ")":
                print("  {}   FnDecl: ".format(Type[2]))
                print("         (return type) Type: {}".format(Type[0]))
                print("  {}      Identifier: {}".format(Ident[2],Ident[0]))
                self.Next()
                body = self.p_StmtBlock()
                print("         (body) StmtBlock: ")
                if len(body) > 0:
                    for stmt_blok in body:
                        st_name = stmt_blok[0]
                        formating = str.replace(st_name[0],st_name[0][0],(st_name[0][0]).upper(),1)
                        print("            {}: ".format(formating+"Stmt"))
                        args = stmt_blok[1][0]
                        tkn = args[0][0]
                        tkn_type = args[0][1]

                        print("  {}            (args) {}: {}".format(st_name[2],tkn_type,tkn[0]))

            else:
                try:
                    formals = self.p_Formals()
                    body = self.p_StmtBlock()
                    self.FunctionDecl(Type,Ident,formals,body)
                except:
                    print('error')
                    raise Exception()
                
        self.formals = []
        self.body = []
                
    def FunctionDecl(self, Type, Ident, formals, body):
        print("  {}   FnDecl: ".format(Type[2]))
        print("         (return type) Type: {}".format(Type[0]))
        print("  {}      Identifier: {}".format(Ident[2],Ident[0]))
        if len(formals) > 0:
            for formal in formals:
                self.Formals(formal)

        if len(body)>0:
                self.StmtBlock(body)
                
    def StmtBlock(self,body):
        print("         (body) StmtBlock: ")
        if len(body) > 0:
            for stmt_blok in body:
                st_name = stmt_blok[0]
                args = stmt_blok[1]
                formating = str.replace(st_name[0],st_name[0][0],(st_name[0][0]).upper(),1)
                print("            {}: ".format(formating+"Stmt"))
                #print(st_name, args) #ERROR HEWRE ARGS IS NONE
                print("  {}            (args) {}: {}".format(st_name[2],args[0],self.tokens[self.loc-1][0]))

    def p_StmtBlock(self):
        "{ VariableDecl∗ Stmt∗ }"

        if self.curr_token[0] == "{":
            self.Next()
            try:
                try:
                    Type, Ident = self.p_VariableDecl()
                    self.body.append((Type,Ident))
                    return self.body
                except:
                    self.loc = self.loc - 2
                    self.curr_token = self.tokens[self.loc]

                try:
                    stmt,stmt_vals = self.Stmt()
                    self.body.append((stmt,stmt_vals))
                    return self.body
                
                except:
                    self.loc = self.loc - 1
                    self.curr_token = self.tokens[self.loc]
            
            except:
                raise Exception()

        else:
            raise Exception()
        
    def Formals (self, formal):
        if len(formal)>1:
            print("  {}      (formals) VarDecl: ".format(formal[0][2]))
            print("            Type: {}".format(formal[0][0]))
            print("  {}         Identifier: {}".format(formal[1][2],formal[1][0]))
            
    def p_Formals(self):
        try:
            try:
                Type, Ident = self.p_VariableDecl()
                self.formals.append((Type,Ident))
                return self.formals
            except:
                self.loc = self.loc - 2
                self.curr_token = self.tokens[self.loc]
        except:
            raise Exception()
        
    def Stmt(self):
        self.Next()
        if self.curr_token[0] in self.keyStmts:
            stmt = self.curr_token
            try:
                formating = str.replace(self.curr_token[0],self.curr_token[0][0],(self.curr_token[0][0]).upper(),1)
                Statement_Type = methodcaller(str(formating+"Stmt"))
                stmt_vals = Statement_Type(self)
                return stmt,stmt_vals
            except:
                print('formating')

        else:
            print ('error_stmt')    

    def IfStmt(self):
        pass

    def WhileStmt(self):
        pass

    def ForStmt(self):
        pass

    def ReturnStmt(self):
        rt_expr = []
        self.Next()
        expr = self.Expr()
        print("Expresion in return", expr)
        self.Next()
        if self.curr_token == ";":
            return expr
        else:
            raise Exception() 
            
    def BreakStmt(self):
        pass

    def PrintStmt(self):
        pr_expr = []
        self.Next()
        if self.curr_token[0] == "(":
            expression = self.Expr()
            pr_expr.append(expression)
            self.Next()
            return pr_expr

    def Variable(self):
        try:
            self.Type()
        except:
            raise Exception()
        
        self.Next()
        if self.curr_token[1] == "T_Identifier":
            return self.curr_token
        else:
            raise Exception()

    def Type(self):
        if self.curr_token[1] in self.types:
            type = self.curr_token[1]
            return self.types.index(type)
        
    def Expr(self):
        self.expressions = []

        #Check if Constant
        try:
            try:
                if self.curr_token[1] in ['T_Int','T_Double','T_BoolConstant (value = true)','T_BoolConstant (value = false)','T_String']:
                    tkn,tkntype = self.Constant()
                    expression = (tkn,tkntype)
                    self.expressions.append(expression)
                    self.Next()
                    return self.expressions
                
            except:
                raise Exception()

            #Check if ( Expr )
            try:
                if self.curr_token[0] == "(":
                    self.Next() #First next
                    while self.curr_token[0]!= ")":
                        expression = self.Expr()
                        if self.curr_token[0] == ")":
                            pass
                        else:
                            self.expressions.append(expression)
                    
                    return self.expressions
            except:
                raise Exception()
            
        except:
            pass
                
        

    def AritmeticExpression(self):
        if self.curr_token[0] == "+":
            try:
                self.Next()
                expr = self.Expr()
            except:
                pass
            return self.curr_token


    def LValue(self):
        if self.curr_token[1] == "T_Identifier":
            return self.curr_token
        else:
            raise Exception()

    def Constant(self):
        if self.curr_token[1] == "T_Int":
            return self.curr_token,"IntConstant"
        elif self.curr_token[1] == "T_Double":
            return self.curr_token,"DoubleConstant"
        elif self.curr_token[1] == "T_BoolConstant (value = true)":
            return self.curr_token,"BoolConstant"
        elif self.curr_token[1] == "T_BoolConstant (value = false)":
            return self.curr_token,"BoolConstant"
        elif self.curr_token[1] == "T_String":
            return self.curr_token,"StringConstant"
        elif self.curr_token[1] == None:
            self.curr_token == None
        else:
            raise Exception()

    def Parse(self):
        if self.curr_token is None:
            return None

        res = self.Program()

        return res
    
    def old(self):
        try:
            try:
                Lval = self.LValue()
                self.Next()
                if self.curr_token[0] == "=":
                    try:
                        self.Next()
                        expression = self.Expr()
                        expr.append[(Lval,"=",expr)]
                        return(expr)
                    except:
                        pass
                else:
                    self.loc = self.loc - 1 #Return one token so that it can be re examinated
                    self.curr_token = self.tokens[self.loc]
                    raise Exception()
            except:
                pass

            try:
                tken , constant_type = self.Constant()
                self.Next()
                expr.append([tken,constant_type])
                return expr
            except:
                pass

            try:
                Lval = self.LValue()
                self.Next()
                if self.curr_token in [",",")","}"]:
                    expr.append(Lval)
                    self.Next()
                    return expr
                else:
                    raise Exception()
            except:
                self.loc = self.loc - 1 #Return one token so that it can be re examinated
                self.curr_token = self.tokens[self.loc]
                pass
            
            try:
                call = self.p_Call()
            except:
                pass

            try:
                if self.curr_token[0] == "(":
                    expr.append(self.curr_token)
                    self.Next()
                    while self.curr_token[0] != ")":
                        try:
                            expression = self.Expr()
                            expr.append(expression)
                            self.Next()
                        except:
                            raise Exception()
                        if self.curr_token[0] ==")":
                                expr.append(self.curr_token)
                        
                        return expr
                    
            except:
                self.loc = self.loc - 1 #Return one token so that it can be re examinated
                self.curr_token = self.tokens[self.loc]
                pass

            try:
                if self.curr_token[0] in self.KeyAritmetic:
                    operator = self.curr_token
                    self.Next()
                    try:
                        expression = self.Expr()
                        expr.append(operator)
                    except:
                        pass

                    
                    return expr
            except:
                self.loc = self.loc - 1 #Return one token so that it can be re examinated
                self.curr_token = self.tokens[self.loc]
                pass

            ####ADD MISSING EXPR

        except:
            print("aqui error")

        self.curr_token = None




      
class Parser_Old:
    def __init__(self, tokens):
        self.loc = 0
        #Tokens item come as an array of 3 alements [Token, Type, Line, Column]
        self.tokens = tokens

        if len(self.tokens) > 0:
            self.curr_token = self.tokens[self.loc]
        else:
            self.curr_token = None
            print("Empty program is syntactically incorrect.")

    def Next(self):
        try:
            self.loc += 1
            try:
                self.curr_token = self.tokens[self.loc]
            except:
                quit()
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
            elif self.curr_token[0] in [")",";","}"]:
                self.Next()
            else:
                print("passed Variable")
                raise Exception("passed Variable")
        except:
            exit()
            raise Exception()
            if self.curr_token[0] == "T_Identifier":
                print("Hello")

    def getType(self):
        if self.curr_token[1] in ['T_Void','T_Int','T_Double','T_String','T_Bool']:
            return self.curr_token
        
        elif self.curr_token[0] in [")",";","}"]:
            self.Next()

        elif self.curr_token[0] in ["return"]:
            self.ReturnStmt()

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
                    try:
                        type_tk, ident = self.Variable()
                    except:
                        self.ErrorVariable()

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

                elif self.curr_token[0] == "else":
                    self.ErrorStmtBlock()

                else:
                    self.Stmt()
                
                    self.Next()

    def Stmt(self):
        try:
            formating = str.replace(self.curr_token[0],self.curr_token[0][0],(self.curr_token[0][0]).upper(),1)
            Statement_Type = methodcaller(str(formating+"Stmt"))
            stmt_vals = Statement_Type(self)
        except:
            pass
        
        try:
            self.Expr()
        except:
            pass

    def ReturnStmt(self):
        if self.curr_token[0] == "return":
            print("  {}         ReturnStmt: ".format(self.curr_token[2]))
            self.Next()
            if self.curr_token[0] == ";":
                print("               Empty: ")
            else:
                self.Expr()       

    def PrintStmt(self):
        print("            PrintStmt: ")
        self.Next()
        if self.curr_token[0] == "(":
            self.Next()
        self.Expr()

    def WhileStmt(self):
        print("            WhileStmt: ")
        if self.curr_token[0] == "(":
            self.Next()
        self.Expr()

    def IfStmt(self):
        print("                  IfStmt: ")
        self.Next()
        if self.curr_token[0] == "(":
            self.Next()
        self.Expr()

        if self.curr_token[0] == "else":
            print("PTASSS")

    def BreakStmt(self):
        print("  {}                  (then) BreakStmt: ".format(self.curr_token[2]))
        self.Next()
        if self.curr_token[0] == ";":
            self.Next()

    def ReadIntegerStmt(self):
        print("  {}            ReadIntegerExpr: ".format(self.curr_token[2]))

    def ForStmt(self):
        print("            ForStmt: ")
        self.Next()
        if self.curr_token[0] == "(":
            self.Next()
            if self.curr_token[0] == ";":
                print("               (init) Empty: ")
                self.Next()
                self.Expr()
            else:
                self.Expr()
    
    def Expr(self):
        if self.curr_token[0] == "(":
            self.Next()
            while self.curr_token[0] != ")":
                self.Expr()
                self.Next()
            
            self.Next()

        elif self.curr_token[1] == "T_Identifier":
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

            elif self.curr_token[0] == "(":
                #print(" {}               Identifier: {}".format(LValue[2],LValue[0]))
                self.Call(LValue)   

            elif self.curr_token[0] in [")",";",","]:
                if LValue[1] == "T_Identifier":
                    print("  {}               (actuals) FieldAccess: ".format(LValue[2]))
                    print("  {}                   Identifier: {}".format(LValue[2], LValue[0]))
                elif LValue[1] == "T_Int":
                    print("  {}               IntConstant: {}".format(LValue[2],LValue[0]))

                elif LValue[1] == "T_Double":
                    print("  {}               DoubleConstant: {}".format(LValue[2],LValue[0]))

                elif LValue[1] == "T_String":
                    print("  {}            (args) StringConstant: {}".format(LValue[2],LValue[0]))

                elif LValue[1] in ["T_BoolConstant (value = true)","T_BoolConstant (value = false)"]:
                    print("  {}               BoolConstant: {}".format(LValue[2],LValue[0]))
                else:
                    self.Call(LValue)

            elif self.curr_token[0] in ['<','<=','>','>=','==','!=','&&','||','!']:                
                self.Expr()

        elif self.curr_token[0] in ['Print', 'ReadInteger', 'ReadLine']:
            formating = str.replace(self.curr_token[0],self.curr_token[0][0],(self.curr_token[0][0]).upper(),1)
            Statement_Type = methodcaller(str(formating+"Stmt"))
            stmt_vals = Statement_Type(self)

        elif self.curr_token[1] == "T_String":
            print("  {}            (args) StringConstant: {}".format(self.curr_token[2],self.curr_token[0]))
            self.Next()

        elif self.curr_token[1] in ['T_Int','T_Double']:
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

            elif self.curr_token[0] == "(":
                #print(" {}               Identifier: {}".format(LValue[2],LValue[0]))
                self.Call(LValue)   

            elif self.curr_token[0] in [")",";",","]:
                if LValue[1] == "T_Identifier":
                    print("  {}               (actuals) FieldAccess: ".format(LValue[2]))
                    print("  {}                   Identifier: {}".format(LValue[2], LValue[0]))
                elif LValue[1] == "T_Int":
                    print("  {}               IntConstant: {}".format(LValue[2],LValue[0]))

                elif LValue[1] == "T_Double":
                    print("  {}               DoubleConstant: {}".format(LValue[2],LValue[0]))

                elif LValue[1] == "T_String":
                    print("  {}            (args) StringConstant: {}".format(LValue[2],LValue[0]))

                elif LValue[1] in ["T_BoolConstant (value = true)","T_BoolConstant (value = false)"]:
                    print("  {}               BoolConstant: {}".format(LValue[2],LValue[0]))

                else:
                    self.Call(LValue)
        
        elif self.curr_token[0] in ['<','<=','>','>=','==','!=','&&','||','!']:
            if self.curr_token[0] == "!":
                print("  {}            (actuals) LogicalExpr: ".format(self.curr_token[2]))
                operator = self.curr_token
                print("  {}               Operator: {}".format(operator[2],operator[0]))
                self.Next()
                if self.curr_token[1] in ["T_BoolConstant (value = true)","T_BoolConstant (value = false)"]:
                    print("  {}               BoolConstant: {}".format(self.curr_token[2],self.curr_token[0]))
            elif self.curr_token[0] == "==":
                print("  {}            (actuals) LogicalExpr: ".format(self.curr_token[2]))
                self.Back()
                LValue = self.curr_token
                print("  {}               EqualityExpr: ".format(self.curr_token[2]))
                self.Next()
                operator = self.curr_token
                self.Next()
                RValue = self.curr_token

                if LValue[1] == "T_Identifier":
                    print("  {}               (actuals) FieldAccess: ".format(LValue[2]))
                    print("  {}                   Identifier: {}".format(LValue[2], LValue[0]))
                elif LValue[1] == "T_Int":
                    print("  {}               IntConstant: {}".format(LValue[2],LValue[0]))

                elif LValue[1] == "T_Double":
                    print("  {}               DoubleConstant: {}".format(LValue[2],LValue[0]))

                elif LValue[1] == "T_String":
                    print("  {}            (args) StringConstant: {}".format(LValue[2],LValue[0]))

                elif LValue[1] in ["T_BoolConstant (value = true)","T_BoolConstant (value = false)"]:
                    print("  {}               BoolConstant: {}".format(LValue[2],LValue[0]))

                print("  {}                  Operator: {}".format(operator[2],operator[0]))

                if RValue[1] == "T_Identifier":
                    print("  {}               (actuals) FieldAccess: ".format(RValue[2]))
                    print("  {}                   Identifier: {}".format(RValue[2], RValue[0]))
                elif RValue[1] == "T_Int":
                    print("  {}               IntConstant: {}".format(RValue[2],RValue[0]))

                elif RValue[1] == "T_Double":
                    print("  {}               DoubleConstant: {}".format(RValue[2],RValue[0]))

                elif RValue[1] == "T_String":
                    print("  {}            (args) StringConstant: {}".format(RValue[2],RValue[0]))
                
                self.Next()
                self.Expr()

            elif self.curr_token[0] == "&&":
                print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
                self.Next()
                self.Expr()
            
            elif self.curr_token[0] in ['<','<=','>','>=']:
                print("  {}               RelationalExpr: ".format(self.curr_token[2]))
                self.Back()
                LValue = self.curr_token
                self.Next()
                operator = self.curr_token
                self.Next()
                RValue = self.curr_token

                if LValue[1] == "T_Identifier":
                    print("  {}               (actuals) FieldAccess: ".format(LValue[2]))
                    print("  {}                   Identifier: {}".format(LValue[2], LValue[0]))
                elif LValue[1] == "T_Int":
                    print("  {}               IntConstant: {}".format(LValue[2],LValue[0]))

                elif LValue[1] == "T_Double":
                    print("  {}               DoubleConstant: {}".format(LValue[2],LValue[0]))

                elif LValue[1] == "T_String":
                    print("  {}            (args) StringConstant: {}".format(LValue[2],LValue[0]))

                print("  {}                  Operator: {}".format(operator[2],operator[0]))

                if RValue[1] == "T_Identifier":
                    print("  {}               (actuals) FieldAccess: ".format(RValue[2]))
                    print("  {}                   Identifier: {}".format(RValue[2], RValue[0]))
                elif RValue[1] == "T_Int":
                    print("  {}               IntConstant: {}".format(RValue[2],RValue[0]))

                elif RValue[1] == "T_Double":
                    print("  {}               DoubleConstant: {}".format(RValue[2],RValue[0]))

                elif RValue[1] == "T_String":
                    print("  {}            (args) StringConstant: {}".format(RValue[2],RValue[0]))

            else:
                self.Expr()

        elif self.curr_token[0] == "else":
            self.Next()
            self.Expr()

        else:
            raise Exception()

    def Call(self, LValue):
        print("  {}            (args) Call: ".format(LValue[2]))
        print("  {}               Identifier: {}".format(LValue[2],LValue[0]))
        if self.curr_token[0] == "(":
            self.Next()
            while self.curr_token[0] != ")":
                self.Actuals()
                self.Next()

    def Actuals(self):
        self.Expr()

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
                print("  {}               (actuals) FieldAccess: ".format(RValue[2]))
                print("  {}                   Identifier: {}".format(RValue[2], RValue[0]))
            elif RValue[1] == "T_Int":
                print("  {}               IntConstant: {}".format(RValue[2],RValue[0]))

            elif RValue[1] == "T_Double":
                print("  {}               DoubleConstant: {}".format(RValue[2],RValue[0]))

            elif RValue[1] == "T_String":
                print("  {}            (args) StringConstant: {}".format(RValue[2],RValue[0]))
            
            elif RValue[1] in ["T_BoolConstant (value = true)","T_BoolConstant (value = false)"]:
                    print("  {}               BoolConstant: {}".format(RValue[2],RValue[0]))

        else:
            self.Back()
            self.Expr()

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
            if RValue[1] == "T_Identifier":
                print("  {}               (actuals) FieldAccess: ".format(RValue[2]))
                print("  {}                   Identifier: {}".format(RValue[2], RValue[0]))
            elif RValue[1] == "T_Int":
                print("  {}               IntConstant: {}".format(RValue[2],RValue[0]))

            elif RValue[1] == "T_Double":
                print("  {}               DoubleConstant: {}".format(RValue[2],RValue[0]))

            elif RValue[1] == "T_String":
                print("  {}            (args) StringConstant: {}".format(RValue[2],RValue[0]))

            elif RValue[1] in ["T_BoolConstant (value = true)","T_BoolConstant (value = false)"]:
                    print("  {}               BoolConstant: {}".format(RValue[2],RValue[0]))
        else:
            self.Back()
            self.Expr()

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
            pass

    def ErrorVariable(self):
        #print(self.curr_token)
        LINE_UP = '\033[1A'
        LINE_CLEAR = '\x1b[2K'

        try:
            count = 0
            while count in range(100):
                print(LINE_UP, end=LINE_CLEAR)
                count += 1
        
        except:
            pass

        self.loc -= 1
        self.curr_token = self.tokens[self.loc]
        print("")
        print("*** Error line {}.".format(self.curr_token[2]))
        line = []
        for i in self.tokens:
            if i[2] == self.curr_token[2]:
                line.append(i[0])
        line = ' '.join(line)
        print(line)
        print(" "*line.find(self.curr_token[0])+"^")
        print("*** syntax error")
        print("")
        print("")
        exit()

    def ErrorStmtBlock(self):
        LINE_UP = '\033[1A'
        LINE_CLEAR = '\x1b[2K'
        try:
            count = 0
            while count in range(100):
                print(LINE_UP, end=LINE_CLEAR)
                count += 1
        except:
            pass
        print("")
        print("*** Error line {}.".format(self.curr_token[2]))
        line = []
        for i in self.tokens:
            if i[2] == self.curr_token[2]:
                line.append(i[0])
        line = ' '.join(line)
        print("    "+line)
        print("    "+"^^^^")
        print("*** syntax error")
        exit()

    def Parse(self):
        if self.curr_token is None:
            return None

        res = self.Program()

        return res
    