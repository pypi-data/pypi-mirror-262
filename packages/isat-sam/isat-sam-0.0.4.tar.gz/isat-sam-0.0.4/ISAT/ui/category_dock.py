# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/super/PycharmProjects/ISAT_with_segment_anything/ui/category_dock.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(294, 462)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_group_mode = QtWidgets.QPushButton(Form)
        self.pushButton_group_mode.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pushButton_group_mode.setObjectName("pushButton_group_mode")
        self.horizontalLayout.addWidget(self.pushButton_group_mode)
        self.pushButton_decrease = QtWidgets.QPushButton(Form)
        self.pushButton_decrease.setMaximumSize(QtCore.QSize(20, 16777215))
        self.pushButton_decrease.setObjectName("pushButton_decrease")
        self.horizontalLayout.addWidget(self.pushButton_decrease)
        self.lineEdit_currentGroup = QtWidgets.QLineEdit(Form)
        self.lineEdit_currentGroup.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit_currentGroup.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_currentGroup.setText("")
        self.lineEdit_currentGroup.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_currentGroup.setObjectName("lineEdit_currentGroup")
        self.horizontalLayout.addWidget(self.lineEdit_currentGroup)
        self.pushButton_increase = QtWidgets.QPushButton(Form)
        self.pushButton_increase.setMaximumSize(QtCore.QSize(20, 16777215))
        self.pushButton_increase.setObjectName("pushButton_increase")
        self.horizontalLayout.addWidget(self.pushButton_increase)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_group_mode.setStatusTip(_translate("Form", "Group mode"))
        self.pushButton_group_mode.setWhatsThis(_translate("Form", "Group mode"))
        self.pushButton_group_mode.setText(_translate("Form", "Auto"))
        self.pushButton_decrease.setStatusTip(_translate("Form", "Current group -"))
        self.pushButton_decrease.setWhatsThis(_translate("Form", "Current group -"))
        self.pushButton_decrease.setText(_translate("Form", "-"))
        self.lineEdit_currentGroup.setStatusTip(_translate("Form", "Current group"))
        self.lineEdit_currentGroup.setWhatsThis(_translate("Form", "Current group"))
        self.pushButton_increase.setStatusTip(_translate("Form", "Current group +"))
        self.pushButton_increase.setWhatsThis(_translate("Form", "Current group +"))
        self.pushButton_increase.setText(_translate("Form", "+"))
