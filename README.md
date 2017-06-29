# NotACompiler

Laboratorio de construcao de compiladores.

Luis Felipe Hamada Serrano         RA 147091
Caio Dallecio Ferreira dos Santos  RA 139244

Compilador e maquina virtual para execucacao de codigo da linguagem LYA.

Requisitos:
  Eh preciso ter instalado o graphviz e pydot para funcionalidade total. Para execucao do codigo sem utilizar a opcao
    de debug nao eh preciso o uso de graphviz, mas o pydot talvez envie warnings, embora nao influenciem o codigo.
  A estrutura de pastas dentro do programa deve ser a mesma fornecida.

Utilizando o programa:
  Os dois arquivos principais sao Compiler.py e lvm.py. O primeiro eh o compilador, o segundo a LVM. Ambos podem ser
    utilizados pela linha comando utilizando como argumento um arquivo.
  Para o Compiler forneca um arquivo .lya (python3 Compiler.py seuarquivo.lya).
  Para a LVM forneca um arquivo gerado pelo compiler, no formato .lvm (python3 lvm.py seuarquivo.lvm)

Formato do arquivo .lvm:
  O arquivo se inicia por um numero n, logo em seguida estao n strings que serao guardadas no heap H.
  Logo sem seguida ha todas as linhas de comandos na linguagem de montagem da LVM.

Limitacoes e consideracoes:
  O compilador apresenta comportamento estranho ao lidar com referencias sendo passadas a parametros que sao uma refe-
     rencia do parametro.
  Pela maneira como o comando ('rdv') funciona, nao eh possivel ler multiplos valores na mesmoa linha usando read().
     Eh necessario enviar cada valor desejado individualmente pressionando Enter.
  As funcoes resolvem os parametros da direita para a esquerda pela maneira como sao empilhados no stack. Assim se um
     dos parametros eh uma funcao que altera outros parametros, somente os a esquerda serao alterados.
  O metodo print() foi ajustado para sempre imprimir um \n ao seu final, e nao separar argumentos passados. Entao se
     passados dois argumentos seguidos a, b eles estarao "colados". Contudo print(a), print(b) adiciona \n automatica-
     mente.

Funcao dos arquivos e diretorios:
   Compiler      = eh o compilador
   lvm           = eh a lvm
   lexer         = eh o lexer utilizado
   parserlya     = arquivo principal do parser
   parserClasses = possui as classes com os nos da AST gerada
   Semantocer    = implementa as funcoes que lidam com o contexto
   type          = define os tipos
   valueToken    = define o resultado dos token de true e false
   symbol        = define simbolos, eles guardam um tipo e posicao, e sao adicionados ao contexto