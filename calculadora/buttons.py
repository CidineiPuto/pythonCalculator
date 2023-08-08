import math
from typing import TYPE_CHECKING

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton, QWidget
from utils import ConvertToNumber, isEmpty, isNumOrDot, isValidNumber
from variables import MEDIUM_FONT_SIZE

if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow


class Button(QPushButton):
    def __init__(self, text: str, parent: None | QWidget = None) -> None:
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(
        self,
        display: "Display",
        info: "Info",
        window: "MainWindow",
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ["C", "◀", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["N", "0", ".", "="],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ""
        self._equationInitialValue = "Sua conta"
        self._left = None
        self.right = None
        self._op = None

        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value: str):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operadorPressed.connect(self._configLeftOp)
        self.display.negativePressed.connect(self._invertNumber)

        for rowNumber, rowData in enumerate(self._gridMask):
            for columnNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)
                self.addWidget(button, rowNumber, columnNumber)
                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()
        if text == "C":
            self._connectButtonClicked(button, self._clear)

        if text == "N":
            self._connectButtonClicked(button, self._invertNumber)

        if text == "◀":
            self._connectButtonClicked(button, self._backspace)

        if text in "+/*-^":
            self._connectButtonClicked(
                button,
                self._makeSlot(self._configLeftOp, text),
            )

        if text == "=":
            self._connectButtonClicked(button, self._eq)

    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool, result=None)  # Retorna bool, resultado None.
        def realSlot():
            func(*args, **kwargs)

        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        # newNumber = -float(displayText)
        # Ou

        number = ConvertToNumber(displayText) * -1

        self.display.setText(str(number))

    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text
        if not isValidNumber(newDisplayValue):
            return
        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self.right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configLeftOp(self, text):
        # buttonText = button.text()  # Get button text (+-/* etc...)
        displayText = self.display.text()  # Will be the left number "_left"
        self.display.clear()  # Clear display

        # if the person clicked on the operator and did not configure
        # any number v
        if not isValidNumber(displayText) and self._left is None:
            self._showError("Você não digitou nada.")
            return

        # If we have the left number , we will do nothing, and we will wait for
        # the right number.
        self.display.setFocus()

        if self._left is None:
            self._left = ConvertToNumber(displayText)

        self._op = text
        self.equation = f"{self._left} {self._op} ???"

    @Slot()
    def _eq(self):
        displayText = self.display.text()
        if not isValidNumber(displayText) or self._left is None:
            self._showError("Conta incompleta.")
            return

        self._right = ConvertToNumber(displayText)
        self.equation = f"{self._left} {self._op} {self._right}"
        result = "error"

        try:
            if "^" in self.equation and isinstance(self._left, float | int):
                result = math.pow(self._left, self._right)  # pow = potenciação
                result = ConvertToNumber(str(result))
            else:
                result = eval(self.equation)  # Cuidado usar eval
            if len(str(result)) > 20:
                result = "error"
                raise OverflowError

        except ZeroDivisionError:
            self._showError("Divisão com zero")
        except OverflowError:
            self._showError("Essa conta não pode ser realizada")
        except TypeError:
            self._showError("Conta impossível de ser realizada.")

        self.display.clear()
        self.info.setText(f"{self.equation} = {result}")
        self._left = result
        self._right = None

        if result == "error":
            self._left = None
        if type(result) == float:
            self.display.setText(str(round(result, 4)))
        else:
            self.display.setText(str(result))
        self.display.setFocus()

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
