from type import *
class Symbol(object):
    def __init__(self,id,type):
        if not isinstance(type,Type):
            raise TypeError('Type %s must be a valid Type-class' %(type))
        if isinstance(type,Procedure):
            self.id = (id,type.getParameters().toString())
            self.type = type.getReturn()
            self.parameters = type.getParameters()
        else:
            self.id = id
            self.type = type
            self.parameters = None
        self.count = 0
        self.pos = 0

    def getType(self):
        return self.type

    def getId(self):
        return self.id

    def getParameters(self):
        return self.parameters