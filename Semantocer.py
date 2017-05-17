class Context(object):

    def __init__(self):
        self.contextList =[]

    def addToContext(self,id,type):
        #print('Adding %s of type %s to context %d' %(id,type,len(self.contextList)))
        if not isinstance(id,list):
            self.contextList[-1][id] = type
        else:
            for i in id:
                self.contextList[-1][i] = type
        

    def getFromContext(self,id):
        return self.contextList[-1][id]

    def pushContext(self):
        self.contextList.append(dict())
        #print('Pushed New Context')
        return self.context[-1]

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
