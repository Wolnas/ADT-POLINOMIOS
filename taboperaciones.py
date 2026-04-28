
###esta pestaña es exclusiva para mi interfaz grafica, aqui se encuentran las operaciones 
# 
# que se pueden realizar con los polinomios, como la suma, la derivada y la evaluacion. 
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QGroupBox
)
from polinomio import Polinomio
from graficas import GraficaCanvas


class TabOperaciones(QWidget):
    """
    
    representado como grafico, en mi lista enlazda. 
    """

    def __init__(self):
        super().__init__()
        self.poly1     = None
        self.poly2     = None
        self.poly_suma = None
        self._build()

    def _build(self):
        root = QHBoxLayout(self)
        root.setSpacing(14)
        root.setContentsMargins(12, 12, 12, 12)

        #Panel izquierdo 
        panel = QWidget()
        panel.setFixedWidth(360)
        col = QVBoxLayout(panel)
        col.setSpacing(10)

        col.addWidget(self._grupo_entrada("Polinomio P11111", "p1"))
        col.addWidget(self._grupo_entrada("Polinomio P2", "p2"))

        btn_suma = QPushButton("Sumar P1 + P2")
        btn_suma.setObjectName("btn_principal")
        btn_suma.clicked.connect(self._sumar)
        col.addWidget(btn_suma)

        btn_deriv = QPushButton("Derivar P1 ∂")
        btn_deriv.setObjectName("btn_secundario") #este boton es para la derivada, lo he llamado asi porque es una operacion secundaria
        btn_deriv.clicked.connect(self._derivar)
        col.addWidget(btn_deriv)

        grp_eval = QGroupBox("Evaluar en x =")
        grp_eval.setObjectName("grupo")
        lay_e = QHBoxLayout(grp_eval)
        self.inp_x = QLineEdit("2")
        self.inp_x.setObjectName("entrada")
        btn_eval = QPushButton("Calcular")
        btn_eval.setObjectName("btn_secundario")
        btn_eval.clicked.connect(self._evaluar)
        lay_e.addWidget(self.inp_x)
        lay_e.addWidget(btn_eval)
        col.addWidget(grp_eval)

        self.consola = QTextEdit()
        self.consola.setObjectName("consola")
        self.consola.setReadOnly(True)
        self.consola.setPlaceholderText("Los resultados aparecerán aquí...")
        col.addWidget(self.consola)

        root.addWidget(panel)

        # ── Gráfica ──────────────────────────────────────────
        self.canvas = GraficaCanvas()
        root.addWidget(self.canvas, stretch=1)

    def _grupo_entrada(self, nombre, prefijo):
        """Crea un grupo con campo de texto y botón de carga."""
        grp = QGroupBox(nombre)
        grp.setObjectName("grupo")
        lay = QVBoxLayout(grp)
        hint = QLabel("Términos: coef,exp separados por espacio")
        hint.setObjectName("hint")
        lay.addWidget(hint)
        inp = QLineEdit()
        inp.setObjectName("entrada")
        inp.setPlaceholderText("3,4 2,1 1,0  →  3x⁴ + 2x + 1")
        setattr(self, f"inp_{prefijo}", inp)
        lay.addWidget(inp)
        btn = QPushButton(f"Cargar {nombre}")
        btn.setObjectName("btn_secundario")
        btn.clicked.connect(lambda _, p=prefijo: self._cargar(p))
        lay.addWidget(btn)
        return grp

    #Lógica 

    def _parsear(self, texto: str) -> Polinomio:
        """Convierte '3,4 2,1 1,0' en un Polinomio"""
        poly = Polinomio()
        for par in texto.strip().split():###separo cada termino por espacio, y 
            #luego cada coeficiente y exponente por coma.
            c, e = par.split(",") #separo por termino, controlo el valor.
            poly.insertar(int(c), int(e))
        return poly

    def _cargar(self, prefijo: str):
        inp = getattr(self, f"inp_{prefijo}")#uso un prefijo ya que desconozco si sera p1 o p2
        try:
            poly = self._parsear(inp.text())
            if prefijo == "p1":
                self.poly1 = poly
            else:
                self.poly2 = poly
            self._log(f"✅ {prefijo.upper()} → {poly.mostrar()}")#upper funciona que lo vuelve mayuscula. 
            self._graficar()
        except Exception as err:
            self._log(f"Error, capa 8: {err}")#el error, capa 8. 

    def _sumar(self):
        if not self.poly1 or not self.poly2:
            self._log("⚠️  Carga P1 y P2 primero.")
            return
        self.poly_suma = self.poly1.sumar(self.poly2)
        self._log(f"➕ P1 + P2 = {self.poly_suma.mostrar()}")
        self._graficar()

    def _derivar(self):
        if not self.poly1:
            self._log("⚠️  Carga P1 primero.")
            return
        deriv = self.poly1.derivar()
        self._log(f"∂ P1' = {deriv.mostrar()}")
        self.canvas.graficar(
            [self.poly1, deriv],
            [f"P1: {self.poly1.mostrar()}", f"P1': {deriv.mostrar()}"],
            titulo="P1 y su Derivada"
        )

    def _evaluar(self):
        try:
            x = float(self.inp_x.text())
        except ValueError:
            self._log("❌ Número inválido.")
            return
        if self.poly1:
            self._log(f"📌 P1({x}) = {self.poly1.evaluar(x):.6f}")
        if self.poly2:
            self._log(f"📌 P2({x}) = {self.poly2.evaluar(x):.6f}")
        if self.poly_suma:
            self._log(f"📌 Suma({x}) = {self.poly_suma.evaluar(x):.6f}")

    def _graficar(self):
        polys, labels = [], []
        if self.poly1:
            polys.append(self.poly1)
            labels.append(f"P1: {self.poly1.mostrar()}")
        if self.poly2:
            polys.append(self.poly2)
            labels.append(f"P2: {self.poly2.mostrar()}")
        if self.poly_suma:
            polys.append(self.poly_suma)
            labels.append(f"P1+P2: {self.poly_suma.mostrar()}")
        if polys:
            self.canvas.graficar(polys, labels)

    def _log(self, msg: str):
        self.consola.append(msg)