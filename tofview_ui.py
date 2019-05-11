# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tofview.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_tofView(object):
    def setupUi(self, tofView):
        tofView.setObjectName("tofView")
        tofView.resize(761, 318)
        self.graphicsView = PlotWidget(tofView)
        self.graphicsView.setGeometry(QtCore.QRect(220, 10, 531, 271))
        self.graphicsView.setObjectName("graphicsView")
        self.btnNextTOF = QtWidgets.QPushButton(tofView)
        self.btnNextTOF.setGeometry(QtCore.QRect(550, 290, 75, 23))
        self.btnNextTOF.setObjectName("btnNextTOF")
        self.btnPrevTOF = QtWidgets.QPushButton(tofView)
        self.btnPrevTOF.setGeometry(QtCore.QRect(360, 290, 75, 23))
        self.btnPrevTOF.setObjectName("btnPrevTOF")
        self.labelTOFNum = QtWidgets.QLabel(tofView)
        self.labelTOFNum.setGeometry(QtCore.QRect(470, 293, 47, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelTOFNum.setFont(font)
        self.labelTOFNum.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTOFNum.setObjectName("labelTOFNum")
        self.qlxpos = QtWidgets.QLabel(tofView)
        self.qlxpos.setGeometry(QtCore.QRect(150, 30, 47, 13))
        self.qlxpos.setObjectName("qlxpos")
        self.label_2 = QtWidgets.QLabel(tofView)
        self.label_2.setGeometry(QtCore.QRect(130, 50, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(tofView)
        self.label.setGeometry(QtCore.QRect(130, 30, 47, 13))
        self.label.setObjectName("label")
        self.qlypos = QtWidgets.QLabel(tofView)
        self.qlypos.setGeometry(QtCore.QRect(150, 50, 47, 13))
        self.qlypos.setObjectName("qlypos")
        self.label_3 = QtWidgets.QLabel(tofView)
        self.label_3.setGeometry(QtCore.QRect(120, 10, 81, 16))
        self.label_3.setObjectName("label_3")
        self.btnAutoscale = QtWidgets.QPushButton(tofView)
        self.btnAutoscale.setGeometry(QtCore.QRect(220, 290, 75, 23))
        self.btnAutoscale.setAcceptDrops(False)
        self.btnAutoscale.setAutoDefault(False)
        self.btnAutoscale.setDefault(False)
        self.btnAutoscale.setFlat(False)
        self.btnAutoscale.setObjectName("btnAutoscale")
        self.markerTable = QtWidgets.QTableWidget(tofView)
        self.markerTable.setGeometry(QtCore.QRect(10, 70, 201, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.markerTable.setFont(font)
        self.markerTable.setCornerButtonEnabled(True)
        self.markerTable.setColumnCount(3)
        self.markerTable.setObjectName("markerTable")
        self.markerTable.setRowCount(0)
        self.markerTable.horizontalHeader().setCascadingSectionResizes(False)
        self.markerTable.horizontalHeader().setDefaultSectionSize(100)
        self.markerTable.horizontalHeader().setSortIndicatorShown(False)
        self.markerTable.verticalHeader().setVisible(False)
        self.btnLoad = QtWidgets.QPushButton(tofView)
        self.btnLoad.setGeometry(QtCore.QRect(10, 10, 101, 23))
        self.btnLoad.setObjectName("btnLoad")
        self.label_4 = QtWidgets.QLabel(tofView)
        self.label_4.setGeometry(QtCore.QRect(10, 40, 51, 16))
        self.label_4.setObjectName("label_4")
        self.leTolerance = QtWidgets.QLineEdit(tofView)
        self.leTolerance.setGeometry(QtCore.QRect(60, 40, 51, 20))
        self.leTolerance.setObjectName("leTolerance")

        self.retranslateUi(tofView)
        QtCore.QMetaObject.connectSlotsByName(tofView)

    def retranslateUi(self, tofView):
        _translate = QtCore.QCoreApplication.translate
        tofView.setWindowTitle(_translate("tofView", "Form"))
        self.btnNextTOF.setText(_translate("tofView", "-->"))
        self.btnPrevTOF.setText(_translate("tofView", "<--"))
        self.labelTOFNum.setText(_translate("tofView", "1"))
        self.qlxpos.setText(_translate("tofView", "None"))
        self.label_2.setText(_translate("tofView", "y:"))
        self.label.setText(_translate("tofView", "x:"))
        self.qlypos.setText(_translate("tofView", "None"))
        self.label_3.setText(_translate("tofView", "Mouse Position:"))
        self.btnAutoscale.setText(_translate("tofView", "Autoscale"))
        self.markerTable.setSortingEnabled(True)
        self.btnLoad.setText(_translate("tofView", "Load TOF"))
        self.label_4.setText(_translate("tofView", "Abs. Tol."))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    tofView = QtWidgets.QWidget()
    ui = Ui_tofView()
    ui.setupUi(tofView)
    tofView.show()
    sys.exit(app.exec_())

