from lexer import Lexer as LexerHandle
from parserClasses import *
import ply.yacc as yacc


class Parser():

    def __init__(self):
        self.lexerHandle = LexerHandle()
        self.lexer = self.lexerHandle.lexer
        self.tokens = self.lexerHandle.tokens
        self.parser = yacc.yacc(module=self, start='Program')
        self.ast = 0

    def p_Program(self,p):
        """ Program : StatementList """
        p[0] = Program(p[1])
        self.ast = AST(p[0])

    def p_StatementList(self,p):
        """ StatementList : Statement
                          | StatementList Statement """
        if(len(p) == 2):
            p[0] = StatementList([p[1]])
        else:
            p[0] = StatementList(p[1]._fields[0] + [p[2]])

    def p_Statement(self,p):
        """ Statement : DeclarationStatement """
        p[0] = Statement(p[1])

    def p_DeclarationStatement(self,p):
        """ DeclarationStatement : DCL DeclaratioList SEMICOLON """
        p[0] = DeclarationStatement(p[2])

    def p_DeclarationList(self,p):
        """DeclaratioList : DeclaratioList COMMA Declaration
                          | Declaration """
        if(len(p) == 2):
            p[0] = DeclaratioList([p[1]])
        else:
            p[0] = DeclaratioList(p[1]._fields[0] + [p[2]])

    def p_Declaration(self,p):
        """ Declaration : IdentifierList Mode 
                        | IdentifierList Mode Initialization  """
        if len(p) == 4:
            p[0] = Declaration(p[1],p[2],p[3])
        else:
            p[0] = Declaration(p[1],p[2])

    def p_IdentifierList(self,p):
        """ IdentifierList : IdentifierList COMMA Identifier 
                           | Identifier """
        if(len(p) == 2):
            p[0] = IdentifierList([p[1]])
        else:
            print(p[1].fields[0] + [p[3]])
            p[0] = IdentifierList(p[1].fields[0] + [p[3]])

    def p_Identifier(self,p):
        """ Identifier : ID """
        p[0] = p[1]

    #Simplified
    def p_Mode(self,p):
        """ Mode :  ID 
                 | DiscreteMode """

        p[0] = Mode(p[1])

    #Simplified
    def p_DiscreteMode(self,p):
        """DiscreteMode :  INT
                        |  BOOL
                        |  CHAR """
        p[0] = DiscreteMode(p[1])

    def p_Initialization(self,p):
        """ Initialization : ATRIB Expression """
        p[0] = Initialization(p[2])

    #Simplified
    def p_Expression(self,p):
        """ Expression : Operand0"""
        p[0] = Expression(p[1])

    def p_Operand0(self,p):
        """Operand0 : Operand1
                     | Operand0 Operator1 Operand1 """
        if len(p) == 2 :
            p[0] = Operand0(p[1])
        else:
            p[0] = Operand0(p[1],p[2],p[3])

    def p_Operand1(self,p):
        """ Operand1 : Operand2
                     | Operand1 Operator2 Operand2 """
        if len(p) == 2 :
            p[0] = Operand1(p[1])
        else:
            p[0] = Operand1(p[1],p[2],p[3])

    def p_Operand2(self,p):
        """ Operand2 : Operand3
                     | Operand2 MUL Operand3
                     | Operand2 DIV Operand3
                     | Operand2 MOD Operand3 """
        if len(p) == 2:
            p[0] = Operand2(p[1])
        else:
            p[0] = Operand2(p[1],p[2],p[3])

    def p_Operand3(self,p):
        """ Operand3 : MINUS Operand4
                     | NOT  Operand4
                     | ICONST """
        if len(p) == 2:
            p[0] = Operand3(p[1])
        else:
            p[0] = Operand3(p[1],p[2])

    #Simplified
    def p_Operand4(self,p):
        """ Operand4 : PrimitiveValue """
        p[0] = Operand4(p[1])

    #Simplified
    def p_PrimitiveValue(self,p):
        """ PrimitiveValue : Literal """
        p[0] = PrimitiveValue(p[1])

    def p_Literal(self,p):
        """ Literal : ICONST
                     | FALSE
                     | TRUE
                     | CHALIT
                     | NULL
                     | STR """
        p[0] = Literal(p[1])

    def p_Operator1(self,p):
        """Operator1 : RelationalOperator
                     | IN """
        p[0] = Operator1(p[1])

    def p_RelationalOperator(self,p):
        """ RelationalOperator : AND 
                               | OR 
                               | EQUAL 
                               | NEQUAL 
                               | MORETHEN 
                               | EQMORETHEN 
                               | LESSTHEN 
                               | EQLESSTHEN"""
        p[0] = RelationalOperator(p[1])

    def p_Operator2(self,p):
        """ Operator2 : PLUS
                      | STRCAT
                      | MINUS """
        p[0] = Operand2(p[1])

    def p_error(self, p):
            print("Systax error in input()")

    def parse(self, text):
        self.parser.parse(text)
        print(self.ast)


a = Parser()
a.parse("dcl i,j int = 10;")
a.ast.buildGraph()



