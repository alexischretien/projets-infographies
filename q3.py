import sys
from math import sin, cos, pi

ERR_NB_PARAMS = "Error : invalid number of parameters."
ERR_INVALID_OBJECT = "Error : \"{}\" is not a valid object. " \
                   + "The available options are \"sphere\" and \"tore\"."
ERR_NB_PARAMS_OBJECT = "Error : the specification of a {} requires {} integers."
ERR_PARAM_TYPE = "Error : the object's parameters need to be integers " \
               + "strictly greater than 0." 


def getObjectParams():
    
    nbArgs = len(sys.argv)
    error = False

    if (nbArgs < 2):
        print(ERR_NB_PARAMS)
        error = True
    
    elif (sys.argv[1] != "sphere" and sys.argv[1] != "tore"):
        print(ERR_INVALID_OBJECT.format(sys.argv[1]))
        error = True

    elif (sys.argv[1] == "sphere" and nbArgs != 5):
        print(ERR_NB_PARAMS_OBJECT.format("sphere", 3))
        error = True       

    elif (sys.argv[1] == "tore" and nbArgs != 6):
        print(ERR_NB_PARAMS_OBJECT.format("tore", 4))
        error = True

    else:
        params = [int(s) for s in sys.argv if s.isdigit() and int(s) > 0]

        if (nbArgs - len(params) != 2):
            print(ERR_PARAM_TYPE)
            error = True

    if (error):
        sys.exit(0)
    
    return params

def printSphere(radius, nbLon, nbLat):

    u = pi/2
    v = 0.0
    du = pi/nbLon
    dv = 2*pi/nbLat

    while (u < 3*pi/2):
        v = 0.0
        while (v < 2*pi):

            x = radius * sin(u) * cos(v)
            y = radius * sin(u) * sin(v)
            z = radius * cos(u) 
            print("v {} {} {}".format(x,y,z))   
            v += dv
        u += du
"""Main
"""
params = getObjectParams()
if (sys.argv[1] == "sphere"):
    printSphere(params[0], params[1], params[2])
else:
    printTore(params[0], params[1], params[2], params[3])
