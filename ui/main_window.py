# Form implementation generated from reading ui file 'LS_manager.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1154, 678)
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(parent=self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(0, 10, 1151, 611))
        self.tableView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.tableView.setAcceptDrops(True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView.setObjectName("tableView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1154, 32))
        self.menubar.setObjectName("menubar")
        self.menuSearchParticipant = QtWidgets.QMenu(parent=self.menubar)
        self.menuSearchParticipant.setEnabled(True)
        self.menuSearchParticipant.setAcceptDrops(False)
        self.menuSearchParticipant.setObjectName("menuSearchParticipant")
        self.menuEditar_alumne = QtWidgets.QMenu(parent=self.menubar)
        self.menuEditar_alumne.setObjectName("menuEditar_alumne")
        self.menuEdit_participant = QtWidgets.QMenu(parent=self.menuEditar_alumne)
        self.menuEdit_participant.setObjectName("menuEdit_participant")
        MainWindow.setMenuBar(self.menubar)
        self.actionDescarregar_Documentaci = QtGui.QAction(parent=MainWindow)
        self.actionDescarregar_Documentaci.setEnabled(True)
        self.actionDescarregar_Documentaci.setObjectName("actionDescarregar_Documentaci")
        self.actionSearch_Participant = QtGui.QAction(parent=MainWindow)
        self.actionSearch_Participant.setObjectName("actionSearch_Participant")
        self.actionChange_email = QtGui.QAction(parent=MainWindow)
        self.actionChange_email.setObjectName("actionChange_email")
        self.actionDownload_participant_files = QtGui.QAction(parent=MainWindow)
        self.actionDownload_participant_files.setObjectName("actionDownload_participant_files")
        self.menuEdit_participant.addAction(self.actionChange_email)
        self.menuEditar_alumne.addAction(self.actionSearch_Participant)
        self.menuEditar_alumne.addAction(self.menuEdit_participant.menuAction())
        self.menuEditar_alumne.addAction(self.actionDownload_participant_files)
        self.menubar.addAction(self.menuSearchParticipant.menuAction())
        self.menubar.addAction(self.menuEditar_alumne.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuSearchParticipant.setTitle(_translate("MainWindow", "File"))
        self.menuEditar_alumne.setTitle(_translate("MainWindow", "Participant"))
        self.menuEdit_participant.setTitle(_translate("MainWindow", "Edit participant"))
        self.actionDescarregar_Documentaci.setText(_translate("MainWindow", "Descarregar Documentació"))
        self.actionSearch_Participant.setText(_translate("MainWindow", "Search participant"))
        self.actionChange_email.setText(_translate("MainWindow", "Change email"))
        self.actionDownload_participant_files.setText(_translate("MainWindow", "Download participant files"))
