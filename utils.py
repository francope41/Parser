from operator import methodcaller
import os
import lex as lex

class Lex_Analyzer:
    def __init__(self,path):
        file = open(path, 'r')
        self.program = file
        self.tokens_list = []
        self.lines_list = []


    def Tokenize(self):
        # Define Tokens
        tokens = [
            'VOID','INT','DOUBLE','BOOL','STRING','NULL',
            'FOR','WHILE','IF','ELSE','RETURN','BREAK',
            'PRINT','READINTEGER','READLINE', 'IDENTIFIER',
            'TRUE','FALSE','N_INT','N_DOUBLE', 'STR', 'PLUS', 'MINUS', 
            'MULTIPLY', 'DIVIDE', 'MODULUS',
            'LESS_THAN', 'LESS_THAN_EQUAL', 
            'GREATER_THAN', 'GREATER_THAN_EQUAL',
            'EQUAL', 'EQUALITY', 'NOT_EQUAL', 'AND', 'OR', 'NOT',
            'SEMICOLON', 'COMMA', 'POINT', 'LEFT_PAREN', 'RIGHT_PAREN',
            'LEFT_BRACE', 'RIGHT_BRACE'
        ]

        # Specify regex for each token
        t_VOID = r'void'
        t_INT = r'int'
        t_DOUBLE = r'double'
        t_BOOL = r'bool'
        t_STRING = r'string'
        t_NULL = r'null'
        t_FOR = r'for'
        t_WHILE = r'while'
        t_IF = r'if'
        t_ELSE = r'else'
        t_RETURN = r'return'
        t_BREAK = r'break'
        t_PRINT = r'Print'
        t_READINTEGER = r'ReadInteger'
        t_READLINE = r'ReadLine'
        t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
        t_TRUE = r'true'
        t_FALSE = r'false'
        t_N_INT = r'[0-9]+'
        t_N_DOUBLE = r'[0-9]+\.[0-9]*'
        t_STR = r'\"(.*?)\"'
        t_PLUS = r'\+'
        t_MINUS = r'-'
        t_MULTIPLY = r'\*'
        t_DIVIDE = r'/'
        t_MODULUS = r'%'
        t_LESS_THAN = r'<'
        t_LESS_THAN_EQUAL = r'<='
        t_GREATER_THAN = r'>'
        t_GREATER_THAN_EQUAL = r'>='
        t_EQUAL = r'='
        t_EQUALITY = r'=='
        t_NOT_EQUAL = r'!='
        t_AND = r'&&'
        t_OR = r'\|\|'
        t_NOT = r'!'
        t_SEMICOLON = r';'
        t_COMMA = r','
        t_POINT = r'\.'
        t_LEFT_PAREN = r'\('
        t_RIGHT_PAREN = r'\)'
        t_LEFT_BRACE = r'{'
        t_RIGHT_BRACE = r'}'

        # Ignore Spaces and Comments
        t_ignore = ' \t\n'
        t_ignore_COMMENT = r'\/\/.*'

        # Invalid token actions
        def t_error(token):
            #print(f'Invalid Token: {token.value[0]}')
            token.lexer.skip(1)

        # Create Lexer
        lexer = lex.lex()

        #Open and read file to tokenize
        line_count = 1
        for line in self.program:
            self.lines_list.append(line)
            lexer.input(line)
            #Tokens item come as an array of 4 alements [Token, Type, Line, Column]
            for token in lexer:
                if token.value in ['void','int','double','bool','string','null','for','while','if','else','return','break','Print','ReadInteger','ReadLine']:
                    tk_str = token.value
                    self.tokens_list.append([token.value,"T_{}".format((tk_str.capitalize())),line_count,token.lexpos])
                
                elif token.value in ['true','false']:
                    self.tokens_list.append([token.value,'T_BoolConstant',line_count,token.lexpos])
                
                else:
                    self.tokens_list.append([token.value,token.type,line_count,token.lexpos])
            line_count += 1

        return self.tokens_list, self.lines_list

class Parser:
    def __init__(self, tokens, linesList):
        self.loc = 0
        #Tokens item come as an array of 3 alements [Token, Type, Line, Column]
        self.tokens = tokens
        self.lines_list = linesList
        self.Var_Declared_List = []
        self.Function_Declared_List = []
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
        "Variable ;"
        tkn_type = self.curr_token
        tkn_iden = self.tokens[self.loc+1]
        self.Variable()
        if self.curr_token[0] == ";":
            print("  {}         VarDecl: ".format(self.curr_token[2]))
            print("               Type: {}".format(tkn_type[0]))
            print("  {}            Identifier: {}".format(tkn_iden[2],tkn_iden[0]))
            self.Next()
        else:
            self.Back()
            self.Back()
            raise Exception("Variable Decl Error")
        
    def Variable(self):
        "Type ident"
        self.Type()
        if self.curr_token[1] == "IDENTIFIER":
            self.Next()
        else:
            self.Error(self.curr_token)
            raise Exception("Variable Error")
        
    def Type(self):
        "int | double | bool | string"
        if self.curr_token[0] in ["int","double","bool","string"]:
            self.Next()
        else:
            raise Exception("Type Error")
        
    def Void(self):
        "void"
        if self.curr_token[0] == "void":
            self.Next()
        else:
            raise Exception("Void")

    def FunctionDecl(self):
        "Type ident ( Formals ) StmtBlock | void ident ( Formals ) StmtBlock"
        print("  {}   FnDecl: ".format(self.curr_token[2]))

        try:
            tkn_type = self.curr_token
            self.Type()
            print("         (return type) Type: {}".format(tkn_type[0]))
        except:
            tkn_type = self.curr_token
            self.Void()
            print("         (return type) Type: {}".format(tkn_type[0]))


        if self.curr_token[1] == "IDENTIFIER":
            print("  {}      Identifier: {}".format(self.curr_token[2],self.curr_token[0]))
            self.Next()
            if self.curr_token[0] == "(":
                self.Next()
                self.Formals()
                self.StmtBlock()
        else:
            raise Exception("SSSss")

    def Formals(self):
        "Variable+, | ϵ"
        while self.curr_token[0] != ")":
            if self.curr_token[0] == ",":
                self.Next()
            
            tkn_type = self.curr_token
            tkn_iden = self.tokens[self.loc+1]
            self.Variable()
            print("  {}      (formals) VarDecl: ".format(tkn_type[2]))
            print("            Type: {}".format(tkn_type[0]))
            print("  {}         Identifier: {}".format(tkn_iden[2],tkn_iden[0]))
        
        self.Next()
        
    def StmtBlock(self):
        "{ VariableDecl∗ Stmt∗ }"
        if self.curr_token[0] == "{":
            print("         (body) StmtBlock: ")
            self.Next()
            while self.curr_token[0] != "}":
                if self.curr_token[0] in ["int","double","bool","string"]:
                    self.Var_Declared_List.append([self.curr_token[0], self.curr_token[2]])
                    self.VariableDecl()
                else:
                    try:
                        self.Stmt()
                    except:
                        self.Next()

                    if self.curr_token[0] in ["int","double","bool","string"] or self.curr_token[1] == "IDENTIFIER":
                        self.Error(self.curr_token)


            if self.curr_token[0] == '}':
                self.Next()

    def Stmt(self):
        "<Expr>; | IfStmt | WhileStmt | ForStmt | BreakStmt | ReturnStmt | PrintStmt | StmtBlock"
        if self.curr_token[0] == 'if':
            self.IfStmt()

        elif self.curr_token[0] == 'while':
            self.WhileStmt()

        elif self.curr_token[0] == 'for':
            self.ForStmt()

        elif self.curr_token[0] == 'break':
            self.BreakStmt()

        elif self.curr_token[0] == 'return':
            self.ReturnStmt()

        elif self.curr_token[0] == 'Print':
            self.PrintStmt()
            
        elif self.curr_token[0] == '{':
            self.StmtBlock()

        elif self.curr_token[0] == "else":
            self.Error(self.curr_token)

        else:
            self.Expr()

        if self.curr_token[0] == ";":
            self.Next()
        else:
            pass
            #raise Exception("theres and ex here")

    def IfStmt(self):
        "if ( Expr ) Stmt <else Stmt>"
        if self.curr_token[0] == "if":
            print("                  IfStmt: ")
            self.Next()
            if self.curr_token[0] == "(":
                while self.curr_token[0] != ")":
                    self.Expr()
                    
                self.Next()#Skip closing parenthesis
                self.Stmt()
                self.Next()
                if self.curr_token[0] == "else":
                    self.Stmt()
                else:
                    pass

    def WhileStmt(self):
        "while ( Expr ) Stmt"
        if self.curr_token[0] == "while":
            print("            WhileStmt: ")
            self.Next()
            if self.curr_token[0] == "(":
                self.Next()
                while self.curr_token[0] !=")":
                    self.Expr()

                self.Next() #Skip closing parenthesis
                
                self.Stmt()


    def ForStmt(self):
        "for ( <Expr>; Expr ; <Expr>) Stmt"
        if self.curr_token[0] == "for":
            print("            ForStmt: ")
            self.Next()
            if self.curr_token[0] == "(":
                self.Next()
                while self.curr_token[0] !=")":
                    if self.curr_token[0] == ';':
                        print("               (init) Empty: ")
                        self.Next()

                        self.Expr()
                    
                    else:
                        raise Exception("For error missing ';'")

                    try:
                        self.Expr()
                    except:
                        if self.curr_token[0] == ")":
                            self.Next()
                        else:
                            raise Exception("For error missing ')'")     

                    self.Stmt()

    def ReturnStmt(self):
        "return < Expr > ;"
        if self.curr_token[0] == "return":
            print("  {}         ReturnStmt: ".format(self.curr_token[2]))
            self.Next()
            if self.curr_token[0] == ";":
                print("               Empty: ")
                self.Next()
            else:
                self.Expr()
                
    def BreakStmt(self):
        "break ;"
        if self.curr_token[0] == "break":
            print("  {}                  (then) BreakStmt: ".format(self.curr_token[2]))
            self.Next()
            if self.curr_token[0] == ";":
                self.Next()
            else:
                raise Exception("Break error missing ';'")

    def PrintStmt(self):
        "Print ( Expr+, ) ;"
        if self.curr_token[0] == "Print":
            print("            PrintStmt: ")
            self.Next()
            if self.curr_token[0] == "(":
                self.Next()
                while self.curr_token[0] !=")":
                    self.Expr()

                if self.curr_token[0] == ")":
                    self.Next()  #Skip closing parenthesis

                elif self.curr_token[0] == ";":
                    self.Next()                
                
    def Expr(self):
        """
            LValue = Expr | Constant | LValue | Call | ( Expr ) |
            Expr + Expr | Expr - Expr | Expr * Expr | Expr / Expr |
            Expr % Expr | - Expr | Expr < Expr | Expr <= Expr |
            Expr > Expr | Expr >= Expr | Expr == Expr | Expr ! = Expr |
            Expr && Expr | Expr || Expr | ! Expr | ReadInteger ( ) |
            ReadLine ( )
        """
        if self.curr_token[1] == 'IDENTIFIER':
            self.LValue()
            if self.curr_token[0] == "=":
                self.Assign(self.Lval)
                self.Expr()

            elif self.curr_token[0] == "(":
                if self.tokens[self.loc-2][0] == "(":
                    self.Call(self.Lval,"args")
                else:
                    self.Call(self.Lval,"free")
            
            elif self.curr_token[0] == ")":
                self.TypeIdent(self.Lval,"actuals")
                #self.Next()

            elif self.curr_token[0] == ",":
                self.Args()
                self.Next()

            elif self.curr_token[0] == ";":
                self.TypeIdent(self.Lval)
            else:
                self.Expr()

        elif self.curr_token[1] in ['N_INT','N_DOUBLE','T_BoolConstant','STR','T_Null']:
            if self.tokens[self.loc+1][0] in ["+","-"]:
                self.Lval = self.curr_token
                self.Next()
                self.Expr()
            
            elif self.tokens[self.loc+1][0] in ["*","/","%"]:
                self.Lval = self.curr_token
                self.Next()
                self.Expr()

            else:
                self.Constant("args")
                if self.curr_token[0] == ".":
                    self.Error(self.curr_token)

        elif self.curr_token[0] == "(":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == "+":
            print("  {}            ArithmeticExpr: ".format(self.curr_token[2]))
            self.TypeIdent(self.Lval)
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))

            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            
            else:
                self.Next()
                self.Expr()
        
        elif self.curr_token[0] == "-":
            print("  {}            ArithmeticExpr: ".format(self.curr_token[2]))
            self.TypeIdent(self.Lval)
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))

            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == "*":
            print("  {}            ArithmeticExpr: ".format(self.curr_token[2]))
            self.TypeIdent(self.Lval)
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))

            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()

            elif self.tokens[self.loc+2][0] in ["+","-"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
                print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
                self.Next()
                self.Expr()
            
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == "/":
            print("  {}            ArithmeticExpr: ".format(self.curr_token[2]))
            self.TypeIdent(self.Lval)
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))

            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == "%":
            print("  {}            ArithmeticExpr: ".format(self.curr_token[2]))
            self.TypeIdent(self.Lval)
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))

            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            
            elif self.tokens[self.loc+2][0] in ["&&","||","=="]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
                print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
                self.Next()
                self.TypeIdent(self.curr_token)
                self.Next()
            
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == "<":
            print("  {}               RelationalExpr: ".format(self.curr_token[2]))
            self.TypeIdent(self.Lval)
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == "<=":
            print("  {}               RelationalExpr: ".format(self.curr_token[2]))
            self.TypeIdent(self.Lval)
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == ">":
            print("  {}               RelationalExpr: ".format(self.curr_token[2]))
            self.TypeIdent(self.Lval)
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == ">=":
            print("  {}               RelationalExpr: ".format(self.curr_token[2]))
            self.TypeIdent(self.Lval)
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == "==":
            print("  {}            LogicalExpr: ".format(self.curr_token[2]))
            print("  {}               EqualityExpr: ".format(self.curr_token[2]))
            self.TypeIdent(self.Lval)
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))

            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()

            elif self.tokens[self.loc+2][0] in ["&&","||","!"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
                self.Expr()

            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == "!=":
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
            print("  {}               RelationalExpr: ".format(self.curr_token[2]))
            self.Next()
            self.TypeIdent(self.curr_token)

            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == "&&":
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
            print("  {}               RelationalExpr: ".format(self.curr_token[2]))
            self.Next()
            self.TypeIdent(self.curr_token)

            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == "||":
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
            print("  {}               RelationalExpr: ".format(self.curr_token[2]))
            self.Next()
            self.TypeIdent(self.curr_token)

            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == "!":
            print("  {}            LogicalExpr: ".format(self.curr_token[2]))
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))

            if self.tokens[self.loc+2][0] in [";",",",")"]:
                self.Next()
                Rval = self.curr_token
                self.TypeIdent(Rval)
                self.Next()
            
            else:
                self.Next()
                self.Expr()

        elif self.curr_token[0] == "ReadInteger":
            self.ReadIntegerExpr()
        
        elif self.curr_token[0] == "ReadLine":
            self.ReadLineExpr()
        
        else:
            raise Exception("NO EXPRESION")

    def LValue(self):
        "ident"
        if self.curr_token[1] == "IDENTIFIER":
            self.Lval = self.curr_token
            self.Next()

    def Call(self,ident,loc="free"):
        "ident ( Actuals )"

        if loc == "args":
            if ident[1] == "IDENTIFIER":
                if self.curr_token[0] == "(":
                    self.Next()
                    print("  {}            (args) Call: ".format(ident[2]))
                    print("  {}               Identifier: {}".format(ident[2],ident[0]))
                    while self.curr_token[0] != ")":
                        self.Actuals()
                    self.Next() #Skip closing parenthesis

        elif loc == "free":
            if ident[1] == "IDENTIFIER":
                if self.curr_token[0] == "(":
                    print("  {}            Call: ".format(self.curr_token[2]))
                    print("  {}               Identifier: {}".format(ident[2],ident[0]))
                    while self.curr_token[0] != ")":
                        self.Actuals()
                        
    def Actuals(self):
        self.Expr()

    def Args(self):
        if self.Lval[1] == "IDENTIFIER":
            print("  {}               (args) FieldAccess: ".format(self.Lval[2]))
            print("  {}                   Identifier: {}".format(self.Lval[2],self.Lval[0]))
        elif self.Lval[1] == "N_INT":
            print("  {}                   (args) IntConstant: {}".format(self.Lval[2],self.Lval[0]))
        elif self.Lval[1] == "N_DOUBLE":
            print("  {}                   (args) DoubleConstant: {}".format(self.Lval[2],self.Lval[0]))
        elif self.Lval[1] == "STR":
            print("  {}                   (args) StringConstant: {}".format(self.Lval[2],self.Lval[0]))
        elif self.Lval[1] == "T_BoolConstant":
            print("  {}                   (args) BoolConstant: {}".format(self.Lval[2],self.Lval[0]))
        elif self.Lval[1] == "T_Null":
            print("  {}                   (args) NullConstant: {}".format(self.Lval[2],self.Lval[0]))
        
    def Constant(self,loc):
        "intConstant | doubleConstant | boolConstant | stringConstant | null"

        if loc == "args":
            if self.curr_token[1] == "N_INT":
                print("  {}            (args) IntConstant: {}".format(self.curr_token[2],self.curr_token[0]))

                self.Next()
            elif self.curr_token[1] == "N_DOUBLE":
                print("  {}            (args) DoubleConstant: {}".format(self.curr_token[2],self.curr_token[0]))
                self.Next()

            elif self.curr_token[1] == "T_BoolConstant":
                print("  {}            (args) BoolConstant: {}".format(self.curr_token[2],self.curr_token[0]))

                self.Next()
            elif self.curr_token[1] == "STR":
                print("  {}            (args) StringConstant: {}".format(self.curr_token[2],self.curr_token[0]))
                self.Next()
            elif self.curr_token[1] == "T_Null":
                print("  {}            (args) NullConstant: {}".format(self.curr_token[2],self.curr_token[0]))

                self.Next()
            else:
                raise Exception("No Constant")
            
        elif loc == "free":
            if self.curr_token[1] == "N_INT":
                print("  {}            IntConstant: {}".format(self.curr_token[2],self.curr_token[0]))

                self.Next()
            elif self.curr_token[1] == "N_DOUBLE":
                print("  {}            DoubleConstant: {}".format(self.curr_token[2],self.curr_token[0]))
                self.Next()

            elif self.curr_token[1] == "T_BoolConstant":
                print("  {}            BoolConstant: {}".format(self.curr_token[2],self.curr_token[0]))

                self.Next()
            elif self.curr_token[1] == "STR":
                print("  {}            StringConstant: {}".format(self.curr_token[2],self.curr_token[0]))
                self.Next()
            elif self.curr_token[1] == "T_Null":
                print("  {}            NullConstant: {}".format(self.curr_token[2],self.curr_token[0]))

                self.Next()
            else:
                raise Exception("No Constant")

    def TypeIdent(self,tok,loc="free"):
        if loc == "free":
            if tok[1] == "IDENTIFIER":
                print("  {}               FieldAccess: ".format(tok[2]))
                print("  {}                   Identifier: {}".format(tok[2],tok[0]))
            elif tok[1] == "N_INT":
                print("  {}                   IntConstant: {}".format(tok[2],tok[0]))
            elif tok[1] == "N_DOUBLE":
                print("  {}                   DoubleConstant: {}".format(tok[2],tok[0]))
            elif tok[1] == "STR":
                print("  {}                   StringConstant: {}".format(tok[2],tok[0]))
            elif tok[1] == "T_BoolConstant":
                print("  {}                   BoolConstant: {}".format(tok[2],tok[0]))
            elif tok[1] == "T_Null":
                print("  {}                   NullConstant: {}".format(tok[2],tok[0]))

        elif loc == "actuals":
            if tok[1] == "IDENTIFIER":
                print("  {}               (actuals) FieldAccess: ".format(tok[2]))
                print("  {}                   Identifier: {}".format(tok[2],tok[0]))
            elif tok[1] == "N_INT":
                print("  {}               (actuals) IntConstant: {}".format(tok[2],tok[0]))
            elif tok[1] == "N_DOUBLE":
                print("  {}               (actuals) DoubleConstant: {}".format(tok[2],tok[0]))
            elif tok[1] == "STR":
                print("  {}               (actuals) StringConstant: {}".format(tok[2],tok[0]))
            elif tok[1] == "T_BoolConstant":
                print("  {}               (actuals) BoolConstant: {}".format(tok[2],tok[0]))
            elif tok[1] == "T_Null":
                print("  {}               (actuals) NullConstant: {}".format(tok[2],tok[0]))

    def Assign(self,tok):
        print("  {}         AssignExpr: ".format(tok[2]))
        self.TypeIdent(tok)
        print("  {}            Operator: {}".format(self.curr_token[2],self.curr_token[0]))

        if self.tokens[self.loc+2][0] in [";",",",")"]:
            self.Next()
            Rval = self.curr_token
            self.TypeIdent(Rval)
            self.Next()

        elif self.tokens[self.loc+2][0] in ["*","/","%"]:
            print("sssssss")
        
        elif self.tokens[self.loc+2][0] in ["+","-"]:
            print("  {}            ArithmeticExpr: ".format(self.curr_token[2]))
            self.Next()
            self.Expr()



            
        else:
            self.Next()
            self.Expr()
        # self.TypeIdent()
    
    def ReadIntegerExpr(self):
        print("  {}            ReadIntegerExpr: ".format(self.curr_token[2]))
        self.Next()

    def Error(self, errorTkn):
        #[Token, Type, Line, Column]
        print("")
        print("*** Error line {}.".format(errorTkn[2]))
        errline = self.lines_list[errorTkn[2]-1].strip()
        print(errline)
        print(" "*errorTkn[3]+"^")
        print("*** syntax error")
        print("")
        quit(1)
        #os._exit(1) #Fix this

    def Parse(self):
        if self.curr_token is None:
            return None

        res = self.Program()

        return res