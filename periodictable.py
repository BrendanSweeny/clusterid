import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QCheckBox
from PyQt5.QtCore import pyqtSignal
from periodictableui import Ui_PeriodicTable
from elements import Element
from ligand import Ligand
from elementdata import ElementData
import utils

class PeriodicTable(QWidget):

    # Custom signal
    elementEmitted = pyqtSignal(object, bool)

    def __init__(self):
        super().__init__()

        self.ui = Ui_PeriodicTable()
        self.ui.setupUi(self)

        # Custom ligands
        self.ligand_1 = None
        self.ligand_2 = None
        self.ligand_3 = None
        # Element Objects
        self.elements = ElementData().elements
        self.periodicTable = {}

        for element in self.elements:
            self.periodicTable[element['symbol']] = Element(element['mass'], element['symbol'], element['name'], element['number'])

        # Iterates through all of the UI object names and connects slots/signals
        # This widget is highly dependent on the naming convention of the buttons
        # and line edits, changing the names will break the function assignments
        for name in dir(self.ui):
            # Element buttons:
            if 'ebtn' in name:
                btn = getattr(self.ui, name)
                btn.clicked[bool].connect(self.emitElement)
            # Custom ligand check boxes:
            elif 'ligCheckBox' in name:
                cb = getattr(self.ui, name)
                cb.clicked[bool].connect(self.emitLigand)
            elif 'ligClear' in name:
                btn = getattr(self.ui, name)
                btn.clicked.connect(self.clearCustomLigand)
            elif 'ligFormula' in name:
                le = getattr(self.ui, name)
                le.returnPressed.connect(self.handleLigandReturnPressed)

    # Slot for element button clicked signal
    # Emits custom signal with elemental symbol and boolean
    def emitElement(self, checked):
        symbol = self.sender().text()
        elementObject = self.periodicTable[symbol]
        self.elementEmitted.emit(elementObject, checked)

    def retrieveLigandWidgets(self):
        senderName = self.sender().objectName()
        rowNumber = senderName[-1]

        # Find the widgets and stored ligand object corresponding to the row:
        cb = getattr(self.ui, 'ligCheckBox' + rowNumber)
        formulaLineEdit = getattr(self.ui, 'ligFormula' + rowNumber)
        massLineEdit = getattr(self.ui, 'ligMass' + rowNumber)
        storedLigand = getattr(self, 'ligand_' + rowNumber)
        return cb, formulaLineEdit, massLineEdit, rowNumber, storedLigand

    def handleLigandReturnPressed(self):
        # Find widgets corresponding to ligand row:
        (cb, formulaLineEdit,
            massLineEdit, rowNumber, storedLigand) = self.retrieveLigandWidgets()

        # Functionality that updates fields and ligandObject when the formulaLineEdit
        # is changed to a new value (i.e. is not cleared first using the button)
        if storedLigand:
            if cb.isChecked():
                # Removes ligand already in clusterid.py list:
                self.emitLigand(False)
            # Removes stored ligandObject:
            setattr(self, 'ligand_' + rowNumber, None)
            # Emits new ligand object
            self.emitLigand(True)
        # Functionality for when the field has been cleared or is empty
        else:
            self.emitLigand(True)
        cb.setChecked(True)

    # Clears the particular custom ligand row
    def clearCustomLigand(self):
        # Find widgets corresponding to ligand row:
        (cb, formulaLineEdit,
            massLineEdit, rowNumber, storedLigand) = self.retrieveLigandWidgets()
        if cb.isChecked():
            cb.setChecked(False)
            self.emitLigand(False)
            setattr(self, 'ligand_' + rowNumber, None)
            formulaLineEdit.setText('')
            massLineEdit.setText('')
        else:
            setattr(self, 'ligand_' + rowNumber, None)
            formulaLineEdit.setText('')
            massLineEdit.setText('')


    # Uses values from the custom ligand section to generate an object to be
    # emitted
    def generateLigandObject(self, formulaText, rowNumber):
        # Convert to formula list:
        formulaList = utils.formulaToList(formulaText)
        # Validate and calculate mass of ligand:
        totalMass = 0
        if utils.validateFormulaList(self.elements, formulaList):
            totalMass = utils.recursiveFindMass(formulaList, self.elements)
        # Assign mass to mass lineEdit:
        massLineEdit = getattr(self.ui, 'ligMass' + rowNumber)
        massLineEdit.setText(str(round(totalMass, 2)))
        # Create ligand object:
        ligandObject = Ligand(totalMass, '(' + formulaText + ')')
        return ligandObject

    # Emits custom ligand object to custerid MainWindow and tofviewwidget
    def emitLigand(self, checked):
        # Find widgets corresponding to ligand row:
        (cb, formulaLineEdit,
            massLineEdit, rowNumber, storedLigand) = self.retrieveLigandWidgets()

        formulaText = formulaLineEdit.text()
        if formulaText != '':
            # Re-emit the same object if it exists (otherwise it won't be toggled
            # on and off properly):
            if storedLigand:
                self.elementEmitted.emit(storedLigand, checked)
            else:
                ligandObject = self.generateLigandObject(formulaText, rowNumber)
                # Store ligand object
                setattr(self, 'ligand_' + rowNumber, ligandObject)
                # Emit object:
                self.elementEmitted.emit(ligandObject, checked)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PeriodicTable()
    window.show()
    sys.exit(app.exec_())
