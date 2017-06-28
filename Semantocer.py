from symbol import Symbol
from type import *
class Context(object):

    def __init__(self):
        self.contextList = []
        self.contextId = []
        self.memoryCount = []
        self.contextType = []
        self.functionCount = 0
        self.totalContext = 0

    def addToContext(self,symbol,flag=False):
        print('Added %s of type %s of total size %d' %(symbol.id,symbol.type.toString(),symbol.type.getSize()))
        if not isinstance(symbol,Symbol):
            raise TypeError('Only symbols can be added to a context')
        if isinstance(symbol.type,Procedure):
            self.functionCount += 1
            symbol.type.myid = self.functionCount
        self.contextList[-1][symbol.getId()] = symbol
        symbol.count = self.contextId[-1]
        if  symbol.count > 0:
            symbol.pos = self.memoryCount[-1] - 3
            if flag:
                symbol.pos = -self.memoryCount[-1]-3
        else:
            symbol.pos = self.memoryCount[-1]

        print(symbol.count,symbol.pos)
        if not isinstance(symbol.type,Synonym):
            self.memoryCount[-1] += symbol.type.getSize()
        
    def getFromContext(self,id):
        return self.contextList[-1][id]

    def pushContext(self,real='False'):
        self.contextList.append(dict())
        self.contextType.append(real)
        if real == 'True':
            self.contextId.append(self.totalContext)
            self.totalContext += 1
            self.memoryCount.append(0)
        else:
            self.contextId.append(self.contextId[-1])
            self.memoryCount.append(self.memoryCount[-1])
        print('Pushed New Context',real)
        return self.contextList[-1]

    def popContext(self):
        if self.contextType[-1] == 'False':
            aux = self.memoryCount.pop()
            self.memoryCount[-1] = aux
        else:
            self.memoryCount.pop()
        self.contextList.pop()
        self.contextId.pop()
        self.contextType.pop()
        print('Poped Context')

    def lookInContexts(self,id):
        for a in reversed(range(len(self.contextList))):
            if id in self.contextList[a]:
                return self.contextList[a][id]
            else:
                continue
        return None

    def getCurrent(self):
        if len(self.contextList)>0:
            return self.contextList[-1]
        else:
            return None

    def setCurrent(self,ct):
        self.currentContext = ct

    def printContext(self):
        for id in range(len(self.contextList)):
            for item in self.contextList[id]:
                print('%s of type %s in context %d' %(str(item),self.contextList[id][item],id))

    def getCurrentContext(self):
        return len(self.contextList) -1

    def contextLen(self):
        return len(self.contextList)

    def alocatedMemory(self):
        return self.memoryCount[-1]

    def lastMemoryPosition(self):
        return self.alocatedMemory()-1

    def trimToLen(self,l):
        size = len(self.contextList) - l
        for a in range(size):
            self.popContext()

    def getCurrentMemoryCount(self):
        return self.memoryCount[-1]