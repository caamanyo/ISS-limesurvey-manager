"""Main module."""
import sys
import pandas as pd

from PyQt6.QtCore import QTranslator, Qt
from PyQt6.QtWidgets import (QApplication, QErrorMessage, QInputDialog,
                             QMainWindow, QTableView, QMessageBox)
from model import TableModel

from credentials import set_creds
from LSCon import LSCon
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
        data = data.set_index("tid")
        self.model.update(data)
        self.model.layoutChanged.emit()

    def download_docs(self):
        """Download all files associated with a participant."""
        index = self.ui.tableView.currentIndex()
        row = self.model.rowToDict(index.row())
        if not row:
            info = QMessageBox(QMessageBox.Icon.Information,
                               "Bon dia", "No has seleccionat cap alumne")
            info.exec()
            return
        token = row[0].data()
        assert self.model.getColumnName(row[0]) == "Token"

        try:
            files = self.ls.extract_all_participant_files(token)
        except Exception as e:
            self.error_dialog.showMessage(e.message, "Warning")
            return

    def print_selection(self):
        rows = self.ui.tableView.selectionModel().selectedRows(0)
        breakpoint()

    def _connectActions(self):
        # Download participant documents
        self.ui.actionDownload_participant_files.triggered.connect(
            self.download_docs)
        self.ui.actionSearch_Participant.triggered.connect(
            self.search_participants)
        self.ui.tableView.clicked.connect(self.print_selection)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator(app)
    translator.load("ui/eng-cat.qm")
    app.installTranslator(translator)
    win = Window()
    win.show()
    sys.exit(app.exec())
