"""Main module."""
import sys
from LSCon import LSCon
from credentials import set_creds
from limesurveyrc2api.exceptions import LimeSurveyError
from exceptions import ParticipantError

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initialize."""
        super().__init__(parent)
        self.setWindowTitle("Matrícula Salvador Seguí")
        self.resize(1024, 768)
        self.centralWidget = QLabel("Aplicació per gestionar la matrícula.")
        self.centralWidget.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setCentralWidget(self.centralWidget)
        self._createActions()
        self._createMenuBar()
        self._connectActions()

    def _createMenuBar(self):
        """Create menu bar for the main window."""
        menuBar = self.menuBar()
        participantMenu = QMenu("Buscar alumnat", self)
        menuBar.addMenu(participantMenu)
        editParticipantMenu = menuBar.addMenu("Editar participant")
        participantDocsMenu = menuBar.addMenu("Documentació")
        participantDocsMenu.addAction(self.downloadDocsAction)

    def _createActions(self):
        self.downloadDocsAction = QAction("Download Documentation", self)

    def download_docs(self):
        """Download all files associated with a participant."""
        creds = set_creds()
        ls = LSCon(creds.url, creds.username)
        ls.open(creds.password)
        try:
            ls.extract_all_participant_files()
        except Exception as e:
            self.centralWidget.setText(e.message)
            return
        self.centralWidget.setText("Documentació descarregada.")

    def _connectActions(self):
        # Download participant documents
        self.downloadDocsAction.triggered.connect(self.download_docs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
