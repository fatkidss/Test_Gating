import math
import numpy as np

class CalcArea:
    data = []
    gate_h = 4.0
    def __init__(self,h,f,q,p,c,name):
        self.h = h  # head 
        self.f = f  # loss factor
        self.q = q  # flow rate
        self.p = p  # casting height over gate
        self.c = c # total casting height
        self.d = 6.9e-6 # metal density
        self.name = name

    def velocity_ave(self):
        he = self.h - self.p**2/(2*self.c)
        v = self.f*140*math.sqrt(he)
        return v
    
    def velocity_graph(self):
        he = self.h - np.linspace(0,self.p,50)
        v = self.f*140*np.sqrt(he)
        return (he,v)
    
    def choke(self):
        v = self.velocity_ave()
        area = self.q/(self.d*v)
        return area
    
    def size(self):
        if self.name.split("_")[0] == 'choke':
            area = self.choke()
            a = math.sqrt(area/2)
            width = a*1.36
            h = a*2/math.cos(3.1316/6)
        if self.name.split("_")[0] == 'runner':
            area = self.choke()
            a = math.sqrt(area/2)
            width = a*1.36
            h = a*2
        if self.name.split("_")[0] == 'ingate':
            area = self.choke()
            h = self.gate_h
            width = int(area/h)
        return [self.name, area, width, h]
    
    def show(self):
        name, area, width, height = self.size()
        print(f'name:{name} , area:{area:.0f} mm2 , width:{width:.0f} mm , height:{height:.1f} mm')

    def save(self):
        name, area, width, height = self.size()
        self.data.append([self.h,self.f,self.q,self.p,self.c,name,round(area,2),round(width,2),round(height,2)])
        return [self.h,self.f,self.q,self.p,self.c,name,round(area,2),round(width,2),round(height,2)]

class CalcRiser:
    data = []
    ratio = {'FC':{'casting':3, 'neck':0.35, 'riser':1.2},
            'FCD':{'casting':4, 'neck':0.45, 'riser':1.4}
            }
    
    def __init__(self,mat,cwt,cmod,cold=False):
        self.mat = mat
        self.cwt = cwt
        self.cmod = cmod
        self.cold = cold

    def calModulus(self):
        mat = 'FCD' if self.mat[:3] == 'FCD' else 'FC'
        nmod = self.cmod*self.ratio[mat]['neck']
        rmod = self.cmod*self.ratio[mat]['riser']
        return nmod, rmod
    
    def sizeNeck(self,nhigh=None):
        nmod, rmod = self.calModulus()
        if nhigh is not None :
            width = 2*10*nmod/(nhigh-2*10*nmod)
            hight = nhigh
        else:
            width = 6*10*nmod
            hight = width/2
        length = 1.3*hight
        return width, hight, length
    
    def sizeRiser(self):
        mat = 'FCD' if self.mat[:3] == 'FCD' else 'FC'
        nmod, rmod = self.calModulus()
        base = 5.5*10*rmod
        top = base - 4*10*self.cmod
        h = 1.5*base
        wt = math.pi*h/12*(base**2+base*top+top**2)*7.2e-6
        return base,top,h,wt
    
    def enoughRiser(self):
        mat = 'FCD' if self.mat[:3] == 'FCD' else 'FC'
        base,top,h,wt = self.sizeRiser()
        if self.cold :
            factor =  round((wt*12/100)/(self.cwt*self.ratio[mat]['casting']/100),2)
        else :
            factor =  round((wt*17/100)/(self.cwt*self.ratio[mat]['casting']/100),2)
        return factor
    

    def show(self,nhigh=None):
        width, hight, length = self.sizeNeck(nhigh)
        base,top,h,wt = self.sizeRiser()
        factor = self.enoughRiser()
        txtR = f'Riser size --> BaseDia {base:.2f} mm : TopDia {top:.2f} mm : height {h:.2f} mm : Weight {wt:.2f} kg\n'
        txtN = f'Neck size ---> Width {width:.0f} mm : Hight {hight:.0f} mm : Length {length:.0f} mm\n'
        txtF = f'Riser feed ratio: {factor:.2f}'
        print(txtN+txtR+txtF)

    def save(self,nhigh=None):
        nmod, rmod = self.calModulus()
        width, hight, length = self.sizeNeck(nhigh)
        base,top,h,wt = self.sizeRiser()
        factor = self.enoughRiser()
        self.data.append([self.mat,self.cwt,self.cmod,self.cold,
                          round(nmod,3),round(rmod,3),
                          round(width,2),round(hight,2),round(length,2),
                          round(base,2),round(top,2),round(h,2),round(wt,2),round(factor,2)
                          ])
        return [self.mat,self.cwt,self.cmod,self.cold,
                          round(nmod,3),round(rmod,3),
                          round(width,2),round(hight,2),round(length,2),
                          round(base,2),round(top,2),round(h,2),round(wt,2),round(factor,2)
                          ]

    
data = []



        

        











    
        
    



