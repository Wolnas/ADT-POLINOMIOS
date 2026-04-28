# ================================================================
#  tab_memoria.py — Pestaña 3: Simulador de Asignación de Memoria
# ================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QGroupBox,
    QComboBox, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QFont, QBrush
from memoria import SimuladorMemoria


# ── Canvas visual ─────────────────────────────────────────────

class MemoriaCanvas(QWidget):

    ALTO = 44
    MARGEN = 10

    def __init__(self):
        super().__init__()
        self.bloques_libres   = []
        self.bloques_ocupados = []
        self.nodos_poly       = []
        self.total            = 1024
        self.setMinimumHeight(140)

    def actualizar(self, sim, nodos_poly=None):
        self.bloques_libres   = sim.bloques_libres()
        self.bloques_ocupados = sim.asignados[:]
        self.nodos_poly       = nodos_poly or []
        self.total            = sim.TAMANIO_TOTAL
        self.update()

    def paintEvent(self, event):
        p     = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        ancho  = self.width() - 2 * self.MARGEN
        escala = ancho / self.total
        y      = self.MARGEN

        # Fondo
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#313244"))
        p.drawRoundedRect(self.MARGEN, y, ancho, self.ALTO, 6, 6)

        # Bloques ocupados
        for b in self.bloques_ocupados:
            x = self.MARGEN + int(b["direccion"] * escala)
            w = max(int(b["tamanio"] * escala), 3)
            p.setBrush(QColor("#f38ba8"))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(x, y, w, self.ALTO, 3, 3)
            if w > 30:
                p.setPen(QColor("#1e1e2e"))
                p.setFont(QFont("Consolas", 8))
                p.drawText(x+3, y+3, w-6, self.ALTO-6,
                           Qt.AlignmentFlag.AlignCenter,
                           b["nombre"][:6])
                p.setPen(Qt.PenStyle.NoPen)

        # Bloques libres
        for dir_, tam in self.bloques_libres:
            x = self.MARGEN + int(dir_ * escala)
            w = max(int(tam * escala), 3)
            p.setBrush(QColor("#a6e3a1"))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(x, y, w, self.ALTO, 3, 3)
            if w > 50:
                p.setPen(QColor("#1e1e2e"))
                p.setFont(QFont("Consolas", 8))
                p.drawText(x+3, y+3, w-6, self.ALTO-6,
                           Qt.AlignmentFlag.AlignCenter,
                           f"{tam}B")
                p.setPen(Qt.PenStyle.NoPen)

        # Nodos del polinomio (segunda fila)
        if self.nodos_poly:
            y2     = y + self.ALTO + 10
            total2 = max(d + t for d, t, _ in self.nodos_poly) + 64
            esc2   = ancho / total2
            self.setMinimumHeight(y2 + self.ALTO + 40)

            lbl_y = y2 - 4
            p.setPen(QColor("#b4befe"))
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(self.MARGEN, lbl_y, 200, 14,
                       Qt.AlignmentFlag.AlignLeft, "Nodos del polinomio:")

            for dir_, tam, termino in self.nodos_poly:
                x = self.MARGEN + int(dir_ * esc2)
                w = max(int(tam * esc2 * 1.2), 70)
                if x + w > self.MARGEN + ancho:
                    x = self.MARGEN + ancho - w - 4
                p.setBrush(QColor("#89b4fa"))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawRoundedRect(x, y2, w, self.ALTO, 4, 4)
                p.setPen(QColor("#1e1e2e"))
                p.setFont(QFont("Consolas", 9))
                p.drawText(x+4, y2+4, w-8, self.ALTO-8,
                           Qt.AlignmentFlag.AlignCenter, termino)
                p.setPen(Qt.PenStyle.NoPen)

            # Flechas entre nodos
            p.setPen(QColor("#cba6f7"))
            p.setFont(QFont("Segoe UI", 10))
            for i in range(len(self.nodos_poly) - 1):
                dir1, tam1, _ = self.nodos_poly[i]
                dir2, _, _    = self.nodos_poly[i + 1]
                x1 = self.MARGEN + int(dir1 * esc2) + max(int(tam1 * esc2 * 1.2), 70)
                x2 = self.MARGEN + int(dir2 * esc2)
                cy = y2 + self.ALTO // 2
                p.drawLine(x1, cy, x2, cy)
                p.drawText(x2 - 8, cy - 6, "→")
            p.setPen(Qt.PenStyle.NoPen)

        # Leyenda
        y_leg = (y + self.ALTO + (self.ALTO + 20) * bool(self.nodos_poly) + 16)
        self.setMinimumHeight(y_leg + 20)
        items = [(QColor("#a6e3a1"), "Libre"),
                 (QColor("#f38ba8"), "Ocupado"),
                 (QColor("#89b4fa"), "Nodo polinomio")]
        xleg = self.MARGEN
        for col, lbl in items:
            p.setBrush(col)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(xleg, y_leg, 12, 12, 3, 3)
            p.setPen(QColor("#cdd6f4"))
            p.setFont(QFont("Segoe UI", 9))
            p.drawText(xleg + 16, y_leg, 110, 14,
                       Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                       lbl)
            xleg += 130


# ── Tabla de nodos ────────────────────────────────────────────

class TablaNodos(QTableWidget):
    """
    Tabla que muestra cada nodo del polinomio con:
    Nodo | Término | Dirección | Tamaño | Siguiente
    """
    HEADERS = ["#", "Término", "Dirección", "Tamaño", "Siguiente →"]

    def __init__(self):
        super().__init__(0, len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setStyleSheet("""
            QTableWidget {
                background-color: #181825;
                color: #cdd6f4;
                gridline-color: #313244;
                border: 1px solid #313244;
                border-radius: 6px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #313244;
                color: #b4befe;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item:alternate {
                background-color: #1e1e2e;
            }
            QTableWidget::item:selected {
                background-color: #45475a;
            }
        """)

    def cargar_nodos(self, nodos):
        """
        Recibe lista de (dir, tam, termino) y llena la tabla.
        La columna Siguiente muestra la dirección del próximo nodo.
        """
        self.setRowCount(len(nodos))
        for i, (dir_, tam, termino) in enumerate(nodos):
            siguiente = (str(nodos[i+1][0]) if i + 1 < len(nodos)
                         else "None")
            valores = [str(i+1), termino, str(dir_),
                       f"{tam} B", siguiente]
            for j, val in enumerate(valores):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # Color especial para la columna Siguiente
                if j == 4:
                    item.setForeground(
                        QBrush(QColor("#cba6f7" if siguiente != "None"
                                       else "#6c7086")))
                self.setItem(i, j, item)


# ── Pestaña principal ─────────────────────────────────────────

class TabMemoria(QWidget):

    def __init__(self, tab_operaciones=None):
        super().__init__()
        self.tab_op     = tab_operaciones
        self.sim        = SimuladorMemoria()
        self.nodos_poly = []
        self._build()
        self._refrescar()

    def _build(self):
        root = QHBoxLayout(self)
        root.setSpacing(14)
        root.setContentsMargins(12, 12, 12, 12)

        # ── Panel izquierdo ──────────────────────────────────
        panel = QWidget()
        panel.setFixedWidth(340)
        col = QVBoxLayout(panel)
        col.setSpacing(10)

        # Solicitar
        grp_sol = QGroupBox("Solicitar memoria")
        grp_sol.setObjectName("grupo")
        lay_s = QVBoxLayout(grp_sol)
        fila1 = QHBoxLayout()
        self.inp_nombre = QLineEdit()
        self.inp_nombre.setObjectName("entrada")
        self.inp_nombre.setPlaceholderText("Nombre")
        self.inp_tam = QLineEdit()
        self.inp_tam.setObjectName("entrada")
        self.inp_tam.setPlaceholderText("Bytes")
        self.inp_tam.setFixedWidth(80)
        fila1.addWidget(self.inp_nombre)
        fila1.addWidget(self.inp_tam)
        lay_s.addLayout(fila1)
        fila2 = QHBoxLayout()
        self.combo_est = QComboBox()
        self.combo_est.setObjectName("combo")
        self.combo_est.addItems(["Primer ajuste", "Mejor ajuste"])
        btn_sol = QPushButton("Solicitar")
        btn_sol.setObjectName("btn_principal")
        btn_sol.clicked.connect(self._solicitar)
        fila2.addWidget(self.combo_est)
        fila2.addWidget(btn_sol)
        lay_s.addLayout(fila2)
        col.addWidget(grp_sol)

        # Liberar
        grp_lib = QGroupBox("Liberar memoria")
        grp_lib.setObjectName("grupo")
        lay_l = QHBoxLayout(grp_lib)
        self.inp_dir = QLineEdit()
        self.inp_dir.setObjectName("entrada")
        self.inp_dir.setPlaceholderText("Dirección")
        btn_lib = QPushButton("Liberar")
        btn_lib.setObjectName("btn_secundario")
        btn_lib.clicked.connect(self._liberar)
        lay_l.addWidget(self.inp_dir)
        lay_l.addWidget(btn_lib)
        col.addWidget(grp_lib)

        # Nodos del polinomio
        grp_poly = QGroupBox("🔗 Nodos del polinomio")
        grp_poly.setObjectName("grupo")
        lay_p = QVBoxLayout(grp_poly)
        hint = QLabel("Carga P1 o P2 en Operaciones")
        hint.setObjectName("hint")
        lay_p.addWidget(hint)
        fila_p = QHBoxLayout()
        btn_p1 = QPushButton("Ver P1")
        btn_p1.setObjectName("btn_secundario")
        btn_p1.clicked.connect(lambda: self._ver_nodos("p1"))
        btn_p2 = QPushButton("Ver P2")
        btn_p2.setObjectName("btn_secundario")
        btn_p2.clicked.connect(lambda: self._ver_nodos("p2"))
        btn_lim = QPushButton("✕")
        btn_lim.setObjectName("btn_secundario")
        btn_lim.setFixedWidth(32)
        btn_lim.clicked.connect(self._limpiar_poly)
        fila_p.addWidget(btn_p1)
        fila_p.addWidget(btn_p2)
        fila_p.addWidget(btn_lim)
        lay_p.addLayout(fila_p)
        col.addWidget(grp_poly)

        # Stats
        grp_st = QGroupBox("📊 Estado")
        grp_st.setObjectName("grupo")
        lay_st = QVBoxLayout(grp_st)
        self.lbl_libre   = QLabel()
        self.lbl_ocup    = QLabel()
        self.lbl_frag    = QLabel()
        self.lbl_bloq    = QLabel()
        for lbl in [self.lbl_libre, self.lbl_ocup,
                    self.lbl_frag, self.lbl_bloq]:
            lbl.setObjectName("info_texto")
            lay_st.addWidget(lbl)
        col.addWidget(grp_st)

        btn_reset = QPushButton("↺  Reiniciar memoria")
        btn_reset.setObjectName("btn_secundario")
        btn_reset.clicked.connect(self._reset)
        col.addWidget(btn_reset)

        self.consola = QTextEdit()
        self.consola.setObjectName("consola")
        self.consola.setReadOnly(True)
        col.addWidget(self.consola)

        root.addWidget(panel)

        # ── Panel derecho ─────────────────────────────────────
        panel_der = QWidget()
        lay_der = QVBoxLayout(panel_der)
        lay_der.setSpacing(10)

        # Mapa visual
        grp_vis = QGroupBox("Mapa de memoria (1024 bytes)")
        grp_vis.setObjectName("grupo")
        lay_v = QVBoxLayout(grp_vis)
        self.canvas = MemoriaCanvas()
        scroll_c = QScrollArea()
        scroll_c.setWidget(self.canvas)
        scroll_c.setWidgetResizable(True)
        scroll_c.setStyleSheet("background: transparent; border: none;")
        scroll_c.setMaximumHeight(200)
        lay_v.addWidget(scroll_c)
        lay_der.addWidget(grp_vis)

        # Tabla de nodos del polinomio
        grp_nodos = QGroupBox("📋 Nodos del polinomio en memoria")
        grp_nodos.setObjectName("grupo")
        lay_n = QVBoxLayout(grp_nodos)
        self.tabla_nodos = TablaNodos()
        scroll_n = QScrollArea()
        scroll_n.setWidget(self.tabla_nodos)
        scroll_n.setWidgetResizable(True)
        scroll_n.setStyleSheet("background: transparent; border: none;")
        lay_n.addWidget(scroll_n)
        lay_der.addWidget(grp_nodos, stretch=1)

        # Tabla de bloques de memoria
        grp_bloq = QGroupBox("Tabla de bloques libres y ocupados")
        grp_bloq.setObjectName("grupo")
        lay_b = QVBoxLayout(grp_bloq)
        self.tabla_bloq = QTextEdit()
        self.tabla_bloq.setObjectName("consola")
        self.tabla_bloq.setReadOnly(True)
        self.tabla_bloq.setMaximumHeight(140)
        lay_b.addWidget(self.tabla_bloq)
        lay_der.addWidget(grp_bloq)

        root.addWidget(panel_der, stretch=1)

    # ── Lógica ───────────────────────────────────────────────

    def _solicitar(self):
        nombre = self.inp_nombre.text().strip() or "Prog"
        try:
            tam = int(self.inp_tam.text())
        except ValueError:
            self._log("❌ Tamaño inválido.")
            return
        est = "primer" if self.combo_est.currentIndex() == 0 else "mejor"
        res = self.sim.solicitar_memoria(tam, nombre, est)
        if res:
            d, t = res
            self._log(f"✅ {nombre} → dir={d}, {t}B ({est} ajuste)")
        else:
            self._log(f"❌ Sin espacio para {tam}B")
        self._refrescar()

    def _liberar(self):
        try:
            dir_ = int(self.inp_dir.text())
        except ValueError:
            self._log("❌ Dirección inválida.")
            return
        ok = self.sim.liberar_memoria(dir_)
        if ok:
            self._log(f"🗑️  Liberado en dir={dir_}")
        else:
            self._log(f"❌ No hay bloque en dir={dir_}")
        self._refrescar()

    def _ver_nodos(self, cual):
        if not self.tab_op:
            self._log("❌ Sin conexión con Operaciones.")
            return
        poly = self.tab_op.poly1 if cual == "p1" else self.tab_op.poly2
        if not poly:
            self._log(f"⚠️  {cual.upper()} no está cargado.")
            return
        self.nodos_poly = self.sim.nodos_polinomio(poly)
        n = len(self.nodos_poly)
        tam_total = sum(t for _, t, _ in self.nodos_poly)
        self._log(f"\n🔵 {cual.upper()}: {n} nodos, {tam_total}B totales")
        self.tabla_nodos.cargar_nodos(self.nodos_poly)
        self._refrescar(self.nodos_poly)

    def _limpiar_poly(self):
        self.nodos_poly = []
        self.tabla_nodos.setRowCount(0)
        self._refrescar()

    def _reset(self):
        self.sim.reset()
        self.nodos_poly = []
        self.tabla_nodos.setRowCount(0)
        self._log("↺ Memoria reiniciada.")
        self._refrescar()

    def _refrescar(self, nodos_poly=None):
        np_ = nodos_poly or self.nodos_poly
        self.canvas.actualizar(self.sim, np_)

        libre  = self.sim.memoria_libre_total()
        ocup   = self.sim.memoria_ocupada_total()
        frag   = self.sim.fragmentacion()
        nbloq  = len(self.sim.bloques_libres())
        self.lbl_libre.setText(f"Libre:         {libre}B  ({libre*100//1024}%)")
        self.lbl_ocup.setText(f"Ocupada:       {ocup}B  ({ocup*100//1024}%)")
        self.lbl_frag.setText(f"Fragmentación: {frag}%")
        self.lbl_bloq.setText(f"Bloques libres: {nbloq}")

        # Tabla de bloques
        lineas = ["Dir       │ Tamaño │ Estado   │ Nombre",
                  "──────────┼────────┼──────────┼──────────"]
        todos = ([{"direccion": d, "tamanio": t,
                   "estado": "LIBRE", "nombre": "—"}
                  for d, t in self.sim.bloques_libres()] +
                 [{**b, "estado": "OCUPADO"} for b in self.sim.asignados])
        todos.sort(key=lambda x: x["direccion"])
        for b in todos:
            lineas.append(f"{b['direccion']:>8}  │ {b['tamanio']:>5}B │ "
                          f"{b['estado']:9}│ {b['nombre']}")
        self.tabla_bloq.setPlainText("\n".join(lineas))

    def _log(self, msg):
        self.consola.append(msg)