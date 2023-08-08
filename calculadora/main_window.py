from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox  # Exibe mensagens na tela
from PySide6.QtWidgets import QLayout, QMainWindow, QVBoxLayout, QWidget
from variables import WINDOW_ICON_PATH


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Configurando o layout básico
        self.cWidget = QWidget()
        self.vLayout = QVBoxLayout()
        self.cWidget.setLayout(self.vLayout)
        self.setCentralWidget(self.cWidget)

        # Título da janela
        self.setWindowTitle("Calculadora")

        # Define o ícone
        icon = QIcon(str(WINDOW_ICON_PATH))
        self.setWindowIcon(icon)

    def adjustFixedSize(self):
        # Última coisa a ser feita
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)

    def addLayoutToVLayout(self, layout: QLayout):
        self.vLayout.addLayout(layout)

    def makeMsgBox(self):
        return QMessageBox(self)
