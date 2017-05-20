class Type(object):

    def __init__(self):
        self.string = ''

    def toString(self):
        return self.string

    def equals(self,t):
        return isinstance(t,self.__class__)

    def isConstant():
        return isConstant()

class Int(Type):
    def __init__(self):
        self.string = 'Int'

class Bool(Type):
    def __init__(self):
        self.string = 'Bool'

class Char(Type):
    def __init__(self):
        self.string = 'Char'

class Chars(Type):
    def __init__(self,r):
        self.subType = Char()
        self.range = r
        self.string = 'Chars'

    def getRange(self):
        return self.range

    def getSubType(self):
        return self.subType

    def toString(self):
        return  self.string + ' ' + self.range.toString()

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
    def __init__(self,begin,end):
        if  not isinstance(begin,int) or not isinstance(end,int):
            raise TypeError('Begin %s and End %s must be integers' %(begin,end))
        self.begin = begin
        self.end = end
        self.string = 'Range[%d:%d]' % (begin,end)

    def getBegin(self):
        return self.begin

    def getEnd(self):
        return self.end

    def getSize(self):
        return self.end - self.begin

    def equals(self,t):
        if isinstance(t,Range):
            return begin == t.begin and end == t.end
        return False

class Parameters(Type):
    def __init__(self,*plist):
        self.parameterList = list(plist)
        for a in self.parameterList:
            if not isinstance(a,Type):
                raise TypeError('All elements must be of type Type' %(a))

    def getParameter(self,pos):
        return self.parameterList[pos]

    def getParameterList(self):
        return self.parameterList

    def toString(self):
        ret = '( '
        for t in self.parameterList:
            ret += t.toString() + ' '
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
        if not isintance(t,Type):
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

class Null(Type):
    def __init__(self):
        self.string = 'Null'

def main():
    t = Procedure(Parameters(Int(),Int()),Int())
    y = Procedure(Parameters(Int(), Int()),Null())
    print(t.equals(y))

if __name__	=='__main__':main()