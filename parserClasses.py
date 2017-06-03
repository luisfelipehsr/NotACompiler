import pydot as dot
import uuid
from type import *
from symbol import Symbol

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
                                             ' '+str(self.type.toString() if self.type is not None else 'None') ))
        for n in self.fields:
            nId = id(n)
            if isinstance(n,AST):
                graph.add_node(dot.Node(nId, label=self.__class__.__name__ +
                                                    ' ' + str(self.type.toString() if self.type is not None else 'None')))
                graph.add_edge(dot.Edge(myId,nId))
                n.build(graph)
            else:
                nId += uuid.uuid4().int & (1<<64)-1
                if isinstance(n,Type):
                    graph.add_node(dot.Node(nId, label=n.toString()))
                else:
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

    def recursiveGenCode(self):
        ret = []
        leng = AST.semantic.contextLen()
        self.updateContext()
        for n in self.fields:
            if isinstance(n,AST):
                ret += n.recursiveGenCode()
        ret += self.genCode()
        AST.semantic.trimToLen(leng)
        return ret

    def typeCheck(self):
        return True

    def propType(self):
        return self.type

    def updateContext(self):
        return

    def genCode(self):
        return []

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
            t1 = self.fields[1].propType()
            t2 = self.fields[2].propType()
            return  t1.equals(t2) and not isinstance(t1,Array)
        else:
            return True

    def propType(self):
            if self.type is not None:
                return self.type
            else:
                self.type = self.fields[1].propType()
                return self.type

    def updateContext(self):
        type = self.fields[1].propType()
        if isinstance(type,ModeType):
            type = type.subType
        for id in self.fields[0].fields:
            AST.semantic.addToContext(Symbol(id,type))

    def genCode(self):
        ret = []
        type = self.fields[1].propType()
        if isinstance(type, ModeType):
            type = type.subType
        first = True
        for id in self.fields[0].fields:
            if len(self.fields) == 2:
                ret += [('alc',self.propType().getSize())]
            else:
                v = self.fields[2].propType()
                if v.value is not None:
                    ret += [('ldc',v.value)]
                else:
                    if first == True:
                        first = AST.semantic.lookInContexts(id)

                    else:
                        ret += [('ldv',first.count,first.pos)]








        return ret

class Initialization(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[-1].propType()
            return self.type

    def genCode(self):
        ret = []
        if len(self.fields) == 1:
            return ret
        else:
            op = self.fields[0]
            if op == '+':
                ret += [('add')]
            elif op == '-':
                ret += [('sub')]
            elif op == '*':
                ret += [('mul')]
            elif op == '/':
                ret += [('div')]
            elif op == '%':
                ret += [('mod')]
            else:
                return ret
            return ret

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
            self.type = self.fields[-1].propType()
            return self.type[:]

    def updateContext(self):
        AST.semantic.addToContext(self.fields[0].fields,self.fields[1].propType())

class NewModeStatement(AST):
    _fields = ['NewModeList']

class NewModeList(AST):
    _fields = ['ModeDefinition', 'NewModeList']

class ModeDefinition(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[1].propType()
            self.type = ModeType(self.type)
            return self.type

    def updateContext(self):
        type = self.fields[1].propType()
        for id in self.fields[0].fields:
            AST.semantic.addToContext(Symbol(id,ModeType(type)))

class Mode(AST):
    def typeCheck(self):
        if isinstance(self.fields[0],AST):
            return True
        else:
            symbol = AST.semantic.lookInContexts(self.fields[0])
            if symbol is None:
                self.type = None
                print(tColors.RED + 'Type Error ' + tColors.RESET + '%s '
                      % (
                          self.fields[
                              0]) + tColors.RED + 'not found in context ' +
                      'at ' + tColors.RESET + 'line %s' % (self.linespan[0]))
                return False
            elif not isinstance(symbol.type,ModeType):
                return False
            else:
                return True

    # The idea is, if we already have a type use that one,
    # if our son is a node from the AST get from him,
    # otherwise it must be in the context
    def propType(self):
         if self.type is not None:
             return self.type
         elif isinstance(self.fields[0],AST):
            self.type = self.fields[0].propType()
            return self.type
         else:
            symbol = AST.semantic.lookInContexts(self.fields[0])
            self.type = symbol.type
            if symbol is None:
                self.type = None
                print(tColors.RED + 'Type Error ' + tColors.RESET + '%s '
                      % (
                      self.fields[0]) + tColors.RED + 'not found in context ' +
                      'at ' + tColors.RESET + 'line %s' % (self.linespan[0]))
                return None
            else:
                if isinstance(self.type,ModeType):
                    self.type = self.type.subType
                return self.type

class DiscreteMode(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        if isinstance(self.fields[0],AST):
            self.type = self.fields[0].propType()
            return self.type
        elif isinstance(self.fields[0],Type):
            self.type = self.fields[0]
            return self.type

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
        t1 = self.fields[0].propType()
        t2 = self.fields[1].propType()
        return type(t1) == type(t2) and isinstance(t1,Int)

    def propType(self):
        if self.type is not None:
            return self.type
        else:
            begin = self.fields[0].propType()
            end = self.fields[1].propType()
            self.type = Range(begin,end)
            return self.type

class ReferenceMode(AST):
    # <ReferenceMode> ::= REF <Mode>
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = Reference(self.fields[0].propType())
            return self.type

class CompositeMode(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

class StringMode(AST):
    # <StringMode> ::= CHARS LBRACKET <StringLength> RBRACKET
    def propType(self):
        lenght = self.fields[0]
        lenght.value -=1
        self.type = Chars(Range(Int(0),lenght))
        return self.type
    #No typecheck needed, lenght is Iconst

class ArrayMode(AST):
    # Pegamos o tipo do element mode e adicionamos o prefixo array
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            type = self.fields[1].propType()
            range = self.fields[0].propType()
            self.type = Array(type,range)
            return self.type

class IndexModeList(AST):
    def propType(self):
        for i in range(len(self.fields)-1):
            if isinstance(self.fields[i].propType(),Range):
                self.fields[i].propType().subRange = self.fields[i+1].propType()

        return self.fields[0].propType()

class IndexMode(AST):
    def typeCheck(self):
        return isinstance(self.fields[0],LiteralRange) or (self.fields[0].propType() is 'int','discreterange_int')

    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

class Location(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        elif isinstance(self.fields[0],AST):
            self.type = self.fields[0].propType()
            return self.type
        else:
            fromContext = AST.semantic.lookInContexts(self.fields[0])
            if fromContext == None:
                self.type = None

                print(tColors.RED + 'Type Error ' + tColors.RESET + '%s '
                      % (self.fields[0]) + tColors.RED + 'not found in ' +
                      'context at ' + tColors.RESET + 'line %s'
                      % (self.linespan[0]))

                return self.type
            else:
                self.type = fromContext.type
                return self.type


class DereferencedReference(AST):
    def  typeCheck(self):
        a = self.fields[0].propType()
        return isinstance(a,Reference)

    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType().getSubType()
            return self.type

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
        parameters = self.fields[1].propType().getParameterList()
        data = self.fields[0].propType()
        if not isinstance(data,Chars) and not isinstance(data,Array):
            return False
        for p in parameters:
            if not isinstance(p,Int):
                return False
        return True





    def propType(self):
        if self.type is not None:
            return self.type

        # Se tivermos so uma expressão retornamos o valor nao um array

        elif len(self.fields[1].fields) == 1:
            type = self.fields[0].propType()
            if isinstance(type,Chars):
                self.type = Char()
            else:
                self.type = type.subType
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

class ExpressionList(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = []
            for f in self.fields:
                self.type += [f.propType()]
            self.type = Parameters(self.type)
            return self.type
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
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

class Literal(AST):
    def propType(self):
        token = self.fields[0]
        if isinstance(token,Type):
            self.type = token
        return self.type

    def genCode(self):
        ret = []
        val = self.fields[0]
        if isinstance(val,Chars):
            return ret
        elif isinstance(val,Bool):
            return ret
        elif isinstance(val,Char):
            return ret
        elif isinstance(val,Int):
            ret += [('ldc',val.value)]
        return ret

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
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

class ConditionalExpression(AST):
    def typeCheck(self):
        a = self.fields[0].propType()
        b = self.fields[1].propType()
        c = self.fields[2].propType()
        if isinstance(a,Bool):
            if len(self.fields) == 3:
                return b.equals(c)
            else:
                d = self.fields[3].propType()
                return  b.equals(c) and b.equals(d)
        else:
            return False


    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[1].propType()
            return self.type

class ThenExpression(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

class ElseExpression(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

class ElsifExpression(AST):
    def typeCheck(self):
        if len(self.fields) == 2:
            a = self.fields[0].propType()
            return isinstance(a,Bool)
        else:
            a = self.fields[0].propType()
            b = self.fields[1].propType()
            c = self.fields[2].propType()
            return isinstance(b, Bool) and a.equals(c)

    def propType(self):
        if self.type is not None:
            return self.type
        elif len(self.fields) == 2:
            self.type = self.fields[1].propType()
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

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
        if self.type is not None:
            return self.type
        elif len(self.fields) == 1:
            self.type = self.fields[0].propType()
            return self.type
        else:
            self.type = Bool()
            return self.type

    def genCode(self):
        ret = []
        if len(self.fields) == 3:
            op = self.fields[1].fields[0]
            if isinstance(op,AST):
                op = op.fields[0]
            if op ==   '&&':
                ret += [('and')]
            elif op == '||':
                ret += [('lor')]
            elif op == '==':
                ret += [('equ')]
            elif op == '!=':
                ret += [('neq')]
            elif op ==  '>':
                ret += [('grt')]
            elif op ==  '<':
                ret += [('less')]
            elif op ==  '>=':
                ret += [('gre')]
            elif op ==  '<=':
                ret += [('leq')]
        return ret

class Operator1(AST):
    _fields = ['Operator']

class RelationalOperator(AST):
    _fields = ['RelationalOperator']

class Operand1(AST):
    def typeCheck(self):
        if len(self.fields) == 1:
            return True
        else:
            a = self.fields[0].propType()
            b = self.fields[2].propType()
            return  a.equals(b)

    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

    def genCode(self):
        ret = []
        if len(self.fields) == 3:
            op = self.fields[1].fields[0]
            if op == '+':
                ret += [('add')]
            elif op == '-':
                ret += [('sub')]
            else:
                return ret
        return ret

class Operator2(AST):
    def genCode(self):
        ret = []


        return ret

class Operand2(AST):
    def typeCheck(self):
        if len(self.fields) == 1:
            return True
        else:
            a = self.fields[0].propType()
            b = self.fields[2].propType()
            return a.equals(b)

    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

    def genCode(self):
        ret = []
        if len(self.fields) == 3:
            op = self.fields[1]
            if op == '*':
                ret += [('mul')]
            elif op == '/':
                ret += [('div')]
            else:
                ret += [('mod')]
            return ret
        return ret

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
        if self.type is not None:
            return self.type
        elif len(self.fields) == 1:
            self.type = self.fields[0].propType()
            return self.type
        else:
            self.type = self.fields[1].propType()
            return self.type

    def genCode(self):
        ret = []
        if len(self.fields) == 2:
            op = self.fields[1]
            if op == '-':
                ret += [('neg')]
            else:
                ret += [('not')]
            return ret
        return ret

class Operand4(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

    def genCode(self):
        ret  = []
        a  = self.fields[0]
        if isinstance(a,Location):
            loc = self.fields[0].fields[0]
            if not isinstance(loc, AST):
                symbol = AST.semantic.lookInContexts(loc)
                if isinstance(symbol, Symbol):
                    ret += [('ldv', symbol.pos, symbol.count)]

        return ret

class ReferencedLocation(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = Reference(self.fields[0].propType())
            return self.type

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
        a = self.fields[0].propType()
        if len(self.fields) == 2:
            b = self.fields[1].propType()
            return a.equals(b)
        elif self.fields[1] == '&':
            b = self.fields[2].propType()
            return (a.equals(b) and isinstance(b,Chars)) or \
                    (isinstance(a,Chars) and isinstance(b,Char))

        else:
            b = self.fields[2].propType()
            return a.equals(b) and isinstance(a,Int)

    def genCode(self):
        ret = []
        loc = self.fields[0].fields[0]
        if len(self.fields) == 3:
            val = self.fields[0]
            if not isinstance(loc, AST):
                symbol = AST.semantic.lookInContexts(loc)
                if isinstance(symbol, Symbol):
                    ret += [('ldv', symbol.pos, symbol.count)]

            op = self.fields[1]
            if op == '+':
                ret += [('add')]
            elif op == '-':
                ret += [('sub')]
            elif op == '*':
                ret += [('mul')]
            elif op == '/':
                ret += [('div')]
            elif op == '%':
                ret += [('mod')]
            else:
                ret += []

        if not isinstance(loc, AST):
            symbol = AST.semantic.lookInContexts(loc)
            if isinstance(symbol, Symbol):
                ret += [('stv', symbol.pos, symbol.count)]

        return ret

class IfAction(AST):
    def typeCheck(self):
        a = self.fields[0].propType()
        return isinstance(a,Bool)

class ActionStatementList(AST):

    def propType(self):
        if len(self.type) >0:
            return self.type[:]
        else:
            for stmt in self.fields:
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

    def typeCheck(self):
        a = self.fields[1].propType()
        b = self.fields[2].propType()
        if not isinstance(a,Int):
            return False
        elif len(self.fields) == 3:
            return a.equals(b)
        elif len(self.fields) == 4:
            c = self.fields[3].propType()
            if isinstance(self.fields[2],AST):
                return a.equals(b) and b.equals(c)
            else:
                return a.equals(c)
        else:
            c = self.fields[4].propType()
            return a.equals(b) and b.equals(c)


    def updateContext(self):
        AST.semantic.addToContext(Symbol(self.fields[0],Int()))

class RangeEnumeration(AST):

    _fields = ['LoopCounter', 'DiscreteMode']

    def updateContext(self):
        id = self.fields[0]
        AST.semantic.addToContext(Symbol(id,Int()))

class WhileControl(AST):
    def typeCheck(self):
        return self.fields[0].propType() == ['bool']

class CallAction(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

class ProcedureCall(AST):

    def typeCheck(self):
        id = self.fields[0]
        param = Parameters() if len(self.fields) == 1  else self.fields[1].propType()
        symbol = AST.semantic.lookInContexts((id, param.toString()))
        return symbol != None


    def propType(self):
        if self.type is not None:
            return self.type
        else:
            id = self.fields[0]
            param = Parameters() if len(self.fields) == 1  else self.fields[1].propType()
            symbol = AST.semantic.lookInContexts((id,param.toString()))

            if (symbol == None):
                print(tColors.RED + 'Type Error ' + tColors.RESET + '%s '
                      % (self.fields[0]) + tColors.RED + 'not found in' +
                      ' context at ' + tColors.RESET + 'line %s'
                      % (self.linespan[0]))
            else:
                self.type = symbol.getType()
            return self.type

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
        type = self.fields[1].propType()

        if t == 'abs':
            ret = isinstance(type,Int)

        elif t == 'length':
            ret = isinstance(type,Array)

        elif t == 'asc':
            ret = isinstance(type,Int)

        elif t == 'num':
            ret = isinstance(type,Char)

        elif t == 'print' or 'read':
            ret = True
            for parameter in type.getParameterList():
                if not isinstance(parameter,Char) and not isinstance(parameter,Int) \
                    and not isinstance(parameter,Chars) and not isinstance(parameter,Bool):
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
        id = self.fields[0]
        type = self.fields[1].propType()
        s = Symbol(id,type)
        AST.semantic.addToContext(s)
        self.context = AST.semantic.pushContext()

class ProcedureDefinition(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        elif  len(self.fields) == 1:
            self.type  = Procedure(Parameters(),Null())
        elif len(self.fields) == 2:
            if isinstance(self.fields[0],FormalParameterList):
                self.type = Procedure(self.fields[0].propType(),Null())
            else:
                self.type = Procedure(Parameters(),self.fields[0].propType())
        else:
            self.type = Procedure(self.fields[0].propType(),self.fields[1].propType())
        return self.type

class FormalParameterList(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = []
            for x in self.fields:
                self.type += [x.propType()]
            self.type = Parameters(self.type)
            return self.type

class FormalParameter(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = []
            for i in self.fields[0].fields:
                self.type += [self.fields[1].propType()]
            self.type = Parameters(self.type)
            return self.type

    def updateContext(self):
        for id in self.fields[0].fields:
            AST.semantic.addToContext(Symbol(id,
                                  self.fields[1].propType()))

class ParameterSpec(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            if isinstance(self.type,ModeType):
                self.type = self.type.subType
            return self.type

class ResultSpec(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type
