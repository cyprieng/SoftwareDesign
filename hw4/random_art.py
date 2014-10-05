# -*- coding: utf-8 -*-
"""
Create random art from random functions
Random_art.py

@author: Cyprien Guillemot, amonmillner, adapted from pruvolo work
"""

#IMPORT
from random import randrange, randint
import Image
import math

def prod(a, b):
    """Return prod of two number.
    
    Keyword arguments:
    a -- first number
    b -- Second number
    """
    return float(a)*float(b)

def cos_pi(a):
    """Return cos(pi*a).
    
    Keyword arguments:
    a -- Number used to calc the cos
    """
    return math.cos(math.pi*float(a))
    
def sin_pi(a):
    """Return sin(pi*a).
    
    Keyword arguments:
    a -- Number used to calc the sin
    """
    return math.sin(math.pi*float(a))

def square(a):
    """Return a².
    
    Keyword arguments:
    a -- Number used to calc the square
    """
    return float(a)*float(a)

def squareRoot(a):
    """Return squareRoot(|a|).
    
    Keyword arguments:
    a -- Number used to calc the square root
    """
    return math.sqrt(abs(float(a)))    

def build_random_function(min_depth, max_depth):
    """Return random function with.
    
    Keyword arguments:
    min_depth -- minimal depth of the function
    max_depth -- maximal depth of the function
    """
    if max_depth == 1: #We reach max depth => stop
        var = ["x", "y"]
        return var[randrange(len(var))]
        
    if min_depth == 0 and randint(0,1) == 1: #We reach min depth => we randomly stop or not
         var = ["x", "y"]
         return var[randrange(len(var))]
    
    #Choose a random function
    baseFunction = ["prod","cos_pi", "sin_pi", "square", "squareRoot"]
    function = baseFunction[randrange(len(baseFunction))]
    
    #Recursive call for arguments of the function
    if function == "prod":
        return [function, [build_random_function(min_depth -1, max_depth -1)], [build_random_function(min_depth -1, max_depth -1)]]
    else:
        return [function, [build_random_function(min_depth -1, max_depth -1)]]

def evaluate_random_function(f, x, y):
    """Evaluate the function at the given point.
    
    Keyword arguments:
    f -- function to evaluate
    x -- value of x
    y -- value of y
    """  
    if f[0] == "x":
        return x
    if f[0] == "y":
        return y
        
    if f[0] == "prod":
        return prod(evaluate_random_function(f[1][0],x,y), evaluate_random_function(f[2][0],x,y))
    if f[0] == "cos_pi":
        return cos_pi(evaluate_random_function(f[1][0],x,y))
    if f[0] == "sin_pi":
        return sin_pi(evaluate_random_function(f[1][0],x,y))
    if f[0] == "square":
        return square(evaluate_random_function(f[1][0],x,y))
    if f[0] == "squareRoot":
        return squareRoot(evaluate_random_function(f[1][0],x,y))
    

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """Remap a value in an interval to another
    
    Keyword arguments:
    val -- Value to remap
    input_interval_start -- start of the input interval
    input_interval_end -- end of the input interval
    output_interval_start -- start of the output interval
    output_interval_end -- end of the output interval
    """  
    percent = float(val - input_interval_start) / float(input_interval_end - input_interval_start)
    return output_interval_start + percent * (output_interval_end - output_interval_start)


#Get function for the tree colors
red = build_random_function(7,10)
green = build_random_function(7,10)
blue = build_random_function(7,10)

#Create image
img = Image.new("RGB",(350,350))

#Color each pixel
for x in range(0,349):
    for y in range(0,349):
        r = remap_interval(evaluate_random_function(red, remap_interval(x,0,349,-1,1), remap_interval(y,0,349,-1,1)), -1,1,0,255)
        g = remap_interval(evaluate_random_function(green, remap_interval(x,0,349,-1,1), remap_interval(y,0,349,-1,1)), -1,1,0,255)
        b = remap_interval(evaluate_random_function(blue, remap_interval(x,0,349,-1,1), remap_interval(y,0,349,-1,1)), -1,1,0,255)
        img.putpixel((x,y), (int(r), int(g), int(b))) 

#Save image
img.save("test.png", 'PNG')