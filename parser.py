import lexer as rawLexer
from parserClasses.py import *
import ply.yacc as yacc


class Parser():

    def __init__(self):

        self.lexer = rawLexer
        self.tokens = rawLexer.tokens

        self.parser = yacc.yacc(module=self, start='Program')

    def p_Program(self,p):
        """ Program : StatementList """
        p[0] = Program(p[1])

    def p_StatementList(self,p):
        """ StatementList : Statement
                          | StatemenList Statement """
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
        """ Declaration : IdentifierList Mode LBRACKET Initialization RBRACKET """
        p[0] = Declaration(p[1],p[2],p[4])

    def p_IdentifierList(self,p):
        """ IdentifierList : IdentifierList COMMA Identifier 
                           | Identifier """
        if(len(p) == 2):
            p[0] = IdentifierList([p[1]])
        else:
            p[0] = IdentifierList(p[1]._fields[0] + [p[2]])

    def p_Identifier(self,p):
        """ Identifier : ID """
        p[0] = p[1]

    def p_Mode(self,p):
        """ Mode :  ModeName """

        p[0] = Mode(p[1])
  
    def p_Initialization(self,p):
        """ Initialization : ATRIB Expression """
        p[0] = Initialization(p[2])
        
    def p_error(self, p):
            print("Systax error in input()")

    def parse(self, text):
        self.parser.parse(text,self.lexer)

a = Parser()
a.parse("dcl i int = 10;")

