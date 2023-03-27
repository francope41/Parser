from operator import methodcaller
import os
import ply.lex as lex

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
            if line != "\n":
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
        self.Variable()
        if self.curr_token[0] == ";":
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
            
            var_decl = self.curr_token
            self.Variable()
            print("  {}      (formals) VarDecl: ".format(var_decl[2]))
            print("            Type: {}".format(var_decl[0]))
            print("  {}         Identifier: {}".format(self.curr_token[2],self.curr_token[0]))
        
        self.Next()
        
    def StmtBlock(self):
        "{ VariableDecl∗ Stmt∗ }"
        if self.curr_token[0] == "{":
            print("         (body) StmtBlock: ")
            self.Next()
            while self.curr_token !="}":
                if self.curr_token[0] in ["int","double","bool","string"]:
                    self.Var_Declared_List.append([self.curr_token[0], self.curr_token[2]])
                    self.VariableDecl()
                    
                else:
                    try:
                        self.Stmt()
                    except:
                        self.Next()

                #self.Next()

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
            self.StmtBlock
        else:
            self.Expr()

        if self.curr_token[0] == ";":
            self.Next()
        else:
            raise Exception("theres and ex here")

    def IfStmt(self):
        "if ( Expr ) Stmt <else Stmt>"
        if self.curr_token[0] == "if":
            self.Next()
            if self.curr_token["("]:
                while self.curr_token != ")":
                    try:
                        self.Expr()
                    except:
                        break
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
            self.Next()
            if self.curr_token[0] == "(":
                while self.curr_token[0] !=")":
                    try:
                        self.Expr()
                    except:
                        break
                self.Next() #Skip closing parenthesis
                self.Stmt()
    
    def ForStmt(self):
        "for ( <Expr>; Expr ; <Expr>) Stmt"
        if self.curr_token[0] == "for":
            self.Next()
            if self.curr_token[0] == "(":
                while self.curr_token[0] !=")":
                    try:
                        self.Expr()
                    except:
                        if self.curr_token[0] == ";":
                            self.Next()
                        else:
                            break
                            raise Exception("For error missing ';'")
                    
                    self.Expr()

                    if self.curr_token[0] == ";":
                        self.Next()
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
                self.Next()
            else:
                self.Expr()
                
    def BreakStmt(self):
        "break ;"
        if self.curr_token[0] == "break":
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
                    if self.curr_token[0] == ",":
                        self.Next()

                self.Next()  #Skip closing parenthesis
                if self.curr_token[0] == ";":
                    self.Next()
                else:
                    raise Exception("Print error missing ';'")
                
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
            self.Expr()

        elif self.curr_token[1] in ['N_INT','N_DOUBLE','T_BoolConstant','STR','T_Null']:
            self.Constant()
            if self.curr_token[0] == ".":
                self.Error(self.curr_token)

        elif self.curr_token[1] == "(":
            self.Next()
            self.Expr()
            if self.curr_token[0] == ")":
                self.Next()
                if self.curr_token[0] == ";":
                    self.Next()
            else:
                print("No funcrion")

        elif self.curr_token[0] == "+":
            print("  {}            ArithmeticExpr: ".format(self.curr_token[2]))
            print("  {}               FieldAccess: ".format(self.Lval[2]))
            print("  {}                   Identifier: {}".format(self.Lval[2],self.Lval[0]))
            print("  {}               Operator: {}".format(self.curr_token[2],self.curr_token[0]))
            self.Next()
            self.Expr()
        
        elif self.curr_token[0] == "-":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == "*":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == "/":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == "%":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == "<":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == "<=":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == ">":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == ">=":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == "==":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == "!=":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == "&&":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == "||":
            self.Next()
            self.Expr()

        elif self.curr_token[0] == "!":
            self.Next()
            self.Expr()

        else:
            try:
                self.ReadIntegerExpr()
            except:
                try:
                    self.ReadLineExpr()
                except:
                    raise Exception("NO EXPRESION")

    def LValue(self):
        "ident"
        if self.curr_token[1] == "IDENTIFIER":
            self.Lval = self.curr_token
            self.Next()

    def Call(self):
        "ident ( Actuals )"
        if self.curr_token[1] == "IDENTIFIER":
            self.Next()
            if self.curr_token[0] == "(":
                while self.curr_token[0] != ")":
                    try:
                        self.Actuals()
                    except:
                        break

                self.Next() #Skip closing parenthesis
        
    def Actuals(self):
        self.Expr()
        if self.curr_token[0] == ",":
            self.Next()
        else:
            pass

    def Constant(self):
        "intConstant | doubleConstant | boolConstant | stringConstant | null"

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

    def Error(self, errorTkn):
        #[Token, Type, Line, Column]
        print("")
        print("*** Error line {}.".format(errorTkn[2]))
        print(self.lines_list[errorTkn[2]].strip())
        print(" " * errorTkn[3]+"^"*len(errorTkn[0]))
        print("*** syntax error")
        print("")
        quit(1)
        #os._exit(1) #Fix this

    def Parse(self):
        if self.curr_token is None:
            return None

        res = self.Program()

        return res