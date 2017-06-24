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

