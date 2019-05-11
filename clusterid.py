# TODO: Add a 'custom field' to periodic table to define a molecule or ligand
# and specify a mass for the ligand to be added to selected masses list
# TODO: remove target val of 217 and provide a check for targetVal somewhere

import sys
import images_qr
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QTableWidgetItem, QLabel, QMainWindow, QLineEdit
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QPoint, pyqtSignal, pyqtSlot, Qt
from clusteridui import Ui_MainWindow
from periodictableui import Ui_PeriodicTable
from massspecui import Ui_MassSpec
from massspecplot import MassSpec
from periodictable import PeriodicTable
from tofviewwidget import TofView
import math
from operator import attrgetter, itemgetter
from elements import Element
from ligand import Ligand
from elementdata import ElementData
import utils
import findMatch
import os
import re
'''
import ctypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
'''

app = QApplication(sys.argv)

#QApplication.setAttribute(Qt.AA_Use96Dpi, True)
# os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '0'

# Redefined 'less than' function for QTableWidgetItem that allows data stored
# as integer (rather than string) to be used when sorting by column
class NumericTableItem(QTableWidgetItem):
    def __lt__(self, other):
        return (self.data(Qt.UserRole) < other.data(Qt.UserRole))

class MainWindow(QMainWindow):

    formulaEmitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.elements = ElementData().elements
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("ClusterID")
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
        self.tofView = TofView()
        self.ui.tabWidget.insertTab(0, self.periodicTableWidget, 'Periodic Table')
        self.ui.tabWidget.insertTab(1, self.massSpecWidget, 'Mass Spec Plot')
        self.ui.tabWidget.insertTab(2, self.tofView, 'TOF View')

        # Connects symbol emitted from periodicTableWidget to slot
        self.periodicTableWidget.elementEmitted.connect(self.handleElementClicked)

        self.periodicTableWidget.elementEmitted.connect(self.tofView.handleElementClicked)

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
        self.ui.filterClusterSeries.returnPressed.connect(lambda: self.handleFilter(self.clusterSeriesDicts, self.ui.seriesOutput, False, self.ui.filterClusterSeries.text()))
        self.ui.filterClusterSeries.setToolTip('Test Tooltip')

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
        self.ui.filterMatched.returnPressed.connect(lambda: self.handleFilter(self.matchedClusters, self.ui.matchOutput, True, self.ui.filterMatched.text()))

        self.ui.formulaLineEdit.returnPressed.connect(self.handleFindFormulaMass)

        self.ui.clearClusterFilterBtn.clicked.connect(lambda: self.handleClearFilter(self.clusterSeriesDicts, self.ui.seriesOutput, False, self.ui.filterClusterSeries))
        self.ui.clearMatchFilterBtn.clicked.connect(lambda: self.handleClearFilter(self.matchedClusters, self.ui.matchOutput, True, self.ui.filterMatched))

        ## TEST AREA ##

    def handleClearFilter(self, combinations, tableWidget, pctDif, filterLineEdit, filterStr=''):
        filterLineEdit.setText('')
        self.handleFilter(combinations, tableWidget, pctDif, filterStr)


    # Slot for emitted element symbol and checked boolean from periodicTableWidget
    # Updates list of selected element objects
    def handleElementClicked(self, elementObject, checked):
        mass = elementObject.mass
        symbol = elementObject.symbol
        formulaList = utils.formulaToList(symbol)
        if not utils.validateFormulaList(self.elements, formulaList):
            self.statusBar().showMessage('Error: Invalid Formula Entered', 5000)
        elif checked and elementObject not in self.selectedElements:
            self.selectedElements.append(elementObject)
        elif not checked:
            self.selectedElements.remove(elementObject)

    def handleLigandClicked(self, ligandObject, checked):
        mass = ligandObject.mass
        formula = ligandObject.symbol
        if checked and ligandObject not in self.selectedElements:
            self.selectedElements.append(ligandObject)
        elif not checked:
            self.selectedElements.remove(ligandObject)

    # Updates target mass when line edit value changes
    def updateTarget(self, value):
        try:
            float(value)
        except ValueError:
            return
        else:
            self.targetVal = float(value)

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

    def handleFindFormulaMass(self):
        formulaList = utils.formulaToList(self.ui.formulaLineEdit.text())
        if utils.validateFormulaList(self.elements, formulaList):
            totalMass = utils.recursiveFindMass(formulaList, self.elements)
            self.ui.formulaMassLineEdit.setText(str(round(totalMass, 2)))
        else:
            self.ui.formulaMassLineEdit.setText('')
            self.statusBar().showMessage('Error: Invalid Formula Entered', 5000)

    # Function that populates the table with rows to be returned for the find matches functionality
    # elementObjects: a list of objects repesenting elements in the periodic table
    # matchList: a set of sets (each set is a suitable combination)
    def showMatches(self, matchList, tableWidget, pctDif):
        # Sorting interferes with insertion order, is enabled after insertion:
        tableWidget.setSortingEnabled(False)
        tableWidget.setRowCount(len(matchList))

        for i in range(len(matchList)):
            if matchList[i]['formula']:
                # Adds <sub> tags to the formula string
                matchString = utils.formatFormula(matchList[i]['formula'])
                tableWidget.setCellWidget(i, 0, QLabel(matchString))
                # Uses the modified QTableWidgetItem with updated sorting method
                preciseMassTableItem = NumericTableItem(str(round(matchList[i]['preciseMass'], 5)))
                # Sets data to the integer value of precise mass for sorting reasons
                preciseMassTableItem.setData(Qt.UserRole, matchList[i]['preciseMass'])
                tableWidget.setItem(i, 1, preciseMassTableItem)
                if pctDif:
                    pctDifTableItem = NumericTableItem(str(round(matchList[i]['pctDif'], 5)) + '%')
                    pctDifTableItem.setData(Qt.UserRole, matchList[i]['pctDif'])
                    tableWidget.setItem(i, 2, pctDifTableItem)
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

    def handleFindMatches(self):
        # Find elemental masses for element list populated by pushbuttons
        # Sort masses highest to lowest
        sortedElementObjects = sorted(self.selectedElements, key=attrgetter('mass'), reverse=True)
        # Sorts by object type (ligands at the end):
        sortedElementObjects.sort(key= lambda x: type(x) is Ligand)

        # Create template of 0s for 'combinations' list used in recursive function
        sortedMasses = [element.mass for element in sortedElementObjects]
        combinationTemplate = [0 for i in sortedMasses]

        # Call to recursive function, needs answer=set() to avoid
        # unwanted mutation
        allanswers = findMatch.recursiveFindCombinations(self.targetVal, sortedMasses, self.absoluteTolerance, combination=combinationTemplate, answer=set())

        # Sort answers by total atoms
        sortedallanswers = sorted(allanswers, key=sum)

        # Create list of dicts and populate with answers (by lowest
        # total atoms), pct dif from target, and precise mass
        answerDicts = []
        for answer in sortedallanswers[:]:
            preciseMass = findMatch.findPreciseMassFromCombination(answer, sortedMasses)
            pctDif = utils.findPercentDifference(preciseMass, self.targetVal)
            answerDict = {}
            formula = ''
            for index in range(len(answer)):
                if answer[index] > 0:
                    formula = formula + sortedElementObjects[index].symbol + str(answer[index])
            answerDict['formula'] = formula
            answerDict['part'] = answer
            answerDict['pctDif'] = pctDif
            answerDict['preciseMass'] = preciseMass
            answerDict['uniqueElements'] = findMatch.findNumberOfElements(answer)
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
            #print(self.matchedClusters)
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

        self.ui.seriesOutput.setSortingEnabled(False)

        if self.ui.filterClusterSeries.text():
            self.handleFilter(self.clusterSeriesDicts, self.ui.seriesOutput, False, filterStr=self.ui.filterClusterSeries.text())
        else:
            #print(combinationDicts)
            self.showMatches(combinationDicts, self.ui.seriesOutput, False)

        self.ui.seriesOutput.setSortingEnabled(True)

    # Allows filtering of formula or number with filter strings
    # separataed by commas
    def handleFilter(self, combinations, tableWidget, pctDif, filterStr=''):
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

if __name__ == '__main__':
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
