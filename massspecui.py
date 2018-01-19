# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'massspec.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MassSpec(object):
    def setupUi(self, MassSpec):
        MassSpec.setObjectName("MassSpec")
        MassSpec.resize(761, 318)
        self.graphicsView = PlotWidget(MassSpec)
        self.graphicsView.setGeometry(QtCore.QRect(250, 0, 501, 311))
        self.graphicsView.setObjectName("graphicsView")
        self.formulaLineEdit = QtWidgets.QLineEdit(MassSpec)
        self.formulaLineEdit.setGeometry(QtCore.QRect(10, 30, 113, 20))
        self.formulaLineEdit.setObjectName("formulaLineEdit")
        self.selectedMoleculesTable = QtWidgets.QTableWidget(MassSpec)
        self.selectedMoleculesTable.setGeometry(QtCore.QRect(10, 60, 221, 231))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.selectedMoleculesTable.setFont(font)
        self.selectedMoleculesTable.setColumnCount(2)
        self.selectedMoleculesTable.setObjectName("selectedMoleculesTable")
        self.selectedMoleculesTable.setRowCount(0)
        self.selectedMoleculesTable.horizontalHeader().setSortIndicatorShown(False)
        self.selectedMoleculesTable.verticalHeader().setVisible(False)
        self.label = QtWidgets.QLabel(MassSpec)
        self.label.setGeometry(QtCore.QRect(170, 20, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(MassSpec)
        self.label_2.setGeometry(QtCore.QRect(170, 40, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(MassSpec)
        self.label_3.setGeometry(QtCore.QRect(160, 0, 81, 16))
        self.label_3.setObjectName("label_3")
        self.qlxpos = QtWidgets.QLabel(MassSpec)
        self.qlxpos.setGeometry(QtCore.QRect(190, 20, 47, 13))
        self.qlxpos.setObjectName("qlxpos")
        self.qlypos = QtWidgets.QLabel(MassSpec)
        self.qlypos.setGeometry(QtCore.QRect(190, 40, 47, 13))
        self.qlypos.setObjectName("qlypos")
        self.label_4 = QtWidgets.QLabel(MassSpec)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 101, 16))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(MassSpec)
        QtCore.QMetaObject.connectSlotsByName(MassSpec)

    def retranslateUi(self, MassSpec):
        _translate = QtCore.QCoreApplication.translate
        MassSpec.setWindowTitle(_translate("MassSpec", "Form"))
        self.selectedMoleculesTable.setSortingEnabled(True)
        self.label.setText(_translate("MassSpec", "x:"))
        self.label_2.setText(_translate("MassSpec", "y:"))
        self.label_3.setText(_translate("MassSpec", "Mouse Position:"))
        self.qlxpos.setText(_translate("MassSpec", "None"))
        self.qlypos.setText(_translate("MassSpec", "None"))
        self.label_4.setText(_translate("MassSpec", "Chemical Formula:"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MassSpec = QtWidgets.QWidget()
    ui = Ui_MassSpec()
    ui.setupUi(MassSpec)
    MassSpec.show()
    sys.exit(app.exec_())

