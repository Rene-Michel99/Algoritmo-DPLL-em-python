import os
import time

class clausula():
    def __init__(self,st,status):
        self.string=st
        self.bool=status
        self.literais=[]
        self.lps=[]
        self.setAtoms()

    def setAtoms(self):
        x=self.string
        for i in range(len(x)):
            if x[i]>='a' and x[i]<='z':
                if i>0 and x[i-1]=='-':
                    self.literais.append('-'+x[i])
                else:
                    self.literais.append(x[i])

def quebraR(f,pos,sen,qlist):
    if pos<len(f):
        if f[pos]=='(':
            return quebraR(f,pos+1,sen,qlist)
        elif f[pos]!=')':
            sen=sen+f[pos]
            return quebraR(f,pos+1,sen,qlist)
        elif f[pos]==')':
            if len(sen)>0:
                if sen[0]=='E':
                    sen=sen.replace('E','')
                qlist.append(sen)
            sen=''
            return quebraR(f,pos+1,sen,qlist)
    else:
        return qlist

def detectls(ls):
    global lps
    lps=[]
    res=[]
    cont=0
    for i in ls:
        for j in i.literais:
            lps.append((j,i))
    for i in lps:
        for j in lps:
            if i[0]==j[0]:
                cont+=1
            if i[0]!=j[0]:
                cont+=1
            if i[0]=='-'+j[0] or j[0]=='-'+i[0]:
                cont-=1
        cont=0
    return ls

def remove_l(j,y,x):
    cont=j.literais.count(y)
    for i in range(cont):
        x=j.literais.index(y)
        j.literais.remove(j.literais[x])
    return j

def search(qlist,l,remover):
    y=''
    if l.find('-')!=-1:
        y=l.replace('-','')
    else:
        y='-'+l
    for j in qlist:
        x=-1
        if j.literais.count(y)>0 and remover.count(j)==0:
            x=j.literais.index(y)
        if x!=-1:
            j=remove_l(j,y,j.literais[x])
    return qlist
    
def simplifica2(qlist,i,remover):
    if i<len(qlist):
        x=qlist[i]
        if len(x.literais)==1:
            for j in qlist:
                pos=-1
                if j.literais.count(x.literais[0])>0:
                    pos=j.literais.index(x.literais[0])
                if pos!=-1:
                    remover.append(j)
            qlist=search(qlist,x.literais[0],remover)
        return simplifica2(qlist,i+1,remover)
    else:
        for i in remover:
            try:
                qlist.remove(i)
            except:
                pass
        return qlist

def quebra(f):
    qlist=quebraR(problem,0,'',[])
    ls=[]
    lps=[]
    for i in qlist:
        ls.append(clausula(i,''))
    return ls
    

def checa(f):
    for i in f:
        if i.literais==[]:
            return True
    return False

def buscaV(f):
    for i in f:
        if len(i.literais)==1:
            x=i.literais[0]
            return x
    for i in f:
        if len(i.literais)>1:
            x=i.literais[0]
            return x
                
def apendicite(f,c):
    if c.find('--')!=-1:
        c=c.replace('--','')
    f.append(clausula(c,''))
    return f

def copy(f):
    x=[]
    cls=''
    for i in f:
        for j in i.literais:
            cls=cls+j+' V '
        cls=cls[:len(cls)-3]
        x.append(clausula(cls,''))
        cls=''
    return x

def dpll(f):
    f=simplifica2(f,0,[])
    if len(f)==0:
        return True
    if checa(f):
        return False
    c=buscaV(f)
    x=copy(f)
    y=copy(f)
    f=[]
    if dpll(apendicite(x,c)) or dpll(apendicite(y,'-'+c)):
        return True
    else:
        return False

def pega_sentença():
    arq=open('Sentenca.txt','r')
    problem=arq.read()
    arq.close()
    return problem

def top(problem):
    if problem.find('--')!=-1:
        problem=problem.replace('--','')
    qlist=quebra(problem)
    print(dpll(qlist))
    

#problem=str(input('digite uma sentença: '))
problem=pega_sentença()
print(problem)
ini=time.time()
top(problem)
fim=time.time()
print('Tempo:',fim-ini)
arq=open('logDPLL.txt','w')
arq.write('Tempo: '+str(fim-ini))
arq.close()
