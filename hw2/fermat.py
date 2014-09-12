# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 14:28:06 2014

@author: Cyprien Guillemot
"""

def checkFermat(a,b,c,n):
    if n > 2 and a > 0 and b > 0 and c > 0:
        if a**n+b**n == c**n:
            print "Holy smokes, Fermat was wrong!"
        else:
            print "No, that doesn’t work."
    else:
        print "Wrong parameters"
            
def getNum():
    a = input("a: ")
    b = input("b: ")
    c = input("c: ")
    n = input("n: ")
    
    checkFermat(int(a),int(b),int(c),int(n))
    
getNum()