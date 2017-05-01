import pydot as dot
import uuid




class AST(object):
    
    def __init__(self, *args):
        self.fields = list(args)
        self.type = []
        #self.line = line

    def removeChanel(self):
        while len(self.fields) == 1:
            aux = self.fields[0]
            if(isinstance(aux,AST)):
                self.fields = aux.fields
            else:
                return

        for n in self.fields:
            if isinstance(n,AST):
                n.removeChanel()

    def build(self,graph):
        #print(self.__class__.__name__)
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
                nId += uuid.uuid4().int & (1<<64)-1
                graph.add_node(dot.Node(nId, label=str(n)))
                graph.add_edge(dot.Edge(myId, nId))

    def buildGraph(self,name):
        graph = dot.Dot(graph_type='graph')
        #self.removeChanel()
        self.build(graph)
        with open(name+'.dot','w') as textFile:
            textFile.write(graph.to_string())
        graph.write_png(name +'.png')

    def typeCheck(self):
        return True

    def propType(self):
        return

    def permTypes(self,types,slice):
        for type,element in types,slice:
            if element.type == type:
                return True
        else:
            return False

    def areEquals(self,sliceA,sliceB):
        for a,b in sliceA,sliceB:
            if a.type != b.type:
                return False
        return True


class Program(AST):
    # <Program> ::= <StatementList>
    _fields = ['StatementList']

class StatementList(AST):
    # <StatementList> ::= <Statement>
    #                  | <StatemenList> <Statement>
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

#Typed
class Declaration(AST):
    # <Declaration> ::= <IdentifierList> <Mode> [ <Initialization> ]
    _fields = ['IdentifierList', 'Mode', 'Initialization']

    def typeCheck(self):
        if len(self.fields) == 3:
            return self.fields[1].type == self.fields[2]
        else:
            return True

    def propType(self):
        self.type = fields[1].type[:]

#Typed
class Initialization(AST):
    def propType(self):
        self.type = self.fields[:-1].type[:]

class IdentifierList(AST):
    # <IdentifierList> ::= <IdentifierList> ,<Identifier>
    #                   | <Identifier>
    _fields = ['IdentifierList']

class SynonymStatement(AST):
    # <SynonymStatement> ::= SYN <SynonymList> ;
    _fields = ['SynonymList']

class SynonymList(AST):
    # <SynonymList> ::= <SynonymDefinition> , <SynonymList>
    #                | <SynonymDefinition>
    _fields = ['synonymDefinition', 'synonymList']

#Typed
class SynonymDefinition(AST):
    # <SynonymDefinition> ::= <IdentifierList> [ <Mode> ] = <ConstantExpression>
    def typeCheck(self):
        if len(self.fields) == 3:
            return self.fields[1].type == self.fields[2].type
        else:
            return True

    def propType(self):
        self.type = self.fields[:-1].type[:]

class NewModeStatement(AST):
    # <NewModeStatement> ::= TYPE <NewModeList>
    _fields = ['NewModeList']

class NewModeList(AST):
    # <NewModeList> ::= <ModeDefinition> , <NewModeList>
    #                | <ModeDefinition>

    _fields = ['ModeDefinition', 'NewModeList']

#Typed
class ModeDefinition(AST):
    # <ModeDefinition> ::= <IdentifierList> = <Mode>

    def propType(self):
        self.type = self.fields[1]
    _fields = ['IdentifierList', 'Mode']

#Typed
class Mode(AST):
    # <Mode> ::=  <ModeName>
    #   | <DiscreteMode>
    #   | <ReferenceMode>
    #   | <CompositeMode>

    def propType(self):
        self.type = self.fields[0].type
    _fields = ['ModeName']

#Typed
class DiscreteMode(AST):
    # <DiscreteMode> ::=  <IntegerMode>
    #            | <BooleanMode>
    #            | <CharacterMode>
    #            | <DiscreteRangeMode>

    def propType(self):
        #Se não for instancia de AST estamos em uma folha
        if not isIsntance(self.fields[0],AST):
            self.type = [str(self.fields[0])]
        #Se for pegamos o tipo vindo de DiscreteRange
        else:
            self.type = self.fields[0].type[:]

#Typed
#TODO
class DiscreteRangeMode(AST):
    # <DiscreteRangeMode> ::= <DiscreteModeName> ( <LiteralRange> )
    #                  | <DiscreteMode> ( <LiteralRange> )


    def propType(self):
        #Prefixo
        self.type = ['discreterange']
        # Se não for instancia de AST o tipo é definido por um ID
        if not isInstance(self.fields[0],AST):
            self.type += str(self.fields[0])
        #Se for pegamos o tipo do modo
        else:
            self.type += self.fields[0].type[:]

#Typed
class LiteralRange(AST):
    # <LiteralRange> ::= <LowerBound> : <UpperBound>

    def typeCheck(self):
        return self.fields[0].type == self.fields[1].type and self.fields[0].type == 'int'
    _fields = ['lowerBound', 'UpperBound']

#Typed
class ReferenceMode(AST):
    # <ReferenceMode> ::= REF <Mode>
    def propType(self):
        # Take type from mode and add prefix ref
        self.type = ['ref']+self.fields[0].type[:]
    _fields = ['Mode']

#Typed
class CompositeMode(AST):
    # <CompositeMode> ::= <StringMode> | <ArrayMode>
    def propType(self):
        # Get the type from ArrayMode or StringMode
        self.type = self.fields[0].type[:]
    _fields = ['StringMode']

#Typed
class StringMode(AST):
    # <StringMode> ::= CHARS LBRACKET <StringLength> RBRACKET
    def propType(self):
        self.type = ['chars']
    #No typecheck needed, lenght is Iconst
    _fields = ['Chars', 'StringLenght']

#Typed
class ArrayMode(AST):
    # <ArrayMode> ::= ARRAY LBRACKET <IndexModeList> RBRACKET <ElementMode>
    # Pegamos o tipo do element mode e adicionamos o prefixo array
    def propType(self):
        self.type = ['array'] + self.fields[1].type[:]

    _fields = ['IndexModeList']

class IndexModeList(AST):
    # <IndexModeList> ::= <IndexMode> , <IndexModeList>
    #               | <IndexMode>
    _fields = ['IndexMode', 'IndexModeList']

#Typed
#Duvida!
class IndexMode(AST):
    # <IndexMode> ::= <DiscreteMode> | <LiteralRange>
    def typeCheck(self):
        return isIstance(self.fields[0],LiteralRange) or (self.fields[0].type is 'int','discreterange_int')

    def propType(self):
        self.type = self.fields[0].type[:]

    _fields = ['DiscreteMode']

#Typed
class Location(AST):
    # <Location> ::=  <LocationName>
    #       | <DereferencedReference>
    #       | <StringElement>
    #       | <StringSlice>
    #       | <ArrayElement>
    #       | <ArraySlice>
    #       | <CallAction>

    def propType(self):
        self.type = self.fields[0].type[:]
    _fields = ['LocationName']

#Typed
class DereferencedReference(AST):
    # <DereferencedReference> ::= <Location> ARROW

    def  typeCheck(self):
        return self.fields[0].type[0] == 'ref'

    def propType(self):
        self.type = self.fields[0].type[1:]
    _fields = ['Location']

#Typed
class StringElement(AST):
    # <StringElement> ::= <StringLocation> LBRACKET <StartElement> RBRACKET
    def typeCheck(self):
        return self.fields[0].type == ['chars']
    def propType(self):
        self.type = ['char']
    _fields = ['StringLocation', 'StartElement']

#Typed
class StringSlice(AST):
    # <StringSlice> ::= <StringLocation> LBRACKET <LeftElement> : <RightElement> RBRACKET
    _fields = ['StringLocation', 'LeftElement', 'RightElement']

    def typeCheck(self):
        return self.fields[0].type == ['chars'] and self.fields[1].type == ['int'] and self.fields[2].type == ['int']

    def propType(self):
        self.type = self.fields[0].type[:]

#Typed
class ArrayElement(AST):

    # <ArrayElement> ::= <ArrayLocation> LBRACKET <ExpressionList> RBRACKET

    def typeCheck(self):
        return self.fields[1].type == ['int'] and self.fields[0].type[0] == 'array'

    # Se tivermos so uma expressão retornamos o valor nao um array
    def propType(self):
        if len(self.fields[1].fields) == 1:
            self.type = self.fields[0].type[1:]
        else:
            self.type = self.fields[0].type[:]
    _fields = ['ArrayLocation', 'ExpressionList']

#Typed
class ExpressionList(AST):
    # <ExpressionList> ::= <Expression> , <ExpressionList>
    #               | <Expression>
    def propType(self):
        type = self.fields[0].type[:]
        for t in self.fields:
            if type != t.type:
                self.type =  None
                return
        self.type = type

    _fields = ['Expression', 'ExpressionList']

#Typed
class ArraySlice(AST):
    # <ArraySlice> ::= <ArrayLocation> LBRACKET <LowerBound> : <UpperBound> RBRACKET
    _fields = ['ArrayLocation', 'LowerBound', 'UpperBound']

    def typeCheck(self):
        return self.fields[0].type[0] == 'array' and self.fields[1].type == ['int'] and self.fields[2].type == ['int']

    def propType(self):
        self.type = self.fields[0].type[:]

#Typed
class PrimitiveValue(AST):
    # <primitive_value> ::=  <Literal>
    #              | <ValueArrayElement>
    #              | <ValueArraySlice>
    #              | <ParenthesizedExpression>
    _fields = ['Literal']

    def propType(self):
        self.type = self.fields[0].type[:]

#Typed
class Literal(AST):
    # <Literal> ::=  <IntegerLiteral>
    #     | <BooleanLiteral>
    #     | <CharacterLiteral>
    #     | <EmptyLiteral>
    #     | <CharacterStringLiteral>
    _fields = ['IntegerLiteral']

    def propType(self):
        self.type = self.fields[0].type[:]

#Typed
class ValueArrayElement(AST):
    # <ValueArrayElement> ::= <ArrayPrimitiveValue> LBRACKET <ExpressionList> RBRACKET
    _fields = ['ArrayPrimitiveValue', 'ExpressionList']

    def typeCheck(self):
        return  self.fields[1].type == ['int'] and self.fields[0].type[0] == 'array'

    # Se tivermos so uma expressão retornamos o valor nao um array
    def propType(self):
        if len(self.fields[1].fields) == 1:
            self.type = self.fields[0].type[1:]
        else:
            self.type = self.fields[0].type[:]

#Typed
class ValueArraySlice(AST):
    # <ValueArraySlice> ::= <ArrayPrimitiveValue> LBRACKET <LowerElement> : <UpperElement> RBRACKET
    _fields = ['ArrayPrimitiveValue', 'LowerElement', 'UpperElement']

    def typeCheck(self):
        return self.fields[0].type[0] == 'array' and self.fields[1].type == ['int'] and self.fields[2].type == ['int']

    def propType(self):
        self.type = self.fields[0].type[:]

#Typed
class Expression(AST):
    # <Expression> ::= <Operand0> | <ConditionalExpression>
    _fields = ['Operand0']

    def propType(self):
        self.type = self.fields[0].type[:]

#Typed
class ConditionalExpression(AST):
    # <ConditionalExpression> ::=  IF <BooleanExpression> <ThenExpression> <ElseExpression> FI
    #                     | IF <BooleanExpression> <ThenExpression> <ElsifExpression> <ElseExpression> FI
    _fields = ['BooleanExpression', 'ThenExpression', 'ElsifExpression',
               'ElseExpression']
    def typeCheck(self):
        return self.fields[0].type == ['bool']

    def propType(self):
        aux = self.fields[0].type[:]
        for f in self.fields:
            if aux != f.type:
                self.type = None
                return
        self.type = aux

#Typed
class ThenExpression(AST):
    # <ThenExpression> ::= THEN <Expression>
    _fields = ['Expression']
    def propType(self):
        self.type = self.fields[0].type[:]

#Typed
class ElseExpression(AST):
    # <ElseExpression> ::= ELSE <Expression>
    _fields = ['Expression']
    def propType(self):
        self.type = self.fields[0].type[:]

#Typed
class ElsifExpression(AST):
    # <ElsifExpression> ::=  ELSIF <BooleanExpression> <ThenExpression>
    #                | <ElsifExpression> ELSIF <BooleanExpression> <ThenExpression>
    _fields = ['ElsifExpression', 'BooleanExpression', 'ThenExpression']
    def typeCheck(self):
        if len(self.fields) == 2:
            return self.fields[0].type == ['bool']
        else:
            return self.fields[1].type == ['bool']

#Typed
class Operand0(AST):
    # <Operand0> ::=  <Operand1>
    #        | <Operand0> <Operator1> <Operand1>
    _fields = ['Operand0', 'Operator1', 'Operand1']

    def typeCheck(self):
        if len(self.fields) == 1:
            return True
        else:
            if isInstance(self.fields[1],RelationalOperator):
                return self.fields[0].type == self.fields[2].type
            else:
                return self.fields[2].type[0] == 'array' or self.fields[2].type[0] == 'chars'

    def propType(self):
        if len(self.fields) == 1:
            self.type = self.fields[0].type[:]
        else:
            self.type = ['bool']

#NotTyped
class Operator1(AST):
    # <Operator1> ::=  <RelationalOperator>
    #         | IN
    _fields = ['Operator']

#NotTyped
class RelationalOperator(AST):
    # <RelationalOperator> ::=  AND | OR | EQUAL | NEQUAL | MORETHEN | EQMORETHEN | LESSTHEN | EQLESSTHEN
    _fields = ['RelationalOperator']

#Typed
class Operand1(AST):
    # <Operand1> ::=  <Operand2>
    #        | <Operand1> <Operator2> <Operand2>
    _fields = ['Operand1', 'Operator2', 'Operand2']

    def typeCheck(self):
        if len(self.fields) == 1:
            return True
        else:
            return  self.fields[0].type == self.fields[2].type

    def propType(self):
        self.type = self.fields[0].type[:]

#NotTyped
class Operator2(AST):
    # <Operator2> ::=  PLUS
    #         | STRCAT
    #         | MINUS
    _fields = ['AddOperator']

#Typed
class Operand2(AST):
    # <Operand2> ::=  <Operand3>
    #        | <Operand2> MUL <Operand3>
    #        | <Operand2> DIV <Operand3>
    #        | <Operand2> MOD <Operand3>
    _fields = ['Operand2', 'MultiOperation', 'Operand3']

    def typeCheck(self):
        if len(self.fields) == 1:
            return True
        else:
            return self.fields[0].type == self.fields[2].type

    def propType(self):
        self.type = self.fields[0].type[:]

#Typed
class Operand3(AST):
    # <Operand3> ::=  [ MINUS ] <Operand4>
    #        | [ NOT ] <Operand4>
    #        | <Operand4>
    _fields = ['MonoOperation', 'Operand4']
    def typeCheck(self):
        if len(self.fields) == 1:
            return True
        else:
            if str(self.fields[0]) == 'minus':
                return self.fields[1].type in [['int'],['float'],['char']]
            else:
                return self.fields[1].type == ['bool']

    def propType(self):
        if len(self.fields) == 1:
            self.type = self.fields[0].type[:]
        else:
            self.type = self.fields[1].type[:]

#Typed
class Operand4(AST):
    # <Operand4> ::=  <Location> | <ReferencedLocation> | <PrimitiveValue>

    def propType(self):
        self.type = self.fields[0].type[:]
    _fields = ['Location']
#TODO
#Typed
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

class ExitAction(AST):
    # <ExitAction> ::= EXIT ID
    _fields = ['Id']

class ReturnAction(AST):
    # <ReturnAction> ::= RETURN [ <Result> ]
    _fields = ['Result']

class ResultAction(AST):
    # <ResultAction> ::= RESULT <Result>
    _fields = ['Result']

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

class ResultSpec(AST):
    # <ResultSpec> ::= RETURNS ( <Mode> [ <ResultAttribute> ] )
    _fields = ['Mode', 'ResultAttribute']
