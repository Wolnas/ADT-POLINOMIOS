# ================================================================
#  taylor.py — Clase TaylorPolinomio (hereda de Polinomio)
# ================================================================

import math
from polinomio import Polinomio


class TaylorPolinomio(Polinomio):

    @classmethod
    def seno(cls, n_terminos):
        p = cls()
        for k in range(n_terminos):
            p.insertar(((-1)**k) / math.factorial(2*k+1), 2*k+1)
        return p

    @classmethod
    def coseno(cls, n_terminos):
        p = cls()
        for k in range(n_terminos):
            p.insertar(((-1)**k) / math.factorial(2*k), 2*k)
        return p

    @classmethod
    def exponencial(cls, n_terminos):
        p = cls()
        for k in range(n_terminos):
            p.insertar(1 / math.factorial(k), k)
        return p

    @classmethod
    def lorentz(cls, n_terminos):
        p = cls()
        for k in range(n_terminos):
            coef = math.factorial(2*k) / (4**k * math.factorial(k)**2)
            p.insertar(coef, 2*k)
        return p

    @classmethod
    def lorentz_ke(cls, n_terminos):
        p = cls.lorentz(n_terminos)
        p.insertar(-1, 0)
        return p