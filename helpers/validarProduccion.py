import platform
import os


def listarContenidoCarpeta(ruta):
    print(ruta)
    estado = os.listdir(ruta)
    return estado


def validarEstadoProduccion(listarContenidoCarpeta, sistema):
    if sistema == 'darwin':
        estadoProduccion = False
    elif sistema == "linux":
        estadoProduccion = False
    else:
        carpetas = listarContenidoCarpeta("C:/Users")
        estadoProduccion = "robotrocket2" in carpetas
    return estadoProduccion


def validarProduccion():
    #sistema = platform.system().lower()
    #print("sistema", sistema)
    #estadoProduccion = validarEstadoProduccion(listarContenidoCarpeta, sistema)
    #return estadoProduccion
    return True