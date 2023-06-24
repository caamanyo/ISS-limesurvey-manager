"""Application model."""

from PyQt6.QtCore import QAbstractTableModel, Qt


class TableModel(QAbstractTableModel):
    """Model to convert LS data to be TableView compatible."""

    def __init__(self, data=None):
        """Initialize class."""
        super().__init__()
        self._data = data

    def data(self, index, role):
        """Create data model."""
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        """Get the number of rows."""
        return len(self._data)

    def columnCount(self, index):
        """Get the number of columns."""
        return len(self._data[0])
