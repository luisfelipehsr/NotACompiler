import parser as lya
import codeGenerationTools as cgt
import sys

def main():
    debug = False
    files = []
    if len(sys.argv) == 2:
        files = [sys.argv[1]]
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'debug':
            debug = True
            r = range(1, int(sys.argv[2]) + 1)
            files = ["Example%s.lya" %i for i in r]
    else:
        sys.exit("ERROR: must have one argument specifying file or two:"
                 + "'debug' '#examples total'")

    lyaParser = lya.Parser()
    #tstList = ["Examples/Example%s.lya" %i for i in r]
    for name in files:
        lvm = lya.LVM(debug=True)
        lyaParser.lexer.lineno = 1;
        print('\n' + name )
        if debug is False:
            file = open(name,'r')
        else :
            file = open('Examples/' + name, 'r')
        lya.AST.semantic = lya.Context()
        lyaParser.parse(file.read())
        lyaParser.ast.recursiveTypeCheck()
        lya.AST.semantic = lya.Context()
        code = lyaParser.ast.recursiveGenCode()
        cgt.solveIf(code)

        codeFilename = name[:(len(name) - 4)]
        if debug is False:
            codeFile = open(codeFilename + '.lvm', 'w')
        else:
            codeFile = open("CompiledExamples/" + codeFilename + ".lvm", 'w')

        for line in code:
            text = ''

            if isinstance(line, str):
                text = '(\'{}\')\n'.format(line)
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
        #if debug is False:
        #    lyaParser.ast.buildGraph(name)
        #else:
        #    lyaParser.ast.buildGraph("CompiledExamples/" + name)
        if debug is True:
            lyaParser.ast.buildGraph("CompiledExamples/" + name)

if __name__ == '__main__':
    main()