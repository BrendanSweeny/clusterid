# TODO: Add a 'custom field' to periodic table to define a molecule or ligand
# and specify a mass for the ligand to be added to selected masses list

import sys
import re
import images_qr
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QTableWidgetItem, QLabel, QMainWindow, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QPoint, pyqtSignal, pyqtSlot, Qt
from clusteridv2bui import Ui_MainWindow
from periodictableui import Ui_PeriodicTable
from massspecui import Ui_MassSpec
from massspecplot import MassSpec
import math
from operator import attrgetter, itemgetter
from elements import Element
from elementdata import ElementData
import pyqtgraph as pg
import numpy as np

#QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class MainWindow(QMainWindow):

    formulaEmitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.elements = ElementData().elements

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("ClusterID v2b")
        self.setWindowIcon(QIcon(':cluster.ico'))

        self.periodicTable = {}
        self.selectedElements = []

        # Assigned following recursiveFindCombinations call:
        # [{'part': (4, 9), 'pctDif': 0.06, 'preciseMass': 347.8}, {...}]
        self.matchedClusters = []

        self.targetVal = 217
        self.clusterSeriesDicts = []
        self.formattedMatchOutput = ''
        self.formattedSeriesOutput = ''
        self.absoluteTolerance = 1
        self.maxClusterAtoms = 10

        for element in self.elements:
            self.periodicTable[element['symbol']] = Element(element['mass'], element['symbol'], element['name'], element['number'])

        self.periodicTableWidget = PeriodicTable()
        self.massSpecWidget = MassSpec()
        self.ui.tabWidget.insertTab(0, self.periodicTableWidget, 'Periodic Table')
        self.ui.tabWidget.insertTab(1, self.massSpecWidget, 'Mass Spec Plot')

        # Connects symbol emitted from periodicTableWidget to slot
        self.periodicTableWidget.elementEmitted.connect(self.handleElementClicked)

        self.formulaEmitted.connect(self.massSpecWidget.handleformulaEmitted)

        # Button that initiates the matching algorithm
        # Type flow pathway:
        # float (target) and list of objects (elements) --> list of objects (matches)
        # --> QTableWidget: QLabel (formula str), float (preciseMass), float (pctDif), QPushButton
        self.ui.btnFindMatches.clicked.connect(self.handleFindMatches)
        self.ui.btnFindClusterSeries.clicked.connect(self.handleFindClusterSeries)

        # Line edit that sets the target mass
        self.ui.targetLineEdit.textChanged[str].connect(self.updateTarget)
        self.ui.targetLineEdit.returnPressed.connect(self.handleFindMatches)

        # Filter line edit for the cluster series
        #self.ui.filterClusterSeries.textChanged.connect(lambda: self.handleFilter(self.ui.seriesOutput, False))
        self.ui.filterClusterSeries.returnPressed.connect(lambda: self.handleFilter(self.clusterSeriesDicts, self.ui.seriesOutput, False))

        # Allows user to set the max single atom number to generate cluster
        # series for
        self.ui.maxAtomsLineEdit.setText(str(self.maxClusterAtoms))
        self.ui.maxAtomsLineEdit.textChanged[str].connect(self.updateMaxAtoms)

        # Allows user to set the absolute tolerance for returned matches
        # (how many amu from target)
        self.ui.toleranceLineEdit.setText(str(self.absoluteTolerance))
        self.ui.toleranceLineEdit.textChanged[str].connect(self.updateTolerance)

        self.ui.matchOutput.setColumnCount(4)
        self.ui.matchOutput.setHorizontalHeaderLabels(['Formula', 'Mass', '% Diff.', 'Plot'])
        self.ui.matchOutput.clicked.connect(self.handleCellClicked)

        self.ui.seriesOutput.setColumnCount(3)
        self.ui.seriesOutput.setHorizontalHeaderLabels(['Formula', 'Mass', 'Plot'])
        self.ui.seriesOutput.clicked.connect(self.handleCellClicked)

        #self.ui.filterMatched.textChanged.connect(self.newHandleFilter)
        self.ui.filterMatched.returnPressed.connect(lambda: self.handleFilter(self.matchedClusters, self.ui.matchOutput, True))

        ## TEST AREA ##
        #print(self.formatFormula('V4O9'))
        #print(self.formatFormula('V4O93H123'))

    # Slot for emitted element symbol and checked boolean from periodicTableWidget
    # Updates list of selected element objects
    def handleElementClicked(self, symbol, checked):
        elementObject = self.periodicTable[symbol]
        mass = self.periodicTable[symbol].mass
        symbol = self.periodicTable[symbol].symbol
        if checked and elementObject not in self.selectedElements:
            self.selectedElements.append(elementObject)
        elif not checked:
            self.selectedElements.remove(elementObject)

    # Updates target mass when line edit value changes
    def updateTarget(self, value):
        try:
            float(value)
        except ValueError:
            return
        else:
            self.targetVal = float(value)


    # Finds the precise mass of the match, used to calculate % difference
    # Takes a set or list as combination and list of selected elements
    # Returns a float
    def findPreciseMass(self, combination, includeList):
      total = 0
      for i in range(len(combination)):
        total = total + combination[i] * includeList[i]
      return total

    # Takes two floats/integers and returns a float/integer
    def findPercentDifference(self, valOne, valTwo):
        return abs((valOne - valTwo)/((valOne + valTwo)/2) * 100)

    # Used by both cluster series and matches to setText of appropriate text box
    def displayFormattedOutput(self, uiObject, outputString):
        uiObject.setHtml(outputString)

    # Updates max atoms per element in cluster series when line edit value changes
    def updateMaxAtoms(self, value):
        if value.isdigit():
            self.maxClusterAtoms = int(value)

    # Updates absolute tolerance when line edit value changes
    def updateTolerance(self, value):
        try:
            float(value)
        except ValueError:
            return
        else:
            self.absoluteTolerance = float(value)

    # Finds all possible ways to partition the target value
    # with the values contained in a list.
    # Recursively finds each combination by incrementing last value in list by +1 until no remainder,
    # then increments the second to last by +1, etc.

    # Returns a set of sets (each being a suitable combination)
    def recursiveFindCombinations(self, target, numList, depth=0, combination=[], answer=set()):
      if numList != []:
        maxIons = int(target // numList[0]) + 1

        # Adds an additional multiple of the current value for each iteration
        for i in range(0, maxIons + 1):

          # Most target values will be integers. This allows for some tolerance between precise atomic
          # masses and imprecise target value
          # if math.isclose(target, numList[0] * i, abs_tol=1):
          if abs(target - numList[0] * i) <= self.absoluteTolerance:
            remainder = 0
          else:
            remainder = target - (numList[0] * i)
          combination[depth] = i

          # Terminating case: when the target is matched, combo list is copied
          if numList[1:] == [] and remainder == 0:
            answer.add(tuple(combination[:]))
          #print('n:', numList[0], 'maxIons:', maxIons, 'i:', i, 'total:', i * numList[0], 'remainder:', remainder, 'numList:', numList[1:], 'combo:', combination, 'answer:', answer)

          # Recursion: calls the function for the next value in numList
          self.recursiveFindCombinations(remainder, numList[1:], depth + 1, combination, answer=answer)
      return answer

    # Checks for '</sub>', '<sub>' in list
    def subsub(self, inputList, index, x):
        #print(inputList, index, x)
        if index + 1 < len(inputList) and x == '</sub>' and inputList[index + 1] == '<sub>':
            return True
        elif x == '<sub>' and inputList[index - 1] == '</sub>':
            return True
        else:
            return False

    # Adds subscripts to formula string for display in output tables
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

    # Function that populates the table with rows to be returned for the find matches functionality
    # elementObjects: a list of objects repesenting elements in the periodic table
    # matchList: a set of sets (each set is a suitable combination)
    def showMatches(self, matchList, tableWidget, pctDif):
        # Sorting interferes with insertion order, is enabled after insertion:
        tableWidget.setSortingEnabled(False)
        tableWidget.setRowCount(len(matchList))
        columnCount = tableWidget.columnCount()

        for i in range(len(matchList)):
            if matchList[i]['formula']:
                matchString = self.formatFormula(matchList[i]['formula'])
                tableWidget.setCellWidget(i, 0, QLabel(matchString))
                tableWidget.setItem(i, 1, QTableWidgetItem(str(round(matchList[i]['preciseMass'], 5))))
                if pctDif:
                    tableWidget.setItem(i, 2, QTableWidgetItem(str(round(matchList[i]['pctDif'], 5)) + '%'))
                    self.addBtn = QPushButton('Add')
                    self.addBtn.clicked.connect(lambda: self.handleCellButton(tableWidget))
                    tableWidget.setCellWidget(i, 3, self.addBtn)
                else:
                    self.addBtn = QPushButton('Add')
                    self.addBtn.clicked.connect(lambda: self.handleCellButton(tableWidget))
                    tableWidget.setCellWidget(i, 2, self.addBtn)

        # Sort re-enabled only once population is finished
        # Otherwise, some cells become empty
        tableWidget.setSortingEnabled(True)

    # Click handler for Plot 'Add' buttons in find matches output table
    def handleCellButton(self, tableWidget):
        clickedButton = self.sender()
        #print(clickedButton.parent())
        index = tableWidget.indexAt(clickedButton.pos())
        formulaCell = tableWidget.cellWidget(index.row(), 0)
        # Switches to Mass Spec Tab
        self.ui.tabWidget.setCurrentIndex(1)
        self.formulaEmitted.emit(formulaCell.text())

    # Click handler for non-custom widget table cells
    def handleCellClicked(self):
        row = self.ui.matchOutput.selectedIndexes()

    # Finds total number of unique elements in a match, used to sort returned matches
    def findNumberOfElements(self, combination):
        totalUniqueElements = 0
        for i in combination:
            if i:
                totalUniqueElements += 1
        return totalUniqueElements

    def handleFindMatches(self):
        # Find elemental masses for element list populated by pushbuttons
        sortedElementObjects = sorted(self.selectedElements, key=attrgetter('mass'), reverse=True)
        #for element in self.selectedElements:
            #selectedMasses.append(self.periodicTable[element].mass)

        # Sort masses highest to lowest
        #sortedMasses = sorted(selectedMasses, reverse=True)
        # Create template of 0s for 'combinations' list used in recursive function
        sortedMasses = [element.mass for element in sortedElementObjects]
        combinationTemplate = [0 for i in sortedMasses]

        # Call to recursive function, needs answer=set() to avoid
        # unwanted mutation
        allanswers = self.recursiveFindCombinations(self.targetVal, sortedMasses, combination=combinationTemplate, answer=set())

        # Sort answers by total atoms
        sortedallanswers = sorted(allanswers, key=sum)
        #print(sortedallanswers)

        # Create list of dicts and populate with first 20 answers (by lowest
        # total atoms), pct dif from target, and precise mass
        answerDicts = []
        for answer in sortedallanswers[:]:
            preciseMass = self.findPreciseMass(answer, sortedMasses)
            pctDif = self.findPercentDifference(preciseMass, self.targetVal)
            answerDict = {}
            formula = ''
            for index in range(len(answer)):
                if answer[index] > 0:
                    formula = formula + sortedElementObjects[index].symbol + str(answer[index])
            answerDict['formula'] = formula
            answerDict['part'] = answer
            answerDict['pctDif'] = pctDif
            answerDict['preciseMass'] = preciseMass
            answerDict['uniqueElements'] = self.findNumberOfElements(answer)
            answerDict['atomSum'] = sum(answer)
            answerDicts.append(answerDict)
        # Sort answer dict by percent difference from target
        #sortedPctDiftAnswers = sorted(answerDicts, key=itemgetter('pctDif'))

        # Sort by number of unique elements, then total number of atoms
        sortedUniqueElementsAndSum = sorted(answerDicts, key=itemgetter('atomSum', 'uniqueElements'))

        # Assigns list of objects:
        # [{'part': (4, 9), 'pctDif': 0.06, 'preciseMass': 347.8}, {...}]
        # to attribute
        self.matchedClusters = sortedUniqueElementsAndSum

        if self.ui.filterMatched.text():
            self.handleFilter(self.matchedClusters, self.ui.matchOutput, True, filterStr=self.ui.filterMatched.text())
        else:
            self.showMatches(self.matchedClusters, self.ui.matchOutput, True)

    # Recursive function used to find all combinations of included elements
    # up to a certain value, returns set of tuples
    def findClusterSeries(self, elementObjects, maxSize, combination=[], depth=0, output=set()):
        if elementObjects != []:
            for i in range(0, maxSize + 1):
                combination[depth] = i
                #print('i:', i, 'depth:', depth, 'combo:', combination, output)
                if elementObjects[1:] == []:
                    output.add(tuple(combination[:]))
                else:
                    self.findClusterSeries(elementObjects[1:], maxSize, combination, depth + 1, output)
        return output

    # Function that handles string formatting of cluster series and assignment
    # of QTextEdit value to formatted string
    def showCombinations(self, elementObjects, combinationDicts):
        outputString = ''
        if combinationDicts == []:
            outputString = 'Select a set of Elements.'
        else:
            for combinationDict in combinationDicts:
                formulaString = ''
                for i in range(len(combinationDict['combination'])):
                    if combinationDict['combination'][i] != 0:
                        formulaString = formulaString + elementObjects[i].symbol + '<sub>' + str(combinationDict['combination'][i]) + '</sub>'
                outputString = outputString + formulaString + ', ' + str(combinationDict['mass']) + '<br/>'
        #print(outputString)
        self.formattedSeriesOutput = outputString
        #print(self.formattedSeriesOutput)
        self.displayFormattedOutput(self.ui.seriesOutput, outputString)

    def handleFindClusterSeries(self):
        sortedElementObjects = sorted(self.selectedElements, key=attrgetter('mass'), reverse=True)
        #print(sortedElementObjects)
        # Needs output=set() to avoid unwanted mutation
        combinationsList = self.findClusterSeries(sortedElementObjects, self.maxClusterAtoms, [0 for i in sortedElementObjects], output=set())
        #print(combinationsList)
        sortedCombinationsList = sorted(combinationsList)

        combinationDicts = []
        for combination in sortedCombinationsList:
            totalMass = 0
            #print(combination)
            formula = ''
            for i in range(len(combination)):
                totalMass = totalMass + combination[i] * sortedElementObjects[i].mass
                if combination[i] > 0:
                    formula = formula + sortedElementObjects[i].symbol + str(combination[i])
            combinationDict = {'formula': formula, 'combination': combination, 'preciseMass': round(totalMass, 5)}
            # Does not append if no formula or mass (e.g. combo (0, 0))
            if formula or totalMass:
                combinationDicts.append(combinationDict)

        self.clusterSeriesDicts = combinationDicts
        #self.showCombinations(sortedElementObjects, self.clusterSeriesDicts)

        if self.ui.filterClusterSeries.text():
            self.handleFilter(self.clusterSeriesDicts, self.ui.seriesOutput, False, filterStr=self.ui.filterClusterSeries.text())
        else:
            self.showMatches(combinationDicts, self.ui.seriesOutput, False)

    # Function called by checking 'sort by mass' QCheckBox
    # Checks for stored clusterseriesdicts and value of box, sorts, and reshows
    # combinations
    def toggleSortByMass(self, bool):
        if bool and self.clusterSeriesDicts:
            sortedClusterSeriesMass = sorted(self.clusterSeriesDicts, key=itemgetter('mass'))
            self.showCombinations(self.lastRunClusterElements, sortedClusterSeriesMass)
        elif not bool and self.clusterSeriesDicts:
            sortedClusterSeriesAtoms = sorted(self.clusterSeriesDicts, key=itemgetter('combination'))
            self.showCombinations(self.lastRunClusterElements, sortedClusterSeriesAtoms)

    # Allows filtering of formula or number with filter strings
    # separataed by commas
    def handleFilter(self, combinations, tableWidget, pctDif, filterStr=[]):
        if not filterStr:
            filterStr = self.sender().text()
        splitFilterStr = filterStr.split(',')
        filteredEntries = []

        for entry in combinations:
            keep = True
            for filterStr in splitFilterStr:
                strippedFilter = filterStr.strip()
                if strippedFilter in entry['formula']:
                    continue
                else:
                    keep = False
            if keep == True:
                filteredEntries.append(entry)
        self.showMatches(filteredEntries, tableWidget, pctDif)

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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
