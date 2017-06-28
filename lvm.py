# Lya Virtual Machine
import re
import sys


class LVM (object):
    def __init__(self, debug=False):
        self.debug = debug
        self.M = dict()
        self.P = dict()
        self.D = dict()
        self.H = list()
        self.pc = 0
        self.sp = 0

    def ldc(self,k):
        self.sp += 1
        self.M[self.sp] = k
        self.pc += 1
        return

    def ldv(self,i,j):
        self.sp += 1
        self.M[self.sp] = self.M[self.D[i] + j]
        self.pc += 1
        return

    def ldr(self,i,j):
        self.sp += 1
        self.M[self.sp] = self.D[i] + j
        self.pc += 1
        return

    def stv(self,i,j):
        self.M[self.D[i] + j] = self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def lrv(self,i,j):
        self.sp += 1
        self.M[self.sp] = self.M[self.M[self.D[i] + j]]
        self.pc += 1
        return

    def srv(self,i,j):
        self.M[self.M[self.D[i] + j]] = self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def add(self):
        self.M[self.sp-1] += self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def sub(self):
        self.M[self.sp -1] -= self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def mul(self):
        self.M[self.sp-1] *= self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def div(self):
        self.M[self.sp-1] /= self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def mod(self):
        self.M[self.sp-1] %= self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def neg(self):
        self.M[self.sp] =- self.M[self.sp]
        self.pc += 1
        return

    def abs(self):
        self.M[self.sp] = abs(self.M[self.sp])
        self.pc += 1
        return

    def land(self):
        self.M[self.sp-1] &= self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def lor(self):
        self.M[self.sp -1] |= self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def lnot(self):
        self.M[self.sp] = not self.M[self.sp]
        self.pc += 1
        return

    def les(self):
        self.M[self.sp-1] = self.M[self.sp-1] < self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def leq(self):
        self.M[self.sp - 1] = self.M[self.sp - 1] <= self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def grt(self):
        self.M[self.sp - 1] = self.M[self.sp - 1] > self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def gre(self):
        self.M[self.sp - 1] = self.M[self.sp - 1] >= self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def equ(self):
        self.M[self.sp - 1] = self.M[self.sp - 1] == self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def neq(self):
        self.M[self.sp - 1] = self.M[self.sp - 1] != self.M[self.sp]
        self.sp -= 1
        self.pc += 1
        return

    def jmp(self,p):
        self.pc = p
        return

    def jof(self,p):
        if not self.M[self.sp]:
            self.pc = p
        else:
            self.pc += 1
        self.sp -= 1
        return

    def alc(self,n):
        for i in range(n):
            self.M[self.sp+i+1] = 0
        self.sp += n
        self.pc += 1
        return

    def dlc(self,n):
        self.sp -=n
        self.pc += 1
        return

    def cfu(self,p):
        self.sp += 1
        self.M[self.sp] = self.pc + 1
        self.pc = p
        return

    def enf(self,k):
        self.sp += 1
        if k not in self.D:
            self.D[k] = 0
        self.M[self.sp] = self.D[k]
        self.D[k] = self.sp + 1
        self.pc += 1
        return

    def ret(self,k,n):
        self.D[k] = self.M[self.sp]
        self.pc = self.M[self.sp-1]
        self.sp -= n+2
        return

    def idx(self,k):
        self.M[self.sp-1] += self.M[self.sp] * k
        self.sp -= 1
        self.pc += 1
        return

    def grc(self):
        self.M[self.sp] = self.M[self.M[self.sp]]
        self.pc += 1
        return

    def lmv(self,k):
        t = self.M[self.sp]
        for i in range(k):
            self.M[self.sp+i] = self.M[t+i]
        self.sp += k-1
        self.pc += 1
        return

    def smv(self,k):
        t = self.M[self.sp-k]
        for i in range(k):
            self.M[t+i] = self.M[self.sp-i]
        #self.M[t:t+k] = self.M[self.sp-k+1:self.sp+1]
        self.sp -= k+1
        self.pc += 1
        return

    def smr(self,k):
        t1 = self.M[self.sp-1]
        t2 = self.M[self.sp]
        self.M[t1:t1+k] = self.M[t2:t2+k]
        self.sp -= 1
        self.pc += 1
        return

    def sts(self,k):
        adr = self.M[self.sp]
        self.M[adr] = len(self.H[k])
        for c in self.H[k]:
            adr += 1
            self.M[adr] = c
        self.sp -= 1
        self.pc += 1
        return

    def rdv(self,):
        self.sp += 1
        self.M[self.sp] = eval(input())
        self.pc += 1
        return

    def rds(self):
        data = input()
        adr = self.M[self.sp]
        self.M[adr] = len(data)
        for k in data:
            adr += 1
            self.M[adr] = k
        self.sp -= 1
        self.pc += 1
        return

    def prv(self,ischar):
        if ischar == 'True':
            print(chr(self.M[self.sp]),'')
        else:
            print(int(self.M[self.sp]),'')
        self.sp -= 1
        self.pc += 1
        return

    def prt(self,k):
        print(self.M[self.sp-k+1:self.sp+1])
        self.sp -= (k-1)
        self.pc += 1
        return

    def prc(self,i):
        print(self.H[i],'')
        self.pc += 1

    def prs(self):
        adr = self.M[self.sp]
        tam = self.M[adr]
        for i in range(0, tam):
            adr += 1
            print(self.M[adr])
        self.sp -= 1
        self.pc += 1
        return

    def stp(self):
        self.sp = -1
        self.D[0] = 0
        self.pc += 1
        return

    def nop(self):
        self.pc += 1
        return

    def end(self):
        return True

    def runInst(self, instruction):
        #print(instruction)
        if instruction[0] == 'ldc':
            self.ldc(instruction[1])
        elif instruction[0] == 'ldv':
            self.ldv(instruction[1], instruction[2])
        elif instruction[0] == 'ldr':
            self.ldr(instruction[1], instruction[2])
        elif instruction[0] == 'stv':
            self.stv(instruction[1], instruction[2])
        elif instruction[0] == 'lrv':
            self.lrv(instruction[1], instruction[2])
        elif instruction[0] == 'srv':
            self.lrv(instruction[1], instruction[2])
        elif instruction[0] == 'add':
            self.add()
        elif instruction[0] == 'sub':
            self.sub()
        elif instruction[0] == 'mul':
            self.mul()
        elif instruction[0] == 'div':
            self.div()
        elif instruction[0] == 'mod':
            self.mod()
        elif instruction[0] == 'neg':
            self.neg()
        elif instruction[0] == 'abs':
            self.abs()
        elif instruction[0] == 'and':
            self.land()
        elif instruction[0] == 'lor':
            self.lor()
        elif instruction[0] == 'not':
            self.lnot()
        elif instruction[0] == 'les':
            self.les()
        elif instruction[0] == 'leq':
            self.leq()
        elif instruction[0] == 'grt':
            self.grt()
        elif instruction[0] == 'gre':
            self.gre()
        elif instruction[0] == 'equ':
            self.equ()
        elif instruction[0] == 'neq':
            self.neq()
        elif instruction[0] == 'jmp':
            self.jmp(instruction[1])
        elif instruction[0] == 'jof':
            self.jof(instruction[1])
        elif instruction[0] == 'alc':
            self.alc(instruction[1])
        elif instruction[0] == 'dlc':
            self.dlc(instruction[1])
        elif instruction[0] == 'cfu':
            self.cfu(instruction[1])
        elif instruction[0] == 'enf':
            self.enf(instruction[1])
        elif instruction[0] == 'ret':
            self.ret(instruction[1], instruction[2])
        elif instruction[0] == 'idx':
            self.idx(instruction[1])
        elif instruction[0] == 'grc':
            self.grc()
        elif instruction[0] == 'lmv':
            self.lmv(instruction[1])
        elif instruction[0] == 'smv':
            self.smv(instruction[1])
        elif instruction[0] == 'smr':
            self.smr(instruction[1])
        elif instruction[0] == 'sts':
            self.sts(instruction[1])
        elif instruction[0] == 'rdv':
            self.rdv()
        elif instruction[0] == 'rds':
            self.rds()
        elif instruction[0] == 'prv':
            self.prv(instruction[1])
        elif instruction[0] == 'prt':
            self.prt(instruction[1])
        elif instruction[0] == 'prc':
            self.prc(instruction[1])
        elif instruction[0] == 'prs':
            self.prs()
        elif instruction[0] == 'stp':
            self.stp()
        elif instruction[0] == 'nop':
            self.nop()
        elif instruction[0] == 'end':
            self.end()
            return False
        else:
            raise TypeError('Oops Invalid Instruction ' + str(instruction[0]))
        return True

    # Executa o codigo passado
    def runCode(self,code):
        while True:
            if not self.runInst(code[self.pc]): # Executa comando na posicao pc
                break
            elif self.debug:
                print('Stack = '+str(self.M))
                print('D = '+str(self.D))
                print('Sp = ' + str(self.sp))
                print('Pc = ' + str(self.pc))

            continue

# Metodo principal do script
def main():
    # Processa argumentos passados ao script
    debug = False
    files = []
    if len(sys.argv) == 2:
        files = [sys.argv[1]]
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'debug':
            debug = True
            r = range(1, int(sys.argv[2]) + 1)
            files = ["CompiledExamples/Example%s.lvm" % i for i in r]
    else:
        sys.exit("ERROR: must have one argument specifying file or two:"
                 + "'debug' '#examples'")

    # Executa os arquivos .lvm passados
    for name in files:
        if debug is True:
            print("Executing object ", name)

        # Inicia LVM
        if debug is True:
            lvm = LVM(debug=True)
        else:
            lvm = LVM()

        # Le linhas do arquivo e as armazena numa lista
        codeFile = open(name, 'r')
        codeList = list(codeFile)

        # Adiciona em H as n strings constantes presentes no inicio do arquivo
        n = codeList[0]
        n = int(n)
        lvm.H += ["\n"]
        for stringLiteral in codeList[2:n+1]:
            tam = len(stringLiteral)
            stringLiteral = stringLiteral[:tam-1]
            lvm.H += [stringLiteral]
        print(lvm.H)
        regex = re.compile(r'\((.*)\)')
        regex2 = re.compile(r'[a-zA-Z0-9]+')
        regex3 = re.compile(r'[a-zA-Z]+')
        code = []
        for line in codeList[n+1:]:
            cmpregex = regex.match(line)
            command = []
            if cmpregex is not None:
                terms = regex2.findall(line) #toma palavras e numeros do comando

                # adiciona cada termo a uma lista
                for term in terms:
                    processed = regex3.match(term)
                    if processed is not None:
                        command += [term]
                    else:
                        command += [int(term)]
            code += [command] # adiciona esta sublista a lista de comandos

        print(code)

        # Executa arquivo
        lvm.runCode(code)

if __name__ == '__main__':
    main()