import os
import time

class clausula():
    def __init__(self,st):
        self.string=st
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

def get_lps(ls,loc,i,resposta):
    if i<len(ls):
        x=ls[i]
        cont1=ls.count(x)
        cont2=len(ls)-cont1
        if x.find('-')==-1:
            cont3=ls.count('-'+x)
        else:
            cont3=ls.count(x[1:])
        if cont1+cont2-cont3==len(ls):
            if resposta.count(loc[i])==0:
                resposta.append(loc[i])
            return get_lps(ls,loc,i+1,resposta)
        else:
            return get_lps(ls,loc,i+1,resposta)
    else:
        return resposta
    
def set_listas(ls,pos,i,lg,loc):
    if i<len(ls):
        lg.append(ls[i])
        loc.append(pos)
        return set_listas(ls,pos,i+1,lg,loc)
    else:
        return lg,loc

def detectlp(ls,i,lg,loc):
    if i<len(ls):
        x=ls[i].literais
        lg,loc=set_listas(x,ls[i],0,lg,loc)
        return detectlp(ls,i+1,lg,loc)
    else:
        z=get_lps(lg,loc,0,[])
        for i in z:
            ls.remove(i)
        return ls

def remove_l(j,i,cont,y):
    if i<cont:
        x=j.literais.index(y)
        j.literais.remove(j.literais[x])
        return remove_l(j,i+1,cont,y)
    else:
        return j


def search(qlist,i,y,remover):
    if i<len(qlist):
        x=-1
        if qlist[i].literais.count(y)>0 and remover.count(qlist[i])==0:
            x=qlist[i].literais.index(y)
        if x!=-1:
            qlist[i]=remove_l(qlist[i],0,qlist[i].literais.count(y),y)
        return search(qlist,i+1,y,remover)
    else:
        return qlist

def set_remover(qlist,i,x,remover):
    if i<len(qlist):
        pos=-1
        if qlist[i].literais.count(x)>0:
            pos=qlist[i].literais.index(x)
        if pos!=-1:
            remover.append(qlist[i])
        return set_remover(qlist,i+1,x,remover)
    else:
        return remover

def simplifica2(qlist,i,remover):
    if i<len(qlist):
        x=qlist[i]
        if len(x.literais)==1:
            remover=set_remover(qlist,0,x.literais[0],[])
            y=''
            if x.literais[0].find('-')!=-1:
                y=x.literais[0].replace('-','')
            else:
                y='-'+x.literais[0]
            qlist=search(qlist,0,y,remover)
        return simplifica2(qlist,i+1,remover)
    else:
        for i in remover:
            qlist.remove(i)
        return qlist

def quebra(f):
    qlist=quebraR(problem,0,'',[])
    ls=[]
    copia=''
    lps=[]
    for i in qlist:
        ls.append(clausula(i))
    copia=ls
    ls=detectlp(ls,0,[],[])
    if ls==[]:
        return copia
    else:
        return ls
    

def checa(f):
    for i in f:
        if i.literais==[]:
            return True
    return False

def mom_sato(f):
    res=[]
    ln=[]
    for i in f:
        for j in i.literais:
            res.append(j)
            ln.append(len(i.literais))
    mom=mom2(res,0,0,0,99999999,ln,'')
    sat=sato(res,0,0,0,0,99999999,ln,'')
    if mom[0]=='' and sat[0]=='':
        return menor_s(res,0,999999,ln,'')
    elif mom[1]>sat[1]:
        return mom[0]
    else:
        return sat[0]

def menor_s(res,i,ln,lens,index):
    if i<len(res):
        x=res[i]
        if lens[i]<ln:
            return menor_s(res,i+1,lens[i],lens,x)
        else:
            return menor_s(res,i+1,ln,lens,index)
    else:
        return index
        

def mom2(res,i,cont,maior,ln,lens,index):
    if i<len(res):
        x=res[i]
        cont=res.count(x)-1
        if cont>maior and lens[i]<ln:
            return mom2(res,i+1,0,cont,lens[i],lens,x)
        else:
            return mom2(res,i+1,0,maior,ln,lens,index)
    else:
        return (index,maior)

def sato(res,i,cont,contNP,maior,ln,lens,index):
    if i<len(res):
        x=res[i]
        cont=res.count(x)-1
        contNP=res.count('-'+x)
        if cont*contNP>maior:
            if index==x and lens[i]<ln:
                return sato(res,i+1,0,0,cont*contNP,lens[i],lens,x)
            else:
                return sato(res,i+1,0,0,cont*contNP,lens[i],lens,x)
        else:
            return sato(res,i+1,0,0,maior,ln,lens,index)
    else:
        return (index,maior)

def apendicite(f,c):
    if c.find('--')!=-1:
        c=c.replace('--','')
    f.append(clausula(c))
    return f

def copy(f):
    x=[]
    cls=''
    for i in f:
        for j in i.literais:
            cls=cls+j+' V '
        cls=cls[:len(cls)-3]
        x.append(clausula(cls))
        cls=''
    return x

def dpll(f):
    f=simplifica2(f,0,[])
    if len(f)==0:
        return True
    if checa(f):
        return False
    if len(f)==1:
        return True
    c=mom_sato(f)
    if dpll(apendicite(copy(f),c)) or dpll(apendicite(copy(f),'-'+c)):
        return True
    else:
        return False

def pega_sentença():
    arq=open('Sentença.txt','r')
    problem=arq.read()
    arq.close()
    return problem

def top(problem):
    if problem.find('--')!=-1:
        problem=problem.replace('--','')
    qlist=quebra(problem)
    print(dpll(qlist))
    
#problem='(-b V -c)'
#problem='(a V b)E(-b V c V -d)E(d V -e)'
#problem='(p V -q)E(-p)E(q)'
#problem='(-a)E(-b)E(b V a)'
#problem='(a)E(-a)'
#problem='(a V b V c V d E f)E(g V h V i V j)'
#problem='(a V b V c V d)E(b V c)E(-b V -c)'
#problem='(p V q)E(r V s)E(r V s))E(r V s)E(r V s)E(r)E(s V p V q V r)E(a V b V c)E(a)E(b)'
#problem='(p V q)E(r V s)E(r V s)E(r V s)E(r V s)'
#problem='(p V q)E(r V s)E(r V s)E(r V s)E(r V s)E(r)E(s)'
#problem='(-x V -t)E(q V -w)E(w V x)E(x V q)E(-x V z)'
#problem=str(input('digite uma sentença: '))
problem=pega_sentença()
print(problem)
ini=time.time()
top(problem)
fim=time.time()
print('Tempo:',fim-ini)
arq=open('logDPLLh.txt','w')
arq.write('Tempo: '+str(fim-ini))
arq.close()
