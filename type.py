class Type(object):
    string = ''

    def toString(self):
        return self.string

    def equals(self,t):
        return isinstance(t,self.__class__)

    def getSize(self):
        return 1

class Int(Type):
    def __init__(self,value = None):
        self.string = 'Int'
        self.value = value

    def isConstant(self):
        return self.value is not None

class Bool(Type):
    def __init__(self,value = None):
        self.string = 'Bool'
        self.value = value

    def isConstant(self):
        return not self.value is not None

class Char(Type):
    def __init__(self,value = None):
        self.string = 'Char'
        self.value = value

    def isConstant(self):
        return self.value is not None

class Chars(Type):
    def __init__(self,r,value = None):
        self.subType = Char()
        self.range = r
        self.value = value
        self.string = 'Chars'

    def getRange(self):
        return self.range

    def getSubType(self):
        return self.subType

    def toString(self):
        return  self.string + ' ' + self.range.toString()

    def getSize(self):
        return self.range.getSize()

    def equals(self,t):
        if isinstance(t,Chars):
            return self.range.equals(t.getRange())
        return False

class Array(Type):
    def __init__(self,t,r):
        if not isinstance(t,Type) or not isinstance(r,Range):
            raise TypeError('t %s must be of type Type, r  %s must be of type Range' % (t,r))

        self.subType = t
        self.range = r
        self.string = 'Array'

    def getSubType(self):
        return self.subType

    def getRange(self):
        return self.range

    def getSize(self):
        return self.range.getCount() * self.subType.getSize()

    def toString(self):
        return self.string + ' ' + self.range.toString() + ' ' + self.subType.toString()

    def equals(self,t):
        if isinstance(t,Array):
            return self.subType.equals(t.getSubType())
        return False

class Procedure(Type):
    def __init__ (self,param,ret):
        if not isinstance(param,Parameters) or not isinstance(ret,Type):
            raise TypeError('param %s must be of type Param and ret %s must be of type Type' %(param,ret))
        self.parameters = param
        self.ret = ret
        self.string = 'Procedure'

    def getParameters(self):
        return self.parameters

    def getReturn(self):
        return self.ret

    def toString(self):
        return self.string + ' ' + self.parameters.toString() + ' Returns ' + self.ret.toString()

    def equals(self,t):
        if isinstance(t,Procedure):
            return self.ret.equals(t.getReturn()) and self.parameters.equals(t.getParameters())

class Range(Type):
    def __init__(self,begin,end,subRange=None):
        if  not isinstance(begin,Int) or not isinstance(end,Int):
            raise TypeError('Begin %s and End %s must be integers' %(begin,end))
        if not isinstance(subRange,Range) and subRange is not None:
            raise TypeError('SubType must be None or Range')
        self.begin = begin
        self.end = end
        self.subRange = subRange
        self.string = 'Range[%s:%s]' % (begin.toString(),end.toString())

    def getBegin(self):
        return self.begin

    def getEnd(self):
        return self.end

    def getLenght(self):
        if(self.end.value is not None and self.begin.value is not None):
            return (self.end.value - self.begin.value)

    def getCount(self):
        return self.getLenght() if self.subRange == None else self.getLenght() * self.subRange.getCount()

    def numberOfRanges(self):
        return 1 if self.subRange is None else 1 + self.subRange.numberOfRanges()

    def equals(self,t):
        if isinstance(t,Range):
            return self.begin == t.begin and self.end == t.end
        return False

    def toString(self):
        if self.subRange is not None:
            return self.string + ' ' +self.subRange.toString()
        else:
            return self.string

class Parameters(Type):
    def __init__(self, plist=None):
        if plist is None:
            plist = []

        self.parameterList = []
        for a in plist:
            if isinstance(a,Parameters):
                self.parameterList += a.parameterList
            elif not isinstance(a,Type) and a is not None:
                raise TypeError('All elements %s must be of type Type' %(str(a)))
            else:
                self.parameterList.append(a)

    def getParameter(self,pos):
        return self.parameterList[pos]

    def getParameterList(self):
        return self.parameterList

    def toString(self):
        ret = '( '
        for t in self.parameterList:
            ret += t.toString() if t is not None else 'None'
            ret += ' '
        ret+= ')'
        return ret

    def equals(self,t):
        if isinstance(t,Parameters):
            if len(self.parameterList) == len(t.getParameterList()):
                for i in range(len(self.parameterList)):
                    if not self.parameterList[i].equals(t.getParameterList()[i]):
                        return False
            return True
        return False

class Reference(Type):
    def __init__(self,t):
        if not isinstance(t,Type):
            raise TypeError('t %s must be of type Type' %(t))
        self.subType = t
        self.string = 'Ref'

    def getSubType(self):
        return self.subType

    def toString(self):
        return self.string + ' ' + self.subType.toString()

    def equals(self,t):
        if isinstance(t,Reference):
            return self.subType.equals(t.subType)

class ModeType(Type):
    def __init__(self, t):
        if not isinstance(t, Type):
            raise TypeError('t %s must be of type Type' % (t))
        self.subType = t
        self.string = 'Mode'

    def getSubType(self):
        return self.subType

    def toString(self):
        return self.string + ' ' + self.subType.toString()

    def equals(self,t):
        if isinstance(t,Reference):
            return self.subType.equals(t.subType)

    def getSize(self):
        return self.subType.getSize()

class Null(Type):
    def __init__(self):
        self.string = 'Null'

class Synonym(Type):
    def __init__(self,t):
        if not isinstance(t,Int) and not isinstance(t,Char) and not isinstance(t,Bool):
            raise TypeError('t %s must be of type Char or Int' %(t))
        self.subType = t
        self.string = 'Syn'


def main():
    #t = Procedure(Parameters(Int(),Int()),Int())
    #y = Procedure(Parameters(Int(), Int()),Null())
    #print(t.equals(y))
    print("TODO")

if __name__	=='__main__':main()