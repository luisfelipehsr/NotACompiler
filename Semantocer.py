from symbol import Symbol

class Context(object):

    def __init__(self):
        self.contextList =[]

    def addToContext(self,symbol):
        #print('Added %s of type %s' %(symbol.id,symbol.type.toString()))
        if not isinstance(symbol,Symbol):
            raise TypeError('Only symbols can be added to a context')
        self.contextList[-1][symbol.getId()] = symbol
        
    def getFromContext(self,id):
        return self.contextList[-1][id]

    def pushContext(self):
        self.contextList.append(dict())
        #print('Pushed New Context')
        return self.contextList[-1]

    def popContext(self):
        self.contextList.pop()
        #print('Poped Context')

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

    def contextLen(self):
        return len(self.contextList)

    def trimToLen(self,l):
        size = len(self.contextList) - l
        for a in range(size):
            self.popContext()
