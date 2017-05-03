class Context(object):

    def __init__(self):
        self.contextList =[]
        self.currentContext = 0

    def newContext(self):
        #print('Creating new context')
        self.contextList.append(dict())

    def addToContext(self,id,type):
        #print('Adding %s of type %s to context %d' %(id,type,self.currentContext))
        if not isinstance(id,list):
            self.contextList[self.currentContext][id] = type
        else:
            for i in id:
                self.contextList[self.currentContext][i] = type

    def getFromContext(self,id):
        return self.contextList[self.currentContext][id]

    def pushContext(self):
        self.currentContext += 1
        #print('Current Context is now %d' % (self.currentContext))

    def popContext(self):
        self.currentContext -= 1
        #print('Current Context is now %d' % (self.currentContext))

    def lookInContexts(self,id):
        for a in reversed(range(self.currentContext)):
            if id in self.contextList[a]:
                return self.contextList[a][id]
            else:
                continue
        return []

    def getCurrent(self):
        return self.currentContext

    def setCurrent(self,ct):
        self.currentContext = ct
        #print('Current Context is now %d' % (self.currentContext))

    def printContext(self):
        for id in range(len(self.contextList)):
            for item in self.contextList[id]:
                print('%s of type %s in context %d' %(str(item),self.contextList[id][item],id))
