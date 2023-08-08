import sys

from buttons import ButtonsGrid
from display import Display
from info import Info
from main_window import MainWindow
from PySide6.QtWidgets import QApplication
from styles import setupTheme

if __name__ == "__main__":
    #  Cria a aplicação
    app = QApplication(sys.argv)
    window = MainWindow()
    setupTheme()

    # info
    info = Info("Sua conta")
    window.addWidgetToVLayout(info)

    # Display
    display = Display()
    window.addWidgetToVLayout(display)

    # Grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.addLayoutToVLayout(buttonsGrid)

    # Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()
