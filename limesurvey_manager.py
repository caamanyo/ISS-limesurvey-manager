"""Main module."""
import sys

from PyQt6.QtCore import QTranslator
from PyQt6.QtWidgets import (QApplication, QErrorMessage, QInputDialog,
                             QMainWindow, QTableView)
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
        data = [[1, 2, 3, 4], [1, 2, 3, 4]]
        self.model = TableModel(data)
        self.ui.tableView.setModel(self.model)
        self.error_dialog = QErrorMessage(self)
        self._connectActions()

    def download_docs(self):
        """Download all files associated with a participant."""
        creds = set_creds()
        ls = LSCon(creds.url, creds.username)
        ls.open(creds.password)
        get_token = QInputDialog.getText(
            self, "Descarregar documentació", "Introdueix el token a buscar")
        if not get_token:
            return

        try:
            ls.extract_all_participant_files(get_token)
        except Exception as e:
            self.error_dialog.showMessage(e.message, "Warning")
            return

    def _connectActions(self):
        # Download participant documents
        self.ui.actionDescarregar_Documentaci.triggered.connect(
            self.download_docs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator(app)
    translator.load("ui/eng-cat.qm")
    app.installTranslator(translator)
    win = Window()
    win.show()
    sys.exit(app.exec())
