from lexer import Lexer as LexerHandle
from parserClasses import *
import ply.yacc as yacc
from os import walk
from Semantocer import Context



class Parser(object):


    def __init__(self):
        self.lexerHandle = LexerHandle()
        self.lexer = self.lexerHandle.lexer
        self.tokens = self.lexerHandle.tokens
        self.parser = yacc.yacc(module=self, start='Program',debug=True)
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
            p[0].fields = p[1].fields + [p[2]]

    def p_Statement(self,p):
        """ Statement : DeclarationStatement
                      | SynonymStatement 
                      | NewModeStatement
                      | ProcedureStatement 
                      | ActionStatement """
        p[0] = Statement(p[1])

    def p_ActionStatement(self,p):
        """ ActionStatement : Action SEMICOLON
                            | ID COLON Action SEMICOLON"""
        if len(p) == 3:
            p[0] = ActionStatement(p[1])
        else:
            p[0] = ActionStatement(p[1],p[3])

    def p_Action(self,p):
        """Action : BracketedAction
                  | AssignmentAction
                  | CallAction
                  | ExitAction
                  | ReturnAction
                  | ResultAction """
        p[0] = Action(p[1])

    def p_AssignmentAction(self,p):
        """ AssignmentAction : Location ATRIB Expression 
                             | Location PLUS ATRIB Expression
                             | Location MINUS ATRIB Expression
                             | Location MUL ATRIB Expression
                             | Location DIV ATRIB Expression
                             | Location MOD ATRIB Expression
                             | Location STRCAT ATRIB Expression"""
        if len(p) == 4:
            p[0] = AssignmentAction(p[1],p[3])
        else:
            p[0] = AssignmentAction(p[1],p[2],p[4])

    def p_ExitAction(self,p):
        """ ExitAction : EXIT ID """
        p[0] = ExitAction(p[2])

    def p_ReturnAction(self,p):
        """ReturnAction : RETURN 
                        | RETURN Expression """
        if len(p) == 2:
            p[0] = ReturnAction()
        else:
            p[0] = ReturnAction(p[2])

    def p_BracketedAction(self,p):
        """ BracketedAction : IfAction 
                            | DoAction """
        p[0] = BracketedAction(p[1])

    def p_ResultAction(self,p):
        """ResultAction : RESULT Expression"""
        p[0] = ResultAction(p[2])

    def p_ControlPart(self,p):
        """ ControlPart : ForControl 
                        | ForControl WhileControl    
                        | WhileControl """
        if isinstance(p[1],ForControl):
            if len(p) == 2:
                p[0] = ControlPart(p[1])
            else:
                p[0] = ControlPart(p[1],p[2])
        else:
            p[0] = ControlPart(p[1])

    def p_ForControl(self,p):
        """ ForControl : FOR Iteration"""
        p[0] = ForControl(p[2])

    def p_Iteration(self,p):
        """Iteration : StepEnumeration 
                     | RangeEnumeration"""
        p[0] = Iteration(p[1])

    def p_StepEnumeration(self,p):
        """ StepEnumeration :  ID ATRIB Operand0 TO Operand0
                            |  ID ATRIB Operand0 BY Operand1 TO Operand0
                            |  ID ATRIB Operand0 DOWN TO Operand0
                            |  ID ATRIB Operand0 BY Operand1 DOWN TO Operand0 """
        if len(p) == 6:
            p[0] = StepEnumeration(p[1],p[3],p[5])
        elif len(p) == 7:
            p[0] = StepEnumeration(p[1],p[3],p[4],p[6])
        elif len(p) == 8:
            p[0] = StepEnumeration(p[1],p[3],p[5],p[7])
        else:
            p[0] = StepEnumeration(p[1],p[3],p[5],p[6],p[8])

    def p_RangeEnumeration(self,p):
        """ RangeEnumeration : ID IN DiscreteMode 
                             | ID DOWN IN DiscreteMode"""
        if len(p) == 4:
            p[0] = RangeEnumeration(p[1],p[3])
        else:
            p[0] = RangeEnumeration(p[1],p[2],p[4])

    def p_WhileControl(self,p):
        """ WhileControl : WHILE Operand0 """
        p[0] = WhileControl(p[2])

    def p_DoAction(self,p):
        """DoAction : DO ActionStatementList OD
                    | DO ControlPart SEMICOLON  ActionStatementList OD"""
        if len(p) == 4:
            p[0] = DoAction(p[2])
        else:
            p[0] = DoAction(p[2],p[4])

    def p_IfAction(self,p):
        """ IfAction : IF Operand0 ThenClause FI
                     | IF Operand0 ThenClause ElseClause FI"""
        if len(p) == 5:
            p[0] = IfAction(p[2],p[3])
        else:
            p[0] = IfAction(p[2],p[3],p[4])

    def p_ThenClause(self,p):
        """ ThenClause : THEN ActionStatementList """
        p[0] = ThenClause(p[2])

    def p_ActionStatementList(self,p):
        """ActionStatementList : ActionStatementList ActionStatement 
                               | ActionStatement """

        if len(p) == 2:
            p[0] = ActionStatementList(p[1])
        else:
            p[0] = ActionStatementList()
            p[0].fields = p[1].fields + [p[2]]

    def p_ProcedureStatement(self,p):
        """ ProcedureStatement : ID COLON ProcedureDefinition SEMICOLON """
        p[0] = ProcedureStatement(p[1],p[3])

    def p_ElseClause(self,p):
        """ ElseClause : ELSE ActionStatementList
                       | ELSIF Operand0 ThenClause
                       | ELSIF Operand0 ThenClause ElseClause """
        if len(p) == 3:
            p[0] = ElseClause(p[2])
        elif len(p) == 4:
            p[0] = ElseClause(p[2],p[3])
        else:
            p[0] = ElseClause(p[2],p[3],p[4])

    def p_ProcedureDefinition(self,p):
        """ ProcedureDefinition : PROC LPAREN RPAREN SEMICOLON StatementList END
                                | PROC LPAREN RPAREN ResultSpec SEMICOLON StatementList END
                                | PROC LPAREN FormalParameterList RPAREN SEMICOLON StatementList END
                                | PROC LPAREN FormalParameterList RPAREN ResultSpec SEMICOLON StatementList END"""

        if len(p) == 7:
            p[0] = ProcedureDefinition(p[5])
        elif len(p) == 8:
            if isinstance(p[3],FormalParameterList) :
                p[0] = ProcedureDefinition(p[3],p[6])
            else:
                p[0] = ProcedureDefinition(p[4],p[6])
        else:
            p[0] = ProcedureDefinition(p[3],p[5],p[7])

    def p_ResultSpec(self,p):
        """ ResultSpec : RETURNS LPAREN Mode RPAREN 
                       | RETURNS LPAREN Mode LOC RPAREN """
        p[0] = ResultSpec(p[3])

    def p_FormalParameterList(self,p):
        """ FormalParameterList : FormalParameterList COMMA FormalParameter  
                                | FormalParameter """
        if len(p) == 2:
            p[0] = FormalParameterList(p[1])
        else:
            p[0] = FormalParameterList()
            p[0].fields = p[1].fields + [p[3]]

    def p_FormalParameter(self,p):
        """ FormalParameter : IdentifierList ParameterSpec """
        p[0] = FormalParameter(p[1],p[2])

    def p_ParameterSpec(self,p):
        """ ParameterSpec : Mode 
                          | Mode LOC """
        p[0] = ParameterSpec(p[1])

    def p_NewModeStatement(self,p):
        """ NewModeStatement : TYPE NewModeList """
        p[0] = NewModeStatement(p[2])

    def p_NewModeList(self,p):
        """ NewModeList : ModeDefinition COMMA NewModeList
                        | ModeDefinition """
        if len(p) == 2:
            p[0] = NewModeList(p[1])
        else:
            p[0] = NewModeList()
            p[0].fields = p[1].fields + [p[2]]

    def p_ModeDefinition(self,p):
        """ ModeDefinition : IdentifierList ATRIB Mode"""
        p[0] = ModeDefinition(p[1],p[3])

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
            p[0].fields = p[1].fields + [p[3]]

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
            p[0].fields = p[1].fields + [p[3]]

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
            p[0].fields = [p[1]] + p[2].fields

    def p_SynonymDefinition(self,p):
        """ SynonymDefinition : IdentifierList ATRIB Expression
                              | IdentifierList Mode ATRIB Expression """
        if len(p) == 4:
            p[0] = SynonymDefinition(p[1],p[3])
        else:
            p[0] = SynonymDefinition(p[1], p[2], p[4])

    def p_Mode(self,p):
        """ Mode :  ID 
                 | CompositeMode
                 | DiscreteMode
                 | ReferenceMode """

        p[0] = Mode(p[1])

    def p_CompositeMode(self,p):
        """ CompositeMode : StringMode
                          | ArrayMode """
        p[0] = CompositeMode(p[1])

    def p_StringMode(self,p):
        """ StringMode ::= CHARS LBRACKET ICONST RBRACKET """
        p[0] = StringMode(p[3])

    def p_ArrayMode(self,p):
        #ElementMode == Mode
        """ ArrayMode : ARRAY LBRACKET IndexModeList RBRACKET Mode """
        p[0] = ArrayMode(p[3],p[5])

    def p_ReferenceMode(self,p):
        """ ReferenceMode : REF Mode """
        p[0] = ReferenceMode(p[2])

    def p_DiscreteMode(self,p):
        """DiscreteMode : INT
                        | BOOL
                        | CHAR 
                        | DiscreteRangeMode"""
        p[0] = DiscreteMode(p[1])

    def p_IndexModeList(self,p):
        """ IndexModeList : IndexMode COMMA IndexModeList
                        | IndexMode"""
        if len(p) == 2:
            p[0] = IndexModeList(p[1])
        else:
            p[0] = IndexModeList()
            p[0].fields = p[1].fields + [p[2]]

    def p_IndexMode(self,p):
        """ IndexMode  : DiscreteMode 
                       | LiteralRange """
        p[0] = IndexMode(p[1])

    def p_DiscreteRangeMode(self,p):
        #DiscreteModeName == ID
        """ DiscreteRangeMode : ID LPAREN LiteralRange RPAREN
                              | DiscreteMode LPAREN LiteralRange RPAREN """
        p[0] = DiscreteRangeMode(p[1],p[3])

    def p_LiteralRange(self,p):
        """ LiteralRange : Operand1 COLON Operand1 """
        p[0] = LiteralRange(p[1],p[3])

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
            p[0] = ExpressionList()
            p[0].fields = p[1].fields + [p[3]]

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
                     | StringElement
                     | StringSlice
                     | ArrayElement
                     | ArraySlice
                     | CallAction """
        p[0] = Location(p[1])

    def p_DereferencedReference(self,p):
        """ DereferencedReference : Location ARROW """

        p[0] = DereferencedReference(p[1])

    def p_StringElement(self,p):
        """ StringElement : ID LBRACKET Operand1 RBRACKET"""

        p[0] = StringElement(p[1],p[3])

    def p_StringSlice(self,p):
        """ StringSlice : ID LBRACKET Operand1 COLON Operand1 RBRACKET"""
        p[0] = StringSlice(p[1],p[3],p[5])

    def p_ArrayElement(self,p):
        """ ArrayElement : Location LBRACKET ExpressionList RBRACKET """
        p[0] = ArrayElement(p[1],p[3])

    def p_ArraySlice(self,p):
        """ ArraySlice : Location LBRACKET Operand1 COLON Operand1 RBRACKET """
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

    def p_BuiltinCall(self,p):
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
            print("Systax error in input(%s) at line (%s)" %(p,p.lexer.lineno))
            self.parser.errok()

    def parse(self, text):
        self.parser.parse(text)



def main():
    a = Parser()
    tstList = ['Example1.lya','Example2.lya']
    for f in tstList:
        print(f)
        file = open(f,'r')
        AST.context = Context()
        a.parse(file.read())
        #a.ast.buildGraph(f)
        a.ast.recursiveTypeCheck()


if __name__ == '__main__':main()



