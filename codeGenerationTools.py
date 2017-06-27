def solveIf(code):
    stack = []
    if isinstance(code,list):
        i = 0
        while i < len(code):
            inst = code[i]
            if inst[0] == 'start':
                if inst[1] == 'if':
                    code.pop(i)
                    continue
                elif inst[1] == 'then':
                    stack.append(i)
            elif inst[0] == 'end':
                if inst[1] == 'if':
                    code.pop(i)
                    continue
                elif inst[1] == 'then':
                    add = stack.pop()
                    code[add] = ('jof',i)
                    code.pop(i)
                    continue
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
                    code.pop(i)
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
                code.pop(i)
                continue
            i+= 1

def solveDoCleanUp(code):
    if isinstance(code, list):
        i = 0
        while i < len(code):
            inst = code[i]
            if inst[0] == 'start' and (inst[1] == 'update' or inst[1] == 'do'):
                code.pop(i)
                continue
            i += 1

def solveDo(code):
    solveDoCleanUp(code)
    solveDoJmpBack(code)
    solveDoJmpOut(code)

def fix(code):
    for i in range(len(code)):
        if isinstance(code[i],tuple):
            code[i] = list(code[i])
        else:
            code[i] = [code[i]]

def solve(code):
    solveIf(code)
    solveDo(code)
    fix(code)