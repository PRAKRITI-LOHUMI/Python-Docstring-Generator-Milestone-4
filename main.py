"""
Main entry point for Docstring Generator Application.
Run this file to start the application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Start the Docstring Generator application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Docstring Generator Pro")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
