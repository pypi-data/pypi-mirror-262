# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/disk2/PycharmProjects/ISAT_with_segment_anything/ISAT/ui/Converter_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1000, 680)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        Dialog.setFont(font)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_COCO = QtWidgets.QWidget()
        self.tab_COCO.setObjectName("tab_COCO")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_COCO)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget = QtWidgets.QWidget(self.tab_COCO)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBox_coco = QtWidgets.QToolBox(self.widget)
        self.toolBox_coco.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.toolBox_coco.setFrameShadow(QtWidgets.QFrame.Plain)
        self.toolBox_coco.setObjectName("toolBox_coco")
        self.toolbox_item_coco2isat = QtWidgets.QWidget()
        self.toolbox_item_coco2isat.setGeometry(QtCore.QRect(0, 0, 138, 109))
        self.toolbox_item_coco2isat.setObjectName("toolbox_item_coco2isat")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.toolbox_item_coco2isat)
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_3 = QtWidgets.QWidget(self.toolbox_item_coco2isat)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget_7 = QtWidgets.QWidget(self.widget_3)
        self.widget_7.setObjectName("widget_7")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_7)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_coco2isat_coco_json_path = QtWidgets.QPushButton(self.widget_7)
        self.pushButton_coco2isat_coco_json_path.setObjectName("pushButton_coco2isat_coco_json_path")
        self.gridLayout.addWidget(self.pushButton_coco2isat_coco_json_path, 0, 1, 1, 1)
        self.lineEdit_coco2isat_isat_json_root = QtWidgets.QLineEdit(self.widget_7)
        self.lineEdit_coco2isat_isat_json_root.setReadOnly(True)
        self.lineEdit_coco2isat_isat_json_root.setObjectName("lineEdit_coco2isat_isat_json_root")
        self.gridLayout.addWidget(self.lineEdit_coco2isat_isat_json_root, 1, 0, 1, 1)
        self.lineEdit_coco2isat_coco_json_path = QtWidgets.QLineEdit(self.widget_7)
        self.lineEdit_coco2isat_coco_json_path.setReadOnly(True)
        self.lineEdit_coco2isat_coco_json_path.setObjectName("lineEdit_coco2isat_coco_json_path")
        self.gridLayout.addWidget(self.lineEdit_coco2isat_coco_json_path, 0, 0, 1, 1)
        self.pushButton_coco2isat_isat_json_root = QtWidgets.QPushButton(self.widget_7)
        self.pushButton_coco2isat_isat_json_root.setObjectName("pushButton_coco2isat_isat_json_root")
        self.gridLayout.addWidget(self.pushButton_coco2isat_isat_json_root, 1, 1, 1, 1)
        self.verticalLayout_7.addWidget(self.widget_7)
        self.widget_8 = QtWidgets.QWidget(self.widget_3)
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(445, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.checkBox_coco2isat_keep_crowd = QtWidgets.QCheckBox(self.widget_8)
        self.checkBox_coco2isat_keep_crowd.setObjectName("checkBox_coco2isat_keep_crowd")
        self.horizontalLayout_3.addWidget(self.checkBox_coco2isat_keep_crowd)
        self.verticalLayout_7.addWidget(self.widget_8)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.toolBox_coco.addItem(self.toolbox_item_coco2isat, "")
        self.toolbox_item_isat2coco = QtWidgets.QWidget()
        self.toolbox_item_isat2coco.setGeometry(QtCore.QRect(0, 0, 960, 153))
        self.toolbox_item_isat2coco.setObjectName("toolbox_item_isat2coco")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.toolbox_item_isat2coco)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_4 = QtWidgets.QWidget(self.toolbox_item_isat2coco)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_5 = QtWidgets.QWidget(self.widget_4)
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_5)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_isat2coco_isat_json_root = QtWidgets.QLineEdit(self.widget_5)
        self.lineEdit_isat2coco_isat_json_root.setReadOnly(True)
        self.lineEdit_isat2coco_isat_json_root.setObjectName("lineEdit_isat2coco_isat_json_root")
        self.gridLayout_2.addWidget(self.lineEdit_isat2coco_isat_json_root, 0, 0, 1, 1)
        self.pushButton_isat2coco_isat_json_root = QtWidgets.QPushButton(self.widget_5)
        self.pushButton_isat2coco_isat_json_root.setObjectName("pushButton_isat2coco_isat_json_root")
        self.gridLayout_2.addWidget(self.pushButton_isat2coco_isat_json_root, 0, 1, 1, 1)
        self.lineEdit_isat2coco_coco_json_path = QtWidgets.QLineEdit(self.widget_5)
        self.lineEdit_isat2coco_coco_json_path.setReadOnly(True)
        self.lineEdit_isat2coco_coco_json_path.setObjectName("lineEdit_isat2coco_coco_json_path")
        self.gridLayout_2.addWidget(self.lineEdit_isat2coco_coco_json_path, 1, 0, 1, 1)
        self.pushButton_isat2coco_coco_json_path = QtWidgets.QPushButton(self.widget_5)
        self.pushButton_isat2coco_coco_json_path.setObjectName("pushButton_isat2coco_coco_json_path")
        self.gridLayout_2.addWidget(self.pushButton_isat2coco_coco_json_path, 1, 1, 1, 1)
        self.verticalLayout_6.addWidget(self.widget_5)
        self.widget_6 = QtWidgets.QWidget(self.widget_4)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(445, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.checkBox_isat2coco_keep_crowd = QtWidgets.QCheckBox(self.widget_6)
        self.checkBox_isat2coco_keep_crowd.setObjectName("checkBox_isat2coco_keep_crowd")
        self.horizontalLayout_2.addWidget(self.checkBox_isat2coco_keep_crowd)
        self.verticalLayout_6.addWidget(self.widget_6)
        self.verticalLayout_5.addWidget(self.widget_4)
        self.toolBox_coco.addItem(self.toolbox_item_isat2coco, "")
        self.verticalLayout.addWidget(self.toolBox_coco)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.verticalLayout_4.addWidget(self.widget)
        self.tabWidget.addTab(self.tab_COCO, "")
        self.tab_YOLO = QtWidgets.QWidget()
        self.tab_YOLO.setObjectName("tab_YOLO")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_YOLO)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.widget_9 = QtWidgets.QWidget(self.tab_YOLO)
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_9)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.toolBox_yolo = QtWidgets.QToolBox(self.widget_9)
        self.toolBox_yolo.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.toolBox_yolo.setFrameShadow(QtWidgets.QFrame.Plain)
        self.toolBox_yolo.setObjectName("toolBox_yolo")
        self.toolbox_item_yolo2isat = QtWidgets.QWidget()
        self.toolbox_item_yolo2isat.setGeometry(QtCore.QRect(0, 0, 161, 144))
        self.toolbox_item_yolo2isat.setObjectName("toolbox_item_yolo2isat")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.toolbox_item_yolo2isat)
        self.verticalLayout_9.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.widget_10 = QtWidgets.QWidget(self.toolbox_item_yolo2isat)
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.widget_11 = QtWidgets.QWidget(self.widget_10)
        self.widget_11.setObjectName("widget_11")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_11)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_yolo2isat_isat_json_root = QtWidgets.QLineEdit(self.widget_11)
        self.lineEdit_yolo2isat_isat_json_root.setReadOnly(True)
        self.lineEdit_yolo2isat_isat_json_root.setObjectName("lineEdit_yolo2isat_isat_json_root")
        self.gridLayout_3.addWidget(self.lineEdit_yolo2isat_isat_json_root, 3, 0, 1, 1)
        self.pushButton_yolo2isat_isat_json_root = QtWidgets.QPushButton(self.widget_11)
        self.pushButton_yolo2isat_isat_json_root.setObjectName("pushButton_yolo2isat_isat_json_root")
        self.gridLayout_3.addWidget(self.pushButton_yolo2isat_isat_json_root, 3, 2, 1, 1)
        self.lineEdit_yolo2isat_yolo_txt_root = QtWidgets.QLineEdit(self.widget_11)
        self.lineEdit_yolo2isat_yolo_txt_root.setReadOnly(True)
        self.lineEdit_yolo2isat_yolo_txt_root.setObjectName("lineEdit_yolo2isat_yolo_txt_root")
        self.gridLayout_3.addWidget(self.lineEdit_yolo2isat_yolo_txt_root, 1, 0, 1, 1)
        self.pushButton_yolo2isat_yolo_txt_root = QtWidgets.QPushButton(self.widget_11)
        self.pushButton_yolo2isat_yolo_txt_root.setObjectName("pushButton_yolo2isat_yolo_txt_root")
        self.gridLayout_3.addWidget(self.pushButton_yolo2isat_yolo_txt_root, 1, 2, 1, 1)
        self.lineEdit_yolo2isat_yolo_image_root = QtWidgets.QLineEdit(self.widget_11)
        self.lineEdit_yolo2isat_yolo_image_root.setReadOnly(True)
        self.lineEdit_yolo2isat_yolo_image_root.setObjectName("lineEdit_yolo2isat_yolo_image_root")
        self.gridLayout_3.addWidget(self.lineEdit_yolo2isat_yolo_image_root, 0, 0, 1, 1)
        self.pushButton_yolo2isat_yolo_image_root = QtWidgets.QPushButton(self.widget_11)
        self.pushButton_yolo2isat_yolo_image_root.setObjectName("pushButton_yolo2isat_yolo_image_root")
        self.gridLayout_3.addWidget(self.pushButton_yolo2isat_yolo_image_root, 0, 2, 1, 1)
        self.lineEdit_yolo2isat_yolo_cate_path = QtWidgets.QLineEdit(self.widget_11)
        self.lineEdit_yolo2isat_yolo_cate_path.setText("")
        self.lineEdit_yolo2isat_yolo_cate_path.setReadOnly(True)
        self.lineEdit_yolo2isat_yolo_cate_path.setObjectName("lineEdit_yolo2isat_yolo_cate_path")
        self.gridLayout_3.addWidget(self.lineEdit_yolo2isat_yolo_cate_path, 2, 0, 1, 1)
        self.pushButton_yolo2isat_yolo_cate_path = QtWidgets.QPushButton(self.widget_11)
        self.pushButton_yolo2isat_yolo_cate_path.setObjectName("pushButton_yolo2isat_yolo_cate_path")
        self.gridLayout_3.addWidget(self.pushButton_yolo2isat_yolo_cate_path, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.widget_11)
        self.label.setToolTip("")
        self.label.setStatusTip("")
        self.label.setWhatsThis("")
        self.label.setStyleSheet("color: rgb(255, 0, 0);")
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget_11)
        self.label_7.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget_11)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.widget_11)
        self.label_9.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 3, 1, 1, 1)
        self.verticalLayout_10.addWidget(self.widget_11)
        self.verticalLayout_9.addWidget(self.widget_10)
        self.toolBox_yolo.addItem(self.toolbox_item_yolo2isat, "")
        self.toolbox_item_isat2yolo = QtWidgets.QWidget()
        self.toolbox_item_isat2yolo.setGeometry(QtCore.QRect(0, 0, 960, 153))
        self.toolbox_item_isat2yolo.setObjectName("toolbox_item_isat2yolo")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.toolbox_item_isat2yolo)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.widget_13 = QtWidgets.QWidget(self.toolbox_item_isat2yolo)
        self.widget_13.setObjectName("widget_13")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.widget_13)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.widget_14 = QtWidgets.QWidget(self.widget_13)
        self.widget_14.setObjectName("widget_14")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget_14)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton_isat2yolo_yolo_txt_root = QtWidgets.QPushButton(self.widget_14)
        self.pushButton_isat2yolo_yolo_txt_root.setObjectName("pushButton_isat2yolo_yolo_txt_root")
        self.gridLayout_4.addWidget(self.pushButton_isat2yolo_yolo_txt_root, 1, 1, 1, 1)
        self.lineEdit_isat2yolo_yolo_txt_root = QtWidgets.QLineEdit(self.widget_14)
        self.lineEdit_isat2yolo_yolo_txt_root.setReadOnly(True)
        self.lineEdit_isat2yolo_yolo_txt_root.setObjectName("lineEdit_isat2yolo_yolo_txt_root")
        self.gridLayout_4.addWidget(self.lineEdit_isat2yolo_yolo_txt_root, 1, 0, 1, 1)
        self.lineEdit_isat2yolo_isat_json_root = QtWidgets.QLineEdit(self.widget_14)
        self.lineEdit_isat2yolo_isat_json_root.setReadOnly(True)
        self.lineEdit_isat2yolo_isat_json_root.setObjectName("lineEdit_isat2yolo_isat_json_root")
        self.gridLayout_4.addWidget(self.lineEdit_isat2yolo_isat_json_root, 0, 0, 1, 1)
        self.pushButton_isat2yolo_isat_json_root = QtWidgets.QPushButton(self.widget_14)
        self.pushButton_isat2yolo_isat_json_root.setObjectName("pushButton_isat2yolo_isat_json_root")
        self.gridLayout_4.addWidget(self.pushButton_isat2yolo_isat_json_root, 0, 1, 1, 1)
        self.verticalLayout_12.addWidget(self.widget_14)
        self.verticalLayout_11.addWidget(self.widget_13)
        self.toolBox_yolo.addItem(self.toolbox_item_isat2yolo, "")
        self.verticalLayout_3.addWidget(self.toolBox_yolo)
        self.label_3 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.verticalLayout_8.addWidget(self.widget_9)
        self.tabWidget.addTab(self.tab_YOLO, "")
        self.tab_LABELME = QtWidgets.QWidget()
        self.tab_LABELME.setObjectName("tab_LABELME")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.tab_LABELME)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.widget_16 = QtWidgets.QWidget(self.tab_LABELME)
        self.widget_16.setObjectName("widget_16")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.widget_16)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.toolBox_labelme = QtWidgets.QToolBox(self.widget_16)
        self.toolBox_labelme.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.toolBox_labelme.setFrameShadow(QtWidgets.QFrame.Plain)
        self.toolBox_labelme.setObjectName("toolBox_labelme")
        self.toolbox_item_labelme2isat = QtWidgets.QWidget()
        self.toolbox_item_labelme2isat.setGeometry(QtCore.QRect(0, 0, 960, 153))
        self.toolbox_item_labelme2isat.setObjectName("toolbox_item_labelme2isat")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.toolbox_item_labelme2isat)
        self.verticalLayout_16.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.widget_17 = QtWidgets.QWidget(self.toolbox_item_labelme2isat)
        self.widget_17.setObjectName("widget_17")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.widget_17)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.widget_18 = QtWidgets.QWidget(self.widget_17)
        self.widget_18.setObjectName("widget_18")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.widget_18)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.pushButton_labelme2isat_labelme_json_root = QtWidgets.QPushButton(self.widget_18)
        self.pushButton_labelme2isat_labelme_json_root.setObjectName("pushButton_labelme2isat_labelme_json_root")
        self.gridLayout_6.addWidget(self.pushButton_labelme2isat_labelme_json_root, 0, 1, 1, 1)
        self.lineEdit_labelme2isat_isat_json_root = QtWidgets.QLineEdit(self.widget_18)
        self.lineEdit_labelme2isat_isat_json_root.setReadOnly(True)
        self.lineEdit_labelme2isat_isat_json_root.setObjectName("lineEdit_labelme2isat_isat_json_root")
        self.gridLayout_6.addWidget(self.lineEdit_labelme2isat_isat_json_root, 1, 0, 1, 1)
        self.lineEdit_labelme2isat_labelme_json_root = QtWidgets.QLineEdit(self.widget_18)
        self.lineEdit_labelme2isat_labelme_json_root.setReadOnly(True)
        self.lineEdit_labelme2isat_labelme_json_root.setObjectName("lineEdit_labelme2isat_labelme_json_root")
        self.gridLayout_6.addWidget(self.lineEdit_labelme2isat_labelme_json_root, 0, 0, 1, 1)
        self.pushButton_labelme2isat_isat_json_root = QtWidgets.QPushButton(self.widget_18)
        self.pushButton_labelme2isat_isat_json_root.setObjectName("pushButton_labelme2isat_isat_json_root")
        self.gridLayout_6.addWidget(self.pushButton_labelme2isat_isat_json_root, 1, 1, 1, 1)
        self.verticalLayout_17.addWidget(self.widget_18)
        self.verticalLayout_16.addWidget(self.widget_17)
        self.toolBox_labelme.addItem(self.toolbox_item_labelme2isat, "")
        self.toolbox_item_isat2labelme = QtWidgets.QWidget()
        self.toolbox_item_isat2labelme.setGeometry(QtCore.QRect(0, 0, 138, 78))
        self.toolbox_item_isat2labelme.setObjectName("toolbox_item_isat2labelme")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.toolbox_item_isat2labelme)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.widget_20 = QtWidgets.QWidget(self.toolbox_item_isat2labelme)
        self.widget_20.setObjectName("widget_20")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.widget_20)
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.widget_21 = QtWidgets.QWidget(self.widget_20)
        self.widget_21.setObjectName("widget_21")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget_21)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.lineEdit_isat2labelme_isat_json_root = QtWidgets.QLineEdit(self.widget_21)
        self.lineEdit_isat2labelme_isat_json_root.setReadOnly(True)
        self.lineEdit_isat2labelme_isat_json_root.setObjectName("lineEdit_isat2labelme_isat_json_root")
        self.gridLayout_7.addWidget(self.lineEdit_isat2labelme_isat_json_root, 0, 0, 1, 1)
        self.pushButton_isat2labelme_isat_json_root = QtWidgets.QPushButton(self.widget_21)
        self.pushButton_isat2labelme_isat_json_root.setObjectName("pushButton_isat2labelme_isat_json_root")
        self.gridLayout_7.addWidget(self.pushButton_isat2labelme_isat_json_root, 0, 1, 1, 1)
        self.lineEdit_isat2labelme_labelme_json_root = QtWidgets.QLineEdit(self.widget_21)
        self.lineEdit_isat2labelme_labelme_json_root.setReadOnly(True)
        self.lineEdit_isat2labelme_labelme_json_root.setObjectName("lineEdit_isat2labelme_labelme_json_root")
        self.gridLayout_7.addWidget(self.lineEdit_isat2labelme_labelme_json_root, 1, 0, 1, 1)
        self.pushButton_isat2labelme_labelme_json_root = QtWidgets.QPushButton(self.widget_21)
        self.pushButton_isat2labelme_labelme_json_root.setObjectName("pushButton_isat2labelme_labelme_json_root")
        self.gridLayout_7.addWidget(self.pushButton_isat2labelme_labelme_json_root, 1, 1, 1, 1)
        self.verticalLayout_19.addWidget(self.widget_21)
        self.verticalLayout_18.addWidget(self.widget_20)
        self.toolBox_labelme.addItem(self.toolbox_item_isat2labelme, "")
        self.verticalLayout_15.addWidget(self.toolBox_labelme)
        self.verticalLayout_20.addWidget(self.widget_16)
        self.label_4 = QtWidgets.QLabel(self.tab_LABELME)
        self.label_4.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_4.setObjectName("label_4")
        self.verticalLayout_20.addWidget(self.label_4)
        self.tabWidget.addTab(self.tab_LABELME, "")
        self.tab_VOC = QtWidgets.QWidget()
        self.tab_VOC.setObjectName("tab_VOC")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.tab_VOC)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.widget_12 = QtWidgets.QWidget(self.tab_VOC)
        self.widget_12.setObjectName("widget_12")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_12)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushButton_isat2voc_voc_png_root = QtWidgets.QPushButton(self.widget_12)
        self.pushButton_isat2voc_voc_png_root.setObjectName("pushButton_isat2voc_voc_png_root")
        self.gridLayout_5.addWidget(self.pushButton_isat2voc_voc_png_root, 1, 1, 1, 1)
        self.lineEdit_isat2voc_voc_png_root = QtWidgets.QLineEdit(self.widget_12)
        self.lineEdit_isat2voc_voc_png_root.setReadOnly(True)
        self.lineEdit_isat2voc_voc_png_root.setObjectName("lineEdit_isat2voc_voc_png_root")
        self.gridLayout_5.addWidget(self.lineEdit_isat2voc_voc_png_root, 1, 0, 1, 1)
        self.lineEdit_isat2voc_isat_json_root = QtWidgets.QLineEdit(self.widget_12)
        self.lineEdit_isat2voc_isat_json_root.setReadOnly(True)
        self.lineEdit_isat2voc_isat_json_root.setObjectName("lineEdit_isat2voc_isat_json_root")
        self.gridLayout_5.addWidget(self.lineEdit_isat2voc_isat_json_root, 0, 0, 1, 1)
        self.pushButton_isat2voc_isat_json_root = QtWidgets.QPushButton(self.widget_12)
        self.pushButton_isat2voc_isat_json_root.setObjectName("pushButton_isat2voc_isat_json_root")
        self.gridLayout_5.addWidget(self.pushButton_isat2voc_isat_json_root, 0, 1, 1, 1)
        self.verticalLayout_14.addWidget(self.widget_12)
        self.widget_15 = QtWidgets.QWidget(self.tab_VOC)
        self.widget_15.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_15.setObjectName("widget_15")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_15)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(708, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.checkBox_is_instance = QtWidgets.QCheckBox(self.widget_15)
        self.checkBox_is_instance.setObjectName("checkBox_is_instance")
        self.horizontalLayout_4.addWidget(self.checkBox_is_instance)
        self.verticalLayout_14.addWidget(self.widget_15)
        self.widget_22 = QtWidgets.QWidget(self.tab_VOC)
        self.widget_22.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_22.setMaximumSize(QtCore.QSize(16777215, 20))
        self.widget_22.setObjectName("widget_22")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_22)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.widget_22)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_5.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.label_10 = QtWidgets.QLabel(self.widget_22)
        self.label_10.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_5.addWidget(self.label_10)
        self.verticalLayout_14.addWidget(self.widget_22)
        self.tabWidget.addTab(self.tab_VOC, "")
        self.tab_VOC_DETECTION = QtWidgets.QWidget()
        self.tab_VOC_DETECTION.setObjectName("tab_VOC_DETECTION")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.tab_VOC_DETECTION)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.widget_19 = QtWidgets.QWidget(self.tab_VOC_DETECTION)
        self.widget_19.setObjectName("widget_19")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.widget_19)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.lineEdit_isat2vocod_isat_json_root = QtWidgets.QLineEdit(self.widget_19)
        self.lineEdit_isat2vocod_isat_json_root.setReadOnly(True)
        self.lineEdit_isat2vocod_isat_json_root.setObjectName("lineEdit_isat2vocod_isat_json_root")
        self.gridLayout_8.addWidget(self.lineEdit_isat2vocod_isat_json_root, 0, 0, 1, 1)
        self.pushButton_isat2vocod_isat_json_root = QtWidgets.QPushButton(self.widget_19)
        self.pushButton_isat2vocod_isat_json_root.setObjectName("pushButton_isat2vocod_isat_json_root")
        self.gridLayout_8.addWidget(self.pushButton_isat2vocod_isat_json_root, 0, 1, 1, 1)
        self.lineEdit_isat2vocod_voc_xml_root = QtWidgets.QLineEdit(self.widget_19)
        self.lineEdit_isat2vocod_voc_xml_root.setReadOnly(True)
        self.lineEdit_isat2vocod_voc_xml_root.setObjectName("lineEdit_isat2vocod_voc_xml_root")
        self.gridLayout_8.addWidget(self.lineEdit_isat2vocod_voc_xml_root, 1, 0, 1, 1)
        self.pushButton_isat2vocod_voc_xml_root = QtWidgets.QPushButton(self.widget_19)
        self.pushButton_isat2vocod_voc_xml_root.setObjectName("pushButton_isat2vocod_voc_xml_root")
        self.gridLayout_8.addWidget(self.pushButton_isat2vocod_voc_xml_root, 1, 1, 1, 1)
        self.verticalLayout_21.addWidget(self.widget_19)
        self.label_6 = QtWidgets.QLabel(self.tab_VOC_DETECTION)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_6.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_21.addWidget(self.label_6)
        self.tabWidget.addTab(self.tab_VOC_DETECTION, "")
        self.verticalLayout_13.addWidget(self.tabWidget)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_13.addWidget(self.textBrowser)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_13.addWidget(self.progressBar)
        self.widget_2 = QtWidgets.QWidget(Dialog)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(308, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_cancel = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.pushButton_convert = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_convert.setObjectName("pushButton_convert")
        self.horizontalLayout.addWidget(self.pushButton_convert)
        self.verticalLayout_13.addWidget(self.widget_2)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(3)
        self.toolBox_coco.setCurrentIndex(1)
        self.toolBox_yolo.setCurrentIndex(1)
        self.toolBox_labelme.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Converter"))
        self.pushButton_coco2isat_coco_json_path.setText(_translate("Dialog", "json path"))
        self.lineEdit_coco2isat_isat_json_root.setPlaceholderText(_translate("Dialog", "ISAT jsons save root"))
        self.lineEdit_coco2isat_coco_json_path.setPlaceholderText(_translate("Dialog", "COCO json path"))
        self.pushButton_coco2isat_isat_json_root.setText(_translate("Dialog", "save root"))
        self.checkBox_coco2isat_keep_crowd.setText(_translate("Dialog", "keep crowd"))
        self.toolBox_coco.setItemText(self.toolBox_coco.indexOf(self.toolbox_item_coco2isat), _translate("Dialog", "COCO to ISAT"))
        self.lineEdit_isat2coco_isat_json_root.setPlaceholderText(_translate("Dialog", "ISAT jsons root"))
        self.pushButton_isat2coco_isat_json_root.setText(_translate("Dialog", "json root"))
        self.lineEdit_isat2coco_coco_json_path.setPlaceholderText(_translate("Dialog", "COCO json save path"))
        self.pushButton_isat2coco_coco_json_path.setText(_translate("Dialog", "save path"))
        self.checkBox_isat2coco_keep_crowd.setText(_translate("Dialog", "keep crowd"))
        self.toolBox_coco.setItemText(self.toolBox_coco.indexOf(self.toolbox_item_isat2coco), _translate("Dialog", "ISAT to COCO"))
        self.label_2.setText(_translate("Dialog", "COCO save annotations to a single JSON file."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_COCO), _translate("Dialog", "COCO"))
        self.lineEdit_yolo2isat_isat_json_root.setPlaceholderText(_translate("Dialog", "ISAT jsons save root"))
        self.pushButton_yolo2isat_isat_json_root.setText(_translate("Dialog", "save root"))
        self.lineEdit_yolo2isat_yolo_txt_root.setPlaceholderText(_translate("Dialog", "YOLO txts root"))
        self.pushButton_yolo2isat_yolo_txt_root.setText(_translate("Dialog", "txt root"))
        self.lineEdit_yolo2isat_yolo_image_root.setPlaceholderText(_translate("Dialog", "YOLO images root"))
        self.pushButton_yolo2isat_yolo_image_root.setText(_translate("Dialog", "image root"))
        self.lineEdit_yolo2isat_yolo_cate_path.setPlaceholderText(_translate("Dialog", "YOLO category file path.(Txt file with one line for one category.)  "))
        self.pushButton_yolo2isat_yolo_cate_path.setText(_translate("Dialog", "category file"))
        self.label.setText(_translate("Dialog", "*"))
        self.label_7.setText(_translate("Dialog", "*"))
        self.label_9.setText(_translate("Dialog", "*"))
        self.toolBox_yolo.setItemText(self.toolBox_yolo.indexOf(self.toolbox_item_yolo2isat), _translate("Dialog", "YOLO to ISAT"))
        self.pushButton_isat2yolo_yolo_txt_root.setText(_translate("Dialog", "save root"))
        self.lineEdit_isat2yolo_yolo_txt_root.setPlaceholderText(_translate("Dialog", "YOLO txts save root"))
        self.lineEdit_isat2yolo_isat_json_root.setPlaceholderText(_translate("Dialog", "ISAT jsons root"))
        self.pushButton_isat2yolo_isat_json_root.setText(_translate("Dialog", "json root"))
        self.toolBox_yolo.setItemText(self.toolBox_yolo.indexOf(self.toolbox_item_isat2yolo), _translate("Dialog", "ISAT to YOLO"))
        self.label_3.setText(_translate("Dialog", "YOLO save annotations to multiple TXT files."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_YOLO), _translate("Dialog", "YOLO"))
        self.pushButton_labelme2isat_labelme_json_root.setText(_translate("Dialog", "json root"))
        self.lineEdit_labelme2isat_isat_json_root.setPlaceholderText(_translate("Dialog", "ISAT jsons save root"))
        self.lineEdit_labelme2isat_labelme_json_root.setPlaceholderText(_translate("Dialog", "LABELME jsons root"))
        self.pushButton_labelme2isat_isat_json_root.setText(_translate("Dialog", "save root"))
        self.toolBox_labelme.setItemText(self.toolBox_labelme.indexOf(self.toolbox_item_labelme2isat), _translate("Dialog", "LABELME to ISAT"))
        self.lineEdit_isat2labelme_isat_json_root.setPlaceholderText(_translate("Dialog", "ISAT jsons root"))
        self.pushButton_isat2labelme_isat_json_root.setText(_translate("Dialog", "json root"))
        self.lineEdit_isat2labelme_labelme_json_root.setPlaceholderText(_translate("Dialog", "LABELME jsons save root"))
        self.pushButton_isat2labelme_labelme_json_root.setText(_translate("Dialog", "save root"))
        self.toolBox_labelme.setItemText(self.toolBox_labelme.indexOf(self.toolbox_item_isat2labelme), _translate("Dialog", "ISAT to LABELME"))
        self.label_4.setText(_translate("Dialog", "LABELME save annotations to multiple JSON files. (When convert LABELME to ISAT for instance segmentation, labelme group id must>0.)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_LABELME), _translate("Dialog", "LABELME"))
        self.pushButton_isat2voc_voc_png_root.setText(_translate("Dialog", "save root"))
        self.lineEdit_isat2voc_voc_png_root.setPlaceholderText(_translate("Dialog", "VOC pngs save root"))
        self.lineEdit_isat2voc_isat_json_root.setPlaceholderText(_translate("Dialog", "ISAT jsons root"))
        self.pushButton_isat2voc_isat_json_root.setText(_translate("Dialog", "json root"))
        self.checkBox_is_instance.setText(_translate("Dialog", "is instance"))
        self.label_5.setText(_translate("Dialog", "VOC save annotations to multiple PNG files."))
        self.label_10.setText(_translate("Dialog", "**The num of classification and the group must in [0, 255]**"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_VOC), _translate("Dialog", "VOC"))
        self.lineEdit_isat2vocod_isat_json_root.setPlaceholderText(_translate("Dialog", "ISAT jsons root"))
        self.pushButton_isat2vocod_isat_json_root.setText(_translate("Dialog", "json root"))
        self.lineEdit_isat2vocod_voc_xml_root.setPlaceholderText(_translate("Dialog", "VOC xmls save root"))
        self.pushButton_isat2vocod_voc_xml_root.setText(_translate("Dialog", "save root"))
        self.label_6.setText(_translate("Dialog", "VOC save annotations to multiple XML files for object detection."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_VOC_DETECTION), _translate("Dialog", "VOC for object detection"))
        self.pushButton_cancel.setText(_translate("Dialog", "Cancel"))
        self.pushButton_convert.setText(_translate("Dialog", "Convert"))
