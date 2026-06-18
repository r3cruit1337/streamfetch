APP_TITLE = "StreamFetch"
APP_VERSION = "1.0.1"


CLR_BG          = "#0f0f11"
CLR_SURFACE     = "#1a1a1f"
CLR_BORDER      = "#2a2a35"
CLR_ACCENT      = "#ff4444"
CLR_ACCENT_DARK = "#cc2222"
CLR_TEXT        = "#e8e8ec"
CLR_SUBTEXT     = "#888896"
CLR_SUCCESS     = "#44cc88"
CLR_ERROR       = "#ff5555"
CLR_WARNING     = "#ffaa44"
CLR_INFO        = "#4488ff"
CLR_PROGRESS    = "#ff4444"

GLOBAL_STYLESHEET = f"""
QWidget {{
    background-color: {CLR_BG};
    color: {CLR_TEXT};
    font-family: "Consolas", "Courier New", monospace;
    font-size: 13px;
}}
QLabel {{
    background: transparent;
    color: {CLR_TEXT};
}}
QLabel#titleLabel {{
    font-size: 22px;
    font-weight: bold;
    color: {CLR_ACCENT};
    letter-spacing: 2px;
}}
QLabel#subtitleLabel {{
    font-size: 11px;
    color: {CLR_SUBTEXT};
    letter-spacing: 1px;
}}
QLabel#sectionLabel {{
    font-size: 11px;
    font-weight: bold;
    color: {CLR_SUBTEXT};
    letter-spacing: 2px;
    text-transform: uppercase;
}}
QLineEdit {{
    background-color: {CLR_SURFACE};
    border: 1px solid {CLR_BORDER};
    border-radius: 6px;
    padding: 10px 14px;
    color: {CLR_TEXT};
    font-size: 13px;
    selection-background-color: {CLR_ACCENT};
}}
QLineEdit:focus {{
    border: 1px solid {CLR_ACCENT};
}}
QLineEdit::placeholder {{
    color: {CLR_SUBTEXT};
}}
QComboBox {{
    background-color: {CLR_SURFACE};
    border: 1px solid {CLR_BORDER};
    border-radius: 6px;
    padding: 8px 12px;
    color: {CLR_TEXT};
    min-width: 160px;
}}
QComboBox:focus {{
    border: 1px solid {CLR_ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    padding-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {CLR_SURFACE};
    border: 1px solid {CLR_BORDER};
    selection-background-color: {CLR_ACCENT};
    color: {CLR_TEXT};
}}
QPushButton {{
    background-color: {CLR_SURFACE};
    border: 1px solid {CLR_BORDER};
    border-radius: 6px;
    padding: 10px 20px;
    color: {CLR_TEXT};
    font-weight: bold;
    font-size: 13px;
}}
QPushButton:hover {{
    background-color: {CLR_BORDER};
    border-color: {CLR_SUBTEXT};
}}
QPushButton:pressed {{
    background-color: #111116;
}}
QPushButton:disabled {{
    color: {CLR_SUBTEXT};
    border-color: {CLR_BORDER};
    background-color: {CLR_SURFACE};
}}
QPushButton#downloadBtn {{
    background-color: {CLR_ACCENT};
    border: none;
    color: #ffffff;
    font-size: 14px;
    letter-spacing: 1px;
    min-width: 140px;
}}
QPushButton#downloadBtn:hover {{
    background-color: #ff6666;
}}
QPushButton#downloadBtn:pressed {{
    background-color: {CLR_ACCENT_DARK};
}}
QPushButton#downloadBtn:disabled {{
    background-color: #552222;
    color: #884444;
}}
QProgressBar {{
    background-color: {CLR_SURFACE};
    border: 1px solid {CLR_BORDER};
    border-radius: 4px;
    text-align: center;
    color: {CLR_TEXT};
    font-size: 11px;
    height: 18px;
}}
QProgressBar::chunk {{
    background-color: {CLR_PROGRESS};
    border-radius: 3px;
}}
QTextEdit {{
    background-color: {CLR_SURFACE};
    border: 1px solid {CLR_BORDER};
    border-radius: 6px;
    padding: 10px;
    color: {CLR_TEXT};
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    selection-background-color: {CLR_ACCENT};
}}
QFrame[frameShape="4"],
QFrame[frameShape="HLine"] {{
    color: {CLR_BORDER};
    background-color: {CLR_BORDER};
    max-height: 1px;
    border: none;
}}
QScrollBar:vertical {{
    background: {CLR_BG};
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {CLR_BORDER};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {CLR_SUBTEXT};
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""