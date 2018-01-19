# TODO: Keep considering what happens to the relative abundance when two isotopes
# from two different clusters overlap
# When consolidating isotope masses (e.g. H2O 19amu), it may be necessary to include
# a tolerance for what it considers the same amu
# TODO: Fix table sorting when formula column (with QLabels as cells) is clicked
# TODO: Add mass  and hide button to plot table
# TODO: Crashes when weird formula ('##$Ca3') added via QLineEdit

import sys
import itertools
from massspecui import Ui_MassSpec
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QTableWidgetItem, QLabel, QMainWindow, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QPoint, pyqtSignal, pyqtSlot, Qt
from elementdata import ElementData
import pyqtgraph as pg
import numpy as np

class MassSpec(QWidget):
    def __init__(self):
        # Set configs before loading module
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        super().__init__()

        self.ui = Ui_MassSpec()
        self.ui.setupUi(self)

        self.elements = ElementData().isotopes

        self.selectedMolecules = []
        self.plotItems = {}
        # Color counter increments each time a new molecule is added to selectedMolecules
        # Avoids having two colors next to each other when one is removed
        self.colorCounter = 0
        self.uniqueColors = 9

        self.ui.selectedMoleculesTable.setColumnCount(2)
        self.ui.selectedMoleculesTable.setHorizontalHeaderLabels(['Molecule', ''])

        self.ui.formulaLineEdit.returnPressed.connect(self.handleAddFromLineEdit)

        self.plot = self.ui.graphicsView.plotItem

        self.plot.showGrid(False, True, 0.2)
        self.plot.showAxis('top', show=True)
        self.plot.showAxis('right', show=True)
        self.plot.setLabels(title='Simulated Mass Spectrum', bottom='m/z')
        self.ui.graphicsView.setYRange(0, 1)

        # Mouseover Plot Signal/Slot
        self.proxy = pg.SignalProxy(self.ui.graphicsView.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

    # Mouse movement event handler used to find the coordinates of the mouse on
    # on the Mass Spec plot
    # Used as the slot for pg.SignalProxy when moused over
    # Sets Qlabels for the x,y coordinates to their respective values
    def mouseMoved(self, e):
        pos = e[0]
        xVal = round(self.plot.vb.mapSceneToView(pos).x(), 2)
        yVal = round(self.plot.vb.mapSceneToView(pos).y(), 3)
        self.ui.qlxpos.setText(str(xVal))
        self.ui.qlypos.setText(str(yVal))

    # Recursive function that breaks up molecular formula to list of elements
    # and number of each element
    # Used in addByFormula
    # Returns formula list, ex. ['V', 2, 'Al', 2, 'O', 4]
    def formulaToList(self, formula, depth=0, resultList=[], workingEntry=''):
        if formula:
            # first iteration working entry is empty string
            if not workingEntry:
                workingEntry = formula[0]
            # Case: working entry is a character and next a character
            elif workingEntry.isalpha() and formula[0].isalpha():
                #print('alpha+alpha')
                if workingEntry[-1].isupper() and formula[0].islower():
                    #print('upper+lower')
                    workingEntry = workingEntry + formula[0]
                elif workingEntry[-1].isupper() and formula[0].isupper():
                    resultList.append(workingEntry)
                    resultList.append(1)
                    workingEntry = formula[0]
                elif workingEntry[-1].islower() and formula[0].isupper():
                    resultList.append(workingEntry)
                    resultList.append(1)
                    workingEntry = formula[0]
            # Case: working entry is a character and next is a number
            elif workingEntry.isalpha() and formula[0].isdigit():
                #print('alpha+num')
                resultList.append(workingEntry)
                workingEntry = formula[0]
            # Case: working entry is number and next is number
            elif workingEntry.isdigit() and formula[0].isdigit():
                #print('num+num')
                workingEntry = workingEntry + formula[0]
            # Case: working entry is number and next is a character
            elif workingEntry.isdigit() and formula[0].isalpha():
                #print('num+alpha')
                resultList.append(int(workingEntry))
                workingEntry = formula[0]
            #resultList.add(formula[0])
            return self.formulaToList(formula[1:], depth + 1, resultList[:], workingEntry)

        # Function terminates when there are no more chars in the formula str
        else:
            # Handles what's left in the workingEntry after formula str is empty
            if workingEntry.isalpha():
                resultList.append(workingEntry)
                resultList.append(1)
            elif workingEntry.isdigit():
                resultList.append(int(workingEntry))
            else:
                resultList.append(workingEntry)
            return resultList

    # Function that removes duplicate elements from a formula list
    # Used in addByFormula
    # Returns new list, ex. 'CCl4' or CClClClCl --> ['C', 1, 'Cl', 4]
    def consolidateFormulaList(self, formulaList):
        outputList = []
        for index in range(len(formulaList)):
            if not self.isFloat(formulaList[index]):
                if formulaList[index] not in outputList:
                    outputList.append(formulaList[index])
                    outputList.append(formulaList[index + 1])
                else:
                    outputIndex = outputList.index(formulaList[index])
                    outputList[outputIndex + 1] = outputList[outputIndex + 1] + formulaList[index + 1]
        return outputList

    # Takes a formula list and returns a list of objects
    # Each object contains the isotopes and number of each element
    # Used in generateMassSpectrum
    # Ex. ['H', 2, 'O', 1] --> [{'isotopes': [[1, 99.9885], [2, 0.0115]], 'num': 2}, {...}]
    def replaceSymWithIsotopes(self, formulaList):
        elements = []
        elemObj = {}
        for entry in formulaList:
            if not self.isFloat(entry):
                for element in self.elements:
                    if element['symbol'] == entry:
                        elemObj['isotopes'] = element['isotopes']

            else:
                elemObj['num'] = entry
                elements.append(elemObj)
                elemObj = {}

        return elements

    # Removes sub tags from formula string
    # Used in handleformulaEmitted slot, handleRemoveMolecule click handler
    # Returns a string of charaters and ints (e.g. 'V3O4')
    def stripSub(self, formula):
        splitFormula = formula.split('<sub>')
        intermediateFormula = ''.join(splitFormula)
        splitFormula = intermediateFormula.split('</sub>')
        finalFormula = ''.join(splitFormula)
        return finalFormula

    # Checks for '</sub>', '<sub>' in list
    # Used in formatFormula to avoid '<sub>', '1', '</sub>', '<sub>', '0', '</sub>'
    # Instead results in: '<sub>', '1', '0', '</sub>'
    # Returns a boolean (e.g. True if the entry is a </sub> and is follwed by <sub>)
    def subsub(self, inputList, index, x):
        #print(inputList, index, x)
        if index + 1 < len(inputList) and x == '</sub>' and inputList[index + 1] == '<sub>':
            return True
        elif x == '<sub>' and inputList[index - 1] == '</sub>':
            return True
        else:
            return False

    # Adds sub tags to appropriate place in formula
    def formatFormula(self, formula):

        splitFormula = list(formula)
        formattedSplitFormula = []

        for char in splitFormula:
            try:
                float(char)
            except ValueError:
                formattedSplitFormula.append(char)
            else:
                formattedSplitFormula.append('<sub>')
                formattedSplitFormula.append(char)
                formattedSplitFormula.append('</sub>')

        # Filter out '</sub>', '<sub>'
        formattedSplitFormula = [x for index, x in enumerate(formattedSplitFormula) if not self.subsub(formattedSplitFormula, index, x)]
        formattedFormula = ''.join(formattedSplitFormula)

        return formattedFormula

    # Checks if number can be typed to float
    def isFloat(self, value):
        try:
            float(value)
        except ValueError:
            return False
        else:
            return True

    # Adds new object to selectedMolecules state if not already in list
    # example state: [{'formula': 'H2O', 'color': 'b'}, {...}]
    def updateSelectedMoleculesList(self, formula, color):
        newEntry = {}
        newEntry['formula'] = formula
        newEntry['color'] = color
        inList = False

        for entry in self.selectedMolecules:
            if entry['formula'] == newEntry['formula']:
                inList = True

        if not inList:
            self.selectedMolecules.append(newEntry)

    # Removes molecule from table and plot
    def handleRemoveMolecule(self, tableWidget):
        # Finds and returns the cell corresponding to the QLabel of the row whose 'remove'
        # button was clicked
        clickedButton = self.sender()
        index = self.ui.selectedMoleculesTable.indexAt(clickedButton.pos())
        formulaCell = self.ui.selectedMoleculesTable.cellWidget(index.row(), 0)

        # Removes table row containing clicked item and formula from list
        self.ui.selectedMoleculesTable.removeRow(index.row())

        # Finds the index of the formula object in the selectedMolecules list
        for i in self.selectedMolecules:
            if i['formula'] == self.stripSub(formulaCell.text()):
                formulaObject = self.selectedMolecules.pop(self.selectedMolecules.index(i))

        # Clears all subplots corresponding to the molecule from the graphicsView
        for array in self.plotItems[formulaObject['formula']]:
            array.clear()

        # Removes the list of subplots and formula key from the plotItems list
        self.plotItems.pop(formulaObject['formula'])

    def updateSelectedMoleculesTable(self):
        self.ui.selectedMoleculesTable.setRowCount(len(self.selectedMolecules))
        for i in range(len(self.selectedMolecules)):
            formula = self.formatFormula(self.selectedMolecules[i]['formula'])
            label = QLabel(formula)
            label.setStyleSheet('QLabel { color: ' + self.selectedMolecules[i]['color'].name() + '; font-weight: bold; font-size: 16px }')
            #label.setStyleSheet('QLabel { color: ' + colorConversion[self.selectedMolecules[i]['color']] + '; font-weight: bold; font-size: 24px }')
            rmBtn = QPushButton('Remove')
            rmBtn.clicked.connect(self.handleRemoveMolecule)
            self.ui.selectedMoleculesTable.setCellWidget(i, 0, label)
            self.ui.selectedMoleculesTable.setCellWidget(i, 1, rmBtn)
            #self.ui.selectedMoleculesTable.setItem(i, 0, QTableWidgetItem(self.selectedMolecules[i]))

    # Finds all combinations (of isotopes) of a single element up to the number
    # dictated by the molecular formula, returns a list of these combinations
    def findIsotopeCombinations(self, isotopeList, num):
        # Creates generator with all combinations of isotopes up to num
        #comboGenerator = itertools.combinations_with_replacement(isotopeList, num)
        comboGenerator = itertools.product(isotopeList, repeat=num)

        # Accumulates amu and abundance for those combinations into a single amu
        # and abundance sublist
        # Returns the outputList
        outputList = []
        for combo in comboGenerator:
            comboTotalMass = 0
            comboAbundance = 1
            for isotope in combo:
                comboTotalMass += isotope[0]
                comboAbundance *= isotope[1] / 100
            if comboAbundance > 0.0001:
                outputList.append([comboTotalMass, comboAbundance])
        return outputList

    # Returns a list of lists with each sublist representing an element
    # Calls findIsotopeCombinations for each element in list and returns list of lists
    def findIsotopeAbundancesByElement(self, elementList):
        outputList = []
        for i in range(len(elementList)):
            combinationsList = self.findIsotopeCombinations(elementList[i]['isotopes'], elementList[i]['num'])
            outputList.append(combinationsList)
        return outputList

    # Uses the generated index sets to combine the total amu and abundances
    # for each element into the amu and abundances for each isotope of the final
    # input molecule
    # Only adds isotope if abundance is greater than 0.0001
    def findFinalIsotopes(self, elementList, indexSets):
        outputList = []
        for indexSet in indexSets:
            combination = [0, 1]
            for index in range(len(elementList)):
                combination[0] += elementList[index][indexSet[index]][0]
                combination[1] *= elementList[index][indexSet[index]][1]
            if combination[1] > 0.0001:
                outputList.append(combination)
        return outputList

    # Generates a list of sets that contain indeces representing all combinations
    # of each possible isotope and abundance
    # The sets will be used to combine the total amu of each element (e.g. H2, O2)
    # in a molecular formula
    def generateIndexSets(self, elementObjects, combination=[], depth=0, output=set()):
        if elementObjects != []:
            for i in range(0, len(elementObjects[0])):
                combination[depth] = i
                #print('i:', i, 'depth:', depth, 'combo:', combination, output)
                if elementObjects[1:] == []:
                    output.add(tuple(combination[:]))
                else:
                    self.generateIndexSets(elementObjects[1:], combination, depth + 1, output)
        return output

    # Checks if target value exists in a list of sublists, returns index of sublist
    # or False
    def isotopeIndex(self, target, checkList):
        for i in checkList:
            if target == i[0]:
                return checkList.index(i)
        return None

    # Consolidates the final isotope list by popping each item from inputList
    # and calling isotopeIndex to check if an isotope already exists in the output
    # Adds abundances if isotope already exists, otherwise adds entry to output
    def consolidateIsotopes(self, isotopeList):
        outputList = []
        for i in range(len(isotopeList)):
            isotope = isotopeList.pop()
            index = self.isotopeIndex(isotope[0], outputList)
            if index != None:
                outputList[index][1] += isotope[1]
            else:
                outputList.append(isotope)
        return outputList

    def constructAndPlotData(self, isotopeList, formulaStr, color):
        arrayList = []

        #self.test = np.array([[6.015, 0], [6.015, 0.0759]])
        #self.testTwo = np.array([[7.016, 0], [7.016, 0.9241]])

        for isotope in isotopeList:
            array = np.array([[isotope[0], 0], [isotope[0], isotope[1]]])
            plotItem = self.ui.graphicsView.plot(array, pen=pg.mkPen(color, width=3))
            arrayList.append(plotItem)

        self.plotItems[formulaStr] = arrayList

    def normalizeIsotopes(self, isotopeList):
        maximum = 0
        for isotope in isotopeList:
            if isotope[1] > maximum:
                maximum = isotope[1]

        for isotope in isotopeList:
            isotope[1] = isotope[1] / maximum

        return isotopeList

    # Checks if element symbol is in self.elements list of objects
    def validElement(self, entry):
        for element in self.elements:
            if entry == element['symbol']:
                return True
        return False

    def validateFormulaList(self, formulaList):
        isValid = True
        if not formulaList:
            isValid = False

        for entry in formulaList:
            # Skip if it's a number
            if self.isFloat(entry):
                continue
            # Check if it's an element
            else:
                for element in self.elements:
                    if not self.validElement(entry):
                        isValid = False
        return isValid

    def generateMassSpectrum(self, consolidatedList, formulaStr, color):
        # Replace the element symbols with an object containing a list of
        # isotopes and the amount of the element in the molecular formula
        # Ex. ['H', 2, 'O', 1] --> [{'isotopes': [[1, 99.9885], [2, 0.0115]], 'num': 2}, {...}]
        isotopesByElement = self.replaceSymWithIsotopes(consolidatedList)

        # Generates a list of lists
        # Each list represents a single element and contains sublists.
        # Each sublist represents the total amu (and abundance)
        # for a combination of isotopes up to the number defined in the molecular formula
        # The lists are organized by element
        # ex. H2O: [[[2, 0.999770013225], [3, 0.000114986775]], [[16, 0.9975700000000001], [17, 0.00037999999999999997], [18, 0.0020499999999999997]]]
        relativeAbundancesByElement = self.findIsotopeAbundancesByElement(isotopesByElement)
        #print(relativeAbundancesByElement)

        # Generates a list of sets of indeces (one index for each element)
        # The index sets represent all possible combinations of element totals
        # Ex. H2O --> [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        indexSets = sorted(self.generateIndexSets(relativeAbundancesByElement, [0 for i in relativeAbundancesByElement], output=set()))

        # Combines the total amu and total abundances by element using the sets of indeces to find
        # all possible isotopic combinations of the final amu and abundances of the
        # input molecular formula
        # Ex. H2O --> [[18, 0.9973405720928633], [19, 0.00037991260502549996], [20, 0.0020495285271112497], [19, 0.00011470735713675001], [19, 0.00011470735713675001]]
        finalIsotopes = self.findFinalIsotopes(relativeAbundancesByElement, indexSets)

        # Sums and removes duplicate amu values
        # Returns a list of mass values and respective abundances for the molecule
        # Changing the amu 'tolerance' here could allow for precise isotope values instead
        # of whole amu values
        # Ex. H2O --> [[18, 0.9973405720928633], [19, 0.000609327319299], [20, 0.0020495285271112497]]
        consolidatedFinalIsotopes = sorted(self.consolidateIsotopes(finalIsotopes))

        # Normalizes by setting most abundant mass to 1.0
        # Ex. H2O --> [[18, 1.0], [19, 0.0006109521023699666], [20, 0.002054993634531912]]
        normalizedFinalIsotopes = self.normalizeIsotopes(consolidatedFinalIsotopes)

        # Constructs the plotItems used to render each simulated mass spectrum
        self.constructAndPlotData(normalizedFinalIsotopes, formulaStr, color)

    def generatePlotColor(self):
        # Determine color of plot
        colorIndex = self.colorCounter % self.uniqueColors
        self.colorCounter += 1

        return pg.intColor(colorIndex, hues=self.uniqueColors, maxValue=200, alpha=150)

    # Calls the appropriate functions to define plot/label color, update molecules list,
    # update molecules table, and generate the mass spec plot
    def addByFormula(self, formula):
        # Determine color of plot
        color = self.generatePlotColor()

        # Convert formula text to list of elements and their number
        formulaList = self.formulaToList(formula)

        # Consolidate the list and sum repeated elements
        consolidatedList = self.consolidateFormulaList(formulaList)

        # Checks if formula to be added is already in selectedMolecules
        inList = False
        for entry in self.selectedMolecules:
            if entry['formula'] == formula:
                inList = True

        # Validates the formula to be added (Checks if all symbols are in self.elements)
        if not inList and self.validateFormulaList(consolidatedList):
            self.updateSelectedMoleculesList(formula, color)
            self.updateSelectedMoleculesTable()
            self.generateMassSpectrum(consolidatedList, formula, color)

    # Event handler for manually entered formula string
    def handleAddFromLineEdit(self):
        # Capture Line Edit Input
        formula = self.sender().text()
        self.addByFormula(formula)

    # Event handler for formula string emitted by another widget (with <sub> tags)
    def handleformulaEmitted(self, formula):
        #print('formula emitted: ', formula)
        formula = self.stripSub(formula)
        self.addByFormula(formula)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MassSpec()
    window.show()
    sys.exit(app.exec_())
