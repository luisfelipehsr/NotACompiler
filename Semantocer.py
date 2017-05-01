class Context(Object):

    def __init__(self,tree):
        self.contextList =[]
        self.currentContext = 0

    def newContext(self):
        self.contextList.append(dict())

    def addToContext(self,id,type):
        if not isIntance(id,List):
            self.contextList[self.currentContext][id] = type
        else:
            for i in id:
                self.contextList[self.currentContext][id] = type

    def getFromContext(self,id):
        return self.contextList[self.currentContext][id]

    def pushContext(self):
        self.currentContext += 1

    def popContext(self):
        self.currentContext -= 1

    def CreateSymbolTable(self):
        return

    def lookInContexts(self,id):
        for a in reversed(range(self.currentContext)):
            if id in self.contextList[a]:
                return self.contextList[a][id]
            else:
                continue
        return []

