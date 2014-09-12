# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 14:44:16 2014

@author: Cyprien Guillemot
"""

def compare(x, y):
    if x>y:
        return 1
    elif x==y:
        return 0
    else:
        return -1
        
print compare(int(input("x:")),int(input("y:")))