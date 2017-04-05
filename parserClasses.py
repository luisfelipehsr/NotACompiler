import pydot as dot
import uuid

class AST(object):
    

    def __init__(self, *args):
        self.fields = list(args)

    def removeChanel(self):
        while len(self.fields) == 1:
            print(self)
            aux = self.fields[0]
            if(isinstance(aux,AST)):
                self.fields = aux.fields
            else:
                return

        for n in self.fields:
            if isinstance(n,AST):
                n.removeChanel()

    def build(self,graph):
        #self.removeLists()
        myId = id(self)
        graph.add_node(dot.Node(myId,label = self.__class__.__name__))
        for n in self.fields:
            nId = id(n)
            if isinstance(n,AST):
                graph.add_node(dot.Node(nId, label=n.__class__.__name__))
                graph.add_edge(dot.Edge(myId,nId))
                n.build(graph)
            else:
                nId += + uuid.uuid4().int & (1<<64)-1
                graph.add_node(dot.Node(nId, label=str(n)))
                graph.add_edge(dot.Edge(myId, nId))

    def buildGraph(self):
        graph = dot.Dot(graph_type='graph')
        #self.removeChanel()
        self.build(graph)
        graph.write_png('ast.png')


class Program(AST):
    # <Program> ::= <StatementList>
    _fields = ['StatementList']


class StatementList(AST):
    # <StatementList> ::= <StatemenList> <Statement>
    #                  | <Statement>
    _fields = ['StatementList']


class Statement(AST):
    # <Statement> ::= <DeclarationStatement>
    #        | <SynonymStatement>
    #        | <NewModeStatement>
    #        | <ProcedureStatement>
    #        | <ActionStatement>
    _fields = ['Statement']


class DeclarationStatement(AST):
    # <DeclarationStatement> ::= DCL <DeclarationList> ;
    _fields = ['DeclarationList']


class DeclarationList(AST):
    # <DeclarationList> ::= <Declaration> , <DeclarationList>
    #                   | <Declaration>
    _fields = ['DeclarationList']


class Declaration(AST):
    # <Declaration> ::= <IdentifierList> <Mode> [ <Initialization> ]
    _fields = ['IdentifierList', 'Mode', 'Initialization']


class Initialization(AST):
    # <Initialization> ::= ATRIB <Expression>
    _fields = ['Expression']


class IdentifierList(AST):
    # <IdentifierList> ::= <IdentifierList> ,<Identifier>
    #                   | <Identifier>
    _fields = ['IdentifierList']


class Identifier(AST):
    # <Identifier> ::= ID
    _fields = ['Id']


class SynonymStatement(AST):
    # <SynonymStatement> ::= SYN <SynonymList> ;
    _fields = ['SynonymList']


class SynonymList(AST):
    # <SynonymList> ::= <SynonymDefinition> , <SynonymList>
    #                | <SynonymDefinition>
    _fields = ['synonymDefinition', 'synonymList']


class SynonymDefinition(AST):
    # <SynonymDefinition> ::= <IdentifierList> [ <Mode> ] = <ConstantExpression>
    _fields = ['IdentifierList', 'Mode', 'ConstantExpression']


class ConstantExpression(AST):
    # <ConstantExpression> ::= <expression>
    _fields = ['expression']


class NewModeStatement(AST):
    # <NewModeStatement> ::= TYPE <NewModeList> ;
    _fields = ['NewModeList']


class NewModeList(AST):
    # <NewModeList> ::= <ModeDefinition> , <NewModeList>
    #                | <ModeDefinition>
    _fields = ['ModeDefinition', 'NewModeList']


class ModeDefinition(AST):
    # <ModeDefinition> ::= <IdentifierList> = <Mode>
    _fields = ['IdentifierList', 'Mode']


class Mode(AST):
    # <Mode> ::=  <ModeName>
    #   | <DiscreteMode>
    #   | <ReferenceMode>
    #   | <CompositeMode>
    _fields = ['ModeName']


class DiscreteMode(AST):
    # <DiscreteMode> ::=  <IntegerMode>
    #            | <BooleanMode>
    #            | <CharacterMode>
    #            | <DiscreteRangeMode>
    _fields = ['integerMode']


class IntegerMode(AST):
    # <IntegerMode> ::=  INT
    _fields = ['int']


class BooleanMode(AST):
    # <BooleanMode> ::=  BOOL
    _fields = ['bool']


class CharacterMode(AST):
    # <CharacterMode> ::= CHAR
    _fields = ['Char']


class DiscreteRangeMode(AST):
    # <DiscreteRangeMode> ::= <DiscreteModeName> ( <LiteralRange> )
    #                  | <DiscreteMode> ( <LiteralRange> )
    _fields = ['DiscreteModeName', 'LiteralRange']


class ModeName(AST):
    # <ModeName> ::= <Identifier>
    _fields = ['Identifier']


class DiscreteModeName(AST):
    # <DiscreteModeName> ::= <Identifier>
    _fields = ['Identifier']


class LiteralRange(AST):
    # <LiteralRange> ::= <LowerBound> : <UpperBound>
    _fields = ['lowerBound', 'UpperBound']


class LowerBound(AST):
    # <LowerBound> ::= <Expression>
    _fields = ['Expression']


class UpperBound(AST):
    # <UpperBound> ::= <Expression>
    _fields = ['Expression']


class ReferenceMode(AST):
    # <ReferenceMode> ::= REF <Mode>
    _fields = ['Mode']


class CompositeMode(AST):
    # <CompositeMode> ::= <StringMode> | <ArrayMode>
    _fields = ['StringMode']


class StringMode(AST):
    # <StringMode> ::= CHARS LBRACKET <StringLength> RBRACKET
    _fields = ['Chars', 'StringLenght']


class StringLength(AST):
    # <StringLength> ::= <IntegerLiteral>
    _fields = ['IntegerLiteral']


class ArrayMode(AST):
    # <ArrayMode> ::= ARRAY LBRACKET <IndexModeList> RBRACKET <ElementMode>
    _fields = ['IndexModeList']


class IndexModeList(AST):
    # <IndexModeList> ::= <IndexMode> , <IndexModeList>
    #               | <IndexMode>
    _fields = ['IndexMode', 'IndexModeList']


class IndexMode(AST):
    # <IndexMode> ::= <DiscreteMode> | <LiteralRange>
    _fields = ['DiscreteMode']


class ElementMode(AST):
    # <ElementMode> ::= <mode>
    _fields = ['Mode']


class Location(AST):
    # <Location> ::=  <LocationName>
    #       | <DereferencedReference>
    #       | <StringElement>
    #       | <StringSlice>
    #       | <ArrayElement>
    #       | <ArraySlice>
    #       | <CallAction>
    _fields = ['LocationName']


class DereferencedReference(AST):
    # <DereferencedReference> ::= <Location> ARROW
    _fields = ['Location']


class StringElement(AST):
    # <StringElement> ::= <StringLocation> LBRACKET <StartElement> RBRACKET
    _fields = ['StringLocation', 'StartElement']


class StartElement(AST):
    # <StartElement> ::= <IntegerExpression>
    _fields = ['IntegerExpression']


class StringSlice(AST):
    # <StringSlice> ::= <StringLocation> LBRACKET <LeftElement> : <RightElement> RBRACKET
    _fields = ['StringLocation', 'LeftElement', 'RightElement']


class StringLocation(AST):
    # <StringLocation> ::= <Identifier>
    _fields = ['Identifier']


class LeftElement(AST):
    # <LeftElement> ::= <IntegerExpression>
    _fields = ['IntegerExpression']


class RightElement(AST):
    # <RightElement> ::= <IntegerExpression>
    _fields = ['IntegerExpression']


class ArrayElement(AST):
    # <ArrayElement> ::= <ArrayLocation> LBRACKET <ExpressionList> RBRACKET
    _fields = ['ArrayLocation', 'ExpressionList']


class ExpressionList(AST):
    # <ExpressionList> ::= <Expression> , <ExpressionList>
    #               | <Expression>
    _fields = ['Expression', 'ExpressionList']


class ArraySlice(AST):
    # <ArraySlice> ::= <ArrayLocation> LBRACKET <LowerBound> : <UpperBound> RBRACKET
    _fields = ['ArrayLocation', 'LowerBound', 'UpperBound']


class ArrayLocation(AST):
    # <ArrayLocation> ::= <Location>
    _fields = ['Location']


class PrimitiveValue(AST):
    # <primitive_value> ::=  <Literal>
    #              | <ValueArrayElement>
    #              | <ValueArraySlice>
    #              | <ParenthesizedExpression>
    _fields = ['Literal']


class Literal(AST):
    # <Literal> ::=  <IntegerLiteral>
    #     | <BooleanLiteral>
    #     | <CharacterLiteral>
    #     | <EmptyLiteral>
    #     | <CharacterStringLiteral>
    _fields = ['IntegerLiteral']


class IntegerLiteral(AST):
    # <IntegerLiteral> ::=  ICONST
    _fields = ['ICONST']


class BooleanLiteral(AST):
    # <BooleanLiteral> ::= FALSE | TRUE
    _fields = ['Bool']


class CharacterLiteral(AST):
    # <CharacterLiteral> ::=  CHALIT
    _fields = ['Chalit']


class EmptyLiteral(AST):
    # <EmptyLiteral> ::= NULL
    _fields = []


class CharacterStringLiteral(AST):
    # <CharacterStringLiteral> ::= STR
    _fields = ['STR']


class ValueArrayElement(AST):
    # <ValueArrayElement> ::= <ArrayPrimitiveValue> LBRACKET <ExpressionList> RBRACKET
    _fields = ['ArrayPrimitiveValue', 'ExpressionList']


class ValueArraySlice(AST):
    # <ValueArraySlice> ::= <ArrayPrimitiveValue> LBRACKET <LowerElement> : <UpperElement> RBRACKET
    _fields = ['ArrayPrimitiveValue', 'LowerElement', 'UpperElement']

#Substituido
class ArrayPrimitiveValue(AST):
    # <ArrayPrimitiveValue> ::= <PrimitiveValue>
    _fields = ['PrimitiveValue']


class ParenthesizedExpression(AST):
    # <ParenthesizedExpression> ::= ( <Expression> )
    _fields = ['Expression']


class Expression(AST):
    # <Expression> ::= <Operand0> | <ConditionalExpression>
    _fields = ['Operand0']


class ConditionalExpression(AST):
    # <ConditionalExpression> ::=  IF <BooleanExpression> <ThenExpression> <ElseExpression> FI
    #                     | IF <BooleanExpression> <ThenExpression> <ElsifExpression> <ElseExpression> FI
    _fields = ['BooleanExpression', 'ThenExpression', 'ElsifExpression',
               'ElseExpression']


class BooleanExpression(AST):
    # <BooleanExpression> ::= <Expression>
    _fields = ['Expression']


class ThenExpression(AST):
    # <ThenExpression> ::= THEN <Expression>
    _fields = ['Expression']


class ElseExpression(AST):
    # <ElseExpression> ::= ELSE <Expression>
    _fields = ['Expression']


class ElsifExpression(AST):
    # <ElsifExpression> ::=  ELSIF <BooleanExpression> <ThenExpression>
    #                | <ElsifExpression> ELSIF <BooleanExpression> <ThenExpression>
    _fields = ['ElsifExpression', 'BooleanExpression', 'ThenExpression']


class Operand0(AST):
    # <Operand0> ::=  <Operand1>
    #        | <Operand0> <Operator1> <Operand1>
    _fields = ['Operand0', 'Operator1', 'Operand1']


class Operator1(AST):
    # <Operator1> ::=  <RelationalOperator>
    #         | IN
    _fields = ['Operator']


class RelationalOperator(AST):
    # <RelationalOperator> ::=  AND | OR | EQUAL | NEQUAL | MORETHEN | EQMORETHEN | LESSTHEN | EQLESSTHEN
    _fields = ['RelationalOperator']

#Unused
class MembershipOperator(AST):
    # <MembershipOperator> ::= IN
    _fields = []


class Operand1(AST):
    # <Operand1> ::=  <Operand2>
    #        | <Operand1> <Operator2> <Operand2>
    _fields = ['Operand1', 'Operator2', 'Operand2']


class Operator2(AST):
    # <Operator2> ::=  PLUS
    #         | STRCAT
    #         | MINUS
    _fields = ['AddOperator']


class Operand2(AST):
    # <Operand2> ::=  <Operand3>
    #        | <Operand2> MUL <Operand3>
    #        | <Operand2> DIV <Operand3>
    #        | <Operand2> MOD <Operand3>
    _fields = ['Operand2', 'MultiOperation', 'Operand3']


# Duvida!!!
class Operand3(AST):
    # <Operand3> ::=  [ MINUS ] <Operand4>
    #        | [ NOT ] <Operand4>
    #        | <Integer_Literal>
    _fields = ['MonoOperation', 'Operand4']


class Operand4(AST):
    # <Operand4> ::=  <Location> | <ReferencedLocation> | <PrimitiveValue>
    _fields = ['Location']


class ReferencedLocation(AST):
    # <ReferencedLocation> ::= ARROW <Location>
    _fields = ['Location']


class ActionStatement(AST):
    # <ActionStatement> ::= [ ID: ] <Action> ;
    _fields = ['Id', 'Action']


class Action(AST):
    # <Action> ::=  <BracketedAction>
    #      | <AssignmentAction>
    #      | <CallAction>
    #      | <ExitAction>
    #      | <ReturnAction>
    #      | <ResultAction>
    _fields = ['Actions']


class BracketedAction(AST):
    # <BracketedAction> ::= <IfAction> | <DoAction>
    _fields = ['IfDoAction']


class AssignmentAction(AST):
    # <AssignmentAction> ::= <Location> <AssigningOperator> <Expression>
    _fields = ['Location', 'AssigningOperator', 'Expression']


class AssigningOperator(AST):
    # <AssigningOperator> ::= [ <ClosedDyadicOperator> ] <AssignmentSymbol>
    _fields = ['ClosedDyadicOperator', 'AssignmentSymbol']


class ClosedDyadicOperator(AST):
    # <ClosedDyadicOperator> ::= PLUS | MINUS | MUL | DIV | MOD | STRCAT
    _fields = ['ClosedDyadicOperator']


class IfAction(AST):
    # <IfAction> ::= IF <BooleanExpression> <ThenClause> [ <ElseClause> ] FI
    _fields = ['BooleanExpression', 'ThenClause', 'ElseClause']


class ActionStatementList(AST):
    # <ActionStatementList> ::= <ActionStatement> <ActionStatementList>
    #                   | <ActionStatement>
    _fields = ['ActionStatement', 'ActionStatementList']


class ThenClause(AST):
    # <ThenClause> ::= THEN <ActionStatementList>
    _fields = ['ActionStatementList']


class ElseClause(AST):
    # <ElseClause> ::=  ELSE <ActionStatementList>
    #           | ELSIF <BooleanExpression> <ThenClause> [ <ElseClause> ]
    _fields = ['BooleanExpression', 'ThenClause', 'ElseClause']


class DoAction(AST):
    # <DoAction> ::= DO [ <ControlPart> ; ] <ActionStatementList> OD
    _fields = ['ControlPart', 'ActionStatementList']


class ControlPart(AST):
    # <ControlPart> ::=  <ForControl> [ <WhileControl> ]
    #            | <WhileControl>
    _fields = ['ForControl', 'WhileControl']


class ForControl(AST):
    # <ForControl> ::= FOR <Iteration>
    _fields = ['Iteration']


class Iteration(AST):
    # <Iteration> ::= <StepEnumeration> | <RangeEnumeration>
    _fields = ['StepEnumeration']


class StepEnumeration(AST):
    # <StepEnumeration> ::=  <LoopCounter> <AssignmentSymbol> <StartValue> [ <StepValue> ] [ DOWN ] <EndValue>
    _fields = ['LoopCounter', 'AssignmentSymbol', 'StartValue', 'StepValue',
               'EndValue']


class LoopCounter(AST):
    # <LoopCounter> ::= ID
    _fields = ['Id']


class StartValue(AST):
    # <StartValue> ::= <DiscreteExpression>
    _fields = ['DiscreteExpression']


class StepValue(AST):
    # <StepValue> ::= BY <IntegerExpression>
    _fields = ['IntegerExpression']


class EndValue(AST):
    # <EndValue> ::= TO <DiscreteExpression>
    _fields = ['DiscreteExpression']


class DiscreteExpression(AST):
    # <DiscreteExpression> ::= <Expression>
    _fields = ['Expression']


class RangeEnumeration(AST):
    # <RangeEnumeration> ::= <LoopCounter> [ DOWN ] IN <DiscreteMode>
    _fields = ['LoopCounter', 'DiscreteMode']


class WhileControl(AST):
    # <WhileControl> ::= WHILE <BooleanExpression>
    _fields = ['BooleanExpression']


class CallAction(AST):
    # <CallAction> ::=  <ProcedureCall> | <BuiltinCall>
    _fields = ['ProcedureCall']


class ProcedureCall(AST):
    # <ProcedureCall> ::= <ProcedureName> ( [ <ParameterList> ] )
    _fields = ['ProcedureName', 'ParameterList']


class ParameterList(AST):
    # <ParameterList> ::= <Parameter> , <ParameterList>
    #                | <Parameter>
    _fields = ['Parameter', 'ParameterList']


class Parameter():
    # <Parameter> ::= <Expression>
    _fields = ['Expression']


class ProcedureName(AST):
    # <ProcedureName> ::= <Identifier>
    _fields = ['Identifier']


class ExitActiom(AST):
    # <ExitActiom> ::= EXIT ID
    _fields = ['Id']


class ReturnAction(AST):
    # <ReturnAction> ::= RETURN [ <Result> ]
    _fields = ['Result']


class ResultAction(AST):
    # <ResultAction> ::= RESULT <Result>
    _fields = ['Result']


class Result(AST):
    # <Result> ::= <Expression>
    _fields = ['Expression']


class BuiltinCall(AST):
    # <BuiltinCall> ::= <BuiltinName> ( [ <ParameterList> ] )
    _fields = ['BuiltinName', 'ParameterList']


class BuiltinName(AST):
    # <BuiltinName> ::= ABS | ASC | NUM | UPPER | LOWER | LENGTH | READ | PRINT
    _fields = ['BuiltinName']


class ProcedureStatement(AST):
    # <ProcedureStatement> ::= ID : <ProcedureDefinition> ;
    _fields = ['Id', 'ProcedureDefinition']


class ProcedureDefinition(AST):
    # <ProcedureDefinition> ::= PROC ( [ <FormalParameterList> ] ) [ <ResultSpec> ]; <StatementList> END
    _fields = ['FormalParameterList', 'ResultSpec', 'StatementList']


class FormalParameterList(AST):
    # <FormalParameterList> ::= <FormalParameter> , <FormalParameterList>
    #                        | <FormalParameter>
    _fields = ['FormalParameter', 'FormalParameterList']


class FormalParameter(AST):
    # <FormalParameter> ::= <IdentifierList> <ParameterSpec>
    _fields = ['IdentifierList', 'ParameterSpec']


class ParameterSpec(AST):
    # <ParameterSpec> ::=  <Mode> [ <ParameterAttribute> ]
    _fields = ['Mode', 'ParameterAttribute']


class ParameterAttribute(AST):
    # <ParameterAttribute> ::= LOC
    _fields = []


class ResultSpec(AST):
    # <ResultSpec> ::= RETURNS ( <Mode> [ <ResultAttribute> ] )
    _fields = ['Mode', 'ResultAttribute']


class ResultAttribute(AST):
    # <ResultAttribute>::= LOC
    _fields = []