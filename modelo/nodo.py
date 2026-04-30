#Este es mi pilar principal, mi atomo para cargar los polinomios
class NodoTermino:
    def __init__(self, coef, exp):
        self.coeficiente = coef   #dominare esta variable como mi coeficiente, mi numero aislado que multiplica a la x
        self.exponente   = exp      #variable que actuara como el exponente de la x, el numero que indica a que potencia se eleva la x 
        self.siguiente   = None    # puntero al siguiente nodo