# ================================================================
#  main.py — Punto de entrada del proyecto Kivy
#  ADT Polinomio — INF-220 Estructuras de Datos I
#  Autor: Witczak Sanabria, M. N.
#  Universidad Autonoma Gabriel Rene Moreno
# ================================================================

from kivy.app import App
from vista.vista_polinomio import PolinomioLayout


class PolinomioApp(App):
    """
    Aplicación principal Kivy.
    Hereda de App — clase base de toda aplicación Kivy.
    """

    def build(self):
        """
        Construye y devuelve el widget raíz de la aplicación.
        Este método se ejecuta automáticamente al iniciar la app.
        """
        self.title = "ADT Polinomio — INF-220"
        return PolinomioLayout()


if __name__ == "__main__":
    PolinomioApp().run()