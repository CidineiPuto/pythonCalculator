from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from utils import isEmpty, isNumOrDot
from variables import BIG_FONT_SIZE, MINIMUM_WIDTH, TEXT_MARGIN


class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operadorPressed = Signal(str)
    negativePressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        margins = [TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f"font-size: {BIG_FONT_SIZE}px")
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [
            KEYS.Key_Plus,
            KEYS.Key_Minus,
            KEYS.Key_Slash,
            KEYS.Key_Asterisk,
            KEYS.Key_P,
            KEYS.Key_AsciiCircum,
        ]
        isNegative = key in [KEYS.Key_N]
        if isEnter:
            self.eqPressed.emit()
            return event.ignore()
        if isDelete:
            self.delPressed.emit()
            return event.ignore()
        if isEsc:
            self.clearPressed.emit()
            return event.ignore()

        if isNegative:
            self.negativePressed.emit(text)
            return event.ignore()

        if isOperator:
            if text.lower() == "p" or text == "~":
                text = "^"
            self.operadorPressed.emit(text)
            return event.ignore()

        # Não passarás se texto não houver.
        if isEmpty(text):
            return event.ignore()

        if isNumOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()
