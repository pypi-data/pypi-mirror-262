import numpy as np
def saludar():
    print("Hola, te saludo desde saludos.saludar()")

def prueba():
    print("Esto es una prueba de la nueva versión")

def generar_array(numeros):
    return np.arange(numeros)

class Saludo:
    def __init__(self):
        print("Hola, te saludo desde saludo.__init__")

if __name__=='__main__':  #Esta variable "name" almacena durante la ejecución de un programa el nombre del script. Nqme en saludos tendrá saludos y en test tendrá test.
    #Sin embargo hay una excepción. El fichero que ejecutamos para empezar el programa, que en nuestro caso es test, tiene un nombre especial que es "__main__"
    #Por tanto, si ejecutamos test desde saludos, el nombre será saludos.
    print(generar_array(5))