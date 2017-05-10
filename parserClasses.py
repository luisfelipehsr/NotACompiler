import pydot as dot
import uuid


class AST(object):
    context = None

    def __init__(self, *args):
        self.fields = list(args)
        self.type = []
        self.isNewContext = False
        self.Declarations = []
        self.context = AST.context

    def removeChanel(self):
        while len(self.fields) == 1:
            aux = self.fields[0]
            if isinstance(aux,AST):
                self.fields = aux.fields
            else:
                return

        for n in self.fields:
            if isinstance(n,AST):
                n.removeChanel()

    def build(self,graph):
        myId = id(self)
        graph.add_node(dot.Node(myId,label = self.__class__.__name__ +
                                             ' '+str(self.type) ))
        for n in self.fields:
            nId = id(n)
            if isinstance(n,AST):
                graph.add_node(dot.Node(nId, label=self.__class__.__name__ +
                                                    ' ' + str(self.type)))
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
        #graph.write_png(name +'.png')

    def recursiveTypeCheck(self):
        len = self.context.contextLen()
        self.updateContext()
        ret = self.typeCheck()
        if not ret:
            print('Type Error at %s' % (self.__class__.__name__))
            return
        else:
            for n in self.fields:
                if isinstance(n,AST):
                    n.recursiveTypeCheck()
        self.context.trimToLen(len)

    def typeCheck(self):
        return True

    def propType(self):
        return

    def updateContext(self):
        return


#Context
class Program(AST):
    # <Program> ::= <StatementList>
    def updateContext(self):
        self.context.pushContext()
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
        self.context.addToContext(self.fields[0].fields,self.fields[1].propType())

#Typed
class Initialization(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[-1].propType()
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
        self.context.addToContext(self.fields[0].fields,self.propType())

#Typed & Context
class Mode(AST):
    # <Mode> ::=  <ModeName>
    #   | <DiscreteMode>
    #   | <ReferenceMode>
    #   | <CompositeMode>

    def typeCheck(self):
        if isinstance(self.fields[0],AST):
            return True
        else:
            print(self.type)
            return self.type[0] == 'mode'

    # The idea is, if we already have a type use that one,
    # if our son is a node from the AST get from him,
    # otherwise it must be in the context
    def propType(self):
         if len(self.type) > 0:
             return self.type[:]
         elif isinstance(self.fields[0],AST):
            self.type = self.fields[0].propType()
            return self.type[:]
         else:
            self.type = self.context.lookInContexts(self.fields[0])[:]
            if len(self.type) == 0:
                self.type = []
                print('Type Error %s not found in context' % (id))
                return []
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
        if isinstance(self.fields[0],AST):
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

        elif isinstance(self.fields[0],AST):
            self.type = prefix + self.fields[0].propType()
            return self.type[:]
        else:
            fromContext = self.context.lookInContexts(self.fields[0])[:]
            if len(fromContext) == 0:
                self.type = []
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
        return isinstance(self.fields[0],LiteralRange) or (self.fields[0].propType() is 'int','discreterange_int')

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
        elif isinstance(self.fields[0],AST):
            self.type = self.fields[0].propType()
            return self.type[:]
        else:
            fromContext = self.context.lookInContexts(self.fields[0])[:]

            if len(fromContext) == 0:
                self.type = []
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
            self.type = self.fields[0].propType()[1:]
            return self.type[:]
    _fields = ['Location']

#Typed
# class StringElement(AST):
#     # <StringElement> ::= <StringLocation> LBRACKET <StartElement> RBRACKET
#     def typeCheck(self):
#         if isinstance(self.fields[0],AST):
#             return self.fields[0].propType() == ['chars']
#         else:
#
#     def propType(self):
#         self.type = ['char']
#         return self.type[:]
#     _fields = ['StringLocation', 'StartElement']

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

        ret = True
        for parameter in self.fields[1].propType():
            if parameter not in [['int']]:
                ret = False

        if self.fields[0].propType() != ['chars'] and \
            self.fields[0].propType()[0] != 'array':
            ret = False

        return ret

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]

        # Se tivermos so uma expressão retornamos o valor nao um array
        elif len(self.fields[1].fields) == 1:
            if self.fields[0].propType() == ['chars']:
                self.type = ['char']
            else:
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
        else:
            for f in self.fields:
                self.type += [f.propType()]
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
            return self.type[:]

#Typed
class PrimitiveValue(AST):
    # <primitive_value> ::=  <Literal>
    #              | <ValueArrayElement>
    #              | <ValueArraySlice>
    #              | <ParenthesizedExpression>
    _fields = ['Literal']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

#Test
#Typed
class Literal(AST):
    # <Literal> ::=  <IntegerLiteral>
    #     | <BooleanLiteral>
    #     | <CharacterLiteral>
    #     | <EmptyLiteral>
    #     | <CharacterStringLiteral>
    _fields = ['IntegerLiteral']

    def propType(self):
        token = self.fields[0]
        _,self.type = token
        self.type = [self.type]
        return self.type[:]

#Typed
class ValueArrayElement(AST):
    # <ValueArrayElement> ::= <ArrayPrimitiveValue> LBRACKET <ExpressionList> RBRACKET
    _fields = ['ArrayPrimitiveValue', 'ExpressionList']

    def typeCheck(self):
        return  self.fields[1].propType() == ['int'] and self.fields[0].propType()[0] == 'array'

    # Se tivermos so uma expressão retornamos o valor nao um array
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        elif len(self.fields[1].fields) == 1:
            self.type = self.fields[0].propType()[1:]
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

#Typed
class ValueArraySlice(AST):
    # <ValueArraySlice> ::= <ArrayPrimitiveValue> LBRACKET <LowerElement> : <UpperElement> RBRACKET
    _fields = ['ArrayPrimitiveValue', 'LowerElement', 'UpperElement']

    def typeCheck(self):
        return self.fields[0].propType()[0] == 'array' and self.fields[1].propType() == ['int'] and self.fields[2].propType() == ['int']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

#Typed
class Expression(AST):
    # <Expression> ::= <Operand0> | <ConditionalExpression>
    _fields = ['Operand0']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

#Typed
class ConditionalExpression(AST):
    # <ConditionalExpression> ::=  IF <BooleanExpression> <ThenExpression> <ElseExpression> FI
    #                     | IF <BooleanExpression> <ThenExpression> <ElsifExpression> <ElseExpression> FI
    _fields = ['BooleanExpression', 'ThenExpression', 'ElsifExpression',
               'ElseExpression']
    def typeCheck(self):
        return self.fields[0].propType() == ['bool']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            aux = self.fields[1].propType()
            for f in self.fields[1:]:
                if aux != f.propType():
                    self.type = []
                    return self.type[:]
            self.type = aux
            return self.type[:]

#Typed
class ThenExpression(AST):
    # <ThenExpression> ::= THEN <Expression>
    _fields = ['Expression']
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

#Typed
class ElseExpression(AST):
    # <ElseExpression> ::= ELSE <Expression>
    _fields = ['Expression']
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

#Typed
class ElsifExpression(AST):
    # <ElsifExpression> ::=  ELSIF <BooleanExpression> <ThenExpression>
    #                | <ElsifExpression> ELSIF <BooleanExpression> <ThenExpression>
    _fields = ['ElsifExpression', 'BooleanExpression', 'ThenExpression']
    def typeCheck(self):
        if len(self.fields) == 2:
            return self.fields[0].propType() == ['bool']
        else:
            return self.fields[1].propType() == ['bool']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        elif len(self.fields) == 2:
            self.type = self.fields[1].propType()
        else:
            if self.fields[0].propType() == self.fields[2].propType():
                self.type = self.fields[0].propType()
                return self.type[:]
            else:
                return []

#Typed
class Operand0(AST):
    # <Operand0> ::=  <Operand1>
    #        | <Operand0> <Operator1> <Operand1>
    _fields = ['Operand0', 'Operator1', 'Operand1']

    def typeCheck(self):
        if len(self.fields) == 1:
            return True
        else:

            operand0Type = self.fields[0].propType()
            operand1Type = self.fields[2].propType()
            operatorType = self.fields[1].fields[0]
            isRelational = isinstance(operatorType,RelationalOperator)

            if isRelational:

                if operand0Type == operand1Type:

                    operator = operatorType.fields[0]

                    if operator in ['&&', '||']:
                        if operand0Type == ['bool']:
                            return True
                        else:
                            print('Operands must be of type bool. Got %s'
                                  %(operand0Type))
                            return False

                    elif operator in ['==','!=']:
                        if operand0Type in [['int'],['bool']]:
                            return True
                        else:
                            print('Operands must be of type bool or int. Got' +
                                  '%s' %(operand0Type))
                            return False

                    else:
                        if operand0Type == ['int']:
                            return True
                        else:
                            print('Operands must be of type int. Got %s'
                                  %(operand0Type))
                            return False

                else:
                    print('Both operands must be of same type')
                    return False

            else:

                if operand1Type[0] == 'array':
                    if operand1Type[1:] == operand0Type:
                        return True
                    else:
                        print('Expected first operand of type %s. Got %s'
                               %(operand1Type[1:],operand0Type))
                        return False

                elif operand1Type == ['chars']:
                    if operand0Type == ['char']:
                        return True
                    else:
                        print('Expected first operand of type char. Got %s'
                              %(operand0Type))
                        return False

                else:
                    print ('On IN operation, second operand must be string or'+
                           ' array. Got %s' %(operand1Type))
                    return False

        return False

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        elif len(self.fields) == 1:
            self.type = self.fields[0].propType()
            return self.type[:]
        else:
            self.type = ['bool']
            return self.type[:]

#NotTyped
class Operator1(AST):
    # <Operator1> ::=  <RelationalOperator>
    #                | IN
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
            return  self.fields[0].propType() == self.fields[2].propType()

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

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
            return self.fields[0].propType() == self.fields[2].propType()

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

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
            if self.fields[0] == '-':
                return self.fields[1].propType() in [['int'],['char']]
            else:
                return self.fields[1].propType() == ['bool']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        elif len(self.fields) == 1:
            self.type = self.fields[0].propType()
            return self.type[:]
        else:
            self.type = self.fields[1].propType()
            return self.type[:]

#Typed
class Operand4(AST):
    # <Operand4> ::=  <Location> | <ReferencedLocation> | <PrimitiveValue>
    _fields = ['Location']
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

#Typed
class ReferencedLocation(AST):
    # <ReferencedLocation> ::= ARROW <Location>
    _fields = ['Location']
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = ['ref'] + self.fields[0].propType()
            return self.type[:]

#Typed
class ActionStatement(AST):
    # <ActionStatement> ::= [ ID: ] <Action> ;
    _fields = ['Id', 'Action']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = ['action'] + self.fields[len(self.fields)-1].propType()
            return self.type[:]

    def updateContext(self):
        if len(self.fields) == 2:
            self.context.addToContext(self.fields[0].value,self.type)

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
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

#NotTyped
class BracketedAction(AST):
    # <BracketedAction> ::= <IfAction> | <DoAction>
    _fields = ['IfDoAction']

#Typed
class AssignmentAction(AST):
    # <AssignmentAction> ::= <Location> <AssigningOperator> <Expression>
    _fields = ['Location', 'AssigningOperator', 'Expression']

    def typeCheck(self):

        if len(self.fields) == 2:
            return self.fields[0].propType() == self.fields[1].propType()
        elif self.fields[1] == '&':
                return (self.fields[0].propType() == ['chars'] and self.fields[1].propType() == ['chars']) or \
                       (self.fields[0].propType() == ['chars'] and self.fields[1].propType() == ['char'])
        else:
            return self.fields[0].propType() == self.fields[2].propType() and self.fields[0].propType() == ['int']

#Typed
class IfAction(AST):
    # <IfAction> ::= IF <BooleanExpression> <ThenClause> [ <ElseClause> ] FI
    _fields = ['BooleanExpression', 'ThenClause', 'ElseClause']
    def typeCheck(self):
        return self.fields[0].propType() == ['bool']

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
            return self.fields[0].propType() == ['bool']
        else:
            return True

#Context
class DoAction(AST):
    # <DoAction> ::= DO [ <ControlPart> ; ] <ActionStatementList> OD
    _fields = ['ControlPart', 'ActionStatementList']

    def updateContext(self):
        self.context.pushContext()

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
        if len(self.fields) == 3:
            return self.fields[1].propType() == self.fields[2].propType() \
                   and self.fields[1].propType() == ['int']
        elif len(self.fields) == 4:
            if isinstance(self.fields[2],AST):
                return self.fields[1].propType() == self.fields[2].propType() \
                       and self.fields[2].propType() == self.fields[3].propType() \
                       and self.fields[1].propType() == ['int']
            else:
                return self.fields[1].propType() == self.fields[3].propType() \
                       and self.fields[1].propType() == ['int']
        else:
            return self.fields[1].propType() == self.fields[2].propType() \
                   and self.fields[2].propType() == self.fields[4].propType() \
                   and self.fields[1].propType() == ['int']

    def updateContext(self):
        self.context.addToContext(self.fields[0],['int'])

#Context + ? DiscreteMode ->DiscreteRangeMode?
class RangeEnumeration(AST):
    # <RangeEnumeration> ::= <LoopCounter> [ DOWN ] IN <DiscreteMode>
    _fields = ['LoopCounter', 'DiscreteMode']

    def updateContext(self):
        self.context.addToContext(self.fields[0],['int'])

#Typed
class WhileControl(AST):
    # <WhileControl> ::= WHILE <BooleanExpression>
    _fields = ['BooleanExpression']
    def typeCheck(self):
        return self.fields[0].propType() == ['bool']

#Typed
class CallAction(AST):
    # <CallAction> ::=  <ProcedureCall> | <BuiltinCall>
    _fields = ['ProcedureCall']
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]
#Todo Error
#Typed & Context
class ProcedureCall(AST):
    # <ProcedureCall> ::= <ProcedureName> ( [ <ParameterList> ] )
    _fields = ['ProcedureName', 'ParameterList']

    def typeCheck(self):
        fromContext = self.context.lookInContexts(self.fields[0])
        fromCall = []
        if len(self.fields) == 2:
            fromCall = self.fields[1].propType()
        return fromCall == fromContext


    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            #The return type is saved with a list with 'ret' as a prefix
            self.type = self.context.lookInContexts(('ret',self.fields[0]))
            return self.type[:]
#Todo Error
#Typed Context maybe create check context function
class ExitAction(AST):
    # <ExitAction> ::= EXIT ID

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.context.lookInContexts(self.fields[0])
            return self.type[:]
    _fields = ['Id']

#Typed
class ReturnAction(AST):
    # <ReturnAction> ::= RETURN [ <Result> ]
    _fields = ['Result']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        if len(self.fields) == 1:
            self.type = []
            return self.type[:]
        else:
            self.type = self.fields[1].propType()
            return self.type[:]

#Typed
class ResultAction(AST):
    # <ResultAction> ::= RESULT <Result>
    _fields = ['Result']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]
#TODO UPPER LOWER
#Typed
class BuiltinCall(AST):
    # <BuiltinCall> ::= <BuiltinName> ( [ <ParameterList> ] )
    _fields = ['BuiltinName', 'ParameterList']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

    def typeCheck(self):
        ret = False
        t = self.fields[0].fields[0]

        if t == 'abs':
            ret = self.fields[1].propType() == ['int']

        elif t == 'length':
            ret = self.fields[1].propType()[0] = 'array'

        elif t == 'asc':
            ret = self.fields[1].propType() == ['int']

        elif t == 'num':
            ret = self.fields[1].propType() == ['char']

        elif t == 'print' or 'read':

            ret = True
            for parameter in self.fields[1].propType():

                if parameter not in [['chars'], ['char'], ['bool'],
                                     ['int']]:
                    ret = False

        else:
            print('Invalid BuiltInCall')


        return ret

#TODO UPPER LOWER
#Typed
class BuiltinName(AST):
    # <BuiltinName> ::= ABS | ASC | NUM | UPPER | LOWER | LENGTH | READ | PRINT
    _fields = ['BuiltinName']
    def propType(self):
        t = self.fields[0].type
        if t == 'ABS':
            self.type = ['int']
        elif t == 'READ':
            self.type = []
        elif t == 'LENGTH':
            self.type = ['int']
        elif t == 'PRINT':
            self.type = []
        elif t == 'ASC':
            self.type = ['char']
        elif t == 'UPPER':
            self.type = ['int']
        elif t == 'LOWER':
            self.type = ['int']
        elif t == 'NUM':
            self.type = ['int']
        return self.type[:]

#Context
class ProcedureStatement(AST):
    # <ProcedureStatement> ::= ID : <ProcedureDefinition> ;
    _fields = ['Id', 'ProcedureDefinition']


    def updateContext(self):
        paran,ret = self.fields[1].propType()
        self.context.addToContext(self.fields[0],paran)
        self.context.addToContext(('ret',self.fields[0]),ret)
        self.context.pushContext()

#Typed
class ProcedureDefinition(AST):
    # <ProcedureDefinition> ::= PROC ( [ <FormalParameterList> ] ) [ <ResultSpec> ]; <StatementList> END
    _fields = ['FormalParameterList', 'ResultSpec', 'StatementList']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        elif  len(self.fields) == 1:
            self.type = ([],[])
        elif len(self.fields) == 2:
            if isinstance(self.fields[0],FormalParameterList):
                self.type = (self.fields[0].propType(),[])
            else:
                self.type = ([],self.fields[0].propType())
        else:
            self.type = (self.fields[0].propType(),self.fields[1].propType())
        return self.type[:]

#Typed
class FormalParameterList(AST):
    # <FormalParameterList> ::= <FormalParameter> , <FormalParameterList>
    #                        | <FormalParameter>
    _fields = ['FormalParameter', 'FormalParameterList']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            for x in self.fields:
                self.type += [x.propType()]
            return self.type[:]

#Typed
class FormalParameter(AST):
    # <FormalParameter> ::= <IdentifierList> <ParameterSpec>
    _fields = ['IdentifierList', 'ParameterSpec']
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            for i in self.fields[0].fields:
                self.type += self.fields[1].propType()
            return self.type[:]

    def updateContext(self):
        self.context.addToContext(self.fields[0].fields,self.fields[1].propType())
#Typed
class ParameterSpec(AST):
    # <ParameterSpec> ::=  <Mode> [ <ParameterAttribute> ]
    _fields = ['Mode', 'ParameterAttribute']
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

#Typed
class ResultSpec(AST):
    # <ResultSpec> ::= RETURNS ( <Mode> [ <ResultAttribute> ] )
    _fields = ['Mode', 'ResultAttribute']
    def propType(self):
        if len(self.type)>0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]
