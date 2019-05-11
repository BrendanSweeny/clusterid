# TODO: Refactor handleFindMatches, migrate most of it to module
# TODO: Decide if markers should be cleared between TOF loads

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QTableWidgetItem, QLabel, QComboBox, QFileDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainterPath, QFont, QTransform, QTextDocument
import sys
import csv
import pyqtgraph as pg
import numpy as np
import pandas as pd
import utils
from tofview_ui import Ui_tofView
import findMatch
from operator import attrgetter, itemgetter
from elements import Element
from elementdata import ElementData

class TofView(QWidget):
    # Set configs before loading module
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    def __init__(self):
        super().__init__()
        self.ui = Ui_tofView()
        self.ui.setupUi(self)

        # Right now this is only here to validate the formula of a ligand emitted
        # from periodicTableWidget
        self.periodicTable = {}
        self.elements = ElementData().elements
        for element in self.elements:
            self.periodicTable[element['symbol']] = Element(element['mass'], element['symbol'], element['name'], element['number'])

        # Mass spectrum plot parameters
        self.plot = self.ui.graphicsView.plotItem

        # Object representing the TOF plot, plotted markers will be kept in seperate array
        self.tofPlot = None

        self.fileIsMultipoint = False

        # Array containing objects for plotted markers:
        self.plotMarkers = []
        self.alphaMarkerList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                                'U', 'V', 'W', 'X', 'Y', 'Z']

        # Mass used for findMatches algorithm (set by default to arbitrary non-zero int)
        self.targetVal = 217
        self.absoluteTolerance = 2

        # Autoscale Boundary List:
        self.boundList = []

        # List of selected element objects:
        self.selectedElements = []

        # Array of DFs, each representing one mass spectrum/flow point:
        self.pointsDFArray = []

        # Currently displayed mass spectrum DF:
        self.plottedDFIndex = 0

        # Length of the loaded DF array
        self.pointsDFArrayLen = 0

        # Absolute tolerance for findMatches:
        self.ui.leTolerance.setText(str(self.absoluteTolerance))

        # Event Handlers:
        self.ui.btnAutoscale.clicked.connect(self.autoscale)
        self.ui.btnNextTOF.clicked.connect(self.handleNextPoint)
        self.ui.btnPrevTOF.clicked.connect(self.handleNextPoint)
        self.ui.btnLoad.clicked.connect(self.handleOpenFile)
        self.ui.leTolerance.textChanged.connect(self.handleChangeTolerance)

        # Mouseover Plot Signal/Slot
        self.mouseOverProxy = pg.SignalProxy(self.ui.graphicsView.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        self.mouseClickProxy = pg.SignalProxy(self.ui.graphicsView.scene().sigMouseClicked, rateLimit=60, slot=self.handlePlotClick)

        # Set Up:
        self.ui.labelTOFNum.setText(str(self.plottedDFIndex + 1))

        self.ui.markerTable.setColumnWidth(0, 25)
        self.ui.markerTable.setColumnWidth(2, 50)
        self.ui.markerTable.setHorizontalHeaderLabels(['', 'Formula', ''])
        self.disableNextBtns()

### Helper Functions ###

    def enableNextBtns(self):
        self.ui.btnNextTOF.setEnabled(True)
        self.ui.btnPrevTOF.setEnabled(True)

    def disableNextBtns(self):
        self.ui.btnNextTOF.setEnabled(False)
        self.ui.btnPrevTOF.setEnabled(False)

    def handleChangeTolerance(self):
        val = self.sender().text()
        if val:
            self.absoluteTolerance = float(val)
        else:
            self.absoluteTolerance = 2

    def handleOpenFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        if filename[0]:
            if self.tofPlot:
                self.tofPlot.clear()
            self.loadTOF(filename[0])

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

    def handleElementClicked(self, elementObject, checked):
        mass = elementObject.mass
        symbol = elementObject.symbol
        formulaList = utils.formulaToList(symbol)
        # Does nothing is teh ligand formula/symbol cannot be validated
        if not utils.validateFormulaList(self.elements, formulaList):
            return
        elif checked and elementObject not in self.selectedElements:
            self.selectedElements.append(elementObject)
        elif not checked:
            self.selectedElements.remove(elementObject)

    def handleRemoveMarker(self):
        # Finds and returns the cell corresponding to the QLabel of the row whose 'remove'
        # button was clicked
        clickedButton = self.sender()
        index = self.ui.markerTable.indexAt(clickedButton.pos())
        symbolCell = self.ui.markerTable.item(index.row(), 0)

        # Finds the index of the formula object in the selectedMolecules list
        for i in self.plotMarkers:
            if i['symbol'] == symbolCell.text():
                markerObject = self.plotMarkers.pop(self.plotMarkers.index(i))
                markerObject['plot'].clear()

        # Removes table row containing clicked item and formula from list
        self.ui.markerTable.removeRow(index.row())

    def handleChangeIndex(self):
        comboBox = self.sender()
        index = self.ui.markerTable.indexAt(comboBox.pos())
        symbolCell = self.ui.markerTable.item(index.row(), 0)

    def updateMarkerTable(self):
        self.ui.markerTable.setRowCount(len(self.plotMarkers))
        for i in range(len(self.plotMarkers)):
            symbol = self.plotMarkers[i]['symbol']
            rmBtn = QPushButton('X')
            formula = utils.formatFormula('V2Al1O13')
            comboBox = QComboBox()
            formLabel = QLabel(formula)
            comboBox.addItem(utils.formatFormulaUnicode('V2Al1O13'))
            comboBox.addItem(utils.formatFormulaUnicode('H2O2'))
            comboBox.addItem(utils.formatFormulaUnicode('V23Al1O3H1'))
            comboBox.setCurrentIndex(0)
            comboBox.currentIndexChanged.connect(self.handleChangeIndex)
            rmBtn.clicked.connect(self.handleRemoveMarker)
            #self.ui.markerTable.setCellWidget(i, 0, label)
            self.ui.markerTable.setItem(i, 0, QTableWidgetItem(symbol))
            self.ui.markerTable.setCellWidget(i, 1, comboBox)
            self.ui.markerTable.setCellWidget(i, 2, rmBtn)

    def generateMarker(self, xVal, yVal):
        # Create list of used markers:
        usedMarkers = [self.ui.markerTable.item(i, 0).data(0) for i in range(self.ui.markerTable.rowCount())]

        # Use next available marker:
        markerLetter = None
        for letter in self.alphaMarkerList:
            if letter not in usedMarkers:
                markerLetter = letter
                break
            else:
                continue

        if not markerLetter:
            raise ValueError('No letters available to use as markers.')
        else:
            marker = QPainterPath()
            marker.addText(0, 0, QFont("San Serif", 1), markerLetter)
            br = marker.boundingRect()
            scale = min(1. / br.width(), 1. / br.height())
            tr = QTransform()
            tr.scale(scale, scale)
            tr.translate(-br.x() - br.width()/2., -br.y() - br.height()/2.)
            marker = tr.map(marker)

            markerDict = {
                'symbol': markerLetter,
                'plot': self.plot.plot([xVal], [yVal], pen=None, symbol=marker)
            }

            return markerDict

    def addRowToMarkerTable(self, markerDict, matchedClusters):
        self.ui.markerTable.setRowCount(len(self.plotMarkers))
        newRowIndex = self.ui.markerTable.rowCount() - 1

        symbol = markerDict['symbol']
        rmBtn = QPushButton('X')
        comboBox = QComboBox()
        for cluster in matchedClusters:
            comboBox.addItem(utils.formatFormulaUnicode(cluster['formula']))
        comboBox.setCurrentIndex(0)
        comboBox.currentIndexChanged.connect(self.handleChangeIndex)
        rmBtn.clicked.connect(self.handleRemoveMarker)
        self.ui.markerTable.setItem(newRowIndex, 0, QTableWidgetItem(symbol))
        self.ui.markerTable.setCellWidget(newRowIndex, 1, comboBox)
        self.ui.markerTable.setCellWidget(newRowIndex, 2, rmBtn)

    # Handles logic for adding a marker and calculating the likely chemical species
    # ('Ctrl + Click' on plot)
    def handlePlotClick(self, e):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            # pyqtgraph MouseClickEvents deliver (<MouseClickEvent (363,152) button=1>,)
            pos = e[0].scenePos()
            xVal = round(self.plot.vb.mapSceneToView(pos).x(), 2)
            yVal = round(self.plot.vb.mapSceneToView(pos).y(), 3)

            # Generates a dict describing the marker
            markerDict = self.generateMarker(xVal, yVal)

            # Needs dev version pyqtgraph-0.11.0 or later to support custom markers
            self.plotMarkers.append(markerDict)
            #self.updateMarkerTable()

            self.targetVal = xVal

            self.handleFindMatches()

            self.addRowToMarkerTable(markerDict, self.matchedClusters)

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

    # Wrapper for pyqtgraph's plotting function:
    def handlePlot(self, df):
        self.tofPlot = self.ui.graphicsView.plot(df.values.astype('float64'), pen=pg.mkPen('k'))

    # Click handler that moves mass spectrum to next/previous flow point
    def handleNextPoint(self):
        sender = self.sender().text()
        self.tofPlot.clear()
        if sender == '-->':
            if self.plottedDFIndex == self.pointsDFArrayLen - 1:
                self.plottedDFIndex = 0
            else:
                self.plottedDFIndex += 1
        elif sender == '<--':
            if self.plottedDFIndex == 0:
                self.plottedDFIndex = self.pointsDFArrayLen - 1
            else:
                self.plottedDFIndex -= 1

        self.ui.labelTOFNum.setText(str(self.plottedDFIndex + 1))
        self.handlePlot(self.pointsDFArray[self.plottedDFIndex])

    def autoscale(self):
        if self.boundList:
            xScaleMin = self.boundList[0]
            xScaleMax = self.boundList[1]
            yScaleMax = self.boundList[2]

            self.ui.graphicsView.setXRange(xScaleMin, xScaleMax, padding=0)
            self.ui.graphicsView.setYRange(0, yScaleMax, padding=0)

    # Algorithm to determine window autoscaling
    def determineSinglePtAutoscale(self, singlePointDF):

        # Remove TOF pulser counts:
        singlePointNoPulseDF = singlePointDF[['mass', 'cts']].loc[566:].astype('float64')

        # Create new DF filtered to select for rows with cts above noise level:
        noiseLevel = 1
        valuesAboveNoiseDF = singlePointNoPulseDF.loc[singlePointNoPulseDF['cts'] > noiseLevel]

        # Determine scaling:
        yMax = valuesAboveNoiseDF['cts'].max()
        xMax = valuesAboveNoiseDF['mass'].iloc[-1]
        xMin = valuesAboveNoiseDF['mass'].iloc[0]
        yScaleMax = yMax + (yMax * 0.1)
        xScaleMax = xMax + (xMax * 0.1)
        xScaleMin = xMin - (xMin * 0.1)

        return [xScaleMin, xScaleMax, yScaleMax]

    # Creates plot bounds that include all peaks found in any of the dfs
    def determineMultiPtAutoscale(self, arrayOfDFs):
        overallBounds = []
        for df in arrayOfDFs:
            bounds = self.determineSinglePtAutoscale(df)
            if overallBounds == []:
                overallBounds = bounds
            else:
                if bounds[0] < overallBounds[0]:
                    overallBounds[0] = bounds[0]
                if bounds[1] > overallBounds[1]:
                    overallBounds[1] = bounds[1]
                if bounds[2] > overallBounds[2]:
                    overallBounds[2] = bounds[2]

        return overallBounds

    def loadTOF(self, tofFile):
        # Load file into pandas DF, add index to rows and header names
        # 'unused1' and 'unused2' are used because multipoint TOF files have strange formatting that results in extra columns of NaNs
        fullTofDF = pd.read_csv(tofFile, delimiter='\t', index_col=False, names=['tof', 'mass', 'cts', 'unused1', 'unused2'])

        multipointFile = False
        for entry in fullTofDF['tof'].unique():
            if 'Flow Point' in entry:
                multipointFile = True
                break
        if multipointFile:
            self.fileIsMultipoint = True
            self.enableNextBtns()
            print('multipoint file loaded.')
        else:
            self.fileIsMultipoint = False
            self.disableNextBtns()
            print('single point file loaded')

        # Checks if single point or multipoint by looking for "Flow Point" designation in DF
        if not multipointFile:
            # Right now, we disregard the first two rows of the table
            singlePointDF = fullTofDF[['mass', 'cts']].loc[2:]
            # Determine plot boundaries based on data:
            boundList = self.determineSinglePtAutoscale(singlePointDF)
            self.boundList = boundList

            # Perform autoscale:
            self.autoscale()

            # Plot TOF data:
            self.handlePlot(singlePointDF)

            self.plottedDFIndex = 0
            self.ui.labelTOFNum.setText(str(1))

        # If it is a multipoint file:
        else:
            flowptDF = fullTofDF[fullTofDF['tof'].str.contains('Flow Point')]

            # Create an array of DF, with each DF representing a spectrum/flow point
            pointsDFArray = []
            for index, location in enumerate(flowptDF.index.values):
                if index != len(flowptDF.index.values) - 1:
                    newPointDF = fullTofDF[['mass', 'cts']].iloc[location + 1: flowptDF.index.values[index + 1]]
                else:
                    newPointDF = fullTofDF[['mass', 'cts']].iloc[location + 1:]
                pointsDFArray.append(newPointDF)

            self.pointsDFArray = pointsDFArray
            self.pointsDFArrayLen = len(pointsDFArray)

            boundList = self.determineMultiPtAutoscale(pointsDFArray)
            self.boundList = boundList

            # Perform autoscale:
            self.autoscale()

            # Plot TOF data:
            self.handlePlot(pointsDFArray[0])

            self.plottedDFIndex = 0
            self.ui.labelTOFNum.setText(str(1))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TofView()
    window.show()
    sys.exit(app.exec_())
