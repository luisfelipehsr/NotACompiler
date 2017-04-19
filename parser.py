from lexer import Lexer as LexerHandle
from parserClasses import *
import ply.yacc as yacc


class Parser:

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
        if len(p) == 2:
            p[0] = StatementList(p[1])
        else:
            p[0] = StatementList()
            p[0].fields = p[1].fields + list(p[2])

    def p_Statement(self,p):
        """ Statement : DeclarationStatement
                      | SynonymStatement """
        p[0] = Statement(p[1])

    def p_DeclarationStatement(self,p):
        """ DeclarationStatement : DCL DeclarationList SEMICOLON """
        p[0] = DeclarationStatement(p[2])

    def p_DeclarationList(self,p):
        """DeclarationList : DeclarationList COMMA Declaration
                          | Declaration """
        if(len(p) == 2):
            p[0] = DeclarationList(p[1])
        else:
            p[0] = DeclarationList()
            p[0].fields = p[1].fields + list(p[3])

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
        if len(p) == 2:
            p[0] = IdentifierList(p[1])
        else:
            p[0] = IdentifierList()
            p[0].fields = p[1].fields + list(p[3])

    def p_Identifier(self,p):
        """ Identifier : ID """
        p[0] = p[1]
        

    def p_SynonymStatement(self,p):
        """ SynonymStatement : SYN SynonymList """

        p[0] = SynonymStatement(p[2])


    def p_SynonymList(self,p):
        """ SynonymList : SynonymDefinition SynonymList
                        | SynonymDefinition """

        if len(p) == 2:
            p[0] = SynonymList(p[1])

        else:
            p[0] = SynonymList()
            p[0].fields = list(p[1]) + p[2].fields

    def p_SynonymDefinition(self,p):
        """ SynonymDefinition : IdentifierList Mode EQUAL Expression
                              | IdentifierList EQUAL Expression """
        if len(p) == 4:
            p[0] = SynonymDefinition(p[1], None, p[3])
        else:
            p[0] = SynonymDefinition(p[1], p[2], p[4])

    # TODO Expand
    def p_Mode(self,p):
        """ Mode :  ID 
                 | DiscreteMode
                 | ReferenceMode """

        p[0] = Mode(p[1])

    def p_ReferenceMode(self, p):
        """ ReferenceMode : REF Mode """

        p[0] = ReferenceMode(p[2])



    # TODO Expand
    def p_DiscreteMode(self,p):
        """DiscreteMode :  INT
                        |  BOOL
                        |  CHAR """
        p[0] = DiscreteMode(p[1])

    def p_Initialization(self,p):
        """ Initialization : ATRIB Expression 
                           | PLUS ATRIB Expression
                           | MINUS ATRIB Expression
                           | STRCAT ATRIB Expression
                           | MUL ATRIB Expression
                           | DIV ATRIB Expression
                           | MOD ATRIB Expression"""
        if len(p) == 3:
            p[0] = Initialization(p[2])
        else:
            p[0] = Initialization(p[1],p[3])

    def p_Expression(self,p):
        """ Expression : Operand0
                       | ConditionalExpression """
        p[0] = Expression(p[1])

    def p_ConditionalExpression(self,p):
        # Boolean Expression == Expression
        """ ConditionalExpression : IF Expression ThenExpression ElseExpression FI
                                  | IF Expression ThenExpression ElsifExpression ElseExpression FI """
        if len(p) == 6:
            p[0] = ConditionalExpression(p[2],p[3],p[4])
        else:
            p[0] = ConditionalExpression(p[2], p[3], p[4],p[5])

    def p_ThenExpression(self,p):
        """ ThenExpression : THEN Expression """
        p[0] = ThenExpression(p[2])

    def p_ElseExpression(self,p):
        """ ElseExpression : ELSE Expression """
        p[0] = ElseExpression(p[2])

    def p_ElsifExpression(self,p):
        #Boolean Expression == Expression
        """ ElsifExpression : ELSIF Expression ThenExpression
                            | ElsifExpression ELSIF Expression ThenExpression """
        if len(p) == 4:
            p[0] = ElsifExpression(p[2],p[3])
        else:
            p[0] = ElsifExpression(p[1],p[3],p[4])

    def p_ExpressionList(self,p):
        """ ExpressionList : ExpressionList COMMA Expression 
                           | Expression"""
        if len(p) == 2:
            p[0] = ExpressionList(p[1])
        else:
            p[0] = ExpressionList
            p[0].fields = p[1].fields + list(p[3])

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
                     | Operand4 """
        if len(p) == 2:
            p[0] = Operand3(p[1])
        else:
            p[0] = Operand3(p[1],p[2])

    def p_Operand4(self,p):
        """ Operand4 : PrimitiveValue 
                     | Location 
                     | ReferencedLocation"""
        p[0] = Operand4(p[1])

    def p_ReferencedLocation(self,p):
        """ReferencedLocation : ARROW Location"""
        p[0] = ReferencedLocation(p[2])

    def p_PrimitiveValue(self,p):
        """ PrimitiveValue : Literal 
                           | ValueArrayElement
                           | ValueArraySlice
                           | LPAREN Expression RPAREN """
        p[0] = PrimitiveValue(p[1])

    def p_ValueArrayElement(self,p):
        """ ValueArrayElement : PrimitiveValue LPAREN ExpressionList RPAREN """
        p[0] = ValueArrayElement(p[1],p[3])

    def p_ValueArraySlice(self, p):
        """ ValueArraySlice : PrimitiveValue LBRACKET Operand1 COLON Operand1 RBRACKET"""
        p[0] = ValueArraySlice(p[1], p[3], p[4])

    def p_Location(self,p):
        """ Location : ID 
                     | DereferencedReference
                     | ArrayElement
                     | StringElement
                     | StringSlice
                     | ArraySlice
                     | CallAction """
        p[0] = Location(p[1])


    def p_DereferencedReference(self,p):
        """ DereferencedReference : Location ARROW """

        p[0] = DereferencedReference(p[1])


    def p_StringElement(self,p):
        """ StringElement : ID LBRACKET Operand1"""

        p[0] = StringElement(p[1],p[3])

    def p_StringSlice(self,p):
        """ StringSlice : ID LBRACKET Operand1 COLON Operand1"""
        p[0] = StringSlice(p[1],p[3],p[5])

    def p_ArrayElement(self,p):
        """ ArrayElement : Location LBRACKET ExpressionList"""
        p[0] = ArrayElement(p[1],p[3])


    def p_ArraySlice(self,p):
        """ ArraySlice : Location LBRACKET Operand1 COLON Operand1"""
        p[0] = ArraySlice(p[1],p[3],p[5])

    def p_CallAction(self,p):
        """ CallAction :  ProcedureCall 
                        | BuiltinCall"""
        p[0] = CallAction(p[1])

    def p_ProcedureCall(self,p):
        # ExpressionList === ParameterList
        """ ProcedureCall : ID LPAREN RPAREN
                          | ID LPAREN ExpressionList RPAREN"""
        if len(p) == 4:
            p[0] = ProcedureCall(p[1])
        else:
            p[0] = ProcedureCall(p[1],p[3])

    def p_BuilinCall(self,p):
        #ParameterList === ExpressionList
        """ BuiltinCall : BuiltinName LPAREN RPAREN
                        | BuiltinName LPAREN ExpressionList RPAREN"""
        if len(p) == 4:
            p[0] = BuiltinCall(p[1])
        else:
            p[0] = BuiltinCall(p[1],p[3])

    def p_BuiltinName(self,p):
        """ BuiltinName : ABS 
                        | ASC 
                        | NUM 
                        | UPPER 
                        | LOWER 
                        | LENGHT 
                        | READ 
                        | PRINT """
        p[0] = BuiltinName(p[1])

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



a = Parser()
a.parse("dcl i int = 10*i ;")
# a.ast.buildGraph()



