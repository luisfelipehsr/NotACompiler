import pydot as dot
import uuid
import copy
from type import *
from symbol import Symbol

class tColors:
    RED = "\033[1;31m"
    YELLOW = '\033[93m'
    RESET = '\033[0m'

class AST(object):
    semantic = None
    stringLiterals = None

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
        label = self.__class__.__name__ + ' ['
        if self.type is not None:
            label += 'Type= ' + str(self.type.toString()) + ' '
        if isinstance(self.type,Int):
            label += 'Value= ' + str(self.type.value)
        label += ']'

        graph.add_node(dot.Node(myId,label = label))
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
        ret += self.addTag()
        for n in self.fields:
            if isinstance(n,AST):
                ret += n.recursiveGenCode()
        ret += self.genCode()
        AST.semantic.trimToLen(leng)
        return ret

    def addStringLiteral(self, stringToBeAdded):
        AST.stringLiterals += [stringToBeAdded]
        return len(AST.stringLiterals) - 1


    def typeCheck(self):
        return True

    def propType(self):
        return self.type

    def updateContext(self):
        return

    def genCode(self):
        return []

    def addTag(self):
        return []


class Program(AST):
    def updateContext(self):
        self.context = AST.semantic.pushContext()

    def addTag(self):
        return [('stp')]

    def genCode(self):
        return [('end')]

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
            if isinstance(t2,Synonym):
                t2 = t2.subType
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
        if len(self.fields) == 3:
            type = self.fields[2].propType()
        else:
            type = self.fields[1].propType()
        if isinstance(type,ModeType):
            type = type.subType
        for id in self.fields[0].fields:
            AST.semantic.addToContext(Symbol(id,type))

    def genCode(self):
        ret = []
        type = self.fields[1].propType()
        if isinstance(type, ModeType) or isinstance(type,Synonym):
            type = type.subType
        first = True
        for id in self.fields[0].fields:
            if len(self.fields) == 2:
                ret += [('alc',self.propType().getSize())]
            else:
                v = self.fields[2].propType()
                if isinstance(v,Synonym):
                    v = v.subType
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
        expression = self.fields[-1].propType()
        if expression.value is None:
            return False
        if len(self.fields) == 3:
            mode = self.fields[1].propType()
            if isinstance(mode,ModeType):
                mode = mode.subType
            if mode.equals(expression):
                return True
        else:
            return True

    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = Synonym(self.fields[-1].propType())
            return self.type

    def updateContext(self):
        identifiers = self.fields[0].fields
        type = self.propType()
        for id in identifiers:
            AST.semantic.addToContext(Symbol(id,type))

    def recursiveGenCode(self):
        self.updateContext()
        return []

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

    def recursiveGenCode(self):
        return []

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
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            type = self.fields[1].propType()
            range = self.fields[0].propType()
            self.type = Array(type,range)
            return self.type

    def recursiveGenCode(self):
        return []

class IndexModeList(AST):
    def propType(self):
        for i in range(len(self.fields)-1):
            if isinstance(self.fields[i].propType(),Range):
                self.fields[i].propType().subRange = self.fields[i+1].propType()
        self.type = self.fields[0].propType()
        return self.type

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
            if fromContext is None:
                self.type = None
                print(tColors.RED + 'Type Error ' + tColors.RESET + '%s '
                      % (self.fields[0]) + tColors.RED + 'not found in ' +
                      'context at ' + tColors.RESET + 'line %s'
                      % (self.linespan[0]))

                return self.type
            else:
                self.type = copy.deepcopy(fromContext.type)
                if hasattr(self.type,'value') and not isinstance(self.type,Synonym):
                    self.type.value = None
                return self.type

    def store(self):
        ret = []
        loc = self.fields[0]
        symbol = AST.semantic.lookInContexts(loc)
        if not isinstance(loc, AST):
            if isinstance(symbol.type, Array):
                ret += [('ldr',symbol.count,symbol.pos)]
                ret += [('smv',symbol.type.getRange().getCount())]
            else:
                ret += [('stv', symbol.count, symbol.pos)]
        else:
            ret += loc.store()
        return ret

    def load(self):
        ret = []
        loc = self.fields[0]
        if not isinstance(loc,AST):
            symbol = AST.semantic.lookInContexts(loc)
            if isinstance(symbol.type,Array):
                ret += [('ldr',symbol.count,symbol.pos)]
                ret += [('lmv',symbol.type.getRange().getCount())]
            elif not isinstance(symbol.type,Synonym):
                ret += [('ldv',symbol.count,symbol.pos)]
            else:
                ret += [('ldc', symbol.type.subType.value)]
        else:
            print(type(loc))
            ret += loc.load()
        return ret

    def reference(self):
        ret = []
        loc = self.fields[0]
        if not isinstance(loc, AST):
            symbol = AST.semantic.lookInContexts(loc)
            ret += [('ldr', symbol.count,symbol.pos)]
        else:
            ret += loc.reference()
        return ret

class DereferencedReference(AST):
    def typeCheck(self):
        a = self.fields[0].propType()
        return isinstance(a,Reference)

    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType().getSubType()
            return self.type

    def store(self):
        loc = self.fields[0]
        ret = [('grc')]
        ret += loc.store()
        return ret

    def load(self):
        loc = self.fields[0]
        ret = [('grc')]
        ret += loc.store()
        return ret

class StringSlice(AST):
    def typeCheck(self):
        mode = self.fields[0].propType()
        exprx = self.fields[1].propType()
        expry = self.fields[2].propType()
        if isinstance(mode,Chars) and isinstance(exprx,Int) and isinstance(expry,Int):
            return exprx.isConstant() and expry.isConstant()
        else:
            return False

    def propType(self):
        if self.type is not None:
            return self.type
        else:
            exprx = self.fields[1].propType()
            expry = self.fields[2].propType()
            ret = Chars(Range(exprx.value,expry.value))
            return self.type

class ArrayElement(AST):
    def typeCheck(self):
        parameters = self.fields[1].propType().getParameterList()
        data = self.fields[0].propType()
        if not isinstance(data,Chars) and not isinstance(data,Array):
            return False
        for p in parameters:
            if not isinstance(p,Int):
                return False
        if len(parameters) > data.getRange().numberOfRanges():
            return False
        return True

    def propType(self):
        if self.type is not None:
            return self.type
        elif isinstance(type,Chars):
            self.type = Char()
        else:
            parameters = self.fields[1].propType().getParameterList()
            self.type = copy.deepcopy(self.fields[0].propType())
            for paran in parameters:
                self.type.range = self.type.range.subRange
            if self.type.range is None:
                self.type = self.type.subType
        return self.type

    def store(self):
        ret = []
        location = self.fields[0].reference()
        locationType = self.fields[0].propType()
        expressionList = self.fields[1].fields
        ret += location
        rng = locationType.range
        val = 1
        for expression in expressionList:
            ret += expression.recursiveGenCode()
            if rng.begin.value != 0:
                ret += [('ldc',rng.begin.value)]
                ret += [('sub')]
            ret += [('idx', locationType.subType.getSize() * val)]
            val = rng.getLenght()
            rng = rng.subRange
        ret += [('smv', 1)]
        return ret

    def load(self):
        ret = []
        location = self.fields[0].reference()
        locationType = self.fields[0].propType()
        expressionList = self.fields[1].fields
        ret += location
        rng = locationType.range
        val = 1
        for expression in expressionList:
            ret += expression.recursiveGenCode()
            if rng.begin.value != 0:
                ret += [('ldc',rng.begin.value)]
                ret += [('sub')]
            ret += [('idx', locationType.subType.getSize() * val)]
            val = rng.getLenght()
            rng = rng.subRange
        ret += [('grc')]
        return ret

    def reference(self):
        ret = []
        location = self.fields[0].reference()
        locationType = self.fields[0].propType()
        expressionList = self.fields[1].fields
        ret += location
        rng = locationType.range
        val = 1
        for expression in expressionList:
            ret += expression.recursiveGenCode()
            if rng.begin != 0:
                ret += [('ldc',rng.begin)]
                ret += [('sub')]
            ret += [('idx', locationType.subType.getSize() * val)]
            val = rng.getLenght()
            rng = rng.subRange
        return ret

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
        mode = self.fields[0].propType()
        exprx = self.fields[1].propType()
        expry = self.fields[2].propType()
        if isinstance(mode,Array) and isinstance(exprx,Int) and isinstance(expry,Int):
            return exprx.isConstant() and expry.isConstant()
        else:
            return False

    def propType(self):

        if self.type is not None:
            return self.type
        else:
            mode = self.fields[0].propType()
            exprx = self.fields[1].propType()
            expry = self.fields[2].propType()
            ret = Array(mode.subType,Range(exprx.value,expry.value,subRange=mode.range.subRange))
            self.type = ret
            return ret

    def load(self):
        ret = []
        location = self.fields[0].reference()
        locationType = self.fields[0].propType()
        exprx = self.fields[1].propType().value
        expry = self.fields[2].propType().value
        k = exprx - expry
        rng = locationType.range
        ret += location
        ret += [('ldc', exprx)]
        if rng.begin.value != 0:
            ret += [('ldc', rng.begin.value)]
            ret += [('sub')]
        ret += [('idx', locationType.subType.getSize())]
        ret += [('lmv',k)]

    def store(self):
        ret = []
        location = self.fields[0].reference()
        locationType = self.fields[0].propType()
        exprx = self.fields[1].propType().value
        expry = self.fields[2].propType().value
        k = exprx - expry
        rng = locationType.range
        ret += location
        ret += [('ldc', exprx)]
        if rng.begin.value != 0:
            ret += [('ldc', rng.begin.value)]
            ret += [('sub')]
        ret += [('idx', locationType.subType.getSize())]
        ret += [('smv', k)]

    def reference(self):
        ret = []
        location = self.fields[0].reference()
        locationType = self.fields[0].propType()
        exprx = self.fields[1].propType().value
        expry = self.fields[2].propType().value
        k = exprx - expry
        rng = locationType.range
        ret += location
        ret += [('ldc', exprx)]
        if rng.begin.value != 0:
            ret += [('ldc', rng.begin.value)]
            ret += [('sub')]
        ret += [('idx', locationType.subType.getSize())]

class PrimitiveValue(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

    def load(self):
        return []

    def reference(self):
        print(tColors.RED +'Cant find reference to PrimitiveValue',self.linespan)
        return []

    def recursiveGenCode(self):
        loc = self.fields[0]
        return loc.recursiveGenCode()

class Literal(AST):
    def propType(self):
        token = self.fields[0]
        if isinstance(token,Type):
            self.type = token
        return self.type

    def genCode(self):
        ret = []
        val = self.propType()
        if isinstance(val,Chars): # Caso de string constante salva em H
            #k = AST.addStringLiteral(self, val.value)
            #print(k, AST.stringLiterals[k])
            #ret += [('sts', k)]
            ret = []
        elif isinstance(val,Bool):
            ret += [('ldc',val.value)]
        elif isinstance(val,Char):
            ret += [('ldc', val.value)]
        elif isinstance(val,Int):
            ret += [('ldc',val.value)]
        return ret

class ValueArrayElement(AST):
    def typeCheck(self):
        return  self.fields[1].propType() == ['int'] and self.fields[0].propType()[0] == 'array'

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

    def recursiveGenCode(self):
        type = self.propType()
        # if isinstance(type,Int) or isinstance(type,Char) or isinstance(type,Bool):
        #     if type.isConstant():
        #         return []
        return self.fields[0].recursiveGenCode()

    def reference(self):
        return self.fields[0].reference()

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
                return b.equals(c) and b.equals(d)
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

                if operand0Type.equals(operand1Type):

                    operator = operatorType.fields[0]

                    if operator in ['&&', '||']:
                        if isinstance(operand0Type,Bool):
                            return True
                        else:
                            print('Operands must be of type bool. Got %s:'
                                  %(operand0Type))
                            return False

                    elif operator in ['==','!=']:
                        if isinstance(operand0Type,Int) or isinstance(operand0Type,Bool) or isinstance(operand0Type,Char):
                            return True
                        else:
                            print('Operands must be of type bool,int or Char. Got' +
                                  '%s:' %(operand0Type))
                            return False

                    else:
                        if isinstance(operand0Type,Int):
                            return True
                        else:
                            print('Operands must be of type int. Got %s:'
                                  %(operand0Type))
                            return False

                else:
                    print('Both operands must be of same type:')
                    return False

            else:

                if operand1Type is None:
                    return False

                if isinstance(operand1Type,Array):
                    if operand1Type.subType.equals(operand0Type):
                        return True
                    else:
                        print('Expected first operand of type %s. Got %s:'
                               %(operand1Type[1:],operand0Type))
                        return False

                elif isinstance(operand1Type,Chars):
                    if isinstance(operand0Type,Char):
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

    def reference(self):
        if len(self.fields) == 1:
            return self.fields[0].reference()
        else:
            print(tColors.RED +'Code generation Error cant find reference to expression',self.linespan)
            return []

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
            val1 = self.fields[0].propType()
            if len(self.fields) == 3:
                op = self.fields[1].fields[0]
                val2 = self.fields[2].propType()
                if isinstance(val1,Int) and isinstance(val2,Int):
                    if val1.isConstant() and val2.isConstant():
                        if op == '+':
                            self.type = Int(val1.value + val2.value)
                        else:
                            self.type = Int(val1.value - val2.value)
                    else:
                        self.type = Int()
                else:
                    if val1.isConstant:
                        self.type = val2
                    else:
                        self.type = val1

            else:
                self.type = val1
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

    def reference(self):
        if len(self.fields) == 1:
            return self.fields[0].reference()
        else:
            print(tColors.RED +'Code generation Error cant find reference to expression',self.linespan)
            return []

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
            return a.equals(b) and isinstance(a,Int)

    def propType(self):
        if self.type is not None:
            return self.type
        else:
            op1 = self.fields[0].propType()
            op1 = op1.subType if isinstance(op1,Synonym) else op1
            if len(self. fields) == 3:
                op2 = self.fields[2].propType()
                op2 = op2.subType if isinstance(op2, Synonym) else op2
                if op1.isConstant() and op2.isConstant():
                    op = self.fields[1]
                    self.type = Int()
                    if op == '*':
                        self.type.value  = op1.value * op2.value
                    elif op == '/':
                        self.type.value = op1.value / op2.value
                    else:
                        self.type.value = op1.value % op2.value
                else:
                    self.type = Int(None)
            else:
                self.type = op1
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

    def reference(self):
        if len(self.fields) == 1:
            return self.fields[0].reference()
        else:
            print(tColors.RED +'Code generation Error cant find reference to expression',self.linespan)
            return []

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

    def reference(self):
        if len(self.fields) == 1:
            return self.fields[0].reference()
        else:
            print(tColors.RED +'Code generation Error cant find reference to expression',self.linespan)
            return []

class Operand4(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

    def recursiveGenCode(self):
        loc = self.fields[0]
        if isinstance(loc,Location):
            return loc.load()
        return loc.recursiveGenCode()

    def reference(self):
        if len(self.fields) == 1:
            return self.fields[0].reference()
        else:
            print(tColors.RED +'Code generation Error cant find reference to expression',self.linespan)
            return []

class ReferencedLocation(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = Reference(self.fields[0].propType())
            return self.type

    def recursiveGenCode(self):
        ret = []
        loc = self.fields[0]
        ret += loc.reference()
        return ret

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

    def operation(self):
        if len(self.fields) != 3:
            return []
        else:
            op = self.fields[1]
            if op == '+':
                return [('add')]
            elif op == '-':
                return [('sub')]
            elif op == '*':
                return [('mul')]
            elif op == '/':
                return [('div')]
            elif op == '%':
                return [('mod')]
            else:
                return []

    def recursiveGenCode(self):
        locStore = self.fields[0].store()
        expression = self.fields[-1].recursiveGenCode()
        ret = []
        if len(self.fields) == 3:
            locLoad = self.fields[0].load()
            operation = self.operation()
            ret += locStore[:-1] + locLoad + expression + operation + [locStore[-1]]
        else:
            ret += locStore[:-1] + expression + [locStore[-1]]
        return ret

class IfAction(AST):
    def typeCheck(self):
        a = self.fields[0].propType()
        return isinstance(a,Bool)

    def addTag(self):
        return [('start','if')]

    def genCode(self):
        return [('end','if')]

class ActionStatementList(AST):

    def propType(self):
        if len(self.type) >0:
            return self.type[:]
        else:
            for stmt in self.fields:
                self.type += [stmt.propType()]
            return self.type[:]

class ThenClause(AST):
    def addTag(self):
        return [('start','then')]
    def genCode(self):
        return [('end','then')]

class ElseClause(AST):
    def typeCheck(self):
        if len(self.fields) != 1:
            return isinstance(self.fields[0].propType(),Bool)
        else:
            return True

    def addTag(self):
        return [('start','else')]

    def genCode(self):
        return [('end','else')]

class DoAction(AST):
    def updateContext(self):
        self.context = AST.semantic.pushContext()

    def recursiveGenCode(self):
        l = AST.semantic.contextLen()
        ret = []
        ret += [('start','do')]
        if len(self.fields) == 1:
            ret += self.fields[0].recursiveGenCode()
        else:
            control = self.fields[0]
            code = self.fields[1]
            ret += control.initialization()
            ret += [('start','condition')]
            ret += control.condition()
            ret += [('end', 'condition')]
            ret += code.recursiveGenCode()
            ret += [('start', 'update')]
            ret += control.update()
            ret += [('end', 'update')]
        ret += [('end','do')]
        AST.semantic.trimToLen(l)
        return ret

class ControlPart(AST):
    def initialization(self):
        first = self.fields[0]
        if isinstance(first,ForControl):
            return first.initialization()
        return []

    def condition(self):
        ret = []
        ret += self.fields[0].condition()
        if len(self.fields) == 2:
            ret += self.fields[1].condition()
            ret += [('and')]
        return ret

    def update(self):
        first = self.fields[0]
        if isinstance(first, ForControl):
            return first.update()
        return []

    def recursiveGenCode(self):
        return []

class ForControl(AST):
    # def addTag(self):
    #     return [('start','for')]
    #
    # def genCode(self):
    #     ret = []
    #     ret += [('end','for')]
    #     return ret

    def initialization(self):
        return self.fields[0].initialization()

    def condition(self):
        return self.fields[0].condition()

    def update(self):
        return self.fields[0].update()

    def recursiveGenCode(self):
        return []

class Iteration(AST):

    def initialization(self):
        return self.fields[0].initialization()

    def condition(self):
        return self.fields[0].condition()

    def update(self):
        return self.fields[0].update()

    def recursiveGenCode(self):
        return []

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

    def initialization(self):
        self.updateContext()
        init = self.fields[1]
        iniVal = init.propType().value
        if  iniVal is not None:
            return [('ldc',iniVal)]
        return self.fields[1].genCode()

    def condition(self):
        id = self.fields[0]
        max  = self.fields[-1]
        maxVal = max.propType().value
        id = AST.semantic.lookInContexts(id)
        ret = []
        ret += [('ldv',id.count,id.pos)]
        if maxVal is not None:
            ret += [('ldc',maxVal)]
        else:
            ret += max.genCode()
        ret += ['neq']
        return ret

    def update(self):
        ret = []
        id = AST.semantic.lookInContexts(self.fields[0])
        if len(self.fields) == 3:
            ret += [('ldv', id.count, id.pos)]
            ret += [('ldc', 1)]
            ret += [('add')]
            ret += [('stv',id.count,id.pos)]
        elif len(self.fields) == 4:
            if self.fields[2] == 'down':
                ret += [('ldv', id.count, id.pos)]
                ret += [('ldc', 1)]
                ret += [('sub')]
                ret += [('stv', id.count, id.pos)]
            else:
                ret += [('ldv', id.count, id.pos)]
                ret += self.fields[2].genCode()
                ret += [('add')]
                ret += [('stv', id.count, id.pos)]
        else:
            ret += [('ldv', id.count, id.pos)]
            ret += self.fields[2].genCode()
            ret += [('sub')]
            ret += [('stv', id.count, id.pos)]
        return ret

    def recursiveGenCode(self):
        return []

    def updateContext(self):
        AST.semantic.addToContext(Symbol(self.fields[0],Int()))

class RangeEnumeration(AST):

    _fields = ['LoopCounter', 'DiscreteMode']

    def updateContext(self):
        id = self.fields[0]
        AST.semantic.addToContext(Symbol(id,Int()))

class WhileControl(AST):

    def typeCheck(self):
        return isinstance(self.fields[0].propType(),Bool)

    def condition(self):
        return self.fields[0].genCode()

    def recursiveGenCode(self):
        return []

class CallAction(AST):
    def propType(self):
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

    #TODO terminar
    def load(self):
        return []

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

            if symbol is None:
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
            if self.type is None:
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
        if self.type is not None:
            return self.type
        else:
            self.type = self.fields[0].propType()
            return self.type

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

    def genCode(self):
        ret = []
        name = self.fields[0].fields[0]
        parameterList = self.fields[1].propType().getParameterList()
        #TODO mais opcoes de print, prt, prc, prs
        if name == 'print':
            for pType in parameterList:
                if isinstance(pType,Int) or isinstance(pType,Bool):
                    ret += [('prv', 'False')]
                elif isinstance(pType,Char):
                    ret += [('prv', 'True')]
                elif isinstance(pType,Chars):
                    if pType.value is None:
                        ret += [('prs')]
                    else:
                        i = AST.addStringLiteral(self, pType.value)
                        print(i, pType.value)
                        ret += [('prc', i)]
            ret += [('prc', 0)]

        if name == 'read':
            for pType in parameterList:
                if isinstance(pType, Int) or isinstance(pType, Bool)\
                        or isinstance(pType, Char):
                    ret += [('rdv')]
                elif isinstance(pType, Chars):
                    ret += [('rds')]
                else:
                    print(tColors.RED + "ERROR: Couldn't match a type for para"
                        + "meter in read built-in call")
            ret += [('smv',len(parameterList))]

        #TODO talvez LOWER E UPPER. retornar indice do prim e ultm cara de array

        return ret

    def recursiveGenCode(self):
        ret = []
        name = self.fields[0].fields[0]
        parameterList = self.fields[1].fields
        for n in reversed(parameterList):
            if isinstance(n, AST):
                if name == 'read':
                    ret += n.reference()
                else:
                    ret += n.recursiveGenCode()
        ret += self.genCode()
        return ret

class BuiltinName(AST):

    def propType(self):
        t = self.fields[0]
        if t == 'abs':
            self.type = Int()
        elif t == 'read':
            self.type = None
        elif t == 'length':
            self.type = Int()
        elif t == 'print':
            self.type = None
        elif t == 'asc':
            self.type = Char
        elif t == 'upper':
            self.type = Int()
        elif t == 'lower':
            self.type = Int()
        elif t == 'num':
            self.type = Int()
        return self.type

class ProcedureStatement(AST):
    def updateContext(self):
        id = self.fields[0]
        type = self.fields[1].propType()
        s = Symbol(id,type)
        AST.semantic.addToContext(s)
        self.context = AST.semantic.pushContext()

    def addTag(self):
        k = self.fields[1].propType().myid
        ret = []
        ret += [('start', 'procedure')]
        ret += [('enf', k)]
        return ret

    def genCode(self):
        procedure = self.fields[1].propType()
        parameterSize = procedure.parameters.getSize()
        menCount = AST.semantic.getCurrentMemoryCount()
        ret = []
        ret += [('dlc', menCount - parameterSize)]
        ret += [('ret', procedure.myid, parameterSize)]
        return ret

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
