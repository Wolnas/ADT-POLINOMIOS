# ================================================================
#  graficas.py — Canvas de matplotlib embebido en PyQt6
# ================================================================

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

COLORES = ["#89b4fa", "#a6e3a1", "#f38ba8", "#fab387", "#cba6f7"]


class GraficaCanvas(FigureCanvas):
    """Canvas de matplotlib embebido en PyQt6."""

    def __init__(self):
        self.fig = Figure(facecolor="#1e1e2e")
        self.ax  = self.fig.add_subplot(111)#111 es para indicar que es una grafica de un solo panel, si fuera 221 seria una grafica de 4 paneles.
        super().__init__(self.fig)
        self._base()

    def _base(self, titulo="Gráfica del Polinomio"):
        ax = self.ax
        ax.set_facecolor("#1e1e2e")
        ax.tick_params(colors="#cdd6f4")
        for spine in ax.spines.values():
            spine.set_color("#45475a")
        ax.set_title(titulo, color="#cdd6f4", fontsize=12, pad=10)
        ax.axhline(0, color="#45475a", linewidth=0.9)
        ax.axvline(0, color="#45475a", linewidth=0.9)
        ax.grid(True, color="#313244", linewidth=0.5, linestyle="--")

    def graficar(self, polinomios, etiquetas,
                 titulo="Gráfica del Polinomio",
                 x_min=-10, x_max=10,
                 exacta=None, lbl_exacta=None):
        """
        Dibuja uno o más polinomios.
        Si se pasa 'exacta' (función numpy), la muestra punteada
        como referencia de la función real.
        """
        self.ax.clear()
        self._base(titulo)
        # Función exacta de referencia (punteada amarilla)
        if exacta is not None:
            xs = np.linspace(x_min, x_max, 600)
            ys = np.clip(exacta(xs), -1e4, 1e4)
            self.ax.plot(xs, ys, color="#f9e2af", linewidth=1.5,
                         linestyle="--", label=lbl_exacta or "Exacta",
                         alpha=0.8)
        # Polinomios aproximados (líneas sólidas)
        for i, (poly, label) in enumerate(zip(polinomios, etiquetas)):
            xs, ys = poly.puntos(x_min, x_max)
            self.ax.plot(xs, ys, color=COLORES[i % len(COLORES)],
                         linewidth=2.2, label=label)
        self.ax.legend(facecolor="#313244", edgecolor="#45475a",
                       labelcolor="#cdd6f4", fontsize=9)
        self.fig.tight_layout()
        self.draw()