import pydot as dot
import uuid

class tColors:
    RED = "\033[1;31m"
    YELLOW = '\033[93m'
    RESET = '\033[0m'

class AST(object):
    semantic = None

    def __init__(self, *args):
        self.fields = list(args)
        self.type = None
        self.linespan = None
        self.context = None
     
    def setLinespan(self, p, start, end):
        s = p.linespan(start)[0]
        e = p.linespan(end)[1]
        self.linespan = (s,e)
        
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
        graph.write_png(name +'.png')

    def recursiveTypeCheck(self):
        leng = AST.semantic.contextLen()
        self.updateContext()
        ret = self.typeCheck()
        if not ret:
            if self.linespan[0] == self.linespan[1]:
                print(tColors.RED + 'Type Error on %s at '
                      %(self.__class__.__name__) + tColors.RESET + 'line %s'
                      %(self.linespan[0]))
            else:
                print(tColors.RED + 'Type Error on %s between '
                      %(self.__class__.__name__) + tColors.RESET + 'lines %s'
                      % (self.linespan[0]) + ' and %s' % (self.linespan[1]))
            return

        else:
            for n in self.fields:
                if isinstance(n,AST):
                    n.recursiveTypeCheck()
        AST.semantic.trimToLen(leng)

    def typeCheck(self):
        return True

    def propType(self):
        return self.type[:]

    def updateContext(self):
        return

class Program(AST):
    def updateContext(self):
        self.context = AST.semantic.pushContext()

class StatementList(AST):
    _fields = ['StatementList']

class Statement(AST):
    _fields = ['Statement']

class DeclarationStatement(AST):
    _fields = ['DeclarationList']

class DeclarationList(AST):
    _fields = ['DeclarationList']

class Declaration(AST):

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
        mode = self.fields[1].propType()
        if mode[0] == 'mode':
            mode = mode[1:]
        AST.semantic.addToContext(self.fields[0].fields,mode)

class Initialization(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[-1].propType()
            return self.type[:]

class IdentifierList(AST):
    _fields = ['IdentifierList']

class SynonymStatement(AST):
    _fields = ['SynonymList']

class SynonymList(AST):
    _fields = ['synonymDefinition', 'synonymList']

class SynonymDefinition(AST):
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
        AST.semantic.addToContext(self.fields[0].fields,self.fields[1].propType())

class NewModeStatement(AST):
    _fields = ['NewModeList']

class NewModeList(AST):
    _fields = ['ModeDefinition', 'NewModeList']

class ModeDefinition(AST):
    def propType(self):
        prefix = ['mode']
        if len(self.type) > 0:
            return (prefix + self.type)[:]
        else:
            self.type = self.fields[1].propType()
            return  (prefix + self.type)[:]

    def updateContext(self):
        AST.semantic.addToContext(self.fields[0].fields,self.propType())

class Mode(AST):
    def typeCheck(self):
        if isinstance(self.fields[0],AST):
            return True
        else:
            aux = AST.semantic.lookInContexts(self.fields[0])[:]
            if len(self.type) == 0:
                self.type = []
                print(tColors.RED + 'Type Error ' + tColors.RESET + '%s '
                      % (
                          self.fields[
                              0]) + tColors.RED + 'not found in context ' +
                      'at ' + tColors.RESET + 'line %s' % (self.linespan[0]))
                return False
            elif aux[0] != 'mode':
                return False
            else:
                return True

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
            self.type = AST.semantic.lookInContexts(self.fields[0])[:]
            if len(self.type) == 0:
                self.type = []
                print(tColors.RED + 'Type Error ' + tColors.RESET + '%s '
                      % (
                      self.fields[0]) + tColors.RED + 'not found in context ' +
                      'at ' + tColors.RESET + 'line %s' % (self.linespan[0]))
                return []
            else:
                if self.type[0] == 'mode':
                    self.type = self.type[1:]
                return self.type[:]

    _fields = ['ModeName']

class DiscreteMode(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        if isinstance(self.fields[0],AST):
            self.type = self.fields[0].propType()
            return self.type[:]
        else:
            self.type = [str(self.fields[0])]
            return self.fields[:]

class DiscreteRangeMode(AST):
    def propType(self):
        #Prefixo
        prefix = ['discreterange']
        if len(self.type) > 0:
            return self.type[:]

        elif isinstance(self.fields[0],AST):
            self.type = prefix + self.fields[0].propType()
            return self.type[:]
        else:
            fromContext = AST.semantic.lookInContexts(self.fields[0])[:]
            if len(fromContext) == 0:
                self.type = []
                print(tColors.RED + 'Type Error ' + tColors.RESET + '%s '
                      % (
                      self.fields[0]) + tColors.RED + 'not found in context ' +
                      'at ' + tColors.RESET + 'line %s' % (self.linespan[0]))
                return self.type
            else:
                self.type = prefix + fromContext
                return self.type[:]

class LiteralRange(AST):
    def typeCheck(self):
        return self.fields[0].propType() == self.fields[1].propType() and self.fields[0].propType() == ['int']
    _fields = ['lowerBound', 'UpperBound']

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

class CompositeMode(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        # Get the type from ArrayMode or StringMode
        else:
            self.type = self.fields[0].propType()
            return self.type[:]
    _fields = ['StringMode']

class StringMode(AST):
    # <StringMode> ::= CHARS LBRACKET <StringLength> RBRACKET
    def propType(self):
        self.type = ['chars']
        return self.type[:]
    #No typecheck needed, lenght is Iconst
    _fields = ['Chars', 'StringLenght']

class ArrayMode(AST):
    # Pegamos o tipo do element mode e adicionamos o prefixo array
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = ['array'] + self.fields[1].propType()
            return self.type[:]

    _fields = ['IndexModeList']

class IndexModeList(AST):
    _fields = ['IndexMode', 'IndexModeList']

class IndexMode(AST):
    def typeCheck(self):
        return isinstance(self.fields[0],LiteralRange) or (self.fields[0].propType() is 'int','discreterange_int')

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.fields[:]

    _fields = ['DiscreteMode']

class Location(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        elif isinstance(self.fields[0],AST):
            self.type = self.fields[0].propType()
            return self.type[:]
        else:


            fromContext = AST.semantic.lookInContexts(self.fields[0])
            if fromContext == None:
                self.type = []

                print(tColors.RED + 'Type Error ' + tColors.RESET + '%s '
                      % (self.fields[0]) + tColors.RED + 'not found in ' +
                      'context at ' + tColors.RESET + 'line %s'
                      % (self.linespan[0]))

                return self.type
            else:
                self.type = fromContext
                return self.type[:]
    _fields = ['LocationName']

class DereferencedReference(AST):
    def  typeCheck(self):
        return self.fields[0].propType()[0] == 'ref'

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()[1:]
            return self.type[:]
    _fields = ['Location']

class StringSlice(AST):
    def typeCheck(self):
        return self.fields[0].propType() == ['chars'] and self.fields[1].propType() == ['int'] and self.fields[2].propType() == ['int']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class ArrayElement(AST):
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

class ExpressionList(AST):

    #If all expressions have the same type the list has a type
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            for f in self.fields:
                self.type += [f.propType()]
            return self.type[:]

    _fields = ['Expression', 'ExpressionList']

class ArraySlice(AST):

    def typeCheck(self):
        return self.fields[0].propType()[0] == 'array' and self.fields[1].propType() == ['int'] and self.fields[2].propType() == ['int']

    def propType(self):

        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class PrimitiveValue(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class Literal(AST):

    def propType(self):
        token = self.fields[0]
        _,self.type = token
        self.type = [self.type]
        return self.type[:]

class ValueArrayElement(AST):
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

class ValueArraySlice(AST):
    def typeCheck(self):
        return self.fields[0].propType()[0] == 'array' and self.fields[1].propType() == ['int'] and self.fields[2].propType() == ['int']

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class Expression(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class ConditionalExpression(AST):
    def typeCheck(self):
        if self.fields[0].propType() == ['bool']:
            if len(self.fields) == 3:
                return self.fields[1].propType() == self.fields[2].propType()
            else:
                a = self.fields[1].propType()
                b = self.fields[2].propType()
                c = self.fields[3].propType()

                return  a==b==c
        else:
            return False


    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[1].propType()
            return self.type[:]

class ThenExpression(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class ElseExpression(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class ElsifExpression(AST):
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
            return self.type[:]
        else:
            if self.fields[0].propType() == self.fields[2].propType():
                self.type = self.fields[0].propType()
                return self.type[:]
            else:
                return []

class Operand0(AST):
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
                            print('Operands must be of type bool. Got %s:'
                                  %(operand0Type))
                            return False

                    elif operator in ['==','!=']:
                        if operand0Type in [['int'],['bool']]:
                            return True
                        else:
                            print('Operands must be of type bool or int. Got' +
                                  '%s:' %(operand0Type))
                            return False

                    else:
                        if operand0Type == ['int']:
                            return True
                        else:
                            print('Operands must be of type int. Got %s:'
                                  %(operand0Type))
                            return False

                else:
                    print('Both operands must be of same type:')
                    return False

            else:

                if operand1Type == []:
                    return False

                if operand1Type[0] == 'array':
                    if operand1Type[1:] == operand0Type:
                        return True
                    else:
                        print('Expected first operand of type %s. Got %s:'
                               %(operand1Type[1:],operand0Type))
                        return False

                elif operand1Type == ['chars']:
                    if operand0Type == ['char']:
                        return True
                    else:
                        print('Expected first operand of type char.' +
                              'Got %s:'
                              %(operand0Type))
                        return False

                else:
                    print ('On IN operation, second operand must be string or'+
                           ' array. Got %s:'
                           %(operand1Type))
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

class Operator1(AST):
    _fields = ['Operator']

class RelationalOperator(AST):
    _fields = ['RelationalOperator']

class Operand1(AST):
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

class Operator2(AST):
    _fields = ['AddOperator']

class Operand2(AST):
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

class Operand3(AST):
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

class Operand4(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class ReferencedLocation(AST):
    _fields = ['Location']
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = ['ref'] + self.fields[0].propType()
            return self.type[:]

class ActionStatement(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[-1].propType()
            return self.type[:]

    def updateContext(self):
        if len(self.fields) == 2:
            AST.semantic.addToContext(self.fields[0],self.type)

class Action(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class BracketedAction(AST):
    _fields = ['IfDoAction']

class AssignmentAction(AST):
    def typeCheck(self):

        if len(self.fields) == 2:
            return self.fields[0].propType() == self.fields[1].propType()
        elif self.fields[1] == '&':
                return (self.fields[0].propType() == ['chars']
                        and self.fields[1].propType() == ['chars']) or \
                       (self.fields[0].propType() == ['chars']
                        and self.fields[1].propType() == ['char'])
        else:

            return self.fields[0].propType() == self.fields[2].propType() and \
                   self.fields[0].propType() == ['int']

class IfAction(AST):
    def typeCheck(self):
        if len(self.fields) == 2:
            return self.fields[0].propType() == ['bool']
        else:
            return self.fields[0].propType() == ['bool']

    def propType(self):
        self.type = self.fields[1].propType()
        if len (self.fields) == 3:
            self.type += self.fields[2].propType()
        return self.type[:]

class ActionStatementList(AST):

    def propType(self):
        if len(self.type) >0:
            return self.type[:]
        else:
            for stmt in self.fields:
                print(self.type)
                self.type += [stmt.propType()]
            return self.type[:]

class ThenClause(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class ElseClause(AST):
    def typeCheck(self):
        if len(self.fields) != 1:
            return self.fields[0].propType() == ['bool']
        else:
            return True

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            if len(self.fields) == 1:
                self.type = self.fields[0].propType()
            else:
                self.type = self.fields[1].propType() + self.fields[2].propType()
            return self.type[:]

class DoAction(AST):
    def updateContext(self):
	    self.context = AST.semantic.pushContext()

class ControlPart(AST):
    _fields = ['ForControl', 'WhileControl']

class ForControl(AST):
    _fields = ['Iteration']

class Iteration(AST):
    _fields = ['StepEnumeration']

class StepEnumeration(AST):
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
        AST.semantic.addToContext(self.fields[0],['int'])

class RangeEnumeration(AST):

    _fields = ['LoopCounter', 'DiscreteMode']

    def updateContext(self):
        AST.semantic.addToContext(self.fields[0],['int'])

class WhileControl(AST):
    def typeCheck(self):
        return self.fields[0].propType() == ['bool']

class CallAction(AST):
    _fields = ['ProcedureCall']
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class ProcedureCall(AST):


    def typeCheck(self):
        fromContext = AST.semantic.lookInContexts(self.fields[0])
        fromCall = []
        if len(self.fields) == 2:
            fromCall = self.fields[1].propType()
            for i in range(len(fromCall)):
                if fromCall[i][0] == 'mode':
                    fromCall[i] = fromCall[i][1:]
        return fromCall == fromContext


    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            #The return type is saved with a list with 'ret' as a prefix
            self.type = AST.semantic.lookInContexts(('ret',self.fields[0]))
            if (self.type == None):
                print(tColors.RED + 'Type Error ' + tColors.RESET + '%s '
                      % (self.fields[0]) + tColors.RED + 'not found in' +
                      ' context at ' + tColors.RESET + 'line %s'
                      % (self.linespan[0]))
            return self.type[:]

class ExitAction(AST):
    # <ExitAction> ::= EXIT ID

    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = AST.semantic.lookInContexts(self.fields[0])
            if (self.type == None):
                print(tColors.RED + 'Type Error ' + tColors.RESET + '%s '
                      % (self.fields[0]) + tColors.RED + 'not found in ' +
                      'context at ' + tColors.RESET + 'line %s'
                      % (self.linespan[0]))
            return self.type[:]
    _fields = ['Id']

class ReturnAction(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        if len(self.fields) == 1:
            self.type = []
            return self.type[:]
        else:
            self.type = self.fields[1].propType()
            return self.type[:]

class ResultAction(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]

class BuiltinCall(AST):

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

class BuiltinName(AST):
    def propType(self):
        t = self.fields[0]
        if t == 'abs':
            self.type = ['int']
        elif t == 'read':
            self.type = []
        elif t == 'length':
            self.type = ['int']
        elif t == 'print':
            self.type = []
        elif t == 'asc':
            self.type = ['char']
        elif t == 'upper':
            self.type = ['int']
        elif t == 'lower':
            self.type = ['int']
        elif t == 'num':
            self.type = ['int']
        return self.type[:]

class ProcedureStatement(AST):
    def updateContext(self):
        paran,ret = self.fields[1].propType()
        AST.semantic.addToContext(self.fields[0],paran)
        AST.semantic.addToContext(('ret',self.fields[0]),ret)
        self.context = AST.semantic.pushContext()

class ProcedureDefinition(AST):
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

class FormalParameterList(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            for x in self.fields:
                self.type += [x.propType()]
            return self.type[:]

class FormalParameter(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            for i in self.fields[0].fields:
                self.type += self.fields[1].propType()
            return self.type[:]

    def updateContext(self):
        AST.semantic.addToContext(self.fields[0].fields,
                                  self.fields[1].propType())

class ParameterSpec(AST):
    def propType(self):
        if len(self.type) > 0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            if self.type[0] == 'mode':
                self.type = self.type[1:]
            return self.type[:]

class ResultSpec(AST):
    def propType(self):
        if len(self.type)>0:
            return self.type[:]
        else:
            self.type = self.fields[0].propType()
            return self.type[:]
