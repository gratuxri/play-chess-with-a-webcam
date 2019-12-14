'''
Created on 2019-12-13

@author: wf
'''
from pcwawc.eventhandling import Observable

debug=False
class Counter(Observable):
    def __init__(self):
        super(Counter,self).__init__()
        self.value=0
    def count(self,inc):
        self.inc=inc
        self.value+=inc
        self.fire(type="count",inc=inc,value=self.value,counter=self)
        
class Observer():      
    def __init__(self,name):
        self.name=name 
         
    def onCount(self,e):
        if debug:
            print ("counting up %d to %d observered by %s" % (e.inc, e.value,self.name))
        assert e.counter.value==e.value    
        assert e.counter.inc==e.inc

def test_EventHandling():
    counter=Counter()
    observer1=Observer("observer 1")
    observer2=Observer("observer 2")
    counter.subscribe(observer1.onCount)
    counter.subscribe(observer2.onCount)
    for i in range(5):
        counter.count(i)

test_EventHandling()