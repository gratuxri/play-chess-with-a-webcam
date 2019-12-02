'''
Created on 2019-11-29

@author: wf
'''
import cv2
from timeit import default_timer as timer
from matplotlib import pyplot as plt
import numpy as np
import math
import sys

class Stats:
    """ Calculate Histogram statistics see https://math.stackexchange.com/questions/857566/how-to-get-the-standard-deviation-of-a-given-histogram-image """
    def __init__(self,histindexed):
        self.n=len(histindexed)
        self.max=-sys.maxsize
        self.min=sys.maxsize
        self.sum=0
        self.prod=0
        self.sqsum=0
        for x,y in histindexed:
            self.sum+=y
            self.prod+=x*y
        self.mean=self.prod/self.sum
        for x,y in histindexed:
            if y>0:
                self.min=min(self.min,x)    
                self.max=max(self.max,x)
            dx=x-self.mean
            self.sqsum+=y*dx*dx
        # σ²
        self.variance=self.sqsum/self.sum
        self.stdv=math.sqrt(self.variance)
        self.maxdelta=max(self.mean-self.min,self.max-self.mean)
        self.factor=self.maxdelta/self.stdv
   
class Histogram:
    """ Image Histogram """
    colors = ('blue','green','red')
    
    def __init__(self,image,histSize = 256,histRange = (0, 256)):
        """ construct me from the given image hist Size and histRange """
        self.hist={}
        self.stats={}
        self.image=image
        self.rgb=cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        
        start=timer()
        
        # the upper boundary is exclusive
        for channel in range(len(Histogram.colors)):
            self.hist[channel] = cv2.calcHist([image], [channel], None, [histSize], histRange, accumulate=False)
            histindexed=list(enumerate(np.reshape(self.hist[channel],histSize)))
            self.stats[channel] = Stats(histindexed)
        bstats,gstats,rstats=self.stats[0],self.stats[1],self.stats[2]
        self.color=(bstats.mean,gstats.mean,rstats.mean)
        self.mincolor=(bstats.min,gstats.min,rstats.min)
        self.maxcolor=(bstats.max,gstats.max,rstats.max)
        self.maxdelta=(bstats.maxdelta,gstats.maxdelta,rstats.maxdelta)
        # here we are using the color information! This should make the difference!
        self.factor=(bstats.factor,gstats.factor,rstats.factor)
        self.stdv=(bstats.stdv,gstats.stdv,rstats.stdv)
        end=timer()
        self.time=end-start
        
    def fix(self,value):
        return 0 if value<0 else 255 if value>255 else value    
        
    def colorRangeWithFactor(self,rangeFactor):
        b,g,r=self.color
        bs,gs,rs=self.stdv
        rf=rangeFactor
        lower = np.array([self.fix(b-bs*rf), self.fix(g-gs*rf) ,self.fix(r-rs*rf)], dtype = 'uint8')
        upper = np.array([self.fix(b+bs*rf), self.fix(g+gs*rf) ,self.fix(r+rs*rf)], dtype = 'uint8')
        return lower,upper    
    
    def colorMask(self,image,rangeFactor):
        """ create a color mask for this histogram and apply it to the given image"""
        #lower,upper=self.colorRange(rangeFactor)
        lower,upper=self.mincolor,self.maxcolor
        colorMask=cv2.inRange(image,lower,upper)
        return colorMask
        
    def showDebug(self):
        print("calculation took %.4f s" % (self.time))   
        for channel in range(len(Histogram.colors)):
            print (vars(self.stats[channel])) 
    
    def plotRow(self,ax1,ax2):  
        ax1.imshow(self.rgb), ax1.axis('off')
        for i,col in enumerate(Histogram.colors):
            ax2.plot(self.hist[i],color = col)
            #ax2.xlim([0,256])
            
    def preparePlot(self,rows,cols,title='color histogram',fontsize=20):        
        fig,axes=plt.subplots(rows,cols)
        fig.suptitle(title, fontsize=fontsize)
        return fig,axes
            
    def plot(self):    
        fig,(ax1,ax2)=self.preparePlot(1,2)
        self.plotRow(ax1,ax2)
        return fig    
            
    def save(self,filepath):
        fig=self.plot()
        self.savefig(fig,filepath)
        
    def savefig(self,fig,filepath):    
        fig.savefig(filepath)    
        plt.close(fig)
        
    def show(self):
        fig=self.plot()        
        plt.show()
        plt.close(fig)