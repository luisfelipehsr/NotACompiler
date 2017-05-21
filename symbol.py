from type import *
class Symbol(object):
    def __init__(self,id,type,value=None):
        if not isinstance(type,Type):
            raise TypeError('Type %s must be a valide Type-class' %(type))
        if isinstance(type,Procedure):
            self.id = (id,type.getParameters().toString())
            self.type = type.getReturn()
            self.value = None
        else:
            self.id = id
            self.type = type
            self.value = value

    def isConstant(self):
        return self.value == None

    def getType(self):
        return self.type

    def getId(self):
        return self.id

    def getValue(self):
        return self.value