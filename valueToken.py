from type import Type
class ValueToken(object):
    def __init__(self,type,value):
        if isintance(type,Type):
            raise TypeError('type must b of type Type')
        self.type = type
        self.value = value

    def getValue(self):
        return self.value

    def getType(self):
        return self.type