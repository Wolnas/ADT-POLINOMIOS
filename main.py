# ================================================================
#  main.py — Punto de entrada del proyecto
#  Corre este archivo: python main.py
# ================================================================

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QTabWidget
)
from estilos import estilos1
from taboperaciones import TabOperaciones
from tabtaylors import TabTaylor
from tabmemoria import TabMemoria


class VentanaPrincipal(QMainWindow):
    """
    Ventana principal con tres pestañas conectadas:
      - Pestaña 1: Operaciones con polinomios (lista enlazada)
      - Pestaña 2: Series de Taylor + Física Relativista
      - Pestaña 3: Simulador de Asignación de Memoria
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADT Polinomio — INF-220")
        self.setMinimumSize(1200, 750)
        self.setStyleSheet(estilos1)
        self._build()

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # ── Encabezado ────────────────────────────────────────
        header = QWidget()
        header.setObjectName("header")
        hlay = QHBoxLayout(header)
        hlay.setContentsMargins(20, 12, 20, 12)
        titulo = QLabel("🔢  ADT Polinomio")
        titulo.setObjectName("titulo")
        sub = QLabel(
            "Lista Enlazada · Series de Taylor · "
            "Física Relativista · Memoria · INF-220"
        )
        sub.setObjectName("subtitulo")
        hlay.addWidget(titulo)
        hlay.addWidget(sub)
        hlay.addStretch()
        lay.addWidget(header)

        # ── Pestañas conectadas ───────────────────────────────
        tabs = QTabWidget()
        tabs.setObjectName("tabs")

        # Pestaña 1 — base, las otras la referencian
        self.tab_op  = TabOperaciones()
        self.tab_tay = TabTaylor(tab_operaciones=self.tab_op)
        self.tab_mem = TabMemoria(tab_operaciones=self.tab_op)

        tabs.addTab(self.tab_op,  "  ∑  Operaciones  ")
        tabs.addTab(self.tab_tay, "  ⚡  Taylor & Relatividad  ")
        tabs.addTab(self.tab_mem, "  🧠  Memoria  ")

        lay.addWidget(tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())