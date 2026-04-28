# ================================================================
#  nodo.py — Nodo de la lista enlazada
# ================================================================

class NodoTermino:
    """
    Nodo de la lista enlazada.
    Representa un término del polinomio: coeficiente * x^exponente
    """
    def __init__(self, coef, exp):
        self.coeficiente = coef    # número que multiplica a x
        self.exponente   = exp     # potencia de x
        self.siguiente   = None    # puntero al siguiente nodo