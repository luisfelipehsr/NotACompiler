def solveIf(code):
    stack = []
    if isinstance(code,list):
        for i in range(len(code)):
            inst = code[i]
            if inst[0] == 'start':
                if inst[1] == 'if':
                    code.pop(i)
                elif inst[1] == 'then':
                    stack.append(i)
            elif inst[0] == 'end':
                if inst[1] == 'if':
                    code.pop(i)
                elif inst[1] == 'then':
                    add = stack.pop(i)
                    code[add] = [('jof',i)]

