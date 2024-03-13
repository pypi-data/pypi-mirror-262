# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/disk2/PycharmProjects/ISAT_with_segment_anything/ISAT/ui/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 764)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/isat_bg_50x25.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menubar.setFont(font)
        self.menubar.setAutoFillBackground(False)
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menuView.setFont(font)
        self.menuView.setObjectName("menuView")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menuAbout.setFont(font)
        self.menuAbout.setObjectName("menuAbout")
        self.menuLaguage = QtWidgets.QMenu(self.menuAbout)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/icons/翻译_translate.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuLaguage.setIcon(icon1)
        self.menuLaguage.setObjectName("menuLaguage")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menuTools.setFont(font)
        self.menuTools.setObjectName("menuTools")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.menuEdit.setFont(font)
        self.menuEdit.setObjectName("menuEdit")
        self.menuMode = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.menuMode.setFont(font)
        self.menuMode.setObjectName("menuMode")
        self.menuContour_mode = QtWidgets.QMenu(self.menuMode)
        self.menuContour_mode.setObjectName("menuContour_mode")
        self.menuSAM_model = QtWidgets.QMenu(self.menubar)
        self.menuSAM_model.setObjectName("menuSAM_model")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.toolBar.setFont(font)
        self.toolBar.setIconSize(QtCore.QSize(24, 24))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.info_dock = QtWidgets.QDockWidget(MainWindow)
        self.info_dock.setMinimumSize(QtCore.QSize(85, 43))
        self.info_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.info_dock.setObjectName("info_dock")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.info_dock.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.info_dock)
        self.annos_dock = QtWidgets.QDockWidget(MainWindow)
        self.annos_dock.setMinimumSize(QtCore.QSize(85, 43))
        self.annos_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.annos_dock.setObjectName("annos_dock")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.annos_dock.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.annos_dock)
        self.files_dock = QtWidgets.QDockWidget(MainWindow)
        self.files_dock.setObjectName("files_dock")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.files_dock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.files_dock)
        self.categories_dock = QtWidgets.QDockWidget(MainWindow)
        self.categories_dock.setObjectName("categories_dock")
        self.dockWidgetContents_4 = QtWidgets.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.categories_dock.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.categories_dock)
        self.actionOpen_dir = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/icons/照片_pic.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen_dir.setIcon(icon2)
        self.actionOpen_dir.setObjectName("actionOpen_dir")
        self.actionZoom_in = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/icons/放大_zoom-in.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_in.setIcon(icon3)
        self.actionZoom_in.setObjectName("actionZoom_in")
        self.actionZoom_out = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/icons/缩小_zoom-out.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out.setIcon(icon4)
        self.actionZoom_out.setObjectName("actionZoom_out")
        self.actionFit_wiondow = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icon/icons/全宽_fullwidth.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFit_wiondow.setIcon(icon5)
        self.actionFit_wiondow.setObjectName("actionFit_wiondow")
        self.actionSetting = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icon/icons/设置_setting-two.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSetting.setIcon(icon6)
        self.actionSetting.setObjectName("actionSetting")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icon/icons/开关_power.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon7)
        self.actionExit.setObjectName("actionExit")
        self.actionSave_dir = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icon/icons/文件夹-开_folder-open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_dir.setIcon(icon8)
        self.actionSave_dir.setObjectName("actionSave_dir")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icon/icons/保存_save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon9)
        self.actionSave.setObjectName("actionSave")
        self.actionPrev = QtWidgets.QAction(MainWindow)
        self.actionPrev.setCheckable(False)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icon/icons/上一步_back.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrev.setIcon(icon10)
        self.actionPrev.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.actionPrev.setPriority(QtWidgets.QAction.NormalPriority)
        self.actionPrev.setObjectName("actionPrev")
        self.actionNext = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icon/icons/下一步_next.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNext.setIcon(icon11)
        self.actionNext.setObjectName("actionNext")
        self.actionShortcut = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icon/icons/键盘_keyboard-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShortcut.setIcon(icon12)
        self.actionShortcut.setObjectName("actionShortcut")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icon/icons/我的_me.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon13)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSegment_anything = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icon/icons/M_Favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSegment_anything.setIcon(icon14)
        self.actionSegment_anything.setObjectName("actionSegment_anything")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setEnabled(False)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icon/icons/删除_delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon15)
        self.actionDelete.setObjectName("actionDelete")
        self.actionBit_map = QtWidgets.QAction(MainWindow)
        self.actionBit_map.setCheckable(False)
        self.actionBit_map.setIcon(icon2)
        self.actionBit_map.setObjectName("actionBit_map")
        self.actionEdit = QtWidgets.QAction(MainWindow)
        self.actionEdit.setEnabled(False)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icon/icons/编辑_edit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit.setIcon(icon16)
        self.actionEdit.setObjectName("actionEdit")
        self.actionTo_top = QtWidgets.QAction(MainWindow)
        self.actionTo_top.setEnabled(False)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/icon/icons/去顶部_to-top.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTo_top.setIcon(icon17)
        self.actionTo_top.setObjectName("actionTo_top")
        self.actionTo_bottom = QtWidgets.QAction(MainWindow)
        self.actionTo_bottom.setEnabled(False)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/icon/icons/去底部_to-bottom.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTo_bottom.setIcon(icon18)
        self.actionTo_bottom.setObjectName("actionTo_bottom")
        self.actionChinese = QtWidgets.QAction(MainWindow)
        self.actionChinese.setCheckable(True)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.actionChinese.setFont(font)
        self.actionChinese.setObjectName("actionChinese")
        self.actionEnglish = QtWidgets.QAction(MainWindow)
        self.actionEnglish.setCheckable(True)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.actionEnglish.setFont(font)
        self.actionEnglish.setObjectName("actionEnglish")
        self.actionBackspace = QtWidgets.QAction(MainWindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/icon/icons/删除_delete-two.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBackspace.setIcon(icon19)
        self.actionBackspace.setObjectName("actionBackspace")
        self.actionCancel = QtWidgets.QAction(MainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/icon/icons/关闭_close-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCancel.setIcon(icon20)
        self.actionCancel.setObjectName("actionCancel")
        self.actionFinish = QtWidgets.QAction(MainWindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(":/icon/icons/校验_check-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFinish.setIcon(icon21)
        self.actionFinish.setObjectName("actionFinish")
        self.actionPolygon = QtWidgets.QAction(MainWindow)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(":/icon/icons/锚点_anchor.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPolygon.setIcon(icon22)
        self.actionPolygon.setObjectName("actionPolygon")
        self.actionVisible = QtWidgets.QAction(MainWindow)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(":/icon/icons/眼睛_eyes.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVisible.setIcon(icon23)
        self.actionVisible.setObjectName("actionVisible")
        self.actionContour_Max_only = QtWidgets.QAction(MainWindow)
        self.actionContour_Max_only.setCheckable(True)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.actionContour_Max_only.setFont(font)
        self.actionContour_Max_only.setObjectName("actionContour_Max_only")
        self.actionContour_External = QtWidgets.QAction(MainWindow)
        self.actionContour_External.setCheckable(True)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.actionContour_External.setFont(font)
        self.actionContour_External.setObjectName("actionContour_External")
        self.actionContour_All = QtWidgets.QAction(MainWindow)
        self.actionContour_All.setCheckable(True)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.actionContour_All.setFont(font)
        self.actionContour_All.setObjectName("actionContour_All")
        self.actionModel_manage = QtWidgets.QAction(MainWindow)
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap(":/icon/icons/列表_list-middle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionModel_manage.setIcon(icon24)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.actionModel_manage.setFont(font)
        self.actionModel_manage.setObjectName("actionModel_manage")
        self.actionConverter = QtWidgets.QAction(MainWindow)
        icon25 = QtGui.QIcon()
        icon25.addPixmap(QtGui.QPixmap(":/icon/icons/转换文件夹1_folder-conversion-one.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConverter.setIcon(icon25)
        self.actionConverter.setObjectName("actionConverter")
        self.actionAuto_segment = QtWidgets.QAction(MainWindow)
        self.actionAuto_segment.setIcon(icon14)
        self.actionAuto_segment.setObjectName("actionAuto_segment")
        self.menuFile.addAction(self.actionOpen_dir)
        self.menuFile.addAction(self.actionSave_dir)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPrev)
        self.menuFile.addAction(self.actionNext)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSetting)
        self.menuFile.addAction(self.actionExit)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionZoom_in)
        self.menuView.addAction(self.actionZoom_out)
        self.menuView.addAction(self.actionFit_wiondow)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionBit_map)
        self.menuView.addSeparator()
        self.menuLaguage.addAction(self.actionChinese)
        self.menuLaguage.addAction(self.actionEnglish)
        self.menuAbout.addAction(self.menuLaguage.menuAction())
        self.menuAbout.addAction(self.actionShortcut)
        self.menuAbout.addAction(self.actionAbout)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionConverter)
        self.menuTools.addAction(self.actionAuto_segment)
        self.menuEdit.addAction(self.actionSegment_anything)
        self.menuEdit.addAction(self.actionPolygon)
        self.menuEdit.addAction(self.actionBackspace)
        self.menuEdit.addAction(self.actionFinish)
        self.menuEdit.addAction(self.actionCancel)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionTo_top)
        self.menuEdit.addAction(self.actionTo_bottom)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionEdit)
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addAction(self.actionSave)
        self.menuContour_mode.addAction(self.actionContour_Max_only)
        self.menuContour_mode.addAction(self.actionContour_External)
        self.menuContour_mode.addAction(self.actionContour_All)
        self.menuMode.addAction(self.menuContour_mode.menuAction())
        self.menuSAM_model.addAction(self.actionModel_manage)
        self.menuSAM_model.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSAM_model.menuAction())
        self.menubar.addAction(self.menuMode.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.toolBar.addAction(self.actionPrev)
        self.toolBar.addAction(self.actionNext)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSegment_anything)
        self.toolBar.addAction(self.actionPolygon)
        self.toolBar.addAction(self.actionBackspace)
        self.toolBar.addAction(self.actionFinish)
        self.toolBar.addAction(self.actionCancel)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTo_top)
        self.toolBar.addAction(self.actionTo_bottom)
        self.toolBar.addAction(self.actionEdit)
        self.toolBar.addAction(self.actionDelete)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoom_in)
        self.toolBar.addAction(self.actionZoom_out)
        self.toolBar.addAction(self.actionFit_wiondow)
        self.toolBar.addAction(self.actionBit_map)
        self.toolBar.addAction(self.actionVisible)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ISAT"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.menuLaguage.setTitle(_translate("MainWindow", "Laguage"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuMode.setTitle(_translate("MainWindow", "Mode"))
        self.menuContour_mode.setTitle(_translate("MainWindow", "Contour mode"))
        self.menuSAM_model.setTitle(_translate("MainWindow", "SAM"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.info_dock.setWindowTitle(_translate("MainWindow", "Info"))
        self.annos_dock.setWindowTitle(_translate("MainWindow", "Annos"))
        self.files_dock.setWindowTitle(_translate("MainWindow", "Files"))
        self.categories_dock.setWindowTitle(_translate("MainWindow", "Categories"))
        self.actionOpen_dir.setText(_translate("MainWindow", "Images dir"))
        self.actionOpen_dir.setStatusTip(_translate("MainWindow", "Open images dir."))
        self.actionZoom_in.setText(_translate("MainWindow", "Zoom in"))
        self.actionZoom_in.setStatusTip(_translate("MainWindow", "Zoom in."))
        self.actionZoom_out.setText(_translate("MainWindow", "Zoom out"))
        self.actionZoom_out.setStatusTip(_translate("MainWindow", "Zoom out."))
        self.actionFit_wiondow.setText(_translate("MainWindow", "Fit window"))
        self.actionFit_wiondow.setToolTip(_translate("MainWindow", "Fit window"))
        self.actionFit_wiondow.setStatusTip(_translate("MainWindow", "Fit window."))
        self.actionFit_wiondow.setShortcut(_translate("MainWindow", "F"))
        self.actionSetting.setText(_translate("MainWindow", "Setting"))
        self.actionSetting.setStatusTip(_translate("MainWindow", "Setting."))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setToolTip(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Exit."))
        self.actionSave_dir.setText(_translate("MainWindow", "Label dir"))
        self.actionSave_dir.setStatusTip(_translate("MainWindow", "Open label dir."))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save annotation."))
        self.actionSave.setShortcut(_translate("MainWindow", "S"))
        self.actionPrev.setText(_translate("MainWindow", "Prev image"))
        self.actionPrev.setToolTip(_translate("MainWindow", "Prev image"))
        self.actionPrev.setStatusTip(_translate("MainWindow", "Prev image."))
        self.actionPrev.setShortcut(_translate("MainWindow", "A"))
        self.actionNext.setText(_translate("MainWindow", "Next image"))
        self.actionNext.setToolTip(_translate("MainWindow", "Next image"))
        self.actionNext.setStatusTip(_translate("MainWindow", "Next image."))
        self.actionNext.setShortcut(_translate("MainWindow", "D"))
        self.actionShortcut.setText(_translate("MainWindow", "Shortcut"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionSegment_anything.setText(_translate("MainWindow", "Segment anything"))
        self.actionSegment_anything.setToolTip(_translate("MainWindow", "Segment anything"))
        self.actionSegment_anything.setStatusTip(_translate("MainWindow", "Quick annotate using Segment anything."))
        self.actionSegment_anything.setShortcut(_translate("MainWindow", "Q"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionDelete.setToolTip(_translate("MainWindow", "Delete polygon"))
        self.actionDelete.setStatusTip(_translate("MainWindow", "Delete polygon."))
        self.actionDelete.setShortcut(_translate("MainWindow", "Del"))
        self.actionBit_map.setText(_translate("MainWindow", "Bit map"))
        self.actionBit_map.setStatusTip(_translate("MainWindow", "Show instance or segmeent state."))
        self.actionBit_map.setShortcut(_translate("MainWindow", "Space"))
        self.actionEdit.setText(_translate("MainWindow", "Edit"))
        self.actionEdit.setToolTip(_translate("MainWindow", "Edit polygon"))
        self.actionEdit.setStatusTip(_translate("MainWindow", "Edit polygon attribute."))
        self.actionTo_top.setText(_translate("MainWindow", "To top"))
        self.actionTo_top.setToolTip(_translate("MainWindow", "Move polygon to top layer"))
        self.actionTo_top.setStatusTip(_translate("MainWindow", "Move polygon to top layer."))
        self.actionTo_top.setShortcut(_translate("MainWindow", "T"))
        self.actionTo_bottom.setText(_translate("MainWindow", "To bottom"))
        self.actionTo_bottom.setToolTip(_translate("MainWindow", "Move polygon to bottom layer"))
        self.actionTo_bottom.setStatusTip(_translate("MainWindow", "Move polygon to bottom layer."))
        self.actionTo_bottom.setShortcut(_translate("MainWindow", "B"))
        self.actionChinese.setText(_translate("MainWindow", "中文"))
        self.actionEnglish.setText(_translate("MainWindow", "English"))
        self.actionBackspace.setText(_translate("MainWindow", "Backspace"))
        self.actionBackspace.setToolTip(_translate("MainWindow", "Backspace"))
        self.actionBackspace.setStatusTip(_translate("MainWindow", "Backspace."))
        self.actionBackspace.setShortcut(_translate("MainWindow", "Z"))
        self.actionCancel.setText(_translate("MainWindow", "Cancel"))
        self.actionCancel.setToolTip(_translate("MainWindow", "Annotate canceled"))
        self.actionCancel.setStatusTip(_translate("MainWindow", "Annotate canceled."))
        self.actionCancel.setShortcut(_translate("MainWindow", "Esc"))
        self.actionFinish.setText(_translate("MainWindow", "Finish"))
        self.actionFinish.setToolTip(_translate("MainWindow", "Annotate finished"))
        self.actionFinish.setStatusTip(_translate("MainWindow", "Annotate finished."))
        self.actionFinish.setShortcut(_translate("MainWindow", "E"))
        self.actionPolygon.setText(_translate("MainWindow", "Polygon"))
        self.actionPolygon.setToolTip(_translate("MainWindow", "Draw polygon"))
        self.actionPolygon.setStatusTip(_translate("MainWindow", "Accurately annotate by drawing polygon. "))
        self.actionPolygon.setShortcut(_translate("MainWindow", "C"))
        self.actionVisible.setText(_translate("MainWindow", "Visible"))
        self.actionVisible.setToolTip(_translate("MainWindow", "Visible"))
        self.actionVisible.setStatusTip(_translate("MainWindow", "Visible."))
        self.actionVisible.setShortcut(_translate("MainWindow", "V"))
        self.actionContour_Max_only.setText(_translate("MainWindow", "Max only"))
        self.actionContour_Max_only.setStatusTip(_translate("MainWindow", "Max contour save only."))
        self.actionContour_Max_only.setWhatsThis(_translate("MainWindow", "Max contour save only."))
        self.actionContour_External.setText(_translate("MainWindow", "External"))
        self.actionContour_External.setStatusTip(_translate("MainWindow", "External contour save only."))
        self.actionContour_External.setWhatsThis(_translate("MainWindow", "External contour save only."))
        self.actionContour_All.setText(_translate("MainWindow", "All"))
        self.actionContour_All.setStatusTip(_translate("MainWindow", "All contour save."))
        self.actionContour_All.setWhatsThis(_translate("MainWindow", "All contour save."))
        self.actionModel_manage.setText(_translate("MainWindow", "Model manage"))
        self.actionModel_manage.setStatusTip(_translate("MainWindow", "Model manage."))
        self.actionModel_manage.setWhatsThis(_translate("MainWindow", "Model manage."))
        self.actionConverter.setText(_translate("MainWindow", "Converter"))
        self.actionAuto_segment.setText(_translate("MainWindow", "Auto segment with bounding box"))
