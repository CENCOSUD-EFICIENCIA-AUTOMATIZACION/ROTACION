import os
def rutas():
    rutaRelativa = os.path.abspath('..')
    return rutaRelativa

def rutasGlobales():
    rutaRelativa = os.path.abspath('../../..')
    return rutaRelativa

def rutaPython(sistema):
    if sistema == 'linux':
        rutaPython = '/usr/bin/python3'
    else:
        rutaPython = 'C:/Users/robotrocket2/AppData/Local/Programs/Python/Python39/python.exe'
    return rutaPython