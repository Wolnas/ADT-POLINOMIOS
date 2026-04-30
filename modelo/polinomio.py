#en este apartado son las listas enlazadas


import numpy as np
from modelo.nodo import NodoTermino


class Polinomio:

    def __init__(self):
        self.cabeza = None

    def insertar(self, coef, exp):
        """
        este metodo lo usaremos para insertar mis polinomios.
        """
        if coef == 0:
            return
        nuevo = NodoTermino(coef, exp)
        if self.cabeza is None or exp > self.cabeza.exponente: #busca dentro de cabeza si hay un exponente mayor   
            nuevo.siguiente = self.cabeza #cambio de datos entre nodo y la clase polinomio
            self.cabeza = nuevo 
            return
        actual = self.cabeza
        while actual.siguiente and actual.siguiente.exponente > exp:
            actual = actual.siguiente  
            #no te olvides de esto, sin este dato, no podra acceder al nodo y 
            #se quedara en un bucle infinito. 
        if actual.siguiente and actual.siguiente.exponente == exp:
            actual.siguiente.coeficiente += coef
            if abs(actual.siguiente.coeficiente) < 1e-12: 
                #abs actua como un limpiador y da un valor 
                #absoluto a los numeros, si el coeficiente es muy pequeño lo elimina    
                actual.siguiente = actual.siguiente.siguiente
        else:
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo

    def evaluar(self, x):
        """Evaluamos el polinomio con un valor específico de x."""
        resultado = 0
        actual = self.cabeza
        while actual:
            resultado += actual.coeficiente * (x ** actual.exponente)
            actual = actual.siguiente #nuevamente esta variable es importante para poder iterarla sin quedarse en un bucle infinito, es como el puntero que me permite avanzar al siguiente nodo.
        return resultado

    def sumar(self, otro):
        resultado = Polinomio()
    
    # Copia todos los nodos de P1
        actual = self.cabeza
        while actual:
            resultado.insertar(actual.coeficiente, actual.exponente)
            actual = actual.siguiente
    
    # Para cada nodo de P2, busca si el exponente ya existe
        actual = otro.cabeza
        while actual:
            nodo_resultado = resultado.cabeza
            encontrado = False
        
            while nodo_resultado:
                if nodo_resultado.exponente == actual.exponente:
                # Mismo exponente → suma los coeficientes
                    nodo_resultado.coeficiente += actual.coeficiente
                    encontrado = True
                    break
                nodo_resultado = nodo_resultado.siguiente
        
            if not encontrado:
            # Exponente nuevo → inserta normalmente
                resultado.insertar(actual.coeficiente, actual.exponente)
        
            actual = actual.siguiente
    
        return resultado
    
    def derivar(self):
        """
        extra de derivados dentro de mi polinomio, un dato interesante para saber como interactuan.   
        """
        resultado = Polinomio()
        actual = self.cabeza
        while actual:
            if actual.exponente > 0:
                resultado.insertar(
                    actual.coeficiente * actual.exponente,
                    actual.exponente - 1
                ) #simplmente juego con mis variables de entrada para obtener el resultado de la derivada.
            actual = actual.siguiente
        return resultado

    def mostrar(self, decimales=4):
        """Devuelve string legible del polinomio."""
        if not self.cabeza:
            return "0"
        partes = []
        actual = self.cabeza
        while actual:
            c, e = actual.coeficiente, actual.exponente
            if isinstance(c, float): #isinstance me ayuda a identificar si el tipo de dato es correcto. 
                cs = f"{c:.{decimales}f}".rstrip('0').rstrip('.') #elimina los ceros o el punto si no es necesario. 
            else:
                cs = str(c)
            if e == 0:
                partes.append(cs)
            elif e == 1:
                partes.append(f"{cs}x")
            else:
                partes.append(f"{cs}x^{e}")
            actual = actual.siguiente
        return " + ".join(partes).replace("+ -", "- ") #joins une las listas, como si fuera un string. 

    def puntos(self, x_min=-10, x_max=10, n=600):
        """Genera (xs, ys) para graficar. Recorta valores extremos."""
        xs = np.linspace(x_min, x_max, n) #genera un array de n puntos, usamos numpy para eso. 
        ys = np.array([self.evaluar(float(xi)) for xi in xs])#iteramos cada punto
        ys = np.clip(ys, -1e4, 1e4)#un recorte 
        return xs, ys