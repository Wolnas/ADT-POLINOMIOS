# ================================================================
#  vista/polinomio_view.py — Vista principal en Kivy
#  ADT Polinomio — INF-220 Estructuras de Datos I
#  Pestaña 1: operaciones con lista enlazada
#  Pestaña 2: gráfica del polinomio y su derivada
# ================================================================

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.widget import Widget
from kivy.core.window import Window

from controlador.controladores import CtrlPolinomio

# Fondo oscuro
Window.clearcolor = (0.118, 0.118, 0.180, 1)



#  Widget de Gráfica 


class GraficaWidget(Widget):
    """Dibuja polinomios en un plano cartesiano usando Canvas Kivy."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.curvas = []   # lista de (puntos, color, label)
        self.bind(size=self._redibujar, pos=self._redibujar)

    def actualizar(self, curvas):
        """curvas: lista de tuplas (puntos, color, label)"""
        self.curvas = curvas
        self._redibujar()

    def _redibujar(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Fondo
            Color(0.118, 0.118, 0.180, 1)
            Rectangle(pos=self.pos, size=self.size)

            # Cuadrícula
            Color(0.192, 0.196, 0.247, 1)
            paso = self.width / 20
            x = self.x
            while x <= self.x + self.width:
                Line(points=[x, self.y, x, self.y + self.height], width=0.5)
                x += paso
            y = self.y
            while y <= self.y + self.height:
                Line(points=[self.x, y, self.x + self.width, y], width=0.5)
                y += paso

            # Ejes
            Color(0.271, 0.282, 0.353, 1)
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2
            Line(points=[self.x, cy, self.x + self.width, cy], width=1)
            Line(points=[cx, self.y, cx, self.y + self.height], width=1)

            # Curvas
            for puntos, color, _ in self.curvas:
                self._dibujar_curva(puntos, color)

    def _dibujar_curva(self, datos, color):
        xs, ys = datos
        if xs is None or len(xs) == 0:
            return

        x_min, x_max = float(xs[0]), float(xs[-1])
        y_min, y_max = float(min(ys)), float(max(ys))
        if x_max == x_min or y_max == y_min:
            return

        puntos = []
        for xi, yi in zip(xs, ys):
            px = self.x + (float(xi) - x_min) / (x_max - x_min) * self.width
            py = self.y + (float(yi) - y_min) / (y_max - y_min) * self.height
            puntos.extend([px, py])

        with self.canvas:
            Color(*color)
            Line(points=puntos, width=1.8)



#  Pestaña 1 — Operaciones (lista enlazada)


class TabOperaciones(BoxLayout):
    """
    Pestaña principal. donde se ve toda la parte entre la interaccion usuario-computadora.
    """

    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 14
        self.spacing = 10
        self.ctrl = ctrl
        self._construir()

    def _construir(self):
        # Título
        titulo = Label(
            text="Polinomio, Lista Enlazada, basico",
            font_size=20,
            bold=True,
            color=(0.537, 0.706, 0.980, 1),
            size_hint=(1, 0.06)
        )
        self.add_widget(titulo)

        subtitulo = Label(
            text="Operaciones con polinomios representados como lista enlazada",
            font_size=12,
            color=(0.345, 0.357, 0.439, 1),
            size_hint=(1, 0.04)
        )
        self.add_widget(subtitulo)

        # Polinomio P1
        self.add_widget(self._label("Polinomio P1"))   #parte importante del codigo. 
        self.inp_p1 = self._input(
            "3,4 2,1 1,0 ejemplo:3x⁴ + 2x + 1"
        )
        self.add_widget(self.inp_p1)
        self.add_widget(self._boton(
            "Cargar P1", lambda x: self._cargar("p1") #lambda lo uso porque
            #es una funciona anonima para que no se ejecute inmediatamente.
              
        ))

        # Polinomio P2
        self.add_widget(self._label("Polinomio P2"))
        self.inp_p2 = self._input(
            "3,4 2,1 1,0  ejemplo: 3x⁴ + 2x + 1"
        )
        self.add_widget(self.inp_p2)
        self.add_widget(self._boton(
            "Cargar P2", lambda x: self._cargar("p2")
        ))

        # Sumar
        self.add_widget(self._boton_principal(
            "Sumar P1 + P2", self._sumar
        ))

        # Evaluar
        self.add_widget(self._label("Evaluar en x ="))
        fila_eval = BoxLayout(size_hint=(1, 0.07), spacing=6)
        self.inp_x = TextInput(
            text="2", multiline=False,
            background_color=(0.192, 0.196, 0.247, 1),
            foreground_color=(0.804, 0.839, 0.957, 1),
            font_size=13
        )
        fila_eval.add_widget(self.inp_x)
        fila_eval.add_widget(self._boton("Calcular", self._evaluar))
        self.add_widget(fila_eval)

        # Consola
        self.add_widget(self._label("Resultados")) #datos de las letras
        scroll = ScrollView(size_hint=(1, 0.4))
        self.consola = Label(
            text="Los resultados aparecerán aquí...",
            color=(0.651, 0.890, 0.631, 1),
            font_size=12,
            size_hint_y=None,
            halign="left",
            valign="top",
            text_size=(None, None)
        )
        self.consola.bind(
            width=lambda *x: setattr(
                self.consola, 'text_size',
                (self.consola.width, None)
            ),
            texture_size=lambda *x: setattr(
                self.consola, 'height',
                self.consola.texture_size[1]
            )
        )
        scroll.add_widget(self.consola)
        self.add_widget(scroll)

    # Helpers

    def _label(self, texto):
        return Label(
            text=texto,
            color=(0.706, 0.745, 0.996, 1),
            font_size=12, bold=True,
            size_hint=(1, 0.04), halign="left"
        )

    def _input(self, hint):
        return TextInput(
            hint_text=hint, multiline=False,
            size_hint=(1, 0.06),
            background_color=(0.192, 0.196, 0.247, 1),
            foreground_color=(0.804, 0.839, 0.957, 1),
            cursor_color=(0.537, 0.706, 0.980, 1),
            font_size=13
        )

    def _boton(self, texto, callback):
        btn = Button(
            text=texto, size_hint=(1, 0.06),
            background_color=(0.192, 0.196, 0.247, 1),
            color=(0.804, 0.839, 0.957, 1),
            font_size=13
        )
        btn.bind(on_press=callback)
        return btn

    def _boton_principal(self, texto, callback):
        btn = Button(
            text=texto, size_hint=(1, 0.07),
            background_color=(0.537, 0.706, 0.980, 1),
            color=(0.118, 0.118, 0.180, 1),
            font_size=14, bold=True
        )
        btn.bind(on_press=callback)
        return btn

    # Lógica

    def _cargar(self, cual):
        inp = self.inp_p1 if cual == "p1" else self.inp_p2  #usamos self.inp_p1 o el 2,
        #de la liena 132.
        try:
            resultado = self.ctrl.cargar(inp.text, cual)
            self._log(f"{cual.upper()}:{resultado}")
            nodos = self._listar_nodos(
                self.ctrl.poly1 if cual == "p1" else self.ctrl.poly2
            )
            self._log(f"Nodos:\n{nodos}")
        except Exception as e:
            self._log(f"Error: {e}")

    def _sumar(self, *args):
        resultado = self.ctrl.sumar()
        if resultado:
            self._log(f"P1 + P2 = {resultado}")
        else:
            self._log("Carga P1 y P2 primero.")

    def _evaluar(self, *args):
        try:
            x = float(self.inp_x.text)
            if self.ctrl.poly1:
                self._log(
                    f"P1({x}) = {self.ctrl.poly1.evaluar(x):.6f}"
                )
            if self.ctrl.poly2:
                self._log(
                    f"P2({x}) = {self.ctrl.poly2.evaluar(x):.6f}"
                )
            if self.ctrl.poly_suma:
                self._log(
                    f"Suma({x}) = {self.ctrl.poly_suma.evaluar(x):.6f}"
                )
        except ValueError:
            self._log("Ingresa un número válido.")

    def _listar_nodos(self, poly):
        lineas = []
        actual = poly.cabeza
        i = 1
        while actual:
            sig = "siguiente" if actual.siguiente else "Ninguno"
            lineas.append(
                f"    Nodo {i}: coef={actual.coeficiente}, "
                f"exp={actual.exponente}:{sig}"
            )
            actual = actual.siguiente
            i += 1
        return "\n".join(lineas)

    def _log(self, msg):
        actual = self.consola.text
        if actual == "Los resultados aparecerán aquí...":
            self.consola.text = msg
        else:
            self.consola.text = actual + "\n" + msg #agrego y lo concateno.



#  Pestaña 2 — Gráfica con Derivada (extra)


class TabDerivada(BoxLayout):
    """
    Pestaña secundaria. Muestra la gráfica de P1 y su derivada
    para visualizar la relación matemática entre ambas.
    """

    def __init__(self, ctrl, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 14
        self.spacing = 10
        self.ctrl = ctrl
        self._construir()

    def _construir(self):
        # Título
        titulo = Label(
            text="Análisis Gráfico — Polinomio y su Derivada",
            font_size=18,
            bold=True,
            color=(0.537, 0.706, 0.980, 1),
            size_hint=(1, 0.06)
        )
        self.add_widget(titulo)

        explicacion = Label(
            text=("La derivada de un polinomio muestra su pendiente "
                  "en cada punto. Donde la derivada cruza el eje X, "
                  "el polinomio tiene un máximo o mínimo local."),
            font_size=12,
            color=(0.345, 0.357, 0.439, 1),
            size_hint=(1, 0.06),
            text_size=(800, None),
            halign="center"
        )
        self.add_widget(explicacion)

        # Botón
        btn = Button(
            text="Graficar P1 y su Derivada",
            size_hint=(1, 0.08),
            background_color=(0.537, 0.706, 0.980, 1),
            color=(0.118, 0.118, 0.180, 1),
            font_size=14, bold=True
        )
        btn.bind(on_press=self._graficar_derivada)
        self.add_widget(btn)

        # Estado
        self.lbl_estado = Label(
            text="Carga P1 en la pestaña Operaciones y presiona el botón.",
            color=(0.706, 0.745, 0.996, 1),
            font_size=12,
            size_hint=(1, 0.05)
        )
        self.add_widget(self.lbl_estado)

        # Leyenda
        leyenda = BoxLayout(
            orientation="horizontal",
            size_hint=(1, 0.05),
            spacing=20
        )
        leyenda.add_widget(Label(
            text="[color=89b4fa]——[/color]  P1 (polinomio)",
            markup=True, font_size=12,
            color=(0.804, 0.839, 0.957, 1)
        ))
        leyenda.add_widget(Label(
            text="[color=fab387]——[/color]  P1' (derivada)",
            markup=True, font_size=12,
            color=(0.804, 0.839, 0.957, 1)
        ))
        self.add_widget(leyenda)

        # Gráfica
        self.grafica = GraficaWidget(size_hint=(1, 0.7))
        self.add_widget(self.grafica)

    def _graficar_derivada(self, *args):
        if not self.ctrl.poly1:
            self.lbl_estado.text = (
                "P1 no está cargado. Ve a la pestaña Operaciones."
            )
            return

        deriv = self.ctrl.poly1.derivar()
        puntos_p1     = self.ctrl.poly1.puntos()
        puntos_deriv  = deriv.puntos()

        self.grafica.actualizar([
            (puntos_p1,    (0.537, 0.706, 0.980, 1), "P1"),
            (puntos_deriv, (0.980, 0.702, 0.529, 1), "P1'")
        ])

        self.lbl_estado.text = (
            f"P1 = {self.ctrl.poly1.mostrar()}    |    "
            f"P1' = {deriv.mostrar()}"
        )



#  Layout principal con pestañas


class PolinomioLayout(TabbedPanel):
    """
    Contenedor principal de las pestañas operaciones y derivadas. 
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)#keywords arguments
        self.do_default_tab = False
        self.tab_pos = 'top_left' #topleft es la posicion de mis pestañas 
        self.background_color = (0.118, 0.118, 0.180, 1)

        # Compartir el controlador entre pestañas
        self.ctrl = CtrlPolinomio()

        # Pestaña 1
        tab1 = TabbedPanelItem(text="Polinomios")
        tab1.add_widget(TabOperaciones(self.ctrl))
        self.add_widget(tab1)

        # Pestaña 2
        tab2 = TabbedPanelItem(text="Derivada-Extra")
        tab2.add_widget(TabDerivada(self.ctrl))
        self.add_widget(tab2)