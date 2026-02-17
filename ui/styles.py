"""
UI Styling for Docstring Generator.
Contains all CSS styles for the PyQt5 interface.
"""

MAIN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QTabWidget::pane {
    border: 1px solid #ddd;
    background-color: white;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #e0e0e0;
    color: #333;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    font-weight: bold;
    width: 200px;
}

QTabBar::tab:selected {
    background-color: #2196F3;
    color: white;
}

QTabBar::tab:hover {
    background-color: #64B5F6;
    color: white;
}

QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #1976D2;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton:disabled {
    background-color: #BDBDBD;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 12px;
}

QListWidget {
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
    padding: 5px;
}

QListWidget::item {
    padding: 8px;
    border-radius: 3px;
}

QListWidget::item:selected {
    background-color: #E3F2FD;
    color: #1976D2;
}

QListWidget::item:hover {
    background-color: #F5F5F5;
}

QLabel {
    color: #333;
    font-size: 13px;
}

QGroupBox {
    border: 2px solid #ddd;
    border-radius: 5px;
    margin-top: 10px;
    font-weight: bold;
    background-color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 5px 10px;
    color: #2196F3;
}

QRadioButton {
    spacing: 8px;
    font-size: 13px;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
}

QProgressBar {
    border: 1px solid #ddd;
    border-radius: 4px;
    text-align: center;
    background-color: #f0f0f0;
}

QProgressBar::chunk {
    background-color: #4CAF50;
    border-radius: 3px;
}

QComboBox {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
    font-size: 13px;
}

QComboBox:hover {
    border: 1px solid #2196F3;
}

QComboBox::drop-down {
    border: none;
}

QScrollBar:vertical {
    border: none;
    background-color: #f0f0f0;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #BDBDBD;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9E9E9E;
}
"""

HEADER_STYLE = """
QLabel {
    color: #1976D2;
    font-size: 16px;
    font-weight: bold;
    padding: 5px;
}
"""

SUBHEADER_STYLE = """
QLabel {
    color: #555;
    font-size: 14px;
    font-weight: bold;
    padding: 3px;
}
"""

INFO_LABEL_STYLE = """
QLabel {
    color: #666;
    font-size: 12px;
    padding: 2px;
}
"""

SUCCESS_STYLE = """
QLabel {
    color: #4CAF50;
    font-weight: bold;
}
"""

WARNING_STYLE = """
QLabel {
    color: #FF9800;
    font-weight: bold;
}
"""

ERROR_STYLE = """
QLabel {
    color: #F44336;
    font-weight: bold;
}
"""

CODE_EDITOR_STYLE = """
QPlainTextEdit {
    background-color: #1e1e1e;
    color: #d4d4d4;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 13px;
    line-height: 1.5;
    border: 1px solid #333;
    border-radius: 4px;
}
"""
