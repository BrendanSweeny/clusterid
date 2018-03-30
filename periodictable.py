import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSignal
from periodictableui import Ui_PeriodicTable

class PeriodicTable(QWidget):

    # Custom signal
    elementEmitted = pyqtSignal(str, bool)

    def __init__(self):
        super().__init__()

        self.ui = Ui_PeriodicTable()
        self.ui.setupUi(self)

        # Iterates through all the element buttons ('ebtn') and adds click
        # behavior
        for name in dir(self.ui):
            subClass = 'ebtn'
            if subClass in name:
                btn = getattr(self.ui, name)
                btn.clicked[bool].connect(self.emitElement)

    # Slot for element button clicked signal
    # Emits custom signal with elemental symbol and boolean
    def emitElement(self, checked):
        symbol = self.sender().text()
        self.elementEmitted.emit(symbol, checked)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PeriodicTable()
    window.show()
    sys.exit(app.exec_())
