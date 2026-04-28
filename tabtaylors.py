# ================================================================
#  tab_taylor.py — Pestaña 2: Taylor + Física Relativista
#  Conectada con TabOperaciones para usar los polinomios del usuario
# ================================================================

import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QGroupBox,
    QComboBox, QSlider
)
from PyQt6.QtCore import Qt
from taylor import TaylorPolinomio
from graficas import GraficaCanvas


class TabTaylor(QWidget):
    """
    Pestaña 2: Series de Taylor aplicadas a física relativista.

    Recibe una referencia a TabOperaciones para poder importar
    los polinomios que el usuario cargó y compararlos con las
    funciones exactas (γ, sin, cos, eˣ).

    Conexión clave:
        self.tab_op.poly1  →  polinomio P1 del usuario
        self.tab_op.poly2  →  polinomio P2 del usuario
    """

    FUNCIONES = {
        "sin(x)  — Oscilaciones / MAS": {
            "generador" : TaylorPolinomio.seno,
            "exacta"    : np.sin,
            "lbl_exacta": "sin(x) exacto",
            "x_min": -2 * np.pi, "x_max": 2 * np.pi,
            "info": (
                "sin(x) = x - x³/3! + x⁵/5! - ...\n\n"
                "Aplicaciones físicas:\n"
                "  · Movimiento Armónico Simple (MAS)\n"
                "  · Ondas electromagnéticas\n"
                "  · Interferencia y difracción\n\n"
                "Con pocos términos aproxima bien cerca de x=0.\n"
                "Necesita más términos para rangos mayores."
            )
        },
        "cos(x)  — Ondas / Interferencia": {
            "generador" : TaylorPolinomio.coseno,
            "exacta"    : np.cos,
            "lbl_exacta": "cos(x) exacto",
            "x_min": -2 * np.pi, "x_max": 2 * np.pi,
            "info": (
                "cos(x) = 1 - x²/2! + x⁴/4! - ...\n\n"
                "Aplicaciones físicas:\n"
                "  · Oscilaciones acopladas\n"
                "  · Óptica ondulatoria\n"
                "  · Transformada de Fourier"
            )
        },
        "eˣ      — Decaimiento radiactivo": {
            "generador" : TaylorPolinomio.exponencial,
            "exacta"    : np.exp,
            "lbl_exacta": "eˣ exacto",
            "x_min": -3, "x_max": 3,
            "info": (
                "eˣ = 1 + x + x²/2! + x³/3! + ...\n\n"
                "Aplicaciones físicas:\n"
                "  · Decaimiento radiactivo: N(t) = N₀·e^(-λt)\n"
                "  · Enfriamiento de Newton\n"
                "  · Mecánica cuántica (función de onda)\n\n"
                "Converge para todo x — siempre se acerca\n"
                "a eˣ con suficientes términos."
            )
        },
        "γ(β)    — Factor de Lorentz ★": {
            "generador" : TaylorPolinomio.lorentz,
            "exacta"    : lambda b: 1 / np.sqrt(np.maximum(1 - b**2, 1e-10)),
            "lbl_exacta": "γ(β) exacto",
            "x_min": 0, "x_max": 0.95,
            "info": (
                "γ(β) = 1/√(1−β²)   donde β = v/c\n\n"
                "Taylor: γ ≈ 1 + ½β² + ⅜β⁴ + 5/16·β⁶ + ...\n\n"
                "⚡ INSIGHT FÍSICO:\n"
                "El primer término no trivial (½β²) es\n"
                "exactamente K_clásica / mc²:\n\n"
                "   K_clásica = ½mv² = ½mc²β²\n\n"
                "La mecánica de Newton ES la aproximación\n"
                "de primer orden de la relatividad.\n\n"
                "La diferencia se nota en β > 0.1 (v > 10%c).\n"
                "A β=0.99 → γ ≈ 7.09  ¡el tiempo dilata 7 veces!"
            )
        },
        "K_rel   — Energía cinética relativista ★": {
            "generador" : TaylorPolinomio.lorentz_ke,
            "exacta"    : lambda b: 1 / np.sqrt(np.maximum(1 - b**2, 1e-10)) - 1,
            "lbl_exacta": "K_rel/mc² exacta",
            "x_min": 0, "x_max": 0.95,
            "info": (
                "K_rel/mc² = γ - 1 = ½β² + ⅜β⁴ + ...\n\n"
                "vs K_clásica/mc² = ½β²\n\n"
                "⚡ A bajas velocidades (β << 1):\n"
                "   K_rel ≈ K_clásica  (Newton es válido)\n\n"
                "⚡ A altas velocidades (β → 1):\n"
                "   K_rel → ∞\n\n"
                "Necesitarías energía infinita para llevar\n"
                "una masa hasta la velocidad de la luz.\n"
                "Por eso nada con masa puede alcanzar c."
            )
        },
    }

    def __init__(self, tab_operaciones=None):
        super().__init__()
        # Referencia a la pestaña de operaciones
        # para poder leer poly1 y poly2 del usuario
        self.tab_op      = tab_operaciones
        self.poly_actual = None
        self.poly_usuario = None   # polinomio importado desde Operaciones
        self._build()
        self._actualizar()

    def _build(self):
        root = QHBoxLayout(self)
        root.setSpacing(14)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Panel izquierdo ──────────────────────────────────
        panel = QWidget()
        panel.setFixedWidth(360)
        col = QVBoxLayout(panel)
        col.setSpacing(10)

        # Selector de función
        grp_func = QGroupBox("Función a aproximar")
        grp_func.setObjectName("grupo")
        lay_f = QVBoxLayout(grp_func)
        self.combo = QComboBox()
        self.combo.setObjectName("combo")
        for nombre in self.FUNCIONES:
            self.combo.addItem(nombre)
        self.combo.currentIndexChanged.connect(self._actualizar)
        lay_f.addWidget(self.combo)
        col.addWidget(grp_func)

        # Slider de términos
        grp_terms = QGroupBox("Número de términos de Taylor")
        grp_terms.setObjectName("grupo")
        lay_t = QVBoxLayout(grp_terms)
        self.lbl_terms = QLabel("Términos: 3")
        self.lbl_terms.setObjectName("hint")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setValue(3)
        self.slider.setObjectName("slider")
        self.slider.valueChanged.connect(self._actualizar)
        lay_t.addWidget(self.lbl_terms)
        lay_t.addWidget(self.slider)
        col.addWidget(grp_terms)

        # ── Conexión con Operaciones ──────────────────────────
        grp_import = QGroupBox("🔗 Importar desde Operaciones")
        grp_import.setObjectName("grupo")
        lay_imp = QVBoxLayout(grp_import)

        hint_imp = QLabel("Carga P1 o P2 en la otra pestaña\nluego impórtalo aquí para comparar")
        hint_imp.setObjectName("hint")
        lay_imp.addWidget(hint_imp)

        fila = QHBoxLayout()
        btn_p1 = QPushButton("Importar P1")
        btn_p1.setObjectName("btn_secundario")
        btn_p1.clicked.connect(lambda: self._importar("p1"))

        btn_p2 = QPushButton("Importar P2")
        btn_p2.setObjectName("btn_secundario")
        btn_p2.clicked.connect(lambda: self._importar("p2"))

        btn_limpiar = QPushButton("✕ Quitar")
        btn_limpiar.setObjectName("btn_secundario")
        btn_limpiar.clicked.connect(self._limpiar_usuario)

        fila.addWidget(btn_p1)
        fila.addWidget(btn_p2)
        fila.addWidget(btn_limpiar)
        lay_imp.addLayout(fila)

        self.lbl_importado = QLabel("Sin polinomio importado")
        self.lbl_importado.setObjectName("hint")
        lay_imp.addWidget(self.lbl_importado)

        col.addWidget(grp_import)

        # Evaluar
        grp_eval = QGroupBox("Evaluar en β o x =")
        grp_eval.setObjectName("grupo")
        lay_e = QHBoxLayout(grp_eval)
        self.inp_x = QLineEdit("0.5")
        self.inp_x.setObjectName("entrada")
        btn_eval = QPushButton("Evaluar")
        btn_eval.setObjectName("btn_secundario")
        btn_eval.clicked.connect(self._evaluar)
        lay_e.addWidget(self.inp_x)
        lay_e.addWidget(btn_eval)
        col.addWidget(grp_eval)

        # Contexto físico
        grp_info = QGroupBox("📐 Contexto físico")
        grp_info.setObjectName("grupo")
        lay_i = QVBoxLayout(grp_info)
        self.lbl_info = QLabel()
        self.lbl_info.setObjectName("info_texto")
        self.lbl_info.setWordWrap(True)
        self.lbl_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        lay_i.addWidget(self.lbl_info)
        col.addWidget(grp_info, stretch=1)

        # Consola
        self.consola = QTextEdit()
        self.consola.setObjectName("consola")
        self.consola.setReadOnly(True)
        col.addWidget(self.consola)

        root.addWidget(panel)

        # ── Gráfica ──────────────────────────────────────────
        self.canvas = GraficaCanvas()
        root.addWidget(self.canvas, stretch=1)

    # ── Lógica de conexión ───────────────────────────────────

    def _importar(self, cual: str):
        """
        Lee poly1 o poly2 de TabOperaciones y lo guarda
        localmente para graficarlo junto a Taylor.
        """
        if not self.tab_op:
            self._log("❌ No hay conexión con Operaciones.")
            return
        poly = self.tab_op.poly1 if cual == "p1" else self.tab_op.poly2
        if not poly:
            self._log(f"⚠️  {cual.upper()} no está cargado en Operaciones.")
            return
        self.poly_usuario = poly
        self.lbl_importado.setText(f"Importado: {poly.mostrar()}")
        self._log(f"🔗 {cual.upper()} importado → {poly.mostrar()}")
        self._graficar()

    def _limpiar_usuario(self):
        """Quita el polinomio importado de la gráfica."""
        self.poly_usuario = None
        self.lbl_importado.setText("Sin polinomio importado")
        self._log("✕ Polinomio del usuario removido.")
        self._graficar()

    # ── Lógica de Taylor ─────────────────────────────────────

    def _func_actual(self):
        return self.FUNCIONES[self.combo.currentText()]

    def _actualizar(self):
        n   = self.slider.value()
        cfg = self._func_actual()
        self.lbl_terms.setText(f"Términos: {n}")
        self.poly_actual = cfg["generador"](n)
        self.lbl_info.setText(cfg["info"])
        self.consola.clear()
        self._log(f"📊 Taylor con {n} término(s):")
        self._log(f"   P(x) = {self.poly_actual.mostrar()}")
        self._graficar()

    def _evaluar(self):
        try:
            x = float(self.inp_x.text())
        except ValueError:
            self._log("❌ Número inválido.")
            return
        cfg    = self._func_actual()
        aprox  = self.poly_actual.evaluar(x)
        exacto = float(cfg["exacta"](np.array([x]))[0])
        error  = abs(exacto - aprox)
        self._log(f"\n📌 x = {x}")
        self._log(f"   Taylor   = {aprox:.8f}")
        self._log(f"   Exacto   = {exacto:.8f}")
        self._log(f"   Error    = {error:.2e}")
        # Si hay polinomio importado, también lo evalúa
        if self.poly_usuario:
            val_u  = self.poly_usuario.evaluar(x)
            err_u  = abs(exacto - val_u)
            self._log(f"   Tu poly  = {val_u:.8f}")
            self._log(f"   Error tu = {err_u:.2e}")

    def _graficar(self):
        cfg   = self._func_actual()
        polys = [self.poly_actual]
        labels = [f"Taylor ({self.slider.value()} términos)"]

        # Si hay polinomio importado, lo agrega a la gráfica
        if self.poly_usuario:
            polys.append(self.poly_usuario)
            labels.append(f"Tu polinomio: {self.poly_usuario.mostrar()}")

        self.canvas.graficar(
            polys, labels,
            titulo=self.combo.currentText().split("—")[0].strip(),
            x_min=cfg["x_min"], x_max=cfg["x_max"],
            exacta=cfg["exacta"],
            lbl_exacta=cfg["lbl_exacta"]
        )

    def _log(self, msg: str):
        self.consola.append(msg)