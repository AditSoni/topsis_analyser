import os
import numpy as np
import warnings
from django.conf import settings
class topsis:
    a=None #Matrix
    w=None #Weight matrix and j is the min max matrix
    r=None #Normalisation matrix 
    m=None #Number of rows
    n=None #Number of columns
    aw=[] #worst alternative
    ab=[] #best alternative
    diw=None
    dib=None
    siw=None
    sib=None	

#Return a numpy array with float items
    def floater(self,a):
        ax=[]
        for i in a:
            try:
                ix=[]
                for j in i:
                    ix.append(float(j))
            except:
                ix=float(i)
                pass
            ax.append(ix)
        return np.array(ax)

    def __init__(self,a,w,j):
        self.a=self.floater(a)
        self.m=len(a)
        self.n=len(a[0])
        self.w=self.floater(w)
        self.w=self.w/sum(self.w)
        self.j=np.array(j)
        

    #Step 2 normalization
    def step2(self):
        self.r=self.a
        for i in range(self.m):
            nm=sum(self.a[i,:]**2)**0.5
            for j in range(self.n):
                self.r[i,j]=self.a[i,j]/nm
    #Step 3 wieght matrix
    def step3(self):
        self.t=self.r*self.w

    #Step 4 ideal min max 
    def step4(self):
        self.aw=[]
        self.ab=[]
        for i in range(self.n):
            if self.j[i]==1:
                self.aw.append(min(self.t[:,i]))
                self.ab.append(max(self.t[:,i]))
            else:
                self.aw.append(max(self.t[:,i]))
                self.ab.append(min(self.t[:,i]))
    #Step 5			
    def step5(self):
        self.diw=(self.t-self.aw)**2
        self.dib=(self.t-self.ab)**2
        #print('lol'
        #print(self.diw
        """for j in range(self.n):
            self.diw[:,j]=(self.diw[:,j]-self.aw[j])**2
            self.dib[:,j]=(self.dib[:,j]-self.ab[j])**2
        print(self.diw)"""
        self.dw=[]
        self.db=[]
        for j in range(self.m):
            self.dw.append(sum(self.diw[j,:])**0.5)
            self.db.append(sum(self.dib[j,:])**0.5)
    # 		print(self.dw)
        self.dw=np.array(self.dw)
        self.db=np.array(self.db)
    # 		print(self.dw)
        #print(self.db)

    #Step 6
    def step6(self):
        np.seterr(all='ignore')
        self.siw=self.dw/(self.dw+self.db)
        #print(self.siw)
        m=None
        score=[]
        for i in range(self.m):
            score.append(self.siw[i])
            if  m==None:
                m=self.siw[i]
        return score
    def calc(self):
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        score=self.step6()
        return score




def topsys(file,w,j):

    fr=open(file)
    fw=open(settings.MEDIA_ROOT+'/uploads/'+'dat1.csv','w')

    for line in fr:
        l=line.split(',')
        l=l[1:]
        l=','.join(l)
        fw.write(l)
    fr.close()
    fw.close()

    a=np.loadtxt(open(settings.MEDIA_ROOT+'/uploads/'+'dat1.csv', "rb"), delimiter=",", skiprows=1)

    t=topsis(a,w,j)

    return list(t.calc())

