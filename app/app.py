"""Main module."""
import sys

import pandas as pd
from PyQt6.QtCore import QTranslator
from PyQt6.QtWidgets import (QApplication, QErrorMessage,
                             QMainWindow, QMessageBox)

from credentials import set_creds
from ParticipantData import ParticipantData
from LSCon import LSCon
from model import TableModel
from ui.main_window import Ui_MainWindow
from ui.search_form import Ui_Form


class SearchForm(QMainWindow):
    """Create search form window."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initialize."""
        super().__init__()
        # Initialize main window ui
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)

        # Prepare the rest of ui components
        self.search_ui = SearchForm(self)

        self.creds = set_creds()
        self.ls = LSCon(self.creds.url, self.creds.username)
        self.ls.open(self.creds.password)
        starting_data = pd.DataFrame(
            columns=["token"])
        self.model = TableModel(starting_data)
        self.main_ui.tableView.setModel(self.model)
        self.error_dialog = QErrorMessage(self)
        self._connectActions()

    def toggle_search_form(self):
        """Open search participant window."""
        if self.search_ui.isVisible():
            self.search_ui.hide()
        else:
            self.search_ui.show()


    def search_participant(self):
        """Fetch LS participants based on form responses."""
        invitation_sent_idx = self.search_ui.ui.comboBox.currentIndex()

        conditions = 
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
        index = self.main_ui.tableView.selectionModel().selectedRows()

        # If no row selected, terminate action.
        if not index:
            info = QMessageBox(QMessageBox.Icon.Information,
                               "Bon dia", "No has seleccinat res.")
            info.exec()
            return

        row = index[0].row()
        row_data = self.model.getRowData(row)

        alumnus = ParticipantData(row_data)

        try:
            # Get all files from a token
            exported_files = self.ls.get_all_participant_files(
                alumnus.data.attribute_4, alumnus.data.token)
            alumnus.populate_files(exported_files)
        except Exception as e:
            self.error_dialog.showMessage(e.message, "Warning")
            return

        result = alumnus.export_all_files()
        self.main_ui.statusbar.showMessage(result)

    def print_selection(self):
        # rows = self.main_ui.tableView.selectionModel().selectedRows()
        print(self.search_ui.ui.comboBox.currentText())

    def _connectActions(self):
        # Download participant documents
        self.main_ui.actionDownload_participant_files.triggered.connect(
            self.download_docs)
        self.main_ui.actionSearch_Participant.triggered.connect(
            self.toggle_search_form)
        self.search_ui.ui.pushButton.clicked.connect(self.search_participant)
        # self.ui.tableView.clicked.connect(self.print_selection)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator(app)
    translator.load("ui/eng-cat.qm")
    app.installTranslator(translator)
    win = Window()
    win.show()
    sys.exit(app.exec())
