"""Main module."""
import sys
from LSCon import LSCon
from credentials import set_creds
from ui.main_window import Ui_MainWindow

from PyQt6.QtCore import QTranslator
from PyQt6.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initialize."""
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connectActions()

    def download_docs(self):
        """Download all files associated with a participant."""
        creds = set_creds()
        ls = LSCon(creds.url, creds.username)
        ls.open(creds.password)
        try:
            ls.extract_all_participant_files()
        except Exception as e:
            self.ui.centralWidget.setText(e.message)
            return
        self.ui.centralWidget.setText("Documentació descarregada.")

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
