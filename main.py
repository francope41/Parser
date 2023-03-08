# Programming Languages and Compilers
# Project 1, Phase II, Parser
# By Eulises Franco - 03/07/2023
#### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -####

# Import required libraries
import sys
import numpy as np
from utils import Parser

#### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -####


class SintaxAnalyzer:
    def __init__(self, arr_dir):
        arr_file = open("arr", "rb")

        self.tokens = np.load(arr_file)

        print(self.tokens)

        # precedence= (
        #     ('right')
        # )
        """Type of tokens:

        T_StringConstant
        T_Identifier
        T_DoubleConstant
        T_IntConstant

        """

    def p_Program(self, p):
        "Program : Decl+"
        print("Program")

    def p_Decl(self, p):
        "Decl : VariableDecl"
        print("Decl 1")

    def p_Decl2(self, p):
        "Decl : FunctionDecl"
        print("Decl 2")

    def p_VariableDecl(self, p):
        "VariableDecl : Variable ;"
        print("VariableDecl")

    def p_Variable(self, p):
        "Variable : Type ident"
        print("Variable")

    def p_Type(self, p):
        "Type : int"
        print("Type 1")

    def p_Type2(self, p):
        "Type : double"
        print("Type 2")

    def p_Type3(self, p):
        "Type : bool"
        print("Type 3")

    def p_Type4(self, p):
        "Type : string"
        print("Type 4")

    def p_FunctionDecl(self, p):
        "FunctionDecl : Type ident ( Formals ) StmtBlock"
        print("FunctionDecl 1")

    def p_FunctionDecl2(self, p):
        "FunctionDecl : void ident ( Formals ) StmtBlock"
        print("FunctionDecl 2")

    def p_Formals(self, p):
        "Formals : Variable+ ,"
        print("Formals 1")

    def p_FormalsEmpty(self, p):
        "Formals : empty"
        print("empty")

    def p_StmtBlock(self, p):
        "StmtBlock : { VariableDecl* Stmt* }"
        print("StmtBlock")

    def p_Stmt(self, p):
        "Stmt : Expr ;"
        print("Stmt 1")

    def p_Stmt2(self, p):
        "Stmt : IfStmt"
        print("Stmt 2")

    def p_Stmt3(self, p):
        "Stmt : WhileStmt"
        print("Stmt 3")

    def p_Stmt4(self, p):
        "Stmt : ForStmt"
        print("Stmt 4")

    def p_Stmt5(self, p):
        "Stmt : BreakStmt"
        print("Stmt 5")

    def p_Stmt6(self, p):
        "Stmt : ReturnStmt"
        print("Stmt 6")

    def p_Stmt7(self, p):
        "Stmt : PrintStmt"
        print("Stmt 7")

    def p_Stmt8(self, p):
        "Stmt : StmtBlock"
        print("Stmt 8")

    def p_IfStmt(self, p):
        "IfStmt : if ( Expr ) Stmt else Stmt"
        print("IfStmt")

    def p_WhileStmt(self, p):
        "WhileStmt : while ( Expr ) Stmt"
        print("WhileStmt")

    def p_ForStmt(self, p):
        "ForStmt : for ( Expr ; Expr ; Expr ) Stmt"
        print("ForStmt")

    def p_ReturnStmt(self, p):
        "ReturnStmt : return Expr ;"
        print("ReturnStmt")

    def p_BreakStmt(self, p):
        "BreakStmt : break ;"
        print("BreakStmt")

    def p_PrintStmt(self, p):
        "PrintStmt : Print ( Expr+ , ) ;"
        print("PrintStmt")

    def p_Expr(self, p):
        "Expr : LValue = Expr"
        print("Expr 1")

    def p_Expr2(self, p):
        "Expr : Constant"
        print("Expr 2")

    def p_Expr3(self, p):
        "Expr : LValue"
        print("Expr 3")

    def p_Expr4(self, p):
        "Expr : Call"
        print("Expr 4")

    def p_Expr5(self, p):
        "Expr : ( Expr )"
        print("Expr 5")

    def p_Expr6(self, p):
        "Expr : Expr + Expr"
        print("Expr 6")

    def p_Expr7(self, p):
        "Expr : Expr - Expr"
        print("Expr 7")

    def p_Expr8(self, p):
        "Expr : Expr * Expr"
        print("Expr 8")

    def p_Expr9(self, p):
        "Expr : Expr / Expr"
        print("Expr 9")

    def p_Expr10(self, p):
        "Expr : Expr % Expr"
        print("Expr 10")

    def p_Expr11(self, p):
        "Expr : - Expr"
        print("Expr 11")

    def p_Expr12(self, p):
        "Expr : Expr < Expr"
        print("Expr 12")

    def p_Expr13(self, p):
        "Expr : Expr <= Expr"
        print("Expr 13")

    def p_Expr14(self, p):
        "Expr : Expr > Expr"
        print("Expr 14")

    def p_Expr15(self, p):
        "Expr : Expr >= Expr"
        print("Expr 15")

    def p_Expr16(self, p):
        "Expr : Expr == Expr"
        print("Expr 16")

    def p_Expr17(self, p):
        "Expr : Expr ! = Expr"
        print("Expr 17")

    def p_Expr18(self, p):
        "Expr : Expr && Expr"
        print("Expr 18")

    def p_Expr19(self, p):
        "Expr : Expr || Expr"
        print("Expr 19")

    def p_Expr20(self, p):
        "Expr : ! Expr"
        print("Expr 20")

    def p_Expr21(self, p):
        "Expr : ReadInteger ( )"
        print("Expr 21")

    def p_Expr22(self, p):
        "Expr : ReadLine ( )"
        print("Expr 22")

    def p_LValue(self, p):
        "LValue : ident"
        print("LValue")

    def p_Call(self, p):
        "Call : ident ( Actuals )"
        print("Call")

    def p_Actuals(self, p):
        "Actuals : Expr+ ,"
        print("Actuals 1")

    def p_ActualsEmpty(self, p):
        "Actuals : empty"
        print("empty")

    def p_Constant(self, p):
        "Constant : intConstant"
        print("Constant 1")

    def p_Constant2(self, p):
        "Constant : doubleConstant"
        print("Constant 2")

    def p_Constant3(self, p):
        "Constant : boolConstant"
        print("Constant 3")

    def p_Constant4(self, p):
        "Constant : stringConstant"
        print("Constant 4")

    def p_Constant5(self, p):
        "Constant : null"
        print("Constant 5")

    def p_empty(self, p):
        "empty :"
        pass

    def p_error(self, p):
        print("Syntax Error", p)
        print("error in line" + str(p.lineno))



SintaxAnalyzer(sys.argv[1])