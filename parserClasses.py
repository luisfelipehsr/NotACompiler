import pydot as dot
import uuid
from Semantocer import Context

con = Context()


class AST(object):
    
    def __init__(self, *args):
        self.fields = list(args)
        self.type = []
        self.isNewContext = False
        self.Declarations = []
        self.context = con

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

    def updateContext(self):
        return

    def permTypes(self,types,range):
        for ind in range:
            if self.fields[ind].type not in types:
                return False
        else:
            return True

    def areEquals(self,rangeA,rangeB):
        for a in rangeA:
            for b in rangeB:
                if self.fields[a].type != self.fields[b].type:
                    return False
        return True

    def typeCopy(self,pos):
        self.type = self.fields[pos].type[:]

#Context
class Program(AST):
    # <Program> ::= <StatementList>
    def updateContext(self):
        self.context.newContext()
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

#Typed & Context
class Declaration(AST):
    # <Declaration> ::= <IdentifierList> <Mode> [ <Initialization> ]
    _fields = ['IdentifierList', 'Mode', 'Initialization']

    def typeCheck(self):
        if len(self.fields) == 3:
            return self.fields[1].propType() == self.fields[2].propType()
        else:
            return True

    def propType(self):
            if len(self.type) > 0:
                return self.type[:]
            else:
                self.type = self.fields[1].propType()
                return self.type[:]

    def updateContext(self):
        self.context.addToContext(self.fields[0].fields,self.type)

#Typed
class Initialization(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[:-1].propType()
            return self.type[:]

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

#Typed & Context
class SynonymDefinition(AST):
    # <SynonymDefinition> ::= <IdentifierList> [ <Mode> ] = <ConstantExpression>
    def typeCheck(self):
        if len(self.fields) == 3:
            return self.fields[1].propType() == self.fields[2].propType()
        else:
            return True

    def propType(self):
        if len(self.type)>0:
            return self.type[:]
        else:
            self.type = self.fields[:-1].propType()
            return self.type[:]

    def updateContext(self):
        self.context.addToContext(self.fields[0].fields,self.type)

class NewModeStatement(AST):
    # <NewModeStatement> ::= TYPE <NewModeList>
    _fields = ['NewModeList']

class NewModeList(AST):
    # <NewModeList> ::= <ModeDefinition> , <NewModeList>
    #                | <ModeDefinition>

    _fields = ['ModeDefinition', 'NewModeList']

#Typed & Context
class ModeDefinition(AST):
    # <ModeDefinition> ::= <IdentifierList> = <Mode>
    _fields = ['IdentifierList', 'Mode']
    def propType(self):
        prefix = ['mode']
        if len(self.type) > 0:
            return (prefix + self.type)[:]
        else:
            self.type = self.fields[1].propType()
            return  (prefix + self.type)[:]

    def updateContext(self):
        self.context.addToContext(self.fields[0].fields,self.type)

#Typed & Context
class Mode(AST):
    # <Mode> ::=  <ModeName>
    #   | <DiscreteMode>
    #   | <ReferenceMode>
    #   | <CompositeMode>

    def typeCheck(self):
        if isInstance(self.fields[0],AST):
            return True
        else:
            return self.fields[0].propType()[0] == 'mode'

    # The idea is, if we already have a type use that one,
    # if our son is a node from the AST get from him,
    # otherwise it must be in the context
    def propType(self):
         if len(self.type) > 0:
             return self.type
         elif isInstance(self.fields[0],AST):
            self.type = self.fields[0].propType()
            return self.type[:]
         else:
            self.type = self.context.lookInContexts(self.fields[0])[:]
            if len(self.type) == 0:
                self.type = None
                print('Type Error %s not found in context' % (id))
                return None
            else:
                return self.type[:]

    _fields = ['ModeName']

#Typed
class DiscreteMode(AST):
    # <DiscreteMode> ::=  <IntegerMode>
    #            | <BooleanMode>
    #            | <CharacterMode>
    #            | <DiscreteRangeMode>

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        if isIsntance(self.fields[0],AST):
            self.type = self.fields[0].propType()
            return self.type[:]
        else:
            self.type = [str(self.fields[0])]
            return self.fields[:]

#Typed & Context
class DiscreteRangeMode(AST):
    # <DiscreteRangeMode> ::= <DiscreteModeName> ( <LiteralRange> )
    #                  | <DiscreteMode> ( <LiteralRange> )


    def propType(self):
        #Prefixo
        prefix = ['discreterange']
        if len(self.type) > 0:
            return self.type[:]

        elif isInstance(self.fields[0],AST):
            self.type = prefix + self.fields[0].propType()
            return self.type[:]
        else:
            fromContext = self.context.lookInContexts(self.fields[0])[:]
            if len(fromContext) == 0:
                self.type = None
                print('Type Error %s not found in context' % (id))
                return self.type
            else:
                self.type = prefix + fromContext
                return self.type[:]

#Typed
class LiteralRange(AST):
    # <LiteralRange> ::= <LowerBound> : <UpperBound>

    def typeCheck(self):
        return self.fields[0].propType() == self.fields[1].propType() and self.fields[0].propType() == ['int']
    _fields = ['lowerBound', 'UpperBound']

#Typed
class ReferenceMode(AST):
    # <ReferenceMode> ::= REF <Mode>
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        # Take type from mode and add prefix ref
        else:
            self.type = ['ref'] + self.fields[0].propType()
            return self.type[:]
    _fields = ['Mode']

#Typed
class CompositeMode(AST):
    # <CompositeMode> ::= <StringMode> | <ArrayMode>
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        # Get the type from ArrayMode or StringMode
        else:
            self.type = self.fields[0].propType()
            return self.type[:]
    _fields = ['StringMode']

#Typed
class StringMode(AST):
    # <StringMode> ::= CHARS LBRACKET <StringLength> RBRACKET
    def propType(self):
        self.type = ['chars']
        return self.type[:]
    #No typecheck needed, lenght is Iconst
    _fields = ['Chars', 'StringLenght']

#Typed
class ArrayMode(AST):
    # <ArrayMode> ::= ARRAY LBRACKET <IndexModeList> RBRACKET <ElementMode>
    # Pegamos o tipo do element mode e adicionamos o prefixo array
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = ['array'] + self.fields[1].propType()
            return self.type[:]

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
        return isIstance(self.fields[0],LiteralRange) or (self.fields[0].propType() is 'int','discreterange_int')

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.fields[:]

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
        if len(self.type) > 0:
            return self.type[:]
        elif isIntance(self.fields[0],AST):
            self.type = self.fields[0].propType()
            return self.type[:]
        else:
            fromContext = self.context.lookInContexts(self.fields[0])[:]
            if len(fromContext) == 0:
                self.type = None
                return self.type
            else:
                self.type = fromContext
                return self.type[:]
    _fields = ['LocationName']

#Typed
class DereferencedReference(AST):
    # <DereferencedReference> ::= <Location> ARROW

    def  typeCheck(self):
        return self.fields[0].propType()[0] == 'ref'

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType[1:]
            return self.type[:]
    _fields = ['Location']

#Typed
class StringElement(AST):
    # <StringElement> ::= <StringLocation> LBRACKET <StartElement> RBRACKET
    def typeCheck(self):
        return self.fields[0].propType() == ['chars']
    def propType(self):
        self.type = ['char']
        return self.type[:]
    _fields = ['StringLocation', 'StartElement']

#Typed
class StringSlice(AST):
    # <StringSlice> ::= <StringLocation> LBRACKET <LeftElement> : <RightElement> RBRACKET
    _fields = ['StringLocation', 'LeftElement', 'RightElement']

    def typeCheck(self):
        return self.fields[0].propType() == ['chars'] and self.fields[1].propType() == ['int'] and self.fields[2].propType() == ['int']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

#Typed
class ArrayElement(AST):

    # <ArrayElement> ::= <ArrayLocation> LBRACKET <ExpressionList> RBRACKET
    _fields = ['ArrayLocation', 'ExpressionList']

    def typeCheck(self):
        return self.fields[1].propType() == ['int'] and self.fields[0].propType()[0] == 'array'

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        # Se tivermos so uma expressão retornamos o valor nao um array
        elif len(self.fields[1].fields) == 1:
            self.type = self.fields[0].propType()[1:]
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]


#Typed
class ExpressionList(AST):
    # <ExpressionList> ::= <Expression> , <ExpressionList>
    #               | <Expression>

    #If all expressions have the same type the list has a type
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        type = self.fields[0].propType()
        for t in self.fields:
            if type != t.propType():
                self.type = []
                return
        self.type = type
        return self.type[:]

    _fields = ['Expression', 'ExpressionList']

#Typed
class ArraySlice(AST):
    # <ArraySlice> ::= <ArrayLocation> LBRACKET <LowerBound> : <UpperBound> RBRACKET
    _fields = ['ArrayLocation', 'LowerBound', 'UpperBound']

    def typeCheck(self):
        return self.fields[0].propType()[0] == 'array' and self.fields[1].propType() == ['int'] and self.fields[2].propType() == ['int']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
# Todo
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

#Typed
class ReferencedLocation(AST):
    # <ReferencedLocation> ::= ARROW <Location>

    def propType(self):
        self.type = ['ref'] + self.fields[0].type[:]
    _fields = ['Location']

#Typed
class ActionStatement(AST):
    # <ActionStatement> ::= [ ID: ] <Action> ;
    _fields = ['Id', 'Action']
    def propType(self):
        self.typeCopy(len(self.fields)-1)

#Typed
class Action(AST):
    # <Action> ::=  <BracketedAction>
    #      | <AssignmentAction>
    #      | <CallAction>
    #      | <ExitAction>
    #      | <ReturnAction>
    #      | <ResultAction>
    _fields = ['Actions']


    def propType(self):
        self.typeCopy(0)

#NotTyped
class BracketedAction(AST):
    # <BracketedAction> ::= <IfAction> | <DoAction>
    _fields = ['IfDoAction']

#Typed
class AssignmentAction(AST):
    # <AssignmentAction> ::= <Location> <AssigningOperator> <Expression>
    _fields = ['Location', 'AssigningOperator', 'Expression']

    def typeCheck(self):
        return self.areEquals([1],[2])

#Typed
class IfAction(AST):
    # <IfAction> ::= IF <BooleanExpression> <ThenClause> [ <ElseClause> ] FI
    _fields = ['BooleanExpression', 'ThenClause', 'ElseClause']
    def typeCheck(self):
        return self.permTypes(['bool'],[0])

#NotTyped
class ActionStatementList(AST):
    # <ActionStatementList> ::= <ActionStatement> <ActionStatementList>
    #                   | <ActionStatement>
    _fields = ['ActionStatement', 'ActionStatementList']

#NotTyped
class ThenClause(AST):
    # <ThenClause> ::= THEN <ActionStatementList>
    _fields = ['ActionStatementList']

#Typed
class ElseClause(AST):
    # <ElseClause> ::=  ELSE <ActionStatementList>
    #           | ELSIF <BooleanExpression> <ThenClause> [ <ElseClause> ]

    _fields = ['BooleanExpression', 'ThenClause', 'ElseClause']

    def typeCheck(self):
        if len(self.fields) != 1:
            return self.permTypes(['bool'],[0])

#NotTyped
class DoAction(AST):
    # <DoAction> ::= DO [ <ControlPart> ; ] <ActionStatementList> OD
    _fields = ['ControlPart', 'ActionStatementList']

#NotTyped
class ControlPart(AST):
    # <ControlPart> ::=  <ForControl> [ <WhileControl> ]
    #            | <WhileControl>
    _fields = ['ForControl', 'WhileControl']

#NotTyped
class ForControl(AST):
    # <ForControl> ::= FOR <Iteration>
    _fields = ['Iteration']

#NotTyped
class Iteration(AST):
    # <Iteration> ::= <StepEnumeration> | <RangeEnumeration>
    _fields = ['StepEnumeration']

#Typed
class StepEnumeration(AST):
    # <StepEnumeration> ::=  <LoopCounter> <AssignmentSymbol> <StartValue> [ <StepValue> ] [ DOWN ] <EndValue>
    _fields = ['LoopCounter', 'AssignmentSymbol', 'StartValue', 'StepValue',
               'EndValue']

    def typeCheck(self):
        if len(self.fields) == 2:
            return self.permTypes(['int'],[0,1])
        elif len(self.fields) == 3:
            if isInstance(self.fields[1],AST):
                return self.permTypes(['int'],[0,1,2])
            else:
                return self.permTypes(['int'],[0,2])
        else:
            return self.permTypes(['int'],[0,1,3])

#NotTyped
class RangeEnumeration(AST):
    # <RangeEnumeration> ::= <LoopCounter> [ DOWN ] IN <DiscreteMode>
    _fields = ['LoopCounter', 'DiscreteMode']

#Typed
class WhileControl(AST):
    # <WhileControl> ::= WHILE <BooleanExpression>
    _fields = ['BooleanExpression']
    def typeCheck(self):
        return self.permTypes(['bool'],[0])

#Typed
class CallAction(AST):
    # <CallAction> ::=  <ProcedureCall> | <BuiltinCall>
    _fields = ['ProcedureCall']
    def propType(self):
        self.typeCopy(0)

#Typed
class ProcedureCall(AST):
    # <ProcedureCall> ::= <ProcedureName> ( [ <ParameterList> ] )
    _fields = ['ProcedureName', 'ParameterList']
    def propType(self):
        self.typeCopy(0)

#Typed
class ExitAction(AST):
    # <ExitAction> ::= EXIT ID

    def propType(self):
        self.typeCopy(0)
    _fields = ['Id']

#Typed
class ReturnAction(AST):
    # <ReturnAction> ::= RETURN [ <Result> ]
    _fields = ['Result']

    def propType(self):
        if len(self.fields) == 1:
            self.type = None
        else:
            self.typeCopy(1)

#Typed
class ResultAction(AST):
    # <ResultAction> ::= RESULT <Result>
    _fields = ['Result']

    def propType(self):
        self.typeCopy(0)

#Typed
class BuiltinCall(AST):
    # <BuiltinCall> ::= <BuiltinName> ( [ <ParameterList> ] )
    _fields = ['BuiltinName', 'ParameterList']
    def propType(self):
        if len(self.fields) == 1:
            self.type = None
        else:
            self.typeCopy(1)

#NotTyped
class BuiltinName(AST):
    # <BuiltinName> ::= ABS | ASC | NUM | UPPER | LOWER | LENGTH | READ | PRINT
    _fields = ['BuiltinName']

#Typed
class ProcedureStatement(AST):
    # <ProcedureStatement> ::= ID : <ProcedureDefinition> ;
    _fields = ['Id', 'ProcedureDefinition']

    def propType(self):
        self.typeCopy(1)

#Typed
class ProcedureDefinition(AST):
    # <ProcedureDefinition> ::= PROC ( [ <FormalParameterList> ] ) [ <ResultSpec> ]; <StatementList> END
    _fields = ['FormalParameterList', 'ResultSpec', 'StatementList']

    def propType(self):
        if len(self.fields) == 2 and isInstance(self.fields[0],ResultSpec):
            self.typeCopy(0)
        else:
            self.typeCopy(1)

#NotTyped
class FormalParameterList(AST):
    # <FormalParameterList> ::= <FormalParameter> , <FormalParameterList>
    #                        | <FormalParameter>
    _fields = ['FormalParameter', 'FormalParameterList']

#Typed
class FormalParameter(AST):
    # <FormalParameter> ::= <IdentifierList> <ParameterSpec>
    _fields = ['IdentifierList', 'ParameterSpec']
    def propType(self):
        self.typeCopy(1)

#Typed
class ParameterSpec(AST):
    # <ParameterSpec> ::=  <Mode> [ <ParameterAttribute> ]
    _fields = ['Mode', 'ParameterAttribute']
    def propType(self):
        self.typeCopy(0)

#Typed
class ResultSpec(AST):
    # <ResultSpec> ::= RETURNS ( <Mode> [ <ResultAttribute> ] )
    _fields = ['Mode', 'ResultAttribute']
    def propType(self):
        self.typeCopy(0)
