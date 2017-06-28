def solveIf(code):
    stack = []
    if isinstance(code,list):
        i = 0
        while i < len(code):
            inst = code[i]
            if inst[0] == 'start':
                if inst[1] == 'then':
                    stack.append(i)
                elif inst[1] == 'else':
                    add = stack.pop()
                    code[add] = ('jof', i)
                    code[i] = ('nop')
                    continue
                elif inst[1] == 'elsif':
                    add = stack.pop()
                    code[add] = ('jof', i)
                    code[i] = ('nop')
                    continue

            elif inst[0] == 'end':
                if inst[1] == 'if':
                    if len(stack) > 0:
                        add = stack.pop()
                        code[add] = ('jof', i)
                    code[i] = ('nop')
                    continue
            i += 1

def solveIfLinkage(code):
    stack = []
    if isinstance(code, list):
        i = 0
        while i < len(code):
            inst = code[i]
            if inst[0] == 'end' and inst[1] == 'then':
                stack.append(i)
            elif inst[0] == 'end' and inst[1] == 'if':
                for p in stack:
                    code[p] = ('jmp',i)
            i += 1

def solveDoJmpBack(code):
    stack = []
    if isinstance(code,list):
        i = 0
        while i < len(code):
            inst = code[i]
            if inst[0] == 'start':
                if inst[1] == 'condition':
                    stack.append(i)
                    code[i] = ('nop')
                    continue

            if inst[0] == 'end':
                if inst[1] == 'update':
                    code[i] = ('jmp',stack.pop())
            i+= 1

def solveDoJmpOut(code):
    stack = []
    if isinstance(code, list):
        i = 0
        while i < len(code):
            inst = code[i]
            if inst[0] == 'end' and inst[1] == 'condition':
                stack.append(i)
            elif inst[0] == 'end' and inst[1] == 'do':
                add = stack.pop()
                code[add] = ('jof',i)
                code[i] = ('nop')
                continue
            i+= 1

def solveDoCleanUp(code):
    if isinstance(code, list):
        i = 0
        while i < len(code):
            inst = code[i]
            if (inst[0] == 'start' and (inst[1] == 'update' or inst[1] == 'do' or inst[1] == 'if'))\
                    or inst[0] == 'end' and (inst[1] == 'else' or inst[1] == 'elsif'):
                code.pop(i)
                continue
            i += 1

def solveDo(code):
    solveDoJmpBack(code)
    solveDoJmpOut(code)

def solveProcedure(code):
    stack = []
    if isinstance(code, list):
        i = 0
        while i < len(code):
            inst = code[i]
            if inst[0] == 'start' and inst[1] == 'procedure':
                stack.append(i)
            elif inst[0] == 'end' and inst[1] == 'procedure':
                code[i] = ('nop')
                code[stack.pop()] = ('jmp',i)
                continue
            i += 1

def linkProcedure(code):
    d = dict()
    if isinstance(code, list):
        i = 0
        while i < len(code):
            inst = code[i]
            if inst[0] == 'start' and inst[1] == 'procedure':
                d[inst[2]] = i+1
            elif inst[0] == 'procedure' and inst[1] == 'call':
                code[i] = ('cfu', d[inst[2]])
            i += 1

def returnProcedure(code):
    stack = []
    if isinstance(code, list):
        i = 0
        while i < len(code):
            inst = code[i]
            if inst[0] == 'return' and inst[1] == 'to':
                stack.append(i)
            elif inst[0] == 'return' and inst[1] == 'here':
                for p in stack:
                    code[p] = ('jmp', i)
                code.pop(i)
                continue
            i += 1

def fix(code):
    for i in range(len(code)):
        if isinstance(code[i],tuple):
            code[i] = list(code[i])
        else:
            code[i] = [code[i]]

def solve(code):
    solveDoCleanUp(code)
    solveIfLinkage(code)
    solveIf(code)
    solveDo(code)
    returnProcedure(code)
    linkProcedure(code)
    solveProcedure(code)
    fix(code)