# ================================================================
#  estilos.py — Tema visual (Catppuccin Mocha)
# ================================================================

estilos1 = """
    QMainWindow, QWidget {
        background-color: #1e1e2e;
        color: #cdd6f4;
        font-family: 'Segoe UI', 'Arial', sans-serif;
        font-size: 13px;
    }
    #header {
        background-color: #181825;
        border-bottom: 1px solid #313244;
    }
    #titulo {
        font-size: 20px;
        font-weight: bold;
        color: #89b4fa;
        margin-right: 16px;
    }
    #subtitulo { font-size: 11px; color: #585b70; }
    QTabWidget#tabs::pane {
        border: none;
        background-color: #1e1e2e;
    }
    QTabBar::tab {
        background-color: #181825;
        color: #6c7086;
        padding: 10px 20px;
        border: none;
        font-size: 13px;
    }
    QTabBar::tab:selected {
        background-color: #1e1e2e;
        color: #89b4fa;
        border-bottom: 2px solid #89b4fa;
        font-weight: bold;
    }
    QGroupBox#grupo {
        border: 1px solid #313244;
        border-radius: 8px;
        margin-top: 10px;
        padding: 10px 8px 8px 8px;
        color: #b4befe;
        font-weight: bold;
    }
    QGroupBox#grupo::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }
    QLineEdit#entrada {
        background-color: #313244;
        border: 1px solid #45475a;
        border-radius: 6px;
        padding: 6px 10px;
        color: #cdd6f4;
    }
    QLineEdit#entrada:focus { border: 1px solid #89b4fa; }
    QComboBox#combo {
        background-color: #313244;
        border: 1px solid #45475a;
        border-radius: 6px;
        padding: 6px 10px;
        color: #cdd6f4;
    }
    QComboBox#combo::drop-down { border: none; }
    QComboBox#combo QAbstractItemView {
        background-color: #313244;
        color: #cdd6f4;
        selection-background-color: #45475a;
    }
    QSlider#slider::groove:horizontal {
        height: 4px;
        background: #313244;
        border-radius: 2px;
    }
    QSlider#slider::handle:horizontal {
        background: #89b4fa;
        width: 14px;
        height: 14px;
        margin: -5px 0;
        border-radius: 7px;
    }
    QSlider#slider::sub-page:horizontal {
        background: #89b4fa;
        border-radius: 2px;
    }
    QPushButton#btn_principal {
        background-color: #89b4fa;
        border: none;
        border-radius: 7px;
        padding: 10px;
        color: #1e1e2e;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton#btn_principal:hover { background-color: #b4befe; }
    QPushButton#btn_secundario {
        background-color: #313244;
        border: 1px solid #45475a;
        border-radius: 6px;
        padding: 7px 12px;
        color: #cdd6f4;
    }
    QPushButton#btn_secundario:hover { background-color: #45475a; }
    QTextEdit#consola {
        background-color: #181825;
        border: 1px solid #313244;
        border-radius: 8px;
        padding: 8px;
        color: #a6e3a1;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
    }
    #hint { color: #585b70; font-size: 11px; }
    #info_texto { color: #cdd6f4; font-size: 12px; }
"""