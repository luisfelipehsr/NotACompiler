import parser as lya
import codeGenerationTools as cgt
import sys

# Metodo principal do script
def main():
    # Processa argumentos passados ao scrip
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

    # Gera arquivos compilados de cada arquivo .lya passado
    lyaParser = lya.Parser()
    for name in files:
        lyaParser.lexer.lineno = 1
        print('\n' + name )
        if debug is False:
            file = open(name,'r')
        else :
            file = open('Examples/' + name, 'r')
        lya.AST.semantic = lya.Context()
        lyaParser.parse(file.read()) # realiza parse do arquivo
        lyaParser.ast.recursiveTypeCheck() # adiciona a AST os tipos dos nos
        lya.AST.semantic = lya.Context() # salva os contextos dos nos
        code = lyaParser.ast.recursiveGenCode() # gera pre-codigo do programa
        cgt.solveIf(code) # adiciona pulos no codigo para ifs

        # constroi arquivo de saida
        codeFilename = name[:(len(name) - 4)]
        if debug is False:
            codeFile = open(codeFilename + '.lvm', 'w')
        else:
            codeFile = open("CompiledExamples/" + codeFilename + ".lvm", 'w')

        # adiciona linha ao arquivo com o comando gerado
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

        # constroi grafo da AST se a opcao de debug estiver ativa
        if debug is True:
            lyaParser.ast.buildGraph("CompiledExamples/" + name)

if __name__ == '__main__':
    main()