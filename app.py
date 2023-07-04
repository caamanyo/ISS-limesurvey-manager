"""Main module."""
import sys

import pandas as pd
from PyQt6.QtCore import Qt, QTranslator
from PyQt6.QtWidgets import (QApplication, QErrorMessage, QInputDialog,
                             QMainWindow, QMessageBox, QTableView)

import config as cfg
from credentials import set_creds
from ParticipantData import ParticipantData
from LSCon import LSCon
from model import TableModel
from ui.main_window import Ui_MainWindow


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initialize."""
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.creds = set_creds()
        self.ls = LSCon(self.creds.url, self.creds.username)
        self.ls.open(self.creds.password)
        starting_data = pd.DataFrame(
            columns=["token"])
        self.model = TableModel(starting_data)
        self.ui.tableView.setModel(self.model)
        self.error_dialog = QErrorMessage(self)
        self._connectActions()

    def search_participants(self):
        """Fetch LS participants."""
        res = self.ls.token.list_participants(
            292257,
            attributes=["attribute_3", "attribute_4", "sent", "completed"],
            # conditions={"sent": ["<>", "N"]})
            conditions={"lastname": ["LIKE", "tes"]})
        flat_res = pd.json_normalize(res)
        data = pd.DataFrame.from_dict(flat_res)
        data = data.rename(
            columns={
                "participant_info.email": "email",
                "participant_info.firstname": "firstname",
                "participant_info.lastname": "lastname",
            }
        )
        data = data.set_index("tid")
        self.model.update(data)
        self.model.layoutChanged.emit()

    def download_docs(self):
        """Download all files associated with a participant."""
        # Get selected row.
        index = self.ui.tableView.selectionModel().selectedRows()

        # If no row selected, terminate action.
        if not index:
            info = QMessageBox(QMessageBox.Icon.Information,
                               "Bon dia", "No has seleccinat res.")
            info.exec()
            return
        row = index[0].row()
        row_data = self.model.getColumnData(row)
        alumnus = ParticipantData(row_data)

        try:
            # Get all files from a token
            exported_files = self.ls.get_all_participant_files(alumnus.data.attribute_4, alumnus.data.token)
            alumnus.populate_files(exported_files)
        except Exception as e:
            self.error_dialog.showMessage(e.message, "Warning")
            return

        for file in alumnus.files:
            file.export_file()
            print(file.name)



    def print_selection(self):
        rows = self.ui.tableView.selectionModel().selectedRows()

    def _connectActions(self):
        # Download participant documents
        self.ui.actionDownload_participant_files.triggered.connect(
            self.download_docs)
        self.ui.actionSearch_Participant.triggered.connect(
            self.search_participants)
        # self.ui.tableView.clicked.connect(self.print_selection)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator(app)
    translator.load("ui/eng-cat.qm")
    app.installTranslator(translator)
    win = Window()
    win.show()
    sys.exit(app.exec())
