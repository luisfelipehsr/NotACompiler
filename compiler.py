import parser as lya

def main():

    r = range(1,2)
    tstList = ["Example%s.lya" %i for i in r]
    a = lya.Parser()
    for f in tstList:
        lvm = lya.LVM(debug=True)
        a.lexer.lineno = 1;
        print('\n' + f )
        file = open(f,'r')
        lya.AST.semantic = lya.Context()
        a.parse(file.read())
        a.ast.recursiveTypeCheck()
        lya.AST.semantic = lya.Context()
        code = a.ast.recursiveGenCode()

        codeFile = open("codeFile.lya", 'w')
        for line in code:
            text = ''

            if isinstance(line, str):
                text = '\'{}\'\n'.format(line)
                codeFile.write(text)
            else:
                if type(line[0]) is str:
                    text += '(\'{}\''.format(line[0])
                else:
                    text += '({}'.format(line[0])

                for term in line[1:]:
                    if type(term) is str:
                        text += ', \'{}\''.format(term)
                    elif type(term) is bool:
                        if term is True:
                            text += ', true'
                        else:
                            text += ', false'
                    else:
                        text += ', {}'.format(term)
                text += ')\n'
                codeFile.write(text)



        # for inst in ret:
        #     print(inst)
        #lvm.runCode(code)
        #a.ast.removeChanel()

        # Generates .dot archive to display the AST.
        # Uncomment only if you have pydot library.
        # Uncomment the import of pydot and line 60 on parserClasses.py too.
        a.ast.buildGraph(f)




if __name__ == '__main__':
    main()