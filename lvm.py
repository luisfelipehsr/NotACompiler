class LVM (object):
    def __init__(self):
        self.M = []
        self.P = []
        self.D = []
        self.H = []
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
        self.M[self.D[i] + j] = M[self.sp]
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

    def less(self):
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

    def enq(self):
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
        self.M[t:t+k] = self.M[self.sp-k+1:self.sp+1]
        self.sp -= k+1
        self.pc += 1
        return

    def smr(self,k):
        t1 = self.M[self.sp-1]
        t2 = self.M[self.sp]
        self.M[t1:t1+k] = self.M[t2:t2+k]
        sp -= 1
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
            print(M[adr])
        sp -= 1
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
