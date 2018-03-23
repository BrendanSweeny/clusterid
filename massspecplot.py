# TODO: Keep considering what happens to the relative abundance when two isotopes
# from two different clusters overlap
# When consolidating isotope masses (e.g. H2O 19amu), it may be necessary to include
# a tolerance for what it considers the same amu
# TODO: Fix table sorting when formula column (with QLabels as cells) is clicked
# TODO: Add mass and hide button to plot table
# TODO: Try removing miniscule abundances before plotting

import sys
import itertools
import operator
import functools
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

        # Table for molecules added to plot
        # Creates a column for molecular formula and 'Remove' button
        self.ui.selectedMoleculesTable.setColumnCount(2)
        self.ui.selectedMoleculesTable.setHorizontalHeaderLabels(['Molecule', ''])

        # Add chemical formula to plot by line edit
        self.ui.formulaLineEdit.returnPressed.connect(self.handleAddFromLineEdit)

        # Mass spectrum plot parameters
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
            if not self.isFloat(formulaList[index]) and formulaList[index].isalpha():
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
        outputList = []
        for entry in formulaList:
            if isinstance(entry, str):
                for element in self.elements:
                    if element['symbol'] == entry:
                        isotopes = [[isotope[0], isotope[1] / 100] for isotope in element['isotopes']]
                        outputList.append(isotopes)
            else:
                outputList.append(entry)
        return outputList

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
            rmBtn = QPushButton('Remove')
            rmBtn.clicked.connect(self.handleRemoveMolecule)
            self.ui.selectedMoleculesTable.setCellWidget(i, 0, label)
            self.ui.selectedMoleculesTable.setCellWidget(i, 1, rmBtn)
            #self.ui.selectedMoleculesTable.setItem(i, 0, QTableWidgetItem(self.selectedMolecules[i]))

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

    # Generates the np.arrays and pyqtgraph plotItems and
    # adds them to the Mass Spec Plot
    # Creats plot items for each isotope in the molecule
    # Each isotope is composed of a np.array and represted by a vertical line
    # np.array ex: self.ex = np.array([[6.015, 0], [6.015, 0.0759]])
    # np.array ex: self.exTwo = np.array([[7.016, 0], [7.016, 0.9241]])
    def constructAndPlotData(self, isotopeList, formulaStr, color):
        arrayList = [self.ui.graphicsView.plot(np.array([[isotope[0], 0], [isotope[0], isotope[1]]]),
            pen=pg.mkPen(color, width=3)) for isotope in isotopeList]
        self.plotItems[formulaStr] = arrayList

    # Normalizes the abundance of each isotope to the isotope with the largest
    # abundance
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

    # Consolidates the final isotope list by calling isotopeIndex to check
    # if an isotope already exists in the output
    # Adds abundances if isotope already exists, otherwise adds entry to output
    def consolidateIsotopes(self, isotopeList):
        outputList = []
        for isotope in isotopeList:
            index = self.isotopeIndex(isotope[0], outputList)
            if index != None:
                outputList[index][1] += isotope[1]
            else:
                outputList.append(isotope)
        return outputList

    # Convolutes a single list of isotopes from an element with a list of
    # isotopes representing a molecule
    def convoluteElement(self, totalList, elementList):
        # Ex. H2 --> [([1, 0.999885], [1, 0.999885]), ([1, 0.999885], [2, 0.000115]),
        # ([2, 0.000115], [1, 0.999885]), ([2, 0.000115], [2, 0.000115])]
        combinations = list(itertools.product(totalList, elementList))

        # Ex. H2 --> [2, 3, 3, 4]
        massList = [combo[0][0] + combo[1][0] for combo in combinations]

        # Ex. H2 --> [(2, 0.999770013225), (3, 0.000114986775),
        # (3, 0.000114986775), (4, 1.3225000000000001e-08)]
        abundanceList = [combo[0][1] * combo[1][1] for combo in combinations]

        # Ex. H2 --> [(2, 0.999770013225), (3, 0.000114986775),
        # (3, 0.000114986775), (4, 1.3225000000000001e-08)]
        resultTuples = list(zip(massList, abundanceList))

        # Ex. H2 --> [(2, 0.999770013225), (3, 0.000114986775),
        # (3, 0.000114986775), (4, 1.3225000000000001e-08)]
        resultList = [list(combo) for combo in resultTuples]
        return self.consolidateIsotopes(resultList)

    # Convolutes elements of a formulaList one by one adding each mass and abundance
    # to the previously returned values by way of the self.convoluteElement function
    def recursiveGenerateMasses(self, formulaList, isotopeList, count=0):
        # Terminating Case, no more elements to add
        if formulaList == []:
            return isotopeList

        # Convoluting elements up to 'count' or each element
        elif isinstance(formulaList[0], list) and count < formulaList[1]:
            #isotopeList.append(formulaList[0])
            isotopeList = self.convoluteElement(isotopeList, formulaList[0])
            count += 1
            #print(formulaList[0], isotopeList)
            return self.recursiveGenerateMasses(formulaList, isotopeList=isotopeList[:], count=count)

        # Convolute the last element, skip to next element
        elif isinstance(formulaList[0], list) and count == formulaList[1]:
            #print(formulaList[2:], isotopeList)
            count = 0
            return self.recursiveGenerateMasses(formulaList[2:], isotopeList=isotopeList[:], count=count)


    def generateMassSpectrum(self, consolidatedList, formulaStr, color):

        # Replace the element symbols with an object containing a list of
        # isotopes and the amount of the element in the molecular formula
        # Ex. ['H', 2, 'O', 1] --> [{'isotopes': [[1, 99.9885], [2, 0.0115]], 'num': 2}, {...}]
        #isotopesByElement = self.replaceSymWithIsotopes(consolidatedList)
        isotopesByElement = self.replaceSymWithIsotopes(consolidatedList)
        #print('isotopesByElement: ', isotopesByElement)

        finalIsotopes = self.recursiveGenerateMasses(isotopesByElement, isotopesByElement[0], count=1)
        #print(finalIsotopes)

        # Normalizes by setting most abundant mass to 1.0
        # Ex. H2O --> [[18, 1.0], [19, 0.0006109521023699666], [20, 0.002054993634531912]]
        #normalizedFinalIsotopes = self.normalizeIsotopes(consolidatedFinalIsotopes)
        normalizedFinalIsotopes = sorted(self.normalizeIsotopes(finalIsotopes))
        #print('normalizedFinalIsotopes: ', normalizedFinalIsotopes)

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
        #print(color)

        # Convert formula text to list of elements and their number
        formulaList = self.formulaToList(formula)
        print(formulaList)

        # Consolidate the list and sum repeated elements
        consolidatedList = self.consolidateFormulaList(formulaList)
        #print(consolidatedList)

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
