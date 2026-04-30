# controlador/ctrl_polinomio.py

from modelo.polinomio import Polinomio

class CtrlPolinomio:
    
    def __init__(self):
        self.poly1     = None
        self.poly2     = None
        self.poly_suma = None

    def cargar(self, texto, cual):
        """Convierte texto a Polinomio y lo guarda."""
        poly = Polinomio()
        for par in texto.strip().split():
            c, e = par.split(",")
            poly.insertar(int(c), int(e))
        if cual == "p1":
            self.poly1 = poly
        else:
            self.poly2 = poly
        return poly.mostrar()

    def sumar(self):
        """Suma poly1 y poly2."""
        if not self.poly1 or not self.poly2:
            return None
        self.poly_suma = self.poly1.sumar(self.poly2)
        return self.poly_suma.mostrar()

    def derivar(self):
        """Deriva poly1."""
        if not self.poly1:
            return None
        deriv = self.poly1.derivar()
        return deriv.mostrar()

    def evaluar(self, x):
        """Evalúa poly1 en x."""
        if not self.poly1:
            return None
        return self.poly1.evaluar(float(x))

    def puntos(self, cual="p1"):
        """Devuelve puntos para graficar."""
        if cual == "p1" and self.poly1:
            return self.poly1.puntos()
        if cual == "p2" and self.poly2:
            return self.poly2.puntos()
        if cual == "suma" and self.poly_suma:
            return self.poly_suma.puntos()
        return None, None