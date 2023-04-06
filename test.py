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
                    #self.tokens_list.append([token.value,"T_{}".format((tk_str.capitalize())),line_count,token.lexpos])
                    self.tokens_list.append(token.value)
                
                elif token.value in ['true','false']:
                    #self.tokens_list.append([token.value,'T_BoolConstant',line_count,token.lexpos])
                    self.tokens_list.append(token.value)

                else:
                    #self.tokens_list.append([token.value,token.type,line_count,token.lexpos])
                    self.tokens_list.append(token.value)

            line_count += 1

        return self.tokens_list, self.lines_list

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.parse_program()

    def consume(self, expected_token):
        if self.pos < len(self.tokens) and self.tokens[self.pos] == expected_token:
            self.pos += 1
        else:
            raise SyntaxError(f"Unexpected token: '{self.tokens[self.pos]}', expected: '{expected_token}'")

    def parse_program(self):
        decls = []
        while self.pos < len(self.tokens):
            decls.append(self.parse_decl())
        return decls

    def parse_decl(self):
        if self.tokens[self.pos] in ['int', 'double', 'bool', 'string', 'void']:
            return self.parse_variable_or_function_decl()
        else:
            raise SyntaxError(f"Unexpected token: '{self.tokens[self.pos]}'")

    def parse_variable_or_function_decl(self):
        if self.tokens[self.pos + 2] == '(':
            return self.parse_function_decl()
        else:
            return self.parse_variable_decl()

    def parse_variable_decl(self):
        var_type = self.parse_type()
        ident = self.tokens[self.pos]
        self.consume(ident)  # Consume identifier
        self.consume(';')  # Consume semicolon
        return ('VariableDecl', var_type, ident)

    def parse_type(self):
        if self.tokens[self.pos] in ['int', 'double', 'bool', 'string', 'void']:
            type_token = self.tokens[self.pos]
            self.consume(type_token)
            return type_token
        else:
            print(self.tokens[self.pos])
            raise SyntaxError(f"Unexpected token: '{self.tokens[self.pos]}'")

    def parse_function_decl(self):
        ret_type = self.parse_type()
        ident = self.tokens[self.pos]
        self.consume(ident)  # Consume identifier
        self.consume('(')
        formals = self.parse_formals()
        self.consume(')')
        stmt_block = self.parse_stmt_block()
        return ('FunctionDecl', ret_type, ident, formals, stmt_block)

    def parse_formals(self):
        formals = []
        while self.tokens[self.pos] in ['int', 'double', 'bool', 'string']:
            var_type = self.parse_type()
            ident = self.tokens[self.pos]
            self.consume(ident)  # Consume identifier
            formals.append(('Variable', var_type, ident))
            if self.tokens[self.pos] == ',':
                self.consume(',')
        return formals

    def parse_stmt_block(self):
        stmts = []
        self.consume('{')
        while self.tokens[self.pos] != '}':
            if self.tokens[self.pos] in ['int', 'double', 'bool', 'string']:
                stmts.append(self.parse_variable_decl())
            else:
                stmts.append(self.parse_stmt())
        self.consume('}')
        return ('StmtBlock', stmts)

    def parse_stmt(self):
        if self.tokens[self.pos] == 'if':
            return self.parse_if_stmt()
        elif self.tokens[self.pos] == 'while':
            return self.parse_while_stmt()
        elif self.tokens[self.pos] == 'for':
            return self.parse_for_stmt()
        elif self.tokens[self.pos] == 'return':
            return self.parse_return_stmt()
        elif self.tokens[self.pos] == 'break':
            return self.parse_break_stmt()
        elif self.tokens[self.pos] == 'Print':
            return self.parse_print_stmt()
        elif self.tokens[self.pos] == '{':
            return self.parse_stmt_block()
        else:
            expr = self.parse_expr()
            self.consume(';')
            return ('ExprStmt', expr)

    def parse_if_stmt(self):
        self.consume('if')
        self.consume('(')
        expr = self.parse_expr()
        self.consume(')')
        stmt = self.parse_stmt()
        if self.tokens[self.pos] == 'else':
            self.consume('else')
            else_stmt = self.parse_stmt()
            return ('IfStmt', expr, stmt, else_stmt)
        return ('IfStmt', expr, stmt)

    def parse_while_stmt(self):
        self.consume('while')
        self.consume('(')
        expr = self.parse_expr()
        self.consume(')')
        stmt = self.parse_stmt()
        return ('WhileStmt', expr, stmt)

    def parse_for_stmt(self):
        self.consume('for')
        self.consume('(')
        init_expr = self.parse_expr()
        if init_expr[1] != ";":
            self.consume(';')
            test_expr = self.parse_expr()
            self.consume(';')
            update_expr = self.parse_expr()
            self.consume(')')
            stmt = self.parse_stmt()
            return ('ForStmt', init_expr, test_expr, update_expr, stmt)
        else:
            test_expr = self.parse_expr()
            self.consume(';')
            update_expr = self.parse_expr()
            self.consume(')')
            stmt = self.parse_stmt()
            return ('ForStmt', init_expr, test_expr, update_expr, stmt)


    def parse_return_stmt(self):
        self.consume('return')
        if self.tokens[self.pos] != ';':
            expr = self.parse_expr()
            self.consume(';')
            return ('ReturnStmt', expr)
        self.consume(';')
        return ('ReturnStmt',)

    def parse_break_stmt(self):
        self.consume('break')
        self.consume(';')
        return ('BreakStmt',)

    def parse_print_stmt(self):
        self.consume('Print')
        self.consume('(')
        exprs = [self.parse_expr()]
        while self.tokens[self.pos] == ',':
            self.consume(',')
            exprs.append(self.parse_expr())
        self.consume(')')
        self.consume(';')
        return ('PrintStmt', exprs)
    
    def get_precedence(self, op):
        precedence_table = {
            '=': 1,
            '||': 2,
            '&&': 3,
            '==': 4, '!=': 4,
            '<': 5, '<=': 5, '>': 5, '>=': 5,
            '+': 6, '-': 6,
            '*': 7, '/': 7, '%': 7,
            '!':8,
        }
        return precedence_table.get(op, -1)

    def parse_expr(self, min_precedence=1):
        lhs = self.parse_primary_expr()
    
        while self.pos < len(self.tokens):
            op = self.tokens[self.pos]

            if op not in ('+', '-', '*', '/', '%', '<', '<=', '>', '>=', '==', '!=', '&&', '||', '='):
                break

            precedence = self.get_precedence(op)

            if precedence < min_precedence:
                break

            self.consume(op)

            rhs = self.parse_expr(precedence + 1)
            lhs = (op, lhs, rhs)

        return lhs

    def parse_primary_expr(self):
        if self.tokens[self.pos] in ['intConstant', 'doubleConstant', 'boolConstant', 'stringConstant', 'null']:
            return self.parse_constant()

        if self.tokens[self.pos] == '(':
            self.consume('(')
            expr = self.parse_expr()
            self.consume(')')
            return expr

        if self.tokens[self.pos] == '-':
            self.consume('-')
            expr = self.parse_expr(6)  # Preserving the precedence for unary minus
            return ('UnaryMinus', expr)

        if self.tokens[self.pos] == '!':
            self.consume('!')
            expr = self.parse_expr(6)  # Preserving the precedence for unary not
            return ('UnaryNot', expr)

        if self.tokens[self.pos] == 'ReadInteger':
            self.consume('ReadInteger')
            self.consume('(')
            self.consume(')')
            return ('ReadInteger',)

        if self.tokens[self.pos] == 'ReadLine':
            self.consume('ReadLine')
            self.consume('(')
            self.consume(')')
            return ('ReadLine',)

        if self.tokens[self.pos + 1] == '(':
            return self.parse_call()
        else:
            return self.parse_lvalue()

    def parse_lvalue(self):
        ident = self.tokens[self.pos]
        self.consume(ident)
        return ('LValue', ident)

    def parse_call(self):
        ident = self.tokens[self.pos]
        self.consume(ident)
        self.consume('(')
        actuals = self.parse_actuals()
        self.consume(')')
        return ('Call', ident, actuals)

    def parse_actuals(self):
        actuals = []
        if self.tokens[self.pos] != ')':
            actuals.append(self.parse_expr())
            while self.tokens[self.pos] == ',':
                self.consume(',')
                actuals.append(self.parse_expr())
        return actuals

    def parse_constant(self):
        token = self.tokens[self.pos]

        if token == 'null':
            self.consume('null')
            return ('Constant', None)

        if token == 'true' or token == 'false':
            value = True if token == 'true' else False
            self.consume(token)
            return ('Constant', value)

        # You may need to adjust this condition depending on the format of the intConstant and doubleConstant tokens
        if token.isdigit() or '.' in token:
            value = int(token) if token.isdigit() else float(token)
            self.consume(token)
            return ('Constant', value)

        if token[0] == '"' and token[-1] == '"':
            value = token[1:-1]
            self.consume(token)
            return ('Constant', value)

        raise SyntaxError(f"Unexpected token: {token}")

# Example usage
# tokens = ['int', 'x', ';', 'double', 'y', ';']  # Input as a list of tokens
# parser = Parser(tokens)
# result = parser.parse()
# print(result)

