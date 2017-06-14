class LVM (object):
    def __init__(self,debug = False):
        self.debug = debug
        self.M = dict()
        self.P = dict()
        self.D = dict()
        self.H = dict()
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
        self.M[self.sp:self.sp+k] = self.M[t:t+k]
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

    def rdv(self):
        self.sp += 1
        self.M[self.sp] = input()
        self.pc += 1
        return

    def rds(self):
        str = input()
        adr = self.M[self.sp]
        self.M[adr] = len(str)
        for k in str:
            adr += 1
            self.M[adr] = k
        self.sp -= 1
        self.pc += 1
        return

    def prv(self,ischar):
        if ischar:
            print(chr(self.M[self.sp]))
        else:
            print(self.M[self.sp])
        self.sp -= 1
        self.pc += 1
        return

    def prt(self,k):
        print(self.M[self.sp-k+1:self.sp+1])
        self.sp -= (k-1)
        self.pc += 1
        return

    def prc(self,i):
        print(self.H[i])
        self.pc += 1

    def prs(self):
        adr = self.M[self.sp]
        len = self.M[self.adr]
        for i in range(0,len):
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

    def runInst(self,inst):
        if isinstance(inst,tuple):
            c = list(inst)
        else:
            c = [inst]
        print(c)
        if c[0] == 'ldc':
            self.ldc(c[1])
        elif c[0] == 'ldv':
            self.ldv(c[1],c[2])
        elif c[0] == 'ldr':
            self.ldr(c[1],c[2])
        elif c[0] == 'stv':
            self.stv(c[1],c[2])
        elif c[0] == 'lrv':
            self.lrv(c[1],c[2])
        elif c[0] == 'srv':
            self.lrv(c[1],c[2])
        elif c[0] == 'add':
            self.add()
        elif c[0] == 'sub':
            self.sub()
        elif c[0] == 'mul':
            self.mul()
        elif c[0] == 'div':
            self.div()
        elif c[0] == 'mod':
            self.mod()
        elif c[0] == 'neg':
            self.neg()
        elif c[0] == 'abs':
            self.abs()
        elif c[0] == 'and':
            self.land()
        elif c[0] == 'lor':
            self.lor()
        elif c[0] == 'not':
            self.lnot()
        elif c[0] == 'les':
            self.les()
        elif c[0] == 'leq':
            self.leq()
        elif c[0] == 'grt':
            self.grt()
        elif c[0] == 'gre':
            self.gre()
        elif c[0] == 'equ':
            self.equ()
        elif c[0] == 'neq':
            self.neq()
        elif c[0] == 'jmp':
            self.jmp(c[1])
        elif c[0] == 'jof':
            self.jof(c[1])
        elif c[0] == 'alc':
            self.alc(c[1])
        elif c[0] == 'dlc':
            self.dlc(c[1])
        elif c[0] == 'cfu':
            self.cfu(c[1])
        elif c[0] == 'enf':
            self.enf(c[1])
        elif c[0] == 'ret':
            self.ret(c[1],c[2])
        elif c[0] == 'idx':
            self.idx(c[1])
        elif c[0] == 'grc':
            self.grc()
        elif c[0] == 'lmv':
            self.lmv(c[1])
        elif c[0] == 'smv':
            self.smv(c[1])
        elif c[0] == 'smr':
            self.smr(c[1])
        elif c[0] == 'sts':
            self.sts(c[1])
        elif c[0] == 'rdv':
            self.rdv()
        elif c[0] == 'rds':
            self.rds()
        elif c[0] == 'prv':
            self.prv(c[1])
        elif c[0] == 'prt':
            self.prt(c[1])
        elif c[0] == 'prc':
            self.prc(c[1])
        elif c[0] == 'prs':
            self.prs()
        elif c[0] == 'stp':
            self.stp()
        elif c[0] == 'nop':
            self.nop()
        elif c[0] == 'end':
            self.end()
            return False
        else:
            raise TypeError('Oops Invalid Instruction ' + str(c[0]))
        return True

    def runCode(self,code):
        while True:
            if not self.runInst(code[self.pc]):
                break
            elif self.debug:
                print('Stack = '+str(self.M))
                print('Sp = ' + str(self.sp))
                print('Pc = ' + str(self.pc))
            continue



            
